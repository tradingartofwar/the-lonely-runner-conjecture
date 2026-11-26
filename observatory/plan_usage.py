"""Read private Codex allowance windows or meter a reserved local Observatory dispatch.

Run without arguments to query the signed-in Codex app-server without starting a
model turn. Give read_dispatch_receipt() only the stdout from an Observatory
worker's own already-reserved single-turn `codex exec --json` child.
"""
import argparse
import asyncio
import base64
from contextlib import suppress
from datetime import datetime, time, timedelta, timezone
import json
import shutil
import subprocess
import webbrowser
from zoneinfo import ZoneInfo


UTC = timezone.utc
PACIFIC = ZoneInfo("America/Los_Angeles")
TOKEN_FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")


def iso(value):
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def rate_windows(reply):
    """Use the Codex plan bucket. Never copy account identity, credits or extra buckets."""
    buckets = reply.get("rateLimitsByLimitId")
    bucket = buckets.get("codex") if isinstance(buckets, dict) else None
    if not isinstance(bucket, dict):
        bucket = reply.get("rateLimits")
    if not isinstance(bucket, dict) or bucket.get("limitId") not in (None, "codex"):
        return []
    windows = []
    for kind in ("primary", "secondary"):
        window = bucket.get(kind)
        if not isinstance(window, dict):
            continue
        percent = window.get("usedPercent")
        if type(percent) not in (float, int) or not 0 <= percent <= 100:
            continue
        minutes = window.get("windowDurationMins")
        reset = window.get("resetsAt")
        try:
            dt = datetime.fromtimestamp(reset, UTC) if type(reset) is int else None
        except (OverflowError, OSError, ValueError):
            dt = None
        windows.append(dict(bucket="codex", window=kind, remaining_percent=100-percent,
                            duration_minutes=minutes if type(minutes) is int and minutes > 0 else None,
                            resets_at=iso(dt) if dt else None,
                            resets_at_pt=iso(dt.astimezone(PACIFIC)) if dt else None))
    return windows


class ProbeError(Exception):
    """Fixed reason codes only, never provider output."""


async def allowance_probe(command=("codex", "app-server", "--listen", "stdio://"), timeout=15):
    proc = None
    account = "unknown"
    windows = []
    reason = None

    async def probe():
        nonlocal proc, account, windows, reason
        proc = await asyncio.create_subprocess_exec(
            *command, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL, limit=2**20)

        async def request(method, request_id=None, params=None):
            message = {"method": method}
            if request_id is not None:
                message["id"] = request_id
            if params is not None:
                message["params"] = params
            proc.stdin.write((json.dumps(message) + "\n").encode())
            await proc.stdin.drain()
            if request_id is None:
                return None
            while line := await proc.stdout.readline():
                reply = json.loads(line)
                if isinstance(reply, dict) and reply.get("id") == request_id and "method" not in reply:
                    return reply.get("result") if isinstance(reply.get("result"), dict) else None
            raise ProbeError("app_server_closed")

        if await request("initialize", 1, {"clientInfo": {"name": "lonely_runner_observatory",
                                                          "version": "1.0"}}) is None:
            raise ProbeError("initialize_refused")
        await request("initialized")
        info = await request("account/read", 2, {"refreshToken": False})
        if info is None or "account" not in info:
            raise ProbeError("account_read_unavailable")
        identity = info["account"]
        if identity is None:
            account = "none"
            raise ProbeError("no_account")
        if not isinstance(identity, dict) or not isinstance(identity.get("type"), str):
            raise ProbeError("account_read_unavailable")
        if identity["type"] != "chatgpt":
            account = "other"
            raise ProbeError("not_chatgpt_account")
        account = "chatgpt"
        rates = await request("account/rateLimits/read", 3)
        if rates is None:
            reason = "rate_read_refused"
        else:
            windows = rate_windows(rates)
            if not windows:
                reason = "no_codex_windows"

    try:
        await asyncio.wait_for(probe(), timeout)
    except FileNotFoundError:
        reason = "cli_not_found"
    except asyncio.TimeoutError:
        reason = "read_timed_out"
    except ProbeError as exc:
        reason = str(exc)
    except (OSError, ValueError, RecursionError):
        reason = "app_server_unavailable"
    finally:
        if proc is not None:
            proc.stdin.close()
            if proc.returncode is None:
                with suppress(ProcessLookupError):
                    proc.kill()
            await proc.wait()
    now = datetime.now(UTC)
    return dict(source="codex_app_server", status="available" if windows else "unavailable",
                reason=reason, account_read=account, measured_at=iso(now),
                measured_at_pt=iso(now.astimezone(PACIFIC)), windows=windows)


def completed_usage(event):
    """Cached input is contained in input. Reasoning output is contained in output."""
    if not isinstance(event, dict) or event.get("type") != "turn.completed":
        return None
    usage = event.get("usage")
    if not isinstance(usage, dict):
        return None
    raw = {key: usage.get(key) for key in TOKEN_FIELDS[:3]}
    if any(type(n) is not int or not 0 <= n < 2**63 for n in raw.values()):
        return None
    total = raw["input_tokens"] + raw["output_tokens"]
    if raw["cached_input_tokens"] > raw["input_tokens"] or total >= 2**63:
        return None
    return {**raw, "total_tokens": total}


def read_dispatch_receipt(lines):
    """Return one child's counts or None. The caller owns the dispatch ID and durable deduplication."""
    saw_turn = False
    measured = None
    for line in lines:
        try:
            event = json.loads(line)
        except (ValueError, RecursionError):
            return None
        if not isinstance(event, dict) or event.get("type") == "turn.failed":
            return None
        if event.get("type") != "turn.completed":
            continue
        if saw_turn:
            return None
        saw_turn = True
        measured = completed_usage(event)
    return measured


def pt_day_bounds(day):
    """UTC epoch-second bounds for a Pacific completion day, including DST changes."""
    start = datetime.combine(day, time.min, PACIFIC)
    end = datetime.combine(day + timedelta(days=1), time.min, PACIFIC)
    return int(start.timestamp()), int(end.timestamp())


DEFAULT_SITE = "https://lonely-runner-observatory.senthein.chatgpt.site/"


def allowance_link(site, reading):
    if site not in (DEFAULT_SITE, DEFAULT_SITE.rstrip("/")):
        raise ValueError("Use the private Lonely Runner Observatory HTTPS address.")
    if reading["status"] != "available" or not reading["windows"]:
        return None
    windows = []
    for row in reading["windows"]:
        is_unique = sum(w["duration_minutes"] == row["duration_minutes"] for w in reading["windows"]) == 1
        label = {300: "5-hour", 10080: "Weekly"}.get(row["duration_minutes"]) if is_unique else None
        label = label or row["window"].title()
        windows.append(dict(label=label, remaining_percent=row["remaining_percent"], resets_at=row["resets_at"]))
    payload = dict(measured_at=reading["measured_at"], windows=windows)
    content = json.dumps(payload, separators=(",", ":"), allow_nan=False).encode()
    encoded = base64.urlsafe_b64encode(content).decode().rstrip("=")
    return site.rstrip("/") + "/#sync-allowance=" + encoded


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command")
    link = commands.add_parser("link", help="send current plan windows to your signed-in private Observatory")
    link.add_argument("url", nargs="?", default=DEFAULT_SITE, help="private Observatory HTTPS origin")
    link.add_argument("--open", action="store_true", help="open the private import link in the local browser")
    args = parser.parse_args(argv)
    reading = asyncio.run(allowance_probe())
    if args.command == "link":
        try:
            url = allowance_link(args.url, reading)
        except ValueError as exc:
            parser.exit(2, str(exc) + "\n")
        if not url:
            parser.exit(1, f"No Codex plan windows available ({reading['reason']}, {reading['measured_at']}).\n")
        if args.open:
            wslview = shutil.which("wslview")
            if wslview:
                try:
                    opened = subprocess.run([wslview, url], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL, timeout=10).returncode == 0
                except (OSError, subprocess.TimeoutExpired):
                    opened = False
            else:
                opened = webbrowser.open(url)
            if opened:
                print("Opened the private Observatory to import the measured plan windows.")
                return
        print(url)
    else:
        print(json.dumps(reading, ensure_ascii=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
