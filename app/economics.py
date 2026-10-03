"""Ateliers indépendants. Équations pures ; aucun état de session serveur."""
from dataclasses import asdict
from math import isfinite
from .model import Parameters, solve, ws
from .units import percent, proportion, dashboard, indicator, radar

DEFAULTS = {
    'wsps': {'A': 1., 'mu': 20., 'z': 0., 'alpha': 2.5, 'beta': 1., 'observed': 10.},
    'phillips': {'expected': 2., 'ustar': 10., 'cost': 0., 'slope': .5, 'u': 10., 'adaptation': .5},
    'okun': {'growth': 2., 'threshold': 2., 'reaction': .4, 'initial_u': 10.},
}
LIMITS = {
    'wsps': {'A': (.2, 3), 'mu': (0, 150), 'z': (-1, 1), 'alpha': (.1, 6), 'beta': (0, 1), 'observed': (0, 100)},
    'phillips': {'expected': (-5, 15), 'ustar': (0, 30), 'cost': (-5, 10), 'slope': (.05, 2), 'u': (0, 30), 'adaptation': (0, 1)},
    'okun': {'growth': (-10, 12), 'threshold': (-2, 6), 'reaction': (.05, 1.5), 'initial_u': (0, 100)},
}


def validate(model, values):
    if model not in DEFAULTS:
        raise ValueError('Atelier inconnu.')
    if not isinstance(values, dict) or set(values) - set(DEFAULTS[model]):
        raise ValueError('Paramètres invalides ou inconnus.')
    p = dict(DEFAULTS[model])
    for k, v in values.items():
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v):
            raise ValueError(f'{k} doit être un nombre fini.')
        low, high = LIMITS[model][k]
        if not low <= v <= high:
            raise ValueError(f'{k} doit être compris entre {low} et {high}.')
        p[k] = float(v)
    return p


def curve(name, points, style=0):
    return {'name': name, 'points': points, 'style': style}


def result_wsps(p, axis='unemployment', **_):
    wp = Parameters(**{**p, 'mu': proportion(p['mu']), 'observed': proportion(p['observed'])})
    r = solve(wp)
    position = lambda u: percent(1-u if axis == 'employment' else u)
    series = [curve('WS', [[position(i/100), v] for i, v in enumerate(r['ws'])]),
              curve('PS', [[0, r['index']], [100, r['index']]], 1)]
    points = []
    if r['in_domain']:
        points.append({'name': 'E', 'x': position(r['u']), 'y': r['index']})
    indicators = dashboard(unemployment=indicator(percent(r['u']) if r['interior'] else None, 'calculé', 'Chômage d’équilibre u*, distinct du chômage observé.'))
    warnings = [] if r['interior'] else ['Aucun équilibre intérieur avec ces paramètres. Intersection algébrique u* = %.2f %% ; aucune borne imposée.' % percent(r['u'])]
    return {'curves': series, 'points': points, 'x_label': ('Emploi' if axis == 'employment' else 'Chômage') + ' · % des actifs',
            'y_label': 'Salaire réel · indice base 100 initiale', 'domain_x': [0, 100],
            'observed': {'x': position(wp.observed), 'y1': r['observed_ws'], 'y2': r['index']},
            'metrics': [{'label': 'Chômage d’équilibre', 'value': percent(r['u']) if r['interior'] else None, 'unit': '% des actifs'},
                        {'label': 'Salaire réel d’équilibre', 'value': r['index'] if r['interior'] else None, 'unit': 'indice base 100'},
                        {'label': 'Emploi parmi les actifs', 'value': percent(r['employment']) if r['interior'] else None, 'unit': '% des actifs'}],
            'indicators': indicators, 'warnings': warnings, 'raw': r}


def phillips_value(p, u, expected=None):
    return (p['expected'] if expected is None else expected) - p['slope'] * (u - p['ustar']) + p['cost']


def result_phillips(p, expectation='fixed', period=0, **_):
    expected = p['expected']
    path = []
    for t in range(13):
        inflation = phillips_value(p, p['u'], expected)
        path.append({'t': t, 'expected': expected, 'inflation': inflation, 'unemployment': p['u']})
        if expectation == 'adaptive':
            expected += p['adaptation'] * (inflation - expected)
    row = path[period]
    pi = row['inflation']
    neutral_u = p['ustar'] + p['cost'] / p['slope']
    points = [{'name': 'M', 'x': p['u'], 'y': pi}]
    if 0 <= neutral_u <= 30:
        points.append({'name': 'N : π = πᵉ', 'x': neutral_u, 'y': row['expected']})
    warnings=[]
    if not 0 <= neutral_u <= 30:
        warnings.append(f'Le point N : π = πᵉ se situerait à u = {neutral_u:.2f} %, hors de l’axe [0 ; 30 %] ; il n’est pas ramené aux bornes.')
    return {'curves': [curve('Phillips', [[u/2, phillips_value(p,u/2,row['expected'])] for u in range(61)]),
                       curve('πᵉ · anticipation', [[0,row['expected']],[30,row['expected']]], 1)],
            'points': points, 'domain_x': [0,30], 'x_label': 'Chômage · % des actifs', 'y_label': 'Inflation · % par période',
            'metrics': [{'label': 'Inflation calculée', 'value': pi, 'unit': '% par période'},
                        {'label': 'Inflation anticipée', 'value': row['expected'], 'unit': '% par période'},
                        {'label': 'Écart u − u*', 'value': p['u']-p['ustar'], 'unit': 'points de %'}],
            'indicators': dashboard(inflation=indicator(pi,'calculé','Équation de Phillips ; inflation, pas niveau des prix.'),
                                    unemployment=indicator(p['u'],'donnée','Chômage observé imposé, non déterminé par Phillips.')),
            'warnings': warnings, 'raw': {'pi':pi,'expected':row['expected'],'neutral_u':neutral_u}, 'trajectory':path}


def result_okun(p, **_):
    delta = -p['reaction'] * (p['growth'] - p['threshold'])
    if abs(delta) < 1e-12: delta = 0.0
    next_u = p['initial_u'] + delta
    valid = 0 <= next_u <= 100
    return {'curves': [curve('Okun', [[g/2,-p['reaction']*(g/2-p['threshold'])] for g in range(-20,25)]),
                       curve('Δu = 0', [[-10,0],[12,0]],1)],
            'points': [{'name':'M','x':p['growth'],'y':delta}, {'name':'S : seuil','x':p['threshold'],'y':0}],
            'domain_x':[-10,12], 'x_label':'Croissance du PIB réel · % sur la période', 'y_label':'Variation du chômage · points de %',
            'metrics':[{'label':'Variation du chômage','value':delta,'unit':'points de %'},
                       {'label':'Chômage en fin de période','value':next_u if valid else None,'unit':'% des actifs'},
                       {'label':'Seuil de croissance','value':p['threshold'],'unit':'% sur la période'}],
            'indicators':dashboard(growth=indicator(p['growth'],'donnée','Croissance réelle imposée.'),
                                   unemployment=indicator(next_u if valid else None,'calculé','Chômage de fin de période ; u début + Δu.')),
            'warnings':[] if valid else ['Chômage de fin de période hors de [0 ; 100 %%] : %.2f %%. L’approximation d’Okun sort de son domaine ; résultat non écrêté.' % next_u],
            'raw':{'delta_u':delta,'next_u':next_u,'valid':valid}}


SOLVERS = {'wsps': result_wsps, 'phillips': result_phillips, 'okun': result_okun}


def calculate(payload):
    if not isinstance(payload, dict):
        raise ValueError('Objet JSON attendu.')
    model = payload.get('model', 'wsps')
    if not isinstance(model,str): raise ValueError('Atelier invalide.')
    p = validate(model, payload.get('parameters', {}))
    ref = validate(model, payload.get('reference', {}))
    fraction = payload.get('fraction', 1)
    if isinstance(fraction,bool) or not isinstance(fraction,(int,float)) or not isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError('Progression de comparaison invalide.')
    axis=payload.get('axis','unemployment')
    expectation=payload.get('expectation','fixed')
    period=payload.get('period',0)
    if axis not in ('unemployment','employment') or expectation not in ('fixed','adaptive'):
        raise ValueError('Convention inconnue.')
    if isinstance(period,bool) or not isinstance(period,int) or not 0 <= period <= 12:
        raise ValueError('Période invalide.')
    current={k: ref[k]+fraction*(p[k]-ref[k]) for k in p}
    # Keep exact endpoints and their economic interpretation.
    if fraction==1: current=p
    if fraction==0: current=ref
    options={'axis':axis,'expectation':expectation,'period':period}
    r=SOLVERS[model](current,**options)
    baseline=SOLVERS[model](ref,axis=axis,expectation=expectation,period=0)
    target=SOLVERS[model](p,**options)
    for row in (r,baseline,target): row['radar']=radar(row['indicators'])
    # Precompute a stable vertical extent for all comparison frames and trajectory periods.
    # WS–PS can have interior extrema when interpolating A and beta: sample the
    # full path plus a generous margin; client never rescales an individual frame.
    values=[0]
    for j in range(101):
        between={k:ref[k]+j/100*(p[k]-ref[k]) for k in p}
        sample=SOLVERS[model](between,**options)
        for c in sample['curves']: values.extend(y for _,y in c['points'])
    if model=='phillips':
        for pp in (p,ref):
            for t in range(13):
                sample=SOLVERS[model](pp,axis=axis,expectation=expectation,period=t)
                for c in sample['curves']: values.extend(y for _,y in c['points'])
    span=max(max(values)-min(values),1)
    from .pedagogy import explain
    return {'model':model,'parameters':p,'reference_parameters':ref,'current_parameters':current,
            'result':r,'reference':baseline,'target':target,'fraction':fraction,'period':period,
            'extent_y':[min(values)-span*.12,max(values)+span*.15],
            'explanation':explain(model,current,ref,r,baseline,expectation,period)}


def bridge(payload):
    if payload.get('accepted') is not True:
        raise ValueError('Confirmer les hypothèses de liaison WS–PS → Phillips.')
    p=validate('wsps',payload.get('parameters',{}))
    result=result_wsps(p)
    u=result['raw']['u']
    if not result['raw']['interior']:
        raise ValueError('La liaison exige un équilibre WS–PS intérieur.')
    if percent(u)>LIMITS['phillips']['ustar'][1]:
        raise ValueError('u* dépasse le domaine pédagogique de Phillips (30 %). Aucun écrêtage.')
    return {'ustar':percent(u),'source_parameters':p,
            'assumptions':'Même population active et mêmes institutions ; WS–PS sert de chômage de référence dans une Phillips augmentée des anticipations. Cette identification est une hypothèse, pas une identité générale entre chômage naturel, structurel et NAIRU.'}
