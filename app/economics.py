"""Ateliers indépendants. Équations pures ; aucun état de session serveur."""
from math import exp, isfinite, log
from .model import Parameters, solve
from .units import percent, proportion, dashboard, indicator, radar

DEFAULTS = {
    'wsps': {'A': 1., 'mu': 20., 'z': 0., 'alpha': 2.5, 'beta': 1., 'observed': 10.},
    'phillips': {'expected': 2., 'ustar': 10., 'cost': 0., 'slope': .5, 'u': 10., 'adaptation': .5},
    'okun': {'growth': 2., 'threshold': 2., 'reaction': .4, 'initial_u': 10.},
    'multiplier': {'C0': 20., 'c': .8, 'T0': 0., 't': .2, 'I0': 20., 'G': 10., 'X0': 0., 'M0': 0., 'm': .1},
    'policy': {'G': 20., 'autonomous': 30., 'b': .6, 'a': 4., 'real_money': 20., 'k': .5, 'h': 20., 'expected_inflation': 2., 'r0': 2., 'phi': .5, 'potential': 100.},
    'ad_as': {'d': 0., 's': 0., 'alpha': 1., 'kappa': 1., 'expected_price': 0., 'potential': 100., 'reference_price': 100.},
}
LIMITS = {
    'wsps': {'A': (.2, 3), 'mu': (0, 150), 'z': (-1, 1), 'alpha': (.1, 6), 'beta': (0, 1), 'observed': (0, 100)},
    'phillips': {'expected': (-5, 15), 'ustar': (0, 30), 'cost': (-5, 10), 'slope': (.05, 2), 'u': (0, 30), 'adaptation': (0, 1)},
    'okun': {'growth': (-10, 12), 'threshold': (-2, 6), 'reaction': (.05, 1.5), 'initial_u': (0, 100)},
    'multiplier': {'C0': (0, 100), 'c': (0, .95), 'T0': (0, 100), 't': (0, .8), 'I0': (0, 100), 'G': (0, 100), 'X0': (0, 100), 'M0': (0, 100), 'm': (0, .8)},
    'policy': {'G': (0, 100), 'autonomous': (1, 200), 'b': (0, .9), 'a': (.1, 30), 'real_money': (0, 200), 'k': (.05, 2), 'h': (1, 100), 'expected_inflation': (-5, 15), 'r0': (-5, 15), 'phi': (0, 5), 'potential': (10, 300)},
    'ad_as': {'d': (-20, 20), 's': (-20, 20), 'alpha': (.1, 5), 'kappa': (.1, 5), 'expected_price': (-20, 20), 'potential': (30, 200), 'reference_price': (50, 150)},
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


def result_multiplier(p, period=0, baseline_G=None, **_):
    b=p['c']*(1-p['t'])-p['m']; denominator=1-b
    if denominator <= 0: raise ValueError('Le multiplicateur n’est pas défini : la propension totale b doit rester inférieure à 1.')
    autonomous=p['C0']-p['c']*p['T0']+p['I0']+p['G']+p['X0']-p['M0']
    ystar=autonomous/denominator
    if ystar <= 0: raise ValueError('La production d’équilibre doit être positive avec ces dépenses autonomes.')
    da=lambda y:autonomous+b*y
    # 0 <= b < 1 is required for the pedagogical sequence of spending rounds.
    rounds=[]; delta_g=p['G']-(DEFAULTS['multiplier']['G'] if baseline_G is None else baseline_G); cumulative=0.
    for t in range(1,13):
        amount=delta_g*(b**(t-1)); cumulative+=amount
        rounds.append({'round':t,'contribution':amount,'cumulative':cumulative})
    valid_rounds=0 <= b < 1
    initial=DEFAULTS['multiplier']['G']
    y0=(p['C0']-p['c']*p['T0']+p['I0']+initial+p['X0']-p['M0'])/denominator
    lo=0.; hi=max(ystar,y0,1)*1.25
    xs=[hi*i/80 for i in range(81)]
    curves=[curve('45° · DA = Y',[[x,x] for x in xs],1),curve('Dépense prévue · DA',[[x,da(x)] for x in xs],0)]
    metrics=[{'label':'Production finale / d’équilibre','value':ystar,'unit':'unités monétaires fictives'},
             {'label':'Variation de production vs G initial','value':ystar-y0,'unit':'unités monétaires fictives'},
             {'label':'Multiplicateur de G','value':1/denominator,'unit':'unités de Y par unité de G'},
             {'label':'Variation des importations','value':p['m']*(ystar-y0),'unit':'unités monétaires fictives'},
             {'label':'Variation du solde commercial','value':-p['m']*(ystar-y0),'unit':'unités monétaires fictives'},
             {'label':'Production initiale (référence)','value':y0,'unit':'unités monétaires fictives'}]
    warnings=[] if valid_rounds else ['La suite animée des vagues exige 0 ≤ b < 1. Les paramètres actuels sortent de ce domaine ; l’animation n’est pas applicable.']
    indicators=dashboard(growth=indicator(None,'non calculé','Un niveau de production ne donne pas un taux de croissance.'),external=indicator(None,'non calculé','Variation de solde commercial affichée séparément en unités monétaires.'))
    return {'curves':curves,'points':[{'name':'E','x':ystar,'y':ystar}], 'domain_x':[0,hi], 'x_label':'Production / revenu Y · unités monétaires fictives','y_label':'Dépense prévue DA · unités monétaires fictives',
            'metrics':metrics,'indicators':indicators,'warnings':warnings,'trajectory':rounds if valid_rounds else [],
            'wave': rounds[period-1] if valid_rounds and 1 <= period <= len(rounds) else None,
            'raw':{'autonomous':autonomous,'b':b,'multiplier':1/denominator,'Y':ystar,'Y_initial':y0,'delta_Y':ystar-y0,'delta_imports':p['m']*(ystar-y0),'delta_trade_balance':-p['m']*(ystar-y0),'wave_valid':valid_rounds}}


def result_policy(p, variant='lm', **_):
    A=p['autonomous']+p['G']; q=1-p['b']; a=p['a']
    isr=lambda y:(A-q*y)/a
    if variant=='lm':
        other=lambda y:(p['k']*y-p['real_money'])/p['h']-p['expected_inflation']
        denom=q/a+p['k']/p['h']; numerator=A/a+p['real_money']/p['h']+p['expected_inflation']
        label='LM'
    elif variant=='mp':
        other=lambda y:p['r0']+p['phi']*(y-p['potential'])/p['potential']
        denom=q/a+p['phi']/p['potential']; numerator=A/a-p['r0']+p['phi']
        label='MP'
    else: raise ValueError('Choisir la variante IS–LM ou IS–MP.')
    ystar=numerator/denom
    if denom<=0 or ystar<=0: raise ValueError('Pas d’équilibre positif avec ces paramètres ; ajustez la politique ou la demande autonome.')
    rate=isr(ystar); lo=max(0,min(ystar,p['potential'])*.45); hi=max(ystar,p['potential'])*1.55
    xs=[lo+(hi-lo)*i/80 for i in range(81)]
    curves=[curve('IS',[[y,isr(y)] for y in xs],0),curve(label,[[y,other(y)] for y in xs],1)]
    return {'curves':curves,'points':[{'name':'E','x':ystar,'y':rate}],'domain_x':[lo,hi], 'x_label':'Production Y · unités monétaires fictives','y_label':'Taux d’intérêt réel r · %',
            'metrics':[{'label':'Production d’équilibre','value':ystar,'unit':'unités monétaires fictives'}, {'label':'Taux réel d’équilibre','value':rate,'unit':'%'}, {'label':'Variation de l’investissement vs référence','value':-a*(rate-p['r0'] if variant=='mp' else rate-(p['k']*ystar-p['real_money'])/p['h']+p['expected_inflation']),'unit':'unités monétaires fictives'}],
            'indicators':dashboard(growth=indicator(None,'non calculé','Le niveau de Y ne détermine pas sa croissance.'),inflation=indicator(None,'non calculé','Le taux réel et le niveau des prix sont distincts.')),
            'warnings':[],'raw':{'Y':ystar,'r':rate,'variant':variant,'IS_residual':rate-isr(ystar),'other_residual':rate-other(ystar),'investment_change':-a*(rate-(p['r0'] if variant=='mp' else 0))}}


def result_ad_as(p, **_):
    alpha,kappa=p['alpha'],p['kappa']; de=p['d']; pe=p['expected_price']/100; s=p['s']/100
    x=(de/100-pe-s)/(alpha+kappa); logp=pe+s+kappa*x
    y=p['potential']*exp(x); price=p['reference_price']*exp(logp)
    lo=max(1,min(y,p['potential'])*.55); hi=max(y,p['potential'])*1.45
    ys=[lo+(hi-lo)*i/80 for i in range(81)]
    curves=[curve('DG',[[v,p['reference_price']*exp(de/100-alpha*log(v/p['potential']))] for v in ys],0),
            curve('OG court terme',[[v,p['reference_price']*exp(pe+s+kappa*log(v/p['potential']))] for v in ys],1),
            curve('Production potentielle',[[p['potential'],0],[p['potential'],p['reference_price']*2.5]],2)]
    ref_y=p['reference_price']
    delta_price=price-ref_y
    return {'curves':curves,'points':[{'name':'E','x':y,'y':price}],'domain_x':[lo,hi], 'x_label':'Production Y · unités fictives','y_label':f'Niveau des prix P · indice (P_ref = {p["reference_price"]:g})',
            'metrics':[{'label':'Production d’équilibre','value':y,'unit':'unités fictives'}, {'label':'Niveau des prix','value':price,'unit':'indice base '+str(p['reference_price'])}, {'label':'Écart de production','value':100*(y/p['potential']-1),'unit':'% du potentiel'}, {'label':'Variation du niveau des prix vs référence initiale','value':delta_price,'unit':'points d’indice · pas une inflation annuelle'}],
            'indicators':dashboard(growth=indicator(None,'non calculé','Aucune période de croissance définie.'),inflation=indicator(None,'non calculé','Un niveau de prix ne détermine pas une inflation annuelle.')),
            'warnings':[],'raw':{'x':x,'p':logp,'Y':y,'P':price,'output_gap':100*(y/p['potential']-1),'price_change':delta_price}}


SOLVERS = {'wsps': result_wsps, 'phillips': result_phillips, 'okun': result_okun,
           'multiplier':result_multiplier,'policy':result_policy,'ad_as':result_ad_as}


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
    variant=payload.get('variant','lm')
    period=payload.get('period',0)
    if axis not in ('unemployment','employment') or expectation not in ('fixed','adaptive'):
        raise ValueError('Convention inconnue.')
    if isinstance(period,bool) or not isinstance(period,int) or not 0 <= period <= 12:
        raise ValueError('Période invalide.')
    current={k: ref[k]+fraction*(p[k]-ref[k]) for k in p}
    # Keep exact endpoints and their economic interpretation.
    if fraction==1: current=p
    if fraction==0: current=ref
    options={'axis':axis,'expectation':expectation,'period':period,'variant':variant}
    if model=='multiplier': options['baseline_G']=ref['G']
    r=SOLVERS[model](current,**options)
    baseline=SOLVERS[model](ref,axis=axis,expectation=expectation,period=0,variant=variant)
    target=SOLVERS[model](p,**options)
    if model=='policy':
        baseline['metrics'][2]['value']=0.; baseline['raw']['investment_change']=0.
    if model=='multiplier':
        for index in (1,3,4): baseline['metrics'][index]['value']=0.
        baseline['metrics'][5]['value']=baseline['raw']['Y']
        baseline['raw'].update({'Y_initial':baseline['raw']['Y'],'delta_Y':0.,'delta_imports':0.,'delta_trade_balance':0.})
    if model=='ad_as':
        baseline['metrics'][3]['value']=0.; baseline['raw']['price_change']=0.
    for compared in (r,target):
        if model=='policy':
            compared['metrics'][2]['value']=-current['a']*(compared['raw']['r']-baseline['raw']['r'])
            compared['raw']['investment_change']=compared['metrics'][2]['value']
        if model=='multiplier':
            y0=baseline['raw']['Y']; dy=compared['raw']['Y']-y0
            imports_now=current['M0']+current['m']*compared['raw']['Y']; imports_before=ref['M0']+ref['m']*y0
            trade_now=current['X0']-imports_now; trade_before=ref['X0']-imports_before
            compared['metrics'][1]['value']=dy
            compared['metrics'][3]['value']=imports_now-imports_before
            compared['metrics'][4]['value']=trade_now-trade_before
            compared['metrics'][5]['value']=y0
            compared['raw'].update({'Y_initial':y0,'delta_Y':dy,'delta_imports':imports_now-imports_before,'delta_trade_balance':trade_now-trade_before})
            isolated_spending=(all(k=='G' or abs(p[k]-ref[k])<1e-10 for k in p)
                                and abs(compared['raw']['b']-ref['c']*(1-ref['t'])+ref['m'])<1e-10
                                and abs(p['G']-ref['G'])>1e-10)
            if not isolated_spending:
                compared['trajectory']=[]; compared['wave']=None; compared['raw']['wave_valid']=False
                warning='L’animation des vagues isole un choc de G : elle exige que G seul change depuis la référence et que 0 ≤ b < 1.'
                if warning not in compared['warnings']: compared['warnings'].append(warning)
        if model=='ad_as':
            compared['metrics'][3]['value']=compared['raw']['P']-baseline['raw']['P']
            compared['raw']['price_change']=compared['metrics'][3]['value']
    for row in (r,baseline,target): row['radar']=radar(row['indicators'])
    # Precompute a stable vertical extent for all comparison frames and trajectory periods.
    # WS–PS can have interior extrema when interpolating A and beta: sample the
    # full path plus a generous margin; client never rescales an individual frame.
    values=[0]; x_values=[]
    for j in range(101):
        between={k:ref[k]+j/100*(p[k]-ref[k]) for k in p}
        sample=SOLVERS[model](between,**options)
        x_values.extend(sample['domain_x'])
        for c in sample['curves']: values.extend(y for _,y in c['points'] if isfinite(y))
    if model=='phillips':
        for pp in (p,ref):
            for t in range(13):
                sample=SOLVERS[model](pp,axis=axis,expectation=expectation,period=t)
                for c in sample['curves']: values.extend(y for _,y in c['points'])
    span=max(max(values)-min(values),1)
    from .pedagogy import explain
    stable_x=[min(x_values),max(x_values)]
    for row in (r,baseline,target): row['domain_x']=stable_x
    return {'model':model,'parameters':p,'reference_parameters':ref,'current_parameters':current,'variant':variant,
            'result':r,'reference':baseline,'target':target,'fraction':fraction,'period':period,
            'extent_y':[min(values)-span*.12,max(values)+span*.15],'extent_x':stable_x,
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
