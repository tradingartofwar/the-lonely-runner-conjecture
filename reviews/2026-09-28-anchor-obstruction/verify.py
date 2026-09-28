#!/usr/bin/env python3
"""Independent exact check of one constructed anchor-menu obstruction.

Standard library only; no imports of project or coordinator implementations.
Full first-component scope: q=840, B=1.  The protocol also permits a ratio-seven
boundary check and a B=10**12 formula-only diagnostic.  The review supplies the
unbounded argument.  A rescue from 3/8 is marked as a post-protocol refinement.
"""

from fractions import Fraction as F
from math import floor
import json

DELTA = F(1, 8)
Q = 840
B = 1
SPEEDS = (1, 4, 5, 6, 7, Q, 8 * B * Q)


def distance(x):
    phase = x - floor(x)
    return min(phase, 1 - phase)


def safe_components(speeds, anchor, direction, lo, hi):
    """Threshold-event reconstruction on a displacement interval.

    It evaluates every endpoint and every open threshold cell exactly.  Closed
    components include isolated safe points; no first-lap formula is imported.
    """
    events = {lo, hi}
    for v in speeds:
        phase_lo = v * (anchor + direction * lo)
        phase_hi = v * (anchor + direction * hi)
        small, large = sorted((phase_lo, phase_hi))
        for k in range(floor(small) - 1, floor(large) + 2):
            for boundary in (F(k) + DELTA, F(k + 1) - DELTA):
                displacement = (boundary / v - anchor) / direction
                if lo <= displacement <= hi:
                    events.add(displacement)
    events = sorted(events)

    def safe(s):
        return all(distance(v * (anchor + direction * s)) >= DELTA
                   for v in speeds)

    pieces = [(s, s) for s in events if safe(s)]
    for a, z in zip(events, events[1:]):
        if safe((a + z) / 2):
            assert safe(a) and safe(z), "Closed safety must retain cell ends"
            pieces.append((a, z))
    components = []
    for a, z in sorted(pieces):
        if components and a <= components[-1][1]:
            components[-1] = (components[-1][0], max(z, components[-1][1]))
        else:
            components.append((a, z))
    return components, len(events)


def main():
    anchors = sorted({F(p, d) for d in range(1, 9) for p in range(d)})
    assert len(anchors) == 22
    assert all(Q * a == floor(Q * a) for a in anchors)
    failures = []
    band_count = 0
    threshold_events = 0
    for anchor in anchors:
        for direction in (1, -1):
            first = {}
            for v in SPEEDS:
                components, count = safe_components(
                    (v,), anchor, direction, F(0), F(1, v))
                assert components
                first[v] = components[0]
                band_count += 1
                threshold_events += count
            assert first[Q] == (F(1, 8 * Q), F(7, 8 * Q))
            assert first[8 * Q] == (F(1, 64 * Q), F(7, 64 * Q))
            entry = max(band[0] for band in first.values())
            exit_ = min(band[1] for band in first.values())
            assert entry > exit_
            assert entry - exit_ >= F(1, 64 * Q)
            failures.append({"anchor": str(anchor), "direction": direction,
                             "entry": str(entry), "exit": str(exit_),
                             "first_bands": {
                                 str(v): [str(edge) for edge in first[v]]
                                 for v in SPEEDS
                             }})

    anchor = F(17, 56)
    left = anchor + F(9, 64 * Q)
    right = anchor + F(15, 64 * Q)
    assert right - left == F(3, 32 * Q)
    assert anchor < left < right < F(5, 16)
    epsilon = F(1, 128 * Q)
    local, count = safe_components(SPEEDS, F(0), 1,
                                   left - epsilon, right + epsilon)
    assert local == [(left, right)]
    midpoint = (left + right) / 2
    endpoint_margins = {}
    for v in SPEEDS:
        endpoint_margins[str(v)] = [str(distance(v * t) - DELTA)
                                    for t in (left, right)]
        assert distance(v * midpoint) > DELTA
        if v != 8 * Q:
            assert all(distance(v * t) > DELTA for t in (left, right))
        else:
            assert all(distance(v * t) == DELTA for t in (left, right))

    # Same interval, expressed from the allowed anchor 2/7.  Indices are zero
    # based relative to each runner's colliding lap there, not absolute laps.
    origin = F(2, 7)
    relative_labels = {
        str(v): floor(v * midpoint) - floor(v * origin) for v in (Q, 8 * Q)
    }
    assert relative_labels[str(Q)] == Q // 56
    assert relative_labels[str(8 * Q)] == Q // 7 + 1
    assert distance(Q * origin) == 0 == distance(8 * Q * origin)

    # Post-protocol refinement: keep an anchor that was already in the menu.
    menu_origin = F(3, 8)
    menu_left = menu_origin - F(15, 64 * Q)
    menu_right = menu_origin - F(9, 64 * Q)
    menu_local, menu_events = safe_components(
        SPEEDS, F(0), 1, menu_left - epsilon, menu_right + epsilon)
    assert menu_local == [(menu_left, menu_right)]
    assert F(17, 48) < menu_left < menu_right < menu_origin
    menu_midpoint = (menu_left + menu_right) / 2
    assert floor(Q * (menu_origin - menu_midpoint)) == 0
    assert floor(8 * Q * (menu_origin - menu_midpoint)) == 1

    # Frozen endpoint control: ratio seven makes first laps touch, rather than
    # becoming disjoint.  Reconstruct the singleton in a local neighborhood.
    boundary_speeds = (1, 4, 5, 6, 7, Q, 7 * Q)
    boundary_time = anchor + F(1, 8 * Q)
    boundary_component, boundary_events = safe_components(
        boundary_speeds, F(0), 1,
        boundary_time - epsilon, boundary_time + epsilon)
    assert boundary_component == [(boundary_time, boundary_time)]
    assert distance(Q * boundary_time) == DELTA
    assert distance(7 * Q * boundary_time) == DELTA

    # Frozen formula-only diagnostic: test exactly three candidate points,
    # endpoints plus midpoint; the written lifted-lap proof supplies the whole
    # interval.  This never loops over the B initial safe laps.
    huge_budget = 10 ** 12
    huge_fast = 8 * huge_budget * Q
    last_early_exit = (huge_budget - DELTA) / huge_fast
    assert F(1, 8 * Q) - last_early_exit == F(1, 64 * huge_budget * Q)
    huge_left = anchor + F(8 * huge_budget + 1, 64 * huge_budget * Q)
    huge_right = anchor + F(8 * huge_budget + 7, 64 * huge_budget * Q)
    huge_midpoint = (huge_left + huge_right) / 2
    assert huge_right - huge_left == F(3, 32 * huge_budget * Q)
    for v in (1, 4, 5, 6, 7, Q, huge_fast):
        assert distance(v * huge_midpoint) > DELTA
        for t in (huge_left, huge_right):
            if v == huge_fast:
                assert distance(v * t) == DELTA
            else:
                assert distance(v * t) > DELTA
    assert floor(huge_fast * (huge_midpoint - anchor)) == huge_budget

    print(json.dumps({
        "status": "pass",
        "scope": {"q": Q, "B": B, "reference": 0,
                  "total_runners": 8, "threshold": str(DELTA),
                  "moving_speeds": SPEEDS},
        "anchor_count_modulo_one": len(anchors),
        "directional_first_lap_failures": len(failures),
        "individual_first_components_reconstructed": band_count,
        "individual_threshold_event_evaluations": threshold_events,
        "smallest_pair_incompatibility_gap": str(F(1, 64 * Q)),
        "rescue_component": [str(left), str(right)],
        "rescue_width": str(right - left),
        "local_threshold_event_count": count,
        "endpoint_margins_by_speed": endpoint_margins,
        "relative_zero_based_lap_labels_from_2_over_7": relative_labels,
        "post_protocol_same_menu_rescue": {
            "anchor": str(menu_origin), "direction": -1,
            "component": [str(menu_left), str(menu_right)],
            "width": str(menu_right - menu_left),
            "local_threshold_event_count": menu_events,
            "slow_lap_ordinal": 1, "fast_lap_ordinal": 2,
        },
        "ratio_seven_endpoint_control": {
            "isolated_local_component": str(boundary_time),
            "local_threshold_event_count": boundary_events,
        },
        "large_budget_formula_only": {
            "B": huge_budget, "fast_speed": huge_fast,
            "strict_first_B_lap_gap": str(F(1, 8 * Q) - last_early_exit),
            "later_interval": [str(huge_left), str(huge_right)],
            "width": str(huge_right - huge_left),
            "fast_lap_ordinal": huge_budget + 1,
            "full_safe_set_or_first_B_lap_enumeration": False,
        },
        "failures": failures,
    }, indent=2))


if __name__ == "__main__":
    main()
