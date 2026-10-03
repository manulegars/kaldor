"""Contenus pédagogiques séparés des équations et des composants graphiques."""
from .economics import DEFAULTS, LIMITS
from .units import INDICATORS

CONTROLS = {
 'wsps': [
  ('z','Facteurs renforçant le salaire négocié',.01,'Déplace WS à chômage donné. Un facteur institutionnel ne décrit pas, à lui seul, tous les effets d’une politique.',False),
  ('mu','Marge sur coût · %',1,'μ est une marge sur coût, pas EBE/valeur ajoutée.',False),
  ('A','Productivité · indice',.01,'A = 1 dans la calibration initiale.',False),
  ('alpha','Sensibilité au chômage · α',.05,'Une pente plus forte modifie la relation salariale.',True),
  ('beta','Transmission de la productivité · β',.01,'0 : aucune transmission ; 1 : transmission complète.',True),
  ('observed','Chômage observé · % des actifs',.5,'Ce repère ne déplace ni WS, ni PS, ni E.',True)],
 'phillips': [
  ('u','Chômage observé · % des actifs',.1,'Déplace M le long de la relation, sans déplacer Phillips.',False),
  ('expected','Inflation anticipée initiale · %',.1,'Déplace toute la relation à chômage donné.',False),
  ('cost','Choc de coûts · points d’inflation',.1,'Un choc positif relève la courbe. Dans la trajectoire, le choc est maintenu à toutes les périodes.',False),
  ('ustar','Chômage de référence u* · %',.1,'Imposé ici ou importé de WS–PS sous des hypothèses explicites.',True),
  ('slope','Sensibilité à l’écart de chômage · α',.05,'Points d’inflation par point de chômage. Paramètre pédagogique, pas une estimation.',True),
  ('adaptation','Vitesse d’adaptation · λ',.05,'Poids de l’erreur passée, entre 0 et 1. Inactif avec anticipations fixes ; ce ne sont pas des anticipations rationnelles.',True)],
 'okun': [
  ('growth','Croissance du PIB réel · %',.1,'Une donnée sur une période, pas un niveau de production.',False),
  ('threshold','Croissance de référence · %',.1,'Croissance qui stabilise le chômage dans cette approximation.',False),
  ('reaction','Réaction du chômage · β',.05,'Points de chômage par point d’écart de croissance.',False),
  ('initial_u','Chômage en début de période · %',.1,'Permet de passer d’une variation à un niveau de chômage en fin de période.',True)],
}

WORKSHOPS = {
 'wsps': {
  'title':'WS–PS', 'subtitle':'La formation du chômage d’équilibre',
  'question':'D’où vient le chômage d’équilibre ?', 'dimensions':['unemployment'],
  'equations':['w_WS = A^β × (13/12 + z − αu)','w_PS = A / (1 + μ)','u* = [13/12 + z − A^(1−β)/(1+μ)] / α','Indice du salaire réel = 120 × w'],
  'assumptions':['Population active donnée ; salaires négociés et fixation des prix compatibles à l’intersection.', 'u et μ sont des proportions dans les équations ; les commandes les présentent en %.', 'E est un équilibre intérieur uniquement pour 0 < u* < 1. La partie négative de WS est une extrapolation algébrique.'],
  'authors':'Cadre de négociation salariale et de fixation des prix : Layard, Nickell et Jackman (1991). La calibration linéaire de cet atelier est illustrative.',
  'limits':'WS n’est pas une offre classique de travail, PS n’est pas une demande classique de travail. Le modèle ne calcule ni la demande globale, ni l’inflation chiffrée, ni la croissance, ni l’extérieur.',
  'exam':'L’intersection WS–PS détermine un salaire réel et un chômage compatibles avec les règles de formation des salaires et des prix retenues ; ce résultat reste conditionnel aux institutions, à la productivité et aux marges.',
  'sources':[{'label':'CORE — terminologie WS–PS','url':'https://www.core-econ.org/glossary/'}],
  'scenarios':[{'label':'Renforcement de la négociation','set':{'z':.15}}, {'label':'Hausse des marges','set':{'mu':40}}, {'label':'Productivité +10 %, β = 1','set':{'A':1.1}}, {'label':'Productivité +10 %, β = 0','start':{'beta':0},'set':{'A':1.1,'beta':0}}]},
 'phillips': {
  'title':'Phillips & anticipations', 'subtitle':'Inflation observée, anticipée et écart de chômage',
  'question':'Pourquoi l’arbitrage inflation–chômage se déplace-t-il ?', 'dimensions':['inflation','unemployment'],
  'equations':['π_t = πᵉ_t − α × (u_t − u*) + c_t','Fixes : πᵉ_(t+1) = πᵉ_0','Adaptatives : πᵉ_(t+1) = πᵉ_t + λ × (π_t − πᵉ_t)'],
  'assumptions':['Taux en pourcentage ; écarts de chômage et choc de coûts en points.', 'Dans la trajectoire, u, u*, α et c restent constants sur 12 périodes après la configuration t0. Une période n’est pas nécessairement une année.', 'M est la configuration observée, pas un équilibre obtenu par un modèle de demande. N indique π = πᵉ : avec un choc de coûts non nul, N est à u* + c/α.'],
  'authors':'Phillips (1958) étudie initialement les salaires nominaux. Friedman (1968) et Phelps (1967) mettent les anticipations au centre de l’analyse ; cette équation est une version augmentée en inflation des prix.',
  'limits':'Relation pédagogique linéaire, pas une estimation causale universelle. Anticipations adaptatives ne signifie pas rationnelles. L’identification du chômage de référence à celui de WS–PS est une hypothèse supplémentaire. Une désinflation est un ralentissement de l’inflation ; une déflation est une inflation négative.',
  'exam':'L’arbitrage de court terme dépend des anticipations et des chocs de coûts : leur variation déplace Phillips. À anticipations ajustées, maintenir un chômage inférieur à la référence peut alimenter une accélération de l’inflation dans cette spécification.',
  'sources':[{'label':'St. Louis Fed — anticipations et Phillips','url':'https://www.stlouisfed.org/publications/page-one-economics/2021/07/15/inflation-expectations-the-phillips-curve-and-the-feds-dual-mandate'}],
  'scenarios':[{'label':'Chômage inférieur à la référence','set':{'u':8}}, {'label':'Choc de coûts défavorable','set':{'cost':2}}, {'label':'Anticipations d’inflation plus élevées','set':{'expected':4}}]},
 'okun': {
  'title':'Loi d’Okun', 'subtitle':'De la croissance à la variation du chômage',
  'question':'Pourquoi une croissance positive ne suffit-elle pas toujours à réduire le chômage ?', 'dimensions':['growth','unemployment'],
  'equations':['Δu = −β × (g − g_seuil)','u_fin = u_début + Δu'],
  'assumptions':['g et g_seuil sont des taux de croissance réelle en %. Δu est une variation en points de pourcentage.', 'Le seuil résume notamment la productivité, la population active et les comportements d’emploi. Le coefficient et le seuil sont paramétrés.', 'Une seule période est calculée dans cet atelier. Modifier le chômage initial ne déplace pas la courbe Δu(g).'],
  'authors':'Arthur Okun (1962). Régularité empirique reliant activité et chômage, avec variantes en différences et en écarts de production ; cette application utilise la version en différences.',
  'limits':'Le coefficient varie selon les pays, les périodes, la rétention de main-d’œuvre et la participation. Ce n’est pas une identité comptable. Aucun salaire, taux d’inflation ou solde extérieur n’est calculé.',
  'exam':'Une croissance positive peut s’accompagner d’une hausse du chômage lorsqu’elle reste sous le seuil nécessaire à sa stabilisation. La loi d’Okun est une approximation empirique dont les paramètres ne sont pas universels.',
  'sources':[{'label':'St. Louis Fed — production et chômage','url':'https://www.stlouisfed.org/publications/regional-economist/october-2013/output-and-unemployment-how-do-they-relate-today'}],
  'scenarios':[{'label':'Croissance positive sous le seuil','set':{'growth':1}}, {'label':'Croissance au-dessus du seuil','set':{'growth':4}}, {'label':'Récession','set':{'growth':-2}}]},
}

RELATIONS = [
 {'id':'growth-unemployment','title':'Croissance ↔ chômage','models':['okun'], 'text':'Okun relie la croissance réelle à une variation du chômage, sous un seuil et un coefficient donnés. Une croissance positive peut être insuffisante pour stabiliser le chômage.'},
 {'id':'inflation-unemployment','title':'Inflation ↔ chômage','models':['phillips','wsps'], 'text':'Phillips relie inflation, anticipations et écart de chômage. WS–PS peut fournir une référence sous des hypothèses communes ; les notions de chômage d’équilibre ne sont pas automatiquement identiques.'},
 {'id':'growth-inflation','title':'Croissance ↔ inflation','models':['okun','phillips'], 'text':'Okun et Phillips éclairent deux relations différentes. Passer de g à Δu, puis à π, exige de préciser le chômage initial, la période, les anticipations et les chocs. Cette première livraison ne les assemble pas automatiquement en scénario intégré.'},
 {'id':'growth-external','title':'Croissance ↔ extérieur','models':[], 'text':'Une demande plus forte peut accroître les importations et réduire le solde commercial. Il faut une équation d’importations, d’exportations et un cadre de demande. Ce résultat n’est calculé ni par WS–PS, ni par Phillips, ni par Okun.'},
 {'id':'inflation-external','title':'Inflation ↔ extérieur','models':[], 'text':'Les prix relatifs, le change et les prix des importations peuvent relier inflation et échanges. Le signe dépend des élasticités et des délais. Le solde commercial (biens et services dans le futur module) ne sera pas assimilé au solde courant.'},
 {'id':'external-employment','title':'Extérieur ↔ emploi','models':[], 'text':'La demande adressée à la production nationale peut affecter l’emploi. Les effets nets dépendent des importations, de la productivité, du change et des réactions de demande. Il faut un modèle d’économie ouverte pour les calculer.'},
]

CODES = ['S1','S2','S3','S4','S5','C-NE','C-SW','C-NW','C-SE','D-1','D-2'] + [f'R{i}' for i in range(1,5)] + [f'I{i}' for i in range(1,6)] + [f'X{i}' for i in range(1,5)] + [f'B{i}' for i in range(1,6)]


def catalog():
    workshops = {}
    for key, text in WORKSHOPS.items():
        workshops[key] = {**text,'defaults':DEFAULTS[key], 'controls':[
            {'key':k,'label':label,'min':LIMITS[key][k][0],'max':LIMITS[key][k][1], 'step':step,'help':help_text,'advanced':advanced}
            for k,label,step,help_text,advanced in CONTROLS[key]]}
    return {'workshops':workshops,'indicators':INDICATORS,'relations':RELATIONS,'document_codes':CODES,
            'release':1,'mode':'Explorer un modèle'}


def number(value):
    return f'{value:.2f}'.replace('.', ',')


def explain(model,p,ref,r,base,expectation,period):
    changed=[k for k in p if abs(p[k]-ref[k])>1e-9]
    if model=='wsps':
        from .model import describe, Parameters
        from .units import proportion
        conversion=lambda q:Parameters(**{**q,'mu':proportion(q['mu']),'observed':proportion(q['observed'])})
        text=describe(conversion(p),conversion(ref))
        kind='Déplacement de courbe' if any(k!='observed' for k in changed) else 'Déplacement du repère observé' if changed else 'Configuration initiale'
        steps=['WS décrit le salaire négocié à chaque chômage ; PS le salaire compatible avec les prix.',
               'E est leur intersection. Le chômage observé peut être différent de u*.',
               'Une hausse de productivité avec β = 1 relève le salaire réel, sans changer u*.']
    elif model=='phillips':
        curve_changed=any(k in changed for k in ('expected','ustar','cost','slope')) or (expectation=='adaptive' and period>0 and p['adaptation']>0)
        kind='Déplacement de la courbe de Phillips' if curve_changed else 'Déplacement de M le long de Phillips' if 'u' in changed else 'Configuration sur Phillips'
        pi=r['raw']['pi'];gap=p['u']-p['ustar']
        text=f'Le chômage observé vaut {number(p["u"])} %, soit un écart de {number(gap)} points à u*. Avec les anticipations et les coûts retenus, π = {number(pi)} %. '
        text += 'Modifier u seul déplace M sur une relation inchangée ; modifier les anticipations, les coûts, u* ou la pente change la relation. '
        if expectation=='adaptive':text+=f'À t{period}, les anticipations valent {number(r["raw"]["expected"])} % après application de la règle adaptative. '
        else:text+='Les anticipations sont fixes : la vitesse λ n’a aucun effet. '
        text+='Le point N correspond à π = πᵉ ; avec c ≠ 0, il ne se situe pas à u*. Une inflation stable n’est pas nécessairement nulle.'
        steps=['L’écart u − u* donne une pression salariale et inflationniste conditionnelle.',
               'Le choc de coûts et les anticipations déplacent la relation à chômage donné.',
               'En trajectoire adaptative, l’erreur de prévision modifie les anticipations de la période suivante.']
    else:
        kind='Déplacement de la relation d’Okun' if any(k in changed for k in ('threshold','reaction')) else 'Déplacement de M le long d’Okun' if 'growth' in changed else 'Niveau initial modifié, relation inchangée' if 'initial_u' in changed else 'Configuration initiale'
        text=f'La croissance réelle ({number(p["growth"])} %) est comparée au seuil ({number(p["threshold"])} %). Δu = {number(r["raw"]["delta_u"])} points : '
        text+=('le chômage diminue.' if r['raw']['delta_u']<0 else 'le chômage augmente.' if r['raw']['delta_u']>0 else 'le chômage est stable.')
        text+=' Le taux de chômage final est obtenu en ajoutant cette variation au taux initial. Modifier la croissance déplace M sur la courbe ; modifier le seuil ou β change la courbe. L’inflation et l’extérieur ne sont pas calculés.'
        steps=['Calculer l’écart entre croissance réelle et croissance de référence.',
               'Multiplier cet écart par −β pour obtenir une variation en points de chômage.',
               'Ajouter Δu au chômage de départ, sans confondre taux, niveau et variation.']
    return {'kind':kind,'text':text,'steps':steps}
