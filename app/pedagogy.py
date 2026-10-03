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
 'multiplier': [
  ('G','Dépense publique G · unités monétaires',1,'Une hausse décale la droite de dépense prévue vers le haut, à pente constante.',False),
  ('c','Propension à consommer c',.01,'Part du revenu disponible supplémentaire consommée ; agit sur la pente de DA.',False),
  ('t','Taux proportionnel t',.01,'Part d’un revenu supplémentaire prélevée ; réduit le revenu disponible et la pente.',False),
  ('m','Propension à importer m',.01,'Part du revenu supplémentaire consacrée aux importations ; réduit le multiplicateur.',False),
  ('C0','Consommation autonome C₀',1,'Consommation indépendante du revenu courant.',True),('T0','Impôts autonomes T₀',1,'Prélèvements forfaitaires, indépendants du revenu.',True),
  ('I0','Investissement exogène I₀',1,'Investissement fixé dans cet atelier.',True),('X0','Exportations X₀',1,'Exportations autonomes maintenues constantes.',True),('M0','Importations autonomes M₀',1,'Importations indépendantes du revenu.',True)],
 'policy': [
  ('G','Dépenses publiques G · unités monétaires',1,'Déplace IS vers la droite à demande autonome plus élevée.',False),
  ('real_money','Encaisses réelles M/P · unités',1,'Dans IS–LM, une hausse déplace LM vers le bas. Prix P maintenu fixe.',False),
  ('a','Sensibilité au taux · a',.1,'Une hausse de a rend IS plus plate et l’investissement plus sensible au taux.',False),
  ('b','Propension marginale b',.01,'Part de la production réinjectée dans la demande ; 0 ≤ b < 1.',False),
  ('r0','Taux réel de base r₀ · %',.1,'Dans IS–MP, fixe le taux lorsque Y = Y potentiel.',False),
  ('phi','Réaction du taux φ',.05,'Dans IS–MP, le taux réagit à l’écart de production ; φ = 0 maintient le taux constant.',False),
  ('autonomous','Demande autonome hors G',1,'Consommation, investissement et autres composantes autonomes agrégées.',True),
  ('k','Sensibilité de la demande de monnaie k',.01,'Encaisses demandées par unité de Y dans LM.',True),('h','Sensibilité de la demande de monnaie au taux h',1,'Encaisses demandées en moins quand le taux augmente.',True),
  ('expected_inflation','Inflation anticipée πᵉ · %',.1,'La relation i = r + πᵉ convertit le taux nominal en taux réel.',True),('potential','Production potentielle Y_pot',1,'Repère l’écart de production dans la règle MP.',True)],
 'ad_as': [
  ('d','Impulsion de demande d · points logarithmiques × 100',.5,'Une hausse déplace DG vers le haut ; la production et le niveau des prix augmentent.',False),
  ('s','Choc de coûts s · points logarithmiques × 100',.5,'Un choc positif déplace OG vers le haut ; les prix montent et la production baisse.',False),
  ('kappa','Pente de l’offre κ',.05,'Une offre plus raide amplifie la réaction du niveau des prix.',False),
  ('expected_price','Niveau des prix anticipé · écart logarithmique × 100',.5,'Déplace OG ; il s’agit d’un niveau relatif, pas d’un taux d’inflation.',False),
  ('alpha','Pente de la demande α',.05,'Détermine la baisse des prix quand la production dépasse le potentiel.',True),
  ('potential','Production potentielle Y_pot',1,'Le modèle exprime la demande relativement au potentiel : son changement n’est pas un pur choc d’offre à demande en niveau inchangée.',True),
  ('reference_price','Indice de référence P_ref',1,'Base d’indice pour présenter le niveau des prix.',True)],
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
 'multiplier': {
  'title':'Demande et multiplicateur','subtitle':'La croix keynésienne à prix fixes','question':'Pourquoi une hausse de la dépense publique peut-elle augmenter la production de plus que son montant initial ?','dimensions':['growth','external'],
  'equations':['C = C₀ + c(Y − T) ; T = T₀ + tY ; M = M₀ + mY','DA = A + bY ; b = c(1 − t) − m','Y* = A / (1 − b) ; k_G = 1 / (1 − b)','Vagues : ΔY₁ = ΔG ; ΔYₙ = bⁿ⁻¹ΔG'],
  'assumptions':['Prix fixes, capacités disponibles, investissement et exportations exogènes ; une même unité monétaire fictive pour tous les montants.','La dépense G déplace DA parallèlement ; c, t et m changent sa pente. Les vagues sont des tours de dépense théoriques, pas des années.','Les vagues affichées exigent 0 ≤ b < 1 ; les équilibres hors de ce domaine ne sont pas ramenés artificiellement.'],
  'authors':'Keynes (1936) formalise la demande effective ; Kahn (1931) expose le multiplicateur d’emploi, puis le multiplicateur de dépense est développé dans la tradition keynésienne.',
  'limits':'Prix fixes ; capacités disponibles ; investissement exogène ; aucune réaction monétaire. Le modèle ne calcule pas directement l’inflation. La variation des importations et du solde commercial suppose X inchangées ; ce n’est pas le compte courant.',
  'exam':'Dans une économie à prix fixes et capacités disponibles, une dépense autonome supplémentaire engendre des revenus qui alimentent à leur tour la consommation. L’épargne, les prélèvements proportionnels et les importations constituent des fuites qui réduisent le multiplicateur.',
  'sources':[{'label':'Kahn, The Relation of Home Investment to Unemployment (1931)','url':'https://doi.org/10.2307/2223697'}],
  'scenarios':[{'label':'Hausse de G · économie fermée','set':{'G':15,'m':0}}, {'label':'Même hausse · économie ouverte','set':{'G':15,'m':.2}}, {'label':'Forte épargne · c faible','set':{'c':.55}}, {'label':'Prélèvements proportionnels','set':{'t':.45}}]},
 'policy': {
  'title':'Politiques économiques','subtitle':'Demande, taux réel et équilibre de court terme','question':'Comment une relance budgétaire et une modification des conditions monétaires changent-elles la production ?','dimensions':['growth'],
  'equations':['IS : Y = A + bY − ar ; r_IS(Y) = [A − (1 − b)Y] / a','LM : M/P = kY − hi ; i = r + πᵉ','IS–MP : r_MP(Y) = r₀ + φ × (Y − Y_pot) / Y_pot'],
  'assumptions':['Montants en unités fictives ; taux affichés en % et utilisés en points de pourcentage dans les équations ; a et h sont calibrés dans ces unités.','IS–LM : P et πᵉ fixes, encaisses réelles M/P données. IS–MP : règle de taux simplifiée, distincte d’une quantité de monnaie indépendante.','L’investissement sensible au taux est agrégé dans a. IS–MP n’est pas une règle de Taylor complète.'],
  'authors':'Hicks (1937) propose une représentation IS–LM de l’analyse keynésienne. IS–MP conserve IS mais représente directement une règle de taux de la banque centrale, au lieu d’un équilibre du marché monétaire.',
  'limits':'Économie fermée, prix rigides et équilibres de court terme. Ce noyau ne calcule ni inflation, ni chômage, ni commerce extérieur, ni dette. Il ne s’agit pas d’un modèle intégré de Kaldor.',
  'exam':'À court terme, une relance budgétaire déplace IS vers la droite. En IS–LM, la hausse de Y peut relever le taux d’intérêt et évincer une partie de l’investissement ; en IS–MP, l’ampleur de cet effet dépend de la réaction de taux retenue.',
  'sources':[{'label':'Hicks (1937), Mr. Keynes and the Classics','url':'https://doi.org/10.2307/1882796'}],
  'scenarios':[{'label':'Relance budgétaire avec réaction du taux','variant':'mp','set':{'G':30,'phi':.8}}, {'label':'Relance avec taux maintenu constant','variant':'mp','set':{'G':30,'phi':0}}, {'label':'Assouplissement monétaire · variante LM','variant':'lm','set':{'real_money':35}}, {'label':'Relance et durcissement monétaire','variant':'lm','set':{'G':30,'real_money':10}}]},
 'ad_as': {
  'title':'Offre et demande globales','subtitle':'Production et niveau des prix à court terme','question':'Pourquoi une hausse de la demande et une hausse des coûts peuvent-elles toutes deux augmenter les prix, avec des effets opposés sur la production ?','dimensions':['growth','inflation'],
  'equations':['x = ln(Y / Y_pot) ; p = ln(P / P_ref)','DG : p = d − αx','OG court terme : p = pᵉ + s + κx','x* = (d − pᵉ − s)/(α + κ) ; Y* = Y_pot exp(x*)'],
  'assumptions':['d, s et pᵉ sont saisis en points logarithmiques × 100 puis convertis en logarithmes ; P est présenté comme un indice base P_ref.','Y_pot > 0 ; α > 0 et κ > 0. La demande est écrite relativement au potentiel ; modifier Y_pot n’est donc pas un pur choc d’offre à demande en niveau inchangée.','La variation de P entre deux équilibres n’est pas une inflation annuelle : aucune période n’est définie.'],
  'authors':'Synthèse pédagogique de la demande globale et de l’offre globale de court terme, dans la tradition keynésienne puis néo-keynésienne.',
  'limits':'Le modèle statique calcule un niveau de production et de prix, pas une trajectoire d’ajustement des anticipations. Un choc de coûts défavorable peut produire stagflation ; une inflation persistante requiert une analyse dynamique complémentaire.',
  'exam':'Un choc positif de demande relève simultanément production et prix à court terme. Un choc défavorable de coûts relève le niveau des prix mais réduit la production, combinaison compatible avec une stagflation sans suffire à expliquer la persistance de l’inflation.',
  'sources':[],
  'scenarios':[{'label':'Choc positif de demande','set':{'d':8}}, {'label':'Choc négatif de demande','set':{'d':-8}}, {'label':'Choc de coûts défavorable','set':{'s':8}}, {'label':'Choc de coûts favorable','set':{'s':-8}}]},
}

RELATIONS = [
 {'id':'growth-unemployment','title':'Croissance ↔ chômage','models':['okun','multiplier'], 'text':'Okun relie la croissance réelle à une variation du chômage, sous un seuil et un coefficient donnés. Une croissance positive peut être insuffisante pour stabiliser le chômage. Le multiplicateur calcule un niveau de production ; il ne donne pas directement la croissance ou le chômage.'},
 {'id':'inflation-unemployment','title':'Inflation ↔ chômage','models':['phillips','wsps'], 'text':'Phillips relie inflation, anticipations et écart de chômage. WS–PS peut fournir une référence sous des hypothèses communes ; les notions de chômage d’équilibre ne sont pas automatiquement identiques.'},
 {'id':'growth-inflation','title':'Croissance ↔ inflation','models':['okun','phillips','ad_as'], 'text':'Okun, Phillips et OG–DG éclairent des relations différentes. Passer d’un niveau de production à la croissance, puis au chômage et à l’inflation, exige des périodes et des équations compatibles. Aucun transfert chiffré automatique n’est proposé.'},
 {'id':'growth-external','title':'Croissance ↔ extérieur','models':['multiplier'], 'text':'Dans la croix keynésienne, une hausse de production accroît les importations selon m et peut dégrader le solde commercial si les exportations restent fixes. Cela ne détermine ni le compte courant, ni la croissance annuelle.'},
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
            'release':2,'mode':'Explorer un modèle'}


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
    elif model=='okun':
        kind='Déplacement de la relation d’Okun' if any(k in changed for k in ('threshold','reaction')) else 'Déplacement de M le long d’Okun' if 'growth' in changed else 'Niveau initial modifié, relation inchangée' if 'initial_u' in changed else 'Configuration initiale'
        text=f'La croissance réelle ({number(p["growth"])} %) est comparée au seuil ({number(p["threshold"])} %). Δu = {number(r["raw"]["delta_u"])} points : '
        text+=('le chômage diminue.' if r['raw']['delta_u']<0 else 'le chômage augmente.' if r['raw']['delta_u']>0 else 'le chômage est stable.')
        text+=' Le taux de chômage final est obtenu en ajoutant cette variation au taux initial. Modifier la croissance déplace M sur la courbe ; modifier le seuil ou β change la courbe. L’inflation et l’extérieur ne sont pas calculés.'
        steps=['Calculer l’écart entre croissance réelle et croissance de référence.',
               'Multiplier cet écart par −β pour obtenir une variation en points de chômage.',
               'Ajouter Δu au chômage de départ, sans confondre taux, niveau et variation.']
    elif model=='multiplier':
        changed_keys=set(changed); dy=r['raw']['delta_Y']; dp=r['raw']['delta_imports']
        direction='augmente' if dy>1e-9 else 'diminue' if dy < -1e-9 else 'ne change pas'
        if not changed_keys:
            kind='Configuration de référence'; reason='Aucun paramètre ne diffère de la référence.'
        elif 'G' in changed_keys and all(k=='G' for k in changed_keys):
            kind='Déplacement parallèle de DA'; reason=('La hausse' if p['G']>ref['G'] else 'La baisse')+' de G déplace DA à chaque niveau de revenu ; sa pente reste constante.'
        elif changed_keys & {'c','t','m'}:
            kind='Modification de la pente de DA'; reason='La consommation, les prélèvements et les importations modifient la part du revenu réinjectée dans la demande, donc la pente de DA.'
        else: kind='Modification de la demande autonome'; reason='Une composante autonome modifie l’ordonnée à l’origine de DA.'
        text=f'{reason} La production d’équilibre {direction} et vaut {number(r["raw"]["Y"])}. La production initiale de référence était {number(r["raw"]["Y_initial"])} ; la variation est {number(dy)} unités monétaires. Les importations varient de {number(dp)} et le solde commercial de {number(r["raw"]["delta_trade_balance"])} unités (ΔX₀ − ΔM).'
        if 'G' in changed_keys and len(changed_keys)>1: text+=' G décale aussi la droite de façon parallèle.'
        if period and r.get('wave'): text+=f' Au tour {period}, la contribution théorique est {number(r["wave"]["contribution"])} ; le cumul atteint {number(r["wave"]["cumulative"])}.'
        text+=' Ces tours ne représentent pas des années. Les prix sont supposés fixes et le modèle ne calcule pas l’inflation.'
        steps=['G agit sur la dépense autonome ; c, t et m déterminent la pente b.', 'L’intersection DA = Y donne la production d’équilibre.', 'Les revenus induits alimentent une nouvelle dépense ; les fuites réduisent chaque vague successive.']
    elif model=='policy':
        kind=('Déplacement de IS et équilibre ' if 'G' in changed else 'Nouvel équilibre ') + ('IS–LM' if r['raw']['variant']=='lm' else 'IS–MP')
        delta=r['raw']['Y']-base['raw']['Y']; dr=r['raw']['r']-base['raw']['r']
        text=f"La variante IS–{'LM' if r['raw']['variant']=='lm' else 'MP'} donne Y = {number(r['raw']['Y'])} et r = {number(r['raw']['r'])} %. Par rapport à la référence, la production varie de {number(delta)} et le taux de {number(dr)} point. La variation de l’investissement sensible au taux est {number(r['raw']['investment_change'])} unités. "
        if 'G' in changed: text+=('La hausse' if p['G']>ref['G'] else 'La baisse')+' de G déplace IS vers '+('la droite. ' if p['G']>ref['G'] else 'la gauche. ')
        if r['raw']['variant']=='lm' and 'real_money' in changed: text+=('La hausse' if p['real_money']>ref['real_money'] else 'La baisse')+' des encaisses réelles déplace LM vers '+('le bas. ' if p['real_money']>ref['real_money'] else 'le haut. ')
        if r['raw']['variant']=='mp': text+=('φ = 0 maintient le taux réel constant. ' if p['phi']==0 else f'La règle MP réagit à l’activité avec φ = {number(p["phi"])}. ')
        if 'a' in changed: text+='La sensibilité a modifie l’inclinaison de IS. '
        if 'b' in changed: text+='La propension b modifie la pente de IS. '
        if r['raw']['variant']=='lm' and set(changed)&{'k','h','expected_inflation'}: text+='k, h ou l’inflation anticipée modifient la position ou la pente de LM, à P fixe. '
        if r['raw']['variant']=='mp' and set(changed)&{'r0','potential'}: text+='r₀ ou Y_pot modifie la règle MP. '
        text+='En LM, les encaisses réelles fixent la relation de marché monétaire ; en MP, une règle de taux représente la politique monétaire. Une hausse du taux freine l’investissement dans ce noyau. Le reste du carré n’est pas déterminé.'
        steps=['IS équilibre la demande de biens et dépend de G et du taux réel.', 'LM équilibre la demande et l’offre d’encaisses réelles ; MP représente une règle de taux distincte.', 'Le point E est recalculé à l’intersection des deux relations, sans trajectoire pluriannuelle.']
    else:
        kind='Déplacement de DG' if 'd' in changed else 'Déplacement de OG' if set(changed) & {'s','expected_price'} else 'Équilibre offre–demande globales'
        # Keep the explanation tied to both calculated equilibrium values.
        dx=r['raw']['Y']-base['raw']['Y']; dprice=r['raw']['P']-base['raw']['P']
        effects=[]
        if 'd' in changed: effects.append(('La hausse' if p['d']>ref['d'] else 'La baisse')+' de la demande globale déplace DG ; production et niveau des prix évoluent dans le même sens ici.')
        if 's' in changed: effects.append(('Le choc de coûts défavorable relève' if p['s']>ref['s'] else 'Le choc de coûts favorable abaisse')+' OG ; les prix '+('montent' if p['s']>ref['s'] else 'baissent')+' tandis que la production '+('baisse' if p['s']>ref['s'] else 'augmente')+'.')
        if 'expected_price' in changed: effects.append('Le niveau des prix anticipé déplace OG à court terme.')
        if not effects: effects.append('La pente ou le potentiel modifié change la position de l’équilibre selon les équations affichées.')
        text=' '.join(effects)
        text+=f' Depuis la référence, ΔY = {number(dx)} et ΔP = {number(dprice)} points d’indice. Cette variation entre équilibres n’est pas une inflation annuelle. Un choc défavorable de coûts peut produire une configuration de stagflation ; sa persistance n’est pas calculée.'
        steps=['DG relie le niveau des prix à la production relative au potentiel.', 'OG de court terme intègre anticipations, coûts et pente κ.', 'L’intersection détermine Y et P ; aucune période ni dynamique d’anticipations n’est ajoutée.']
    return {'kind':kind,'text':text,'steps':steps}
