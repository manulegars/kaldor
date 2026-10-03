# Vérification du laboratoire WS–PS et Kaldor

## Résultats réussis

- 20 tests Python : calibration WS–PS originale, équilibre et repères ; sens des
  chocs ; invariance de u* pour β = 1 ; unités d'Okun ; écarts inflation/chômage ;
  calcul des anticipations adaptatives sur 13 périodes ; domaine et valeurs
  manquantes ; normalisation et débordement du radar ; transfert WS–PS → Phillips
  soumis à confirmation ; entrées invalides ; indépendance entre visiteurs.
- Parcours Firefox du laboratoire : carte et six relations, WS–PS puis Phillips
  puis Okun, confirmation de u*, déplacements sur/d'une courbe, 20 saisies rapides,
  lecture t0–t12, pas par pas, comparaison avant/après, graphes à échelles fixes,
  clavier, fenêtre de 390 px, autre onglet indépendant.
- Téléchargement/réimport JSON et export SVG exécutés dans Firefox ; courbes et
  métadonnées présents. Toutes les ressources web sont chargées localement.
- Parcours de la page historique WS–PS : testé dans Firefox après intégration.
- Parcours répété avec la préférence système « réduire les animations » activée.
- `docker compose config --quiet`, compilation Python et `git diff --check` valides.

## Déploiement constaté

Le port 8082 écoute sur `0.0.0.0` et `/health` répond HTTP 200. La page servie
par le conteneur reste cependant l'ancienne application WS–PS : `/` porte encore
le titre « Atelier WS–PS », tandis que `/api/catalog` et `/lab.js` répondent 404.

La mise à jour de l'image avec `docker compose up -d --build --wait` n'a pas pu
être faite depuis cette session : les opérations sur le socket Docker et la
reconstruction requièrent une authentification sudo interactive. Les essais sudo
sans authentification répondent « interactive authentication is required ».

Pour publier les fichiers validés :

```bash
cd /home/manu/projets/admin/ws-ps
sudo docker compose up -d --build --wait
sudo docker compose ps
curl http://localhost:8082/api/catalog
```

Après cela, ouvrir `http://192.168.1.106:8082` depuis le LAN (vérifier l'adresse
actuelle par `ip -4 addr`). Puis refaire `/health`; `/api/catalog` doit renvoyer
le catalogue, et `/` doit titrer « Autour du carré de Kaldor ».
