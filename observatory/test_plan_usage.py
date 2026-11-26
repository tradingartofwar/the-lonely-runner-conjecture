"""Exercise the same handshake, receipts and wire format used by the private board."""
import asyncio
import base64
from datetime import date
import json
import sys
import unittest
from unittest.mock import patch

from . import plan_usage as meter


class UsageTests(unittest.TestCase):
    def test_real_stdio_handshake_with_fixture(self):
        # Only the transport/response is a fixture. The CLI never sends a model call.
        server = """
import json, sys
for method, num, reply in (
 ('initialize',1,{}),('initialized',None,None),
 ('account/read',2,{'account':{'email':'discard@example.org','type':'chatgpt'}}),
 ('account/rateLimits/read',3,{'rateLimitsByLimitId':{'codex':{'primary':
 {'usedPercent':30,'windowDurationMins':300,'resetsAt':1699173000},
 'secondary':{'usedPercent':60,'windowDurationMins':10080,'resetsAt':1699777800},
 'credits':{'balance':'discard private data'}},'other-secret':{}}})):
    req=json.loads(sys.stdin.readline())
    assert req['method']==method and req.get('id')==num
    if method=='account/read': assert req['params']=={'refreshToken':False}
    if num is None: continue
    print(json.dumps({'method':'account/rateLimits/updated','params':{'ignore':True}}),flush=True)
    print(json.dumps({'id':num,'result':reply}),flush=True)
"""
        actual = asyncio.run(meter.allowance_probe([sys.executable, "-c", server]))
        self.assertEqual(actual["status"], "available")
        self.assertEqual(actual["account_read"], "chatgpt")
        self.assertEqual([w["remaining_percent"] for w in actual["windows"]], [70, 40])
        self.assertEqual(actual["windows"][0]["resets_at_pt"], "2023-11-05T01:30:00-07:00")
        text = json.dumps(actual)
        for private in ("other-secret", "discard", "example.org", "credits"):
            self.assertNotIn(private, text)
        link = meter.allowance_link(meter.DEFAULT_SITE, actual)
        encoded = link.split("#sync-allowance=")[1]
        payload = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        self.assertEqual(set(payload), {"measured_at", "windows"})
        self.assertEqual([w["label"] for w in payload["windows"]], ["5-hour", "Weekly"])
        self.assertEqual(set(payload["windows"][0]), {"label", "remaining_percent", "resets_at"})
        with self.assertRaises(ValueError):
            meter.allowance_link("https://elsewhere.example/", actual)

    def test_only_confirmed_chatgpt_account_can_read_rates(self):
        server = """
import json, sys
for line in sys.stdin:
    req = json.loads(line)
    method = req["method"]
    if method == "initialized": continue
    if method == "initialize": result = {}
    elif method == "account/read": result = json.loads(sys.argv[1])
    elif method == "account/rateLimits/read":
        # Make an incorrect follow-up visibly fail the test even if the caller discards its result.
        import time
        time.sleep(2)
        continue
    else: raise AssertionError()
    print(json.dumps({"id":req["id"], "result": result}),flush=True)
"""
        cases = [
            ({"account": {"type": "apiKey"}}, "other", "not_chatgpt_account"),
            ({"account": {"type": "amazonBedrock"}}, "other", "not_chatgpt_account"),
            ({"account": {"type": "unrecognized"}}, "other", "not_chatgpt_account"),
            ({"account": None}, "none", "no_account"),
            ({"account": {}}, "unknown", "account_read_unavailable"),
            ({}, "unknown", "account_read_unavailable"),
            (None, "unknown", "account_read_unavailable"),
        ]
        for result, account, reason in cases:
            with self.subTest(result=result):
                reply = asyncio.run(meter.allowance_probe(
                    [sys.executable, "-c", server, json.dumps(result)], timeout=1))
                self.assertEqual((reply["status"], reply["account_read"], reply["reason"], reply["windows"]),
                                 ("unavailable", account, reason, []))
                self.assertIsNone(meter.allowance_link(meter.DEFAULT_SITE, reply))

    def test_no_read_no_windows_no_import(self):
        result = asyncio.run(meter.allowance_probe(["/missing-codex-usage-test"]))
        self.assertEqual((result["status"], result["reason"], result["windows"]),
                         ("unavailable", "cli_not_found", []))
        self.assertIsNone(meter.allowance_link(meter.DEFAULT_SITE, result))
        result = asyncio.run(meter.allowance_probe([sys.executable, "-c", "import time; time.sleep(2)"], 0.1))
        self.assertEqual(result["reason"], "read_timed_out")

    def test_window_failures_and_legacy_shape(self):
        for percent in (False, None, -1, 101, float("nan")):
            self.assertEqual(meter.rate_windows({"rateLimits": {"primary": {"usedPercent": percent}}}), [])
        row = meter.rate_windows({"rateLimits": {"primary": {"usedPercent": 100}}})[0]
        self.assertEqual(row["remaining_percent"], 0)
        self.assertIsNone(row["resets_at"])
        self.assertIsNone(row["duration_minutes"])
        self.assertEqual(meter.rate_windows({"rateLimits":{"limitId":"other","primary":{"usedPercent":1}}}), [])

    def test_only_one_complete_turn(self):
        end = dict(type="turn.completed", usage=dict(input_tokens=10, cached_input_tokens=6,
                                                     output_tokens=4, reasoning_output_tokens=1))
        expected = dict(input_tokens=10, cached_input_tokens=6, output_tokens=4, total_tokens=14)
        serial = json.dumps(end)
        self.assertEqual(meter.read_dispatch_receipt(['{"type":"item.completed"}', serial]), expected)
        for lines in ([], ['{"type":"item.completed"}'], ["malformed"], [serial, serial],
                      [serial, '{"type":"turn.failed"}'], ['{"type":"turn.completed"}']):
            self.assertIsNone(meter.read_dispatch_receipt(lines))
        for bad in ({"cached_input_tokens": 11}, {"input_tokens": True}, {"output_tokens": -1},
                    {"output_tokens": None}):
            self.assertIsNone(meter.completed_usage(dict(type="turn.completed", usage=end["usage"] | bad)))

    def test_pacific_midnight_gaps_and_folds(self):
        for day, hours in ((date(2026, 3, 8), 23), (date(2026, 11, 1), 25), (date(2026, 9, 1), 24)):
            a, b = meter.pt_day_bounds(day)
            self.assertEqual(b - a, hours * 3600)

    def test_unavailable_link_prints_no_json_or_url(self):
        async def fail():
            return {"status":"unavailable","reason":"no_account","measured_at":"2026-01-01T00:00:00Z","windows":[]}
        with patch.object(meter, "allowance_probe", fail), self.assertRaises(SystemExit) as failure:
            meter.main(["link"])
        self.assertEqual(failure.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
