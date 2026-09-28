"""Independent exact verification of the frozen adaptive reflected pair.

No primary calculator is read or imported. Complete clipped triangular phase
envelopes, including all kinks and affine crossings, verify the eight fixed
controls. Directed intervals are checked inside individual safe laps rather
than by reconstructing full allowed sets. Finite checks are not a mechanical
verification of the accompanying unbounded mathematical argument.
"""
import argparse
import ast
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = '55d73b9e425f4ad8fa74441029cb88569f2091fcb3bdf3494c4cca656d92f7f7'
FIXED = (1, 4, 5, 6, 7)
CONTROLS = (13, 16, 32, 56, 88, 112, 120, 56000000000000)
BRANCHES = ('nonmultiple8', 'multiple8_not56', 'multiple56')
DELTA = Q(1, 8)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def near(value):
    phase = value % 1
    return min(phase, 1-phase)


def adaptive_time(V):
    if V % 8:
        return Q(1, 8), 1
    if V % 56:
        return Q(17, 56), 2
    return Q(17, 56)+Q(1, 8*V), 3


def line(beta, cap, theta):
    phase = (beta+theta) % 1
    distance = min(phase, 1-phase)
    if distance >= cap:
        return Q(0), cap
    slope = Q(1) if phase < Q(1, 2) else Q(-1)
    return slope, distance-slope*theta


def envelope(betas, caps):
    points = {Q(0), Q(1)}
    for beta, cap in zip(betas, caps):
        for corner in (Q(0), Q(1, 2), cap, 1-cap):
            points.add((corner-beta) % 1)
    initial = sorted(points)
    for a, b in zip(initial, initial[1:]):
        lines = [line(beta, cap, (a+b)/2) for beta, cap in zip(betas, caps)]
        for (s, z), (u, w) in combinations(lines, 2):
            if s != u:
                crossing = (w-z)/(s-u)
                if a < crossing < b:
                    points.add(crossing)
    points = sorted(points)
    values = {theta: max(min(cap, near(theta+beta)) for beta, cap in zip(betas, caps))
              for theta in points}
    cells = []
    for a, b in zip(points, points[1:]):
        mid = (a+b)/2
        lines = [line(beta, cap, mid) for beta, cap in zip(betas, caps)]
        for (s, z), (u, w) in combinations(lines, 2):
            if s != u:
                assert not a < (w-z)/(s-u) < b
        winner = max(range(len(betas)), key=lambda i: (lines[i][0]*mid+lines[i][1], -i))
        slope, intercept = lines[winner]
        for i, (beta, cap) in enumerate(zip(betas, caps)):
            for theta in (a, mid, b):
                assert min(cap, near(theta+beta)) == lines[i][0]*theta+lines[i][1]
        assert values[a] == slope*a+intercept and values[b] == slope*b+intercept
        cells.append(dict(left=a, right=b, slope=slope, intercept=intercept, winner=winner))
    return dict(points=points, values=values, cells=cells,
                minimum=min(values.values()), maximum=max(values.values()))


def direct_safe_lap(speed, left, right):
    """One fixed integer lap contains the entire proposed closed interval."""
    lap = (speed*left).numerator//(speed*left).denominator
    low, high = speed*left-lap, speed*right-lap
    assert DELTA <= low <= high <= 1-DELTA
    assert low < high
    # Affinity gives strict safety at every interior point without sampling.
    assert low < 1-DELTA and high > DELTA
    return dict(speed=speed, lap=lap, left_phase=str(low), right_phase=str(high),
                left_distance=str(near(speed*left)), right_distance=str(near(speed*right)))


def inspect(V):
    time, branch = adaptive_time(V)
    reflected = 1-time
    speeds = [*FIXED, V]
    vectors = [[near(speed*t) for speed in speeds] for t in (time, reflected)]
    assert vectors[0] == vectors[1]
    cap = min(vectors[0])
    betas = [(11*t) % 1 for t in (time, reflected)]
    separation = near(betas[1]-betas[0])
    raw = envelope(betas, [Q(1, 2)]*2)
    full = envelope(betas, [cap]*2)
    assert raw['minimum'] == separation/2
    assert full['minimum'] == full['maximum'] == cap == DELTA
    assert all(cell['slope'] == 0 and cell['intercept'] == DELTA for cell in full['cells'])
    equality = [[speed for speed, value in zip(speeds, vector) if value == DELTA] for vector in vectors]
    directed = None
    if branch > 1:
        radius = Q(1, 56*V)
        safe_laps = [direct_safe_lap(speed, time, time+radius) for speed in speeds]
        # Reflection reverses time, preserving all unchanged distances.
        for speed in speeds:
            assert near(speed*(reflected-radius)) == near(speed*(time+radius))
        selected_lower = separation/2-11*radius
        assert selected_lower > DELTA
        directed = dict(radius=radius, safe_laps=safe_laps, selected_endpoint_lower=selected_lower,
                        selected_excess=selected_lower-DELTA)
    else:
        assert near(time) == near(7*time) == DELTA
        assert time == Q(1, 8) and reflected == Q(7, 8)
    return dict(V=V, time=time, reflected=reflected, branch=branch, speeds=speeds,
                vectors=vectors, cap=cap, betas=betas, separation=separation,
                raw=raw, full=full, equality=equality, directed=directed)


def branch_checks():
    """Exact residues and affine coefficient endpoint checks, not a proof assistant."""
    branch1 = [[r, str(near(Q(r, 8)))] for r in range(1, 8)]
    assert all(Q(distance) >= DELTA for _, distance in branch1)
    branch2 = []
    for residue in range(1, 7):
        phase = Q(17*residue, 7) % 1
        endpoint = phase+Q(1, 56)
        assert DELTA < phase < 1-DELTA and DELTA < endpoint <= 1-DELTA
        branch2.append([residue, str(phase), str(endpoint)])
    # z=1/V lies in (0,1/56] in branch3. Exact fixed-runner phases on
    # [t,t+R] are affine in z, with coefficients checked at both bounds.
    branch3 = []
    for speed in FIXED:
        base = Q(17*speed, 56)
        lap = base.numerator//base.denominator
        phase0 = base-lap
        endpoints = []
        for z in (Q(0), Q(1, 56)):
            at_t = phase0+Q(speed, 8)*z
            at_end = phase0+Q(speed, 7)*z
            assert DELTA <= at_t <= at_end < 1-DELTA
            endpoints.append([str(z), str(at_t), str(at_end)])
        branch3.append(dict(speed=speed, fixed_lap=lap, limiting_endpoint_checks=endpoints))
    # Explicit affine room numerators after clearing positive denominators.
    assert 8*2-11 > 0  # branch2 selected margin: (2V-11)/(56V).
    assert 56-44 > 0  # branch3 selected margin: (V-44)/(28V).
    assert 8-2 > 0  # 1/112 - R has numerator V-2 over112V.
    assert 56-16 > 0  # branch3 core room minusR=(V-16)/(112V).
    return dict(branch1_nonzero_mod8_distances=branch1,
                branch2_nonzero_mod7_phases_and_radius_endpoints=branch2,
                branch3_fixed_speed_affine_endpoint_checks=branch3,
                selected_excess_formulas={'branch2': '(2V-11)/(56V)', 'branch3': '(V-44)/(28V)'},
                core_radius_excess_formulas={'branch2': '(V-2)/(112V)', 'branch3': '(V-16)/(112V)'},
                branch3_fastest_phase_interval=['1/8', '1/7'],
                limit='These residue and affine arithmetic checks support the supplied branch argument; they are not a mechanical proof of its unbounded quantifiers.')


def assert_fields(expected, actual, label):
    for field, value in expected.items():
        assert field in actual, (label, 'missing', field)
        assert actual[field] == value, (label, field, 'computed', value, 'archived', actual[field])


def controller_direction(phase):
    return 'right' if phase == DELTA else ('left' if phase == 1-DELTA else None)


def safe_lap_at(speed, time):
    value = speed*time
    lap = value.numerator//value.denominator
    left, right = Q(8*lap+1, 8*speed), Q(8*lap+7, 8*speed)
    phase = value-lap
    assert left <= time <= right
    return dict(lap=lap, interval=[str(left), str(right)], phase=str(phase), distance=str(near(value)),
                left_clearance=str(time-left), right_clearance=str(right-time),
                controller_direction=controller_direction(phase))


def diagnostic(record):
    V, time, reflected = record['V'], record['time'], record['reflected']
    speeds = record['speeds']
    phase_vectors = [[(speed*t) % 1 for speed in speeds] for t in (time, reflected)]
    attaining = [theta for theta in record['raw']['points'][:-1]
                 if record['raw']['values'][theta] == record['raw']['minimum']]
    assert len(attaining) == 1
    result = dict(V=V, branch=BRANCHES[record['branch']-1], times=[str(time), str(reflected)],
                  unchanged_speeds=speeds, unchanged_phase_vectors=[list(map(str, v)) for v in phase_vectors],
                  unchanged_distance_vectors=[list(map(str, v)) for v in record['vectors']],
                  unchanged_cap=str(record['cap']), equality_controllers=record['equality'],
                  equality_controller_directions=[[[speed, controller_direction(phase)]
                                                   for speed, phase in zip(speeds, phases)
                                                   if phase in (DELTA, 1-DELTA)] for phases in phase_vectors],
                  selected_phase_pair=list(map(str, record['betas'])),
                  selected_phase_separation=str(record['separation']),
                  half_separation=str(record['separation']/2),
                  half_separation_slack=str(record['separation']/2-DELTA),
                  raw_pair_minimizer_theta=str(attaining[0]),
                  pair_envelope_minimum=str(record['full']['minimum']),
                  pair_envelope_maximum=str(record['full']['maximum']),
                  constant_in_phase=record['full']['minimum'] == record['full']['maximum'],
                  safe_laps=[dict(speed=speed, at_t=safe_lap_at(speed, time),
                                  at_reflection=safe_lap_at(speed, reflected)) for speed in speeds],
                  directed_certificate=None)
    if record['directed'] is not None:
        radius = record['directed']['radius']
        core_room = Q(5, 16)-time
        variable_room = (1-DELTA-(V*time) % 1)/V
        selected_room = (record['separation']/2-DELTA)/11
        minimum_room = min(core_room, variable_room, selected_room)
        assert radius <= minimum_room
        result['directed_certificate'] = dict(
            radius=str(radius), core_room=str(core_room), variable_room=str(variable_room),
            selected_room=str(selected_room), minimum_room=str(minimum_room),
            radius_within_room=radius <= minimum_room,
            selected_distance_lower_bound_at_radius=str(record['directed']['selected_endpoint_lower']),
            selected_slack_at_radius=str(record['directed']['selected_excess']),
            candidate_intervals=[[str(time), str(time+radius)], [str(reflected-radius), str(reflected)]],
            unchanged_phase_segments=[[row['speed'], row['left_phase'], row['right_phase']]
                                      for row in record['directed']['safe_laps']],
            unchanged_endpoint_distances=[[str(near(speed*t)) for speed in speeds]
                                           for t in (time+radius, reflected-radius)],
            strict_open_interior_verified=True)
    return result


def directed_selected_check(record):
    if record['directed'] is None:
        # The fixed1 and7 threshold controllers point in opposite directions
        # at both candidates, regardless of the chosen runner's phase.
        return dict(opposing_unchanged_controllers=True, phase_cells=0, phase_points=0)
    radius = record['directed']['radius']
    betas = record['betas']
    endpoint_betas = [(betas[0]+11*radius) % 1, (betas[1]-11*radius) % 1]
    events = set(record['raw']['points'])
    for beta in endpoint_betas:
        for corner in (Q(0), Q(1, 2), DELTA, 1-DELTA):
            events.add((corner-beta) % 1)
    events = sorted(events)
    cells = []
    for a, b in zip(events, events[1:]):
        mid = (a+b)/2
        winner = max(range(2), key=lambda i: (near(mid+betas[i]), -i))
        selected = [near(theta+endpoint_betas[winner]) for theta in (a, mid, b)]
        assert min(selected) >= record['directed']['selected_endpoint_lower'] > DELTA
        endpoint_line = line(endpoint_betas[winner], Q(1, 2), mid)
        assert all(near(theta+endpoint_betas[winner]) == endpoint_line[0]*theta+endpoint_line[1]
                   for theta in (a, mid, b))
        cells.append([str(a), str(b), winner, str(min(selected))])
    for theta in events:
        winner = max(range(2), key=lambda i: (near(theta+betas[i]), -i))
        assert near(theta+betas[winner]) >= record['separation']/2
        assert near(theta+endpoint_betas[winner]) >= record['directed']['selected_endpoint_lower'] > DELTA
    return dict(opposing_unchanged_controllers=False, phase_cells=len(cells), phase_points=len(events),
                directed_selected_cells_sha256=digest(cells))


def encode_envelope(value):
    return dict(points=[[str(theta), str(value['values'][theta])] for theta in value['points']],
                cells=[[str(cell['left']), str(cell['right']), str(cell['slope']), str(cell['intercept']), cell['winner']]
                       for cell in value['cells']])


def formula_value(expression, variables):
    """Interpret only rational arithmetic in displayed formula data, never code."""
    expression = re.sub(r'(?<=[0-9])(?=V)', '*', expression)
    def visit(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return Q(node.value)
        if isinstance(node, ast.Name) and node.id in variables:
            return Q(variables[node.id])
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left+right
            if isinstance(node.op, ast.Sub):
                return left-right
            if isinstance(node.op, ast.Mult):
                return left*right
            if isinstance(node.op, ast.Div):
                return left/right
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'min' and not node.keywords:
            return min(map(visit, node.args))
        raise AssertionError(('unsupported formula syntax', expression, type(node).__name__))
    return visit(ast.parse(expression, mode='eval').body)


def verify_symbolic(branches, records):
    assert len(branches) == 3
    rules = [
        'At t: 1 enters right,7 enters left; V enters right if r=1,left if r=7. Reflection reverses directions.',
        'At t only speed7 equals1/8 and enters right. Reflection enters left.',
        'At t only speedV equals1/8 and enters right. Reflection enters left.']
    conditions = ['8 does not divide V', '8 divides V and56 does not divide V', '56 divides V']
    evaluated = 0
    for index, branch in enumerate(branches):
        assert_fields(dict(id=BRANCHES[index], condition=conditions[index],
                           equality_controller_rule=rules[index], constant_in_phase=True,
                           unchanged_inward_direction='none' if index == 0 else 'right'),
                      branch, ('symbolic branch metadata', index))
        for record in records:
            if record['branch'] != index+1:
                continue
            V = record['V']
            variables = dict(V=V, r=V % 8, k=(17*(V//8)) % 7)
            expected = dict(time_formula=record['time'],
                            selected_phase_at_t_formula=record['betas'][0],
                            separation_formula=record['separation'],
                            half_separation_formula=record['separation']/2,
                            half_separation_slack_formula=record['separation']/2-DELTA,
                            envelope_minimum_formula=record['full']['minimum'],
                            envelope_maximum_formula=record['full']['maximum'])
            if record['directed'] is None:
                assert branch['directed_radius_formula'] is None and branch['directed_radius_slack_formula'] is None
            else:
                expected['directed_radius_formula'] = record['directed']['radius']
                expected['directed_radius_slack_formula'] = record['directed']['selected_excess']
            for field, value in expected.items():
                assert formula_value(branch[field], variables) == value, (V, field)
                evaluated += 1
            assert [formula_value(value, variables) for value in branch['unchanged_phase_formulas']] == [
                (speed*record['time']) % 1 for speed in record['speeds']]
            assert [formula_value(value, variables) for value in branch['unchanged_distance_formulas']] == record['vectors'][0]
            evaluated += 12
    return evaluated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = (HERE/'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(raw)
    assert protocol['finite_diagnostics'] == list(CONTROLS)
    checks = branch_checks()
    records = [inspect(V) for V in CONTROLS]
    expected_rows = [diagnostic(record) for record in records]
    source_bytes = (HERE/'results.json').read_bytes()
    source = json.loads(source_bytes)
    assert source['schema_version'] == 1 and source['protocol_sha256'] == PROTOCOL_SHA256
    expected_summary = dict(diagnostic_count=8,
                            branch_counts={branch: sum(row['branch'] == branch for row in expected_rows) for branch in BRANCHES},
                            all_pair_envelopes_constant_threshold=all(row['constant_in_phase'] and row['pair_envelope_minimum'] == '1/8' for row in expected_rows),
                            directed_certificate_count=sum(row['directed_certificate'] is not None for row in expected_rows),
                            all_directed_checks_pass=all(row['directed_certificate'] is None or row['directed_certificate']['strict_open_interior_verified']
                                                        for row in expected_rows))
    stream = sha256()
    for row in expected_rows:
        stream.update((canonical(row)+'\n').encode())
    assert_fields(dict(unchanged_speed_order=[*FIXED, 'V'], diagnostics=expected_rows,
                       diagnostics_sha256=stream.hexdigest(), summary=expected_summary,
                       directed_selection_rule='For each theta choose the candidate maximizing speed11 distance, taking t on a tie; use its directed interval. Do not select by the tied full pair margin.',
                       status='OBSERVED exact eight diagnostics; symbolic general implications remain HYPOTHESIS/proof candidates; no novelty claim'),
                  source, 'primary results')
    symbolic_evaluations = verify_symbolic(source['symbolic_branches'], records)
    verification_rows = []
    for record in records:
        directional = directed_selected_check(record)
        verification_rows.append(dict(V=record['V'], branch=BRANCHES[record['branch']-1],
                                      raw_pair_minimum=str(record['raw']['minimum']),
                                      raw_phase_cells=len(record['raw']['cells']), raw_phase_points=len(record['raw']['points']),
                                      raw_envelope_sha256=digest(encode_envelope(record['raw'])),
                                      full_phase_cells=len(record['full']['cells']), full_phase_points=len(record['full']['points']),
                                      full_envelope_sha256=digest(encode_envelope(record['full'])),
                                      full_pair_margin='1/8', constant_in_phase=True,
                                      directed_radius=str(record['directed']['radius']) if record['directed'] else None,
                                      directed_selected_runner_check=directional))
        print('PASS:', record['V'], 'all diagnostic fields; complete raw/full phase envelopes', flush=True)
    out = dict(status='REPRODUCED eight finite controls; general branch implications remain proof candidates',
               protocol_sha256=PROTOCOL_SHA256, source_results_sha256=sha256(source_bytes).hexdigest(),
               primary_script_sha256=source['script_sha256'],
               verifier_script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
               diagnostics_sha256=stream.hexdigest(),
               control_count=8, raw_and_full_envelopes=16,
               raw_and_full_phase_cells=sum(row['raw_phase_cells']+row['full_phase_cells'] for row in verification_rows),
               raw_and_full_phase_points=sum(row['raw_phase_points']+row['full_phase_points'] for row in verification_rows),
               directed_certificates=7, unchanged_directed_safe_laps=42,
               directed_selected_phase_cells=sum(row['directed_selected_runner_check']['phase_cells'] for row in verification_rows),
               directed_selected_phase_points=sum(row['directed_selected_runner_check']['phase_points'] for row in verification_rows),
               symbolic_formula_substitutions=symbolic_evaluations,
               methods=['direct rational phases and unchanged distance vectors at the prescribed adaptive pair',
                        'complete triangular and clipped phase envelopes from all corners, cap roots and line crossings',
                        'direct unchanged-runner single-safe-lap endpoint inequalities',
                        'raw speed11 maximizer selection with exact directed-endpoint phase partitions',
                        'finite residue and affine endpoint coefficient checks for the supplied branch formulas',
                        'full diagnostic dictionary and canonical digest agreement'],
               verification_limits=[
                   'Only the eight frozen values are substituted; no broad speed enumeration or complete safe-time set is calculated.',
                   'On each algebraic envelope cell every clipped distance is affine and every crossing is included. The winning affine branch and exact endpoints certify the entire cell; no uniform phase grid is used.',
                   'For divisible controls, unchanged phases lie in one closed safe lap throughout each candidate interval. Open interior is strict; a far endpoint can be equality, as for speed16 atV16.',
                   'The chosen candidate maximizes raw speed11 distance, with t on ties. Its selected-runner endpoint is strictly safe across the complete derived phase partition; the distance bound certifies persistence over the interval.',
                   'Seven mod8 residues, six nonzero mod7 residues and affine coefficient endpoints are finite arithmetic checks. Together with displayed formulas they support, but do not mechanically establish, the supplied unbounded branch proof.',
                   'Opposing speed1 and7 controllers prevent a strict one-sided neighborhood at the first-branch pair; this makes no assertion about strictness elsewhere.'],
               branch_checks=checks, summary=expected_summary, cases=verification_rows)
    destination = HERE/'verification.json'
    if args.write:
        destination.write_text(json.dumps(out, indent=2)+'\n')
    else:
        assert json.loads(destination.read_text()) == out
    print('PASS: full independent adaptive-pair comparison;', 'saved' if args.write else 'read-only replay', flush=True)


if __name__ == '__main__':
    main()
