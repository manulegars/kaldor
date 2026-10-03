# Laboratoire de macroéconomie — carré de Kaldor

Application web pédagogique en français. Elle garde le simulateur WS–PS d'origine
à `/ws-ps` et réunit l'accueil du carré de Kaldor, WS–PS, Phillips, Okun, la croix
keynésienne, IS–LM / IS–MP et offre–demande globales. Ces ateliers isolés calculent
uniquement les dimensions déterminées par leurs équations.

## Lancer et mettre à jour avec Docker

Le projet réutilise l'application Python sans dépendances externes et Docker
Compose. Le port hôte configurable est `8082`; il ne modifie pas les deux sites
de fichiers utilisant 8080 et 8081.

```bash
cd /home/manu/projets/admin/ws-ps
docker compose up -d --build --wait
```

Avec Docker exigeant des droits locaux : `sudo docker compose up -d --build --wait`.
Saisir le mot de passe sudo dans le terminal. La première image Python est
construite avec le code local ; après cela, toutes les vues et équations
fonctionnent sans réseau.

- Ce PC : http://localhost:8082
- Réseau maison : http://ADRESSE_IP_DE_CE_PC:8082
- Adresse Wi-Fi précédemment relevée : `192.168.1.106` ; la retrouver avec `ip -4 addr`.
- Santé : http://localhost:8082/health

L'application n'a pas d'authentification : le mode « Explorer un modèle » est
prévu pour le LAN maison. Ne pas rediriger le port 8082 sur Internet.

```bash
docker compose ps
docker compose logs --tail 100 -f
docker compose down
# Reconstruire après avoir modifié l'application :
docker compose up -d --build --wait
```

Les propriétés de sécurité du conteneur restent conservées : utilisateur non
privilégié, système de fichiers en lecture seule, capabilities supprimées et
contrôle de santé HTTP.

## Première livraison — ateliers disponibles

### Accueil Kaldor

Le schéma place croissance au nord, inflation à l'ouest, chômage au sud et
solde commercial à l'est. La dette reste un panneau séparé. Les six relations
sont cliquables ; chacune explique quel atelier les renseigne et ce qui reste
hors calcul. La carte des mécanismes distingue les relations explorables du
radar, qui compare situation initiale et scénario affiché.

Les quatre axes du radar ont des échelles fixes et documentées. Les valeurs
brutes et leurs unités restent visibles. Le radar ne produit aucun score
composite, aucun axe inconnu n'est interprété comme nul, et les dépassements
d'échelle sont signalés. Ses rayons sont une convention de lecture, pas une
mesure de bien-être ou une cible normative.

### WS–PS

Le moteur et le graphique historiques restent à `/ws-ps`. L'atelier commun
représente les mêmes paramètres sur des axes lisibles et garde ses équations,
sa calibration initiale (10 % de chômage, indice salarial 100) et ses contrôles
de domaine. Un bouton mène aussi au simulateur d'origine.

La liaison WS–PS → Phillips demande une case de confirmation. Elle transfère
le chômage d'équilibre du point affiché ; chômage naturel, structurel et NAIRU
ne sont pas présentés comme des synonymes.

### Phillips et anticipations

Équation de court terme : `πₜ = πᵉₜ − α(uₜ − u*) + cₜ`.
Anticipations fixes ou adaptatives :
`πᵉₜ₊₁ = πᵉₜ + λ(πₜ − πᵉₜ)`.
Le graphique distingue point M, courbe de Phillips et point N où `π = πᵉ`.
Le choc de coûts décale N de u* ; les bornes hors graphique sont annoncées.

L'option temporelle calcule t0 à t12 avec la récurrence d'anticipations.
Sur cette trajectoire illustrative, chômage et choc de coûts restent constants :
elle ne prétend pas représenter les années d'une économie réelle. Modifier une
configuration à l'écran demeure une comparaison interpolée, pas une trajectoire.
Une règle adaptative n'est pas une anticipation rationnelle.

### Loi d'Okun

Version en différences : `Δu = −β(g − g_seuil)` ;
`u_fin = u_début + Δu`. Les taux de croissance sont en %, et Δu en points.
La croissance d'équilibre de cette droite peut rester positive. Une valeur de
chômage finale hors de `[0 ; 100 %]` est signalée et n'est jamais écrêtée.

## Deuxième livraison — demande, politiques et offre

### Demande et multiplicateur

La croix keynésienne calcule `DA = A + bY` et `Y* = A / (1 − b)` avec
consommation induite, impôts proportionnels et importations. Les curseurs de
`G`, `c`, `t` et `m` distinguent déplacement parallèle de DA et modification de
sa pente ; les paramètres autonomes sont dans le volet avancé. L'animation
décompose une variation de G en 12 vagues géométriques : ce sont des tours de
dépense théoriques, pas des années. Elle montre aussi `ΔM = m ΔY` et la variation
du solde commercial à exportations inchangées. Prix fixes, capacités disponibles,
investissement exogène et absence de réaction monétaire sont des hypothèses ;
aucune inflation n'est calculée.

### Politiques économiques : IS–LM et IS–MP

Le sélecteur choisit un cadre distinct. IS–LM détermine le taux à partir du
marché monétaire et des encaisses réelles ; IS–MP utilise une règle de taux
réagissant éventuellement à l'écart de production. Le cadre MP ne fixe pas en
même temps une quantité de monnaie indépendante. Les deux variantes résolvent
l'intersection avec IS et affichent production, taux réel et effet du taux sur
l'investissement. Les taux sont affichés en pourcentage et utilisés en points
de pourcentage dans les coefficients calibrés. La règle MP est simplifiée,
pas une règle de Taylor complète.

### Offre et demande globales

DG et OG de court terme sont construites à partir de `x = ln(Y/Y_pot)` et
`p = ln(P/P_ref)`, donc le modèle conserve des valeurs positives de production
et de prix. Un choc positif de demande augmente production et prix ; un choc
défavorable de coûts augmente les prix et réduit la production. La variation de
l'indice des prix compare deux équilibres : faute de période, elle n'est jamais
présentée comme une inflation annuelle. Le modèle est statique et n'explique
pas la persistance d'une inflation.

Dans ces ateliers, une transition entre courbes est une interpolation visuelle
entre équilibres recalculés, pas une trajectoire sur plusieurs années. Les niveaux
de production ne sont pas convertis en croissance. Les dimensions du carré qui
ne sont pas déterminées apparaissent comme non calculées. Les passerelles vers
Okun, Phillips et WS–PS n'effectuent aucun transfert numérique incompatible.

### États, comparaison et exports

Chaque atelier conserve paramètres et référence dans le navigateur de l'onglet
ouvert. L'API Python reste sans état de visiteur. Les boutons **Comparer avant /
après**, **Avancer par étape**, **Lire / Pause**, et la vitesse permettent des
transitions où chaque résultat intermédiaire est calculé par Python. Ces
interpolations ne simulent pas le calendrier économique.

Les paramètres et leur référence s'enregistrent en JSON versionné et se
rechargent après validation complète par le moteur. Les graphiques et leurs
paramètres s'exportent en SVG local. Les essais au clavier et la préférence
système de réduction des animations sont pris en charge.

## Organisation du code

- `app/units.py` : indicateurs, unités et échelles du radar.
- `app/economics.py` : validation pure et calculs des six ateliers, trajectoires et liaison explicite WS–PS → Phillips.
- `app/pedagogy.py` : textes, auteurs, hypothèses, questions, scénarios et réglages.
- `app/server.py` : service HTTP local, API et fichiers statiques.
- `app/static/lab.html`, `lab.css`, `lab.js`, `plots.js` : interface commune, navigation et graphiques SVG.
- `app/model.py` : moteur WS–PS original, conservé.
- `tests/test_lab.py`, `tests/test_model.py` : tests des équations et comportements économiques.
- `tests/lab_browser_check.py` : parcours Firefox sur écran large/mobile, clavier, comparaison, trajectoire, import et export.

Toutes les requêtes de calcul contiennent les paramètres, leur référence, l'atelier
et l'état temporel. Une nouvelle requête annule la précédente et contrôle un
numéro de séquence avant d'afficher son résultat.

## Prochaines livraisons

Les ateliers des livraisons 1 et 2 restent indépendants ; aucun modèle intégré
ne simule une réponse automatique complète du carré de Kaldor.

1. Économie ouverte, délais d'ajustement, courbe en J et Mundell–Fleming.
2. Dette publique et ratio dette/PIB avec taux nominal, croissance nominale,
   solde primaire et sans ajustements stock-flux.
3. Scénarios intégrés documentés, trajectoires cohérentes et comparaison de politiques.

Chaque futur atelier renseignera seulement les indicateurs découlant de ses
équations. Un solde commercial ne sera pas assimilé au compte courant ; le niveau
des prix ne sera pas confondu avec l'inflation.

## Repères du document de synthèse

Les identifiants `S1–S5`, `C-NE`, `C-SW`, `C-NW`, `C-SE`, `D-1`, `D-2`,
`R1–R4`, `I1–I5`, `X1–X4` et `B1–B5` apparaissent comme codes à raccorder.
Le schéma et sa légende source ne sont pas disponibles ; aucune signification
n'est donc inventée. La disposition cardinale suit la consigne textuelle.

## Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/lab_browser_check.py
TEST_REDUCED_MOTION=1 python3 tests/lab_browser_check.py
```

Les tests Firefox utilisent un serveur local temporaire sur 18082 et
Marionette sur 2828. Captures de test dans `tests/artifacts/`.

## Références pédagogiques

- A. W. Phillips (1958), « The Relation between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861–1957 ».
- Edmund Phelps (1967), « Phillips Curves, Expectations of Inflation and Optimal Unemployment over Time ».
- Milton Friedman (1968), « The Role of Monetary Policy ».
- Arthur Okun (1962), « Potential GNP: Its Measurement and Significance ».
- John Maynard Keynes (1936), *The General Theory of Employment, Interest and Money*.
- Richard F. Kahn (1931), [« The Relation of Home Investment to Unemployment »](https://doi.org/10.2307/2223697).
- John R. Hicks (1937), [« Mr. Keynes and the “Classics” »](https://doi.org/10.2307/1907242).
- [CORE Econ — glossaire WS–PS](https://www.core-econ.org/glossary/).
- [Federal Reserve Bank of St. Louis — activité et loi d'Okun](https://www.stlouisfed.org/publications/regional-economist/october-2013/output-and-unemployment-how-do-they-relate-today).
- [Federal Reserve Bank of St. Louis — anticipations et courbe de Phillips](https://www.stlouisfed.org/publications/page-one-economics/2021/07/15/inflation-expectations-the-phillips-curve-and-the-feds-dual-mandate).

Les paramètres sont fictifs et illustratifs. Les exemples historiques ne sont
pas reproduits par le simulateur.
