"""Frozen finite rank-three discovery. Standard library, exact arithmetic."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd, floor, ceil
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROWS = ((1,0,0),(0,1,0),(1,1,0),(2,1,0),(3,1,0),
        (3,2,0),(6,2,0),(3,8,0),(0,0,1))
DELTA = F(1,8)
COUNTS = {'contacts': 0, 'H1_attempts': 0,
          'diagnostic_contacts': 0, 'diagnostic_H1_attempts': 0}


def encode(x):
    if isinstance(x, F):
        return str(x)
    raise TypeError(type(x).__name__)


def save(name, x):
    (HERE/name).write_text(json.dumps(x, default=encode, sort_keys=True,
                                    separators=(',', ':'))+'\n')


def check_pins():
    pins = json.loads((HERE/'INPUTS.json').read_text())
    for path, expected in pins['files'].items():
        raw = (ROOT/path).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == expected['sha256'], path
    return pins


def egcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r//r
        old_r, r = r, old_r-q*r
        old_s, s = s, old_s-q*s
        old_t, t = t, old_t-q*t
    return old_r, old_s, old_t


def lattice(v):
    g = gcd(*v)
    A, B, C = (n//g for n in v)
    d, a, b = egcd(A, B)
    P, Q = A//d, B//d
    h, c, e = egcd(d, C)
    assert h == 1 and a*P+b*Q == 1
    return {'g':g, 'normalized':[A,B,C], 'd':d, 'P':P, 'Q':Q,
            'a':a, 'b':b, 'c':c, 'e':e,
            'relations':[[Q,-P,0],[C*a,C*b,-d]]}


def sources():
    raw = json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())
    records = raw['certificate']['candidates']
    records.sort(key=lambda s: (s['parent'],*s['edge'],s['seventh_lap'],s['eighth_lap']))
    assert len(records) == 36
    result = []
    for s in records:
        endpoints = [list(map(F,p)) for p in s['endpoints']]
        for p in endpoints:
            for row, lap in zip(ROWS[:8],s['labels']):
                assert DELTA <= row[0]*p[0]+row[1]*p[1]-lap <= 1-DELTA
        result.append({**s, 'endpoints':endpoints})
    return result


def objects(src):
    edges, sheets = [], []
    for i, s in enumerate(src):
        for tag, z in [('L',DELTA),('U',1-DELTA)]:
            edges.append({'id':s['id']+':Z'+tag,'source':i,
                          'endpoints':s['endpoints'],'z_range':[z,z]})
        sheets.append({'id':s['id']+':ZSLAB','source':i,
                       'endpoints':s['endpoints'],'z_range':[DELTA,1-DELTA]})
    assert len(edges)+len(sheets) == 108
    return {'edges':edges, 'sheets':sheets}


def dot(row, point):
    return sum(a*b for a,b in zip(row,point))


def at(obj, s, z):
    A, B = obj['endpoints']
    return [A[0]+s*(B[0]-A[0]), A[1]+s*(B[1]-A[1]), z]


def intersect(obj, relations, charge=True):
    """Find one integer contact for a segment times a z interval."""
    hrow, nrow = relations
    zl, zu = obj['z_range']
    h0, h1 = [dot(hrow, at(obj,F(s),zl)) for s in [0,1]]
    lo, hi = ceil(min(h0,h1)), floor(max(h0,h1))
    if hi-lo+1 > 64:
        raise RuntimeError('SCOPE_LIMIT: H1 per contact')
    contact_key = 'contacts' if charge else 'diagnostic_contacts'
    attempt_key = 'H1_attempts' if charge else 'diagnostic_H1_attempts'
    COUNTS[contact_key] += 1
    if COUNTS['contacts']+COUNTS['diagnostic_contacts'] > 100000:
        raise RuntimeError('SCOPE_LIMIT: contact count')
    def attempt():
        COUNTS[attempt_key] += 1
        if COUNTS['H1_attempts']+COUNTS['diagnostic_H1_attempts'] > 5000000:
            raise RuntimeError('SCOPE_LIMIT: H1 total')
    if h0 == h1:
        if h0.denominator != 1:
            return None
        choices = sorted((dot(nrow,at(obj,s,z)),s,z)
                         for s in [F(0),F(1)] for z in [zl,zu])
        low = choices[0]
        high_value = choices[-1][0]
        high = next(v for v in choices if v[0] == high_value)
        n = ceil(low[0])
        attempt()
        if n > high[0]:
            return None
        u = F(0) if high[0] == low[0] else (n-low[0])/(high[0]-low[0])
        s,z = [low[j]+u*(high[j]-low[j]) for j in [1,2]]
        return {'point':at(obj,s,z),'s':s,'H1':int(h0),'H2':n}
    for h in range(lo,hi+1):
        attempt()
        s = (h-h0)/(h1-h0)
        low, high = sorted(dot(nrow,at(obj,s,z)) for z in [zl,zu])
        n = ceil(low)
        if n <= high:
            xy = at(obj,s,F(0))
            z = (n-dot(nrow,xy))/nrow[2]
            return {'point':at(obj,s,z),'s':s,'H1':h,'H2':n}
    return None


def speeds(v):
    return [dot(row,v) for row in ROWS]


def valid(v):
    return len(set([0]+speeds(v))) == 10


def witness(v, lat, obj, hit, src):
    x,y,z = hit['point']
    w = lat['a']*x+lat['b']*y
    T = lat['c']*w+lat['e']*z
    tau = T % 1
    time = tau/lat['g']
    vs = speeds(v)
    laps = [floor(n*time) for n in vs]
    phases = [n*time-l for n,l in zip(vs,laps)]
    labels = src[obj['source']]['labels']+[0]
    ambient = [dot(row,[x,y,z])-l for row,l in zip(ROWS,labels)]
    assert phases == ambient and all(DELTA <= f <= 1-DELTA for f in phases)
    assert [dot(row,[x,y,z]) for row in lat['relations']] == [hit['H1'],hit['H2']]
    assert [n*time % 1 for n in v] == [x,y,z]
    assert 0 < time < F(1,lat['g'])
    return {**hit,'object':obj['id'],'source':obj['source'],
            'pair_clock':w,'recovery_raw':T,'tau':tau,'time':time,
            'torus_laps':labels,'physical_laps':laps,'phases':phases,
            'minimum':min(min(f,1-f) for f in phases)}


def build_rows(triples, split, objs, src):
    rows = []
    for v in triples:
        lat = lattice(v)
        row = {'pqr':list(v),'split':split,'lattice':lat,'hits':{},'_contacts':{}}
        for kind, candidates in objs.items():
            hits = [intersect(o,lat['relations']) for o in candidates]
            row['hits'][kind] = ''.join('1' if h else '0' for h in hits)
            row['_contacts'][kind] = hits
        rows.append(row)
    return rows


def compile_menu(rows, kind, candidates):
    remaining = set(range(len(rows)))
    menu, trace = [], []
    while remaining and len(menu) < 8:
        gains = [sum(rows[j]['hits'][kind][i]=='1' for j in remaining)
                 for i in range(len(candidates))]
        gain = max(gains)
        if not gain:
            break
        i = gains.index(gain)
        covered = sorted(j for j in remaining if rows[j]['hits'][kind][i]=='1')
        menu.append(i)
        remaining.difference_update(covered)
        trace.append({'object_index':i,'gain':gain,'covered_train_rows':covered})
    status = 'COMPACT_TRAIN' if not remaining else ('MENU_CAP' if len(menu)==8 else 'NO_GAIN')
    return {'indices':menu,'ids':[candidates[i]['id'] for i in menu],
            'trace':trace,'uncovered_train_rows':sorted(remaining),'stop':status}


def marginal_possible(obj, relations):
    return all(ceil(min(vals)) <= floor(max(vals)) for vals in
               [[dot(row,at(obj,s,z)) for s in [F(0),F(1)]
                 for z in obj['z_range']] for row in relations])


def run():
    pins = check_pins()
    src = sources()
    objs = objects(src)
    triples = [v for v in itertools.product(range(1,10),repeat=3)
               if gcd(*v)==1 and valid(v)]
    train = build_rows([v for v in triples if max(v)<=6],'train',objs,src)
    menus = {kind:compile_menu(train,kind,candidates) for kind,candidates in objs.items()}
    holdout = build_rows([v for v in triples if max(v)>6],'holdout',objs,src)
    controls0 = [(2,3,4),(2,5,3),(4,3,5),(6,4,3),(3,6,4),(5,4,7)]
    control_triples = [tuple(k*a for a in v) for v in controls0 for k in [1,2]]
    assert all(valid(v) for v in control_triples)
    controls = build_rows(control_triples,'scaling_control',objs,src)
    diagnostics = {'false_marginal':None,'unsaturated_false_point':None,'lost_clock_lift':None}
    all_rows = train+holdout+controls
    for row in sorted(all_rows,key=lambda x:(x['split']=='scaling_control',tuple(x['pqr']))):
        v,lat = row['pqr'],row['lattice']
        row['selected'] = {}
        row['class_fallback'] = {}
        for kind,candidates in objs.items():
            hits = row['_contacts'][kind]
            selected = next((i for i in menus[kind]['indices'] if hits[i]),None)
            fallback = next((i for i,h in enumerate(hits) if h),None)
            row['selected'][kind] = None if selected is None else witness(v,lat,candidates[selected],hits[selected],src)
            row['class_fallback'][kind] = (witness(v,lat,candidates[fallback],hits[fallback],src)
                if selected is None and fallback is not None else None)
        # Diagnostics use reached data only and never alter either menu.
        if row['split'] != 'scaling_control':
            for kind,candidates in objs.items():
                for i,obj in enumerate(candidates):
                    if diagnostics['false_marginal'] is None and not row['_contacts'][kind][i] and marginal_possible(obj,lat['relations']):
                        diagnostics['false_marginal'] = {'pqr':v,'kind':kind,'object_index':i,'object':obj,
                            'relations':lat['relations'],
                            'ranges':[[min(dot(r,at(obj,s,z)) for s in [F(0),F(1)] for z in obj['z_range']),
                                       max(dot(r,at(obj,s,z)) for s in [F(0),F(1)] for z in obj['z_range'])]
                                      for r in lat['relations']]}
                    if diagnostics['unsaturated_false_point'] is None:
                        A,B,C = lat['normalized']
                        raw_relations = [[B,-A,0],[C,0,-A]]
                        h = intersect(obj,raw_relations,charge=False)
                        if h and any(dot(r,h['point']).denominator != 1 for r in lat['relations']):
                            diagnostics['unsaturated_false_point'] = {'pqr':v,'kind':kind,'object_index':i,
                                'object':obj,'raw_relations':raw_relations,'raw_hit':h,
                                'saturated_relations':lat['relations'],
                                'saturated_values':[dot(r,h['point']) for r in lat['relations']]}
            w = row['selected']['sheets'] or row['class_fallback']['sheets']
            if w and diagnostics['lost_clock_lift'] is None:
                canonical = (w['pair_clock'] % 1)/(lat['d']*lat['g'])
                phase = (v[2]*canonical) % 1
                if not DELTA <= phase <= 1-DELTA:
                    diagnostics['lost_clock_lift'] = {'pqr':v,'canonical_time':canonical,
                        'canonical_r_phase':phase,'recovered':w,'lattice':lat,
                        'lift_index':floor(lat['d']*w['tau'])}
        del row['_contacts']
    summary = {'scope':'Frozen finite boxes; no infinite-domain reduction',
               'train_count':len(train),'holdout_count':len(holdout),
               'scaling_control_invocations':len(controls),'counts':COUNTS.copy(),'classes':{}}
    for kind,candidates in objs.items():
        stats = {}
        for split,rows in [('train',train),('holdout',holdout),('scaling_control',controls)]:
            stats[split] = {'total':len(rows),
                'class_hits':sum('1' in row['hits'][kind] for row in rows),
                'menu_hits':sum(row['selected'][kind] is not None for row in rows)}
        stats['objects'] = len(candidates)
        stats['menu_size'] = len(menus[kind]['indices'])
        stats['status'] = ('COMPACT_TRANSFER' if all(stats[s]['menu_hits']==stats[s]['total']
                            for s in ['train','holdout']) else 'PARTIAL_FINITE_COVER')
        summary['classes'][kind] = stats
    result = {'protocol_sha256':pins['protocol_sha256'],'rows':ROWS,'threshold':DELTA,
              'sources':src,'objects':objs,'menus':menus,'cases':all_rows,
              'diagnostics':diagnostics,'summary':summary}
    save('discovery.json',result)
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))


if __name__ == '__main__':
    run()
