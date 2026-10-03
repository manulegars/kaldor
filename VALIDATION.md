# Vérification du laboratoire WS–PS et Kaldor

## Résultats réussis

- 23 tests Python : calibration WS–PS originale, équilibre et repères ; sens des
  chocs ; invariance de u* pour β = 1 ; unités d'Okun ; écarts inflation/chômage ;
  calcul des anticipations adaptatives sur 13 périodes ; domaine et valeurs
  manquantes ; normalisation et débordement du radar ; transfert WS–PS → Phillips
  soumis à confirmation ; croix keynésienne et multiplicateur ; équilibres IS–LM
  et IS–MP ; sens des chocs monétaires et OG–DG ; entrées invalides ; indépendance.
- Parcours Firefox du laboratoire : carte et six relations, WS–PS puis Phillips
  puis Okun, confirmation de u*, déplacements sur/d'une courbe, 20 saisies rapides,
  lecture t0–t12, pas par pas, comparaison avant/après, graphes à échelles fixes,
  clavier, fenêtre de 390 px, autre onglet indépendant.
- Téléchargement/réimport JSON et export SVG exécutés dans Firefox ; courbes et
  métadonnées présents. Toutes les ressources web sont chargées localement.
- Parcours de la page historique WS–PS : testé dans Firefox après intégration.
- Parcours répété avec la préférence système « réduire les animations » activée.
- Deuxième livraison vérifiée dans Firefox : multiplicateur de G et vagues,
  changement de variante IS–LM / IS–MP, choc de coûts OG–DG, unités et explications.
- `docker compose config --quiet`, compilation Python et `git diff --check` valides.

## Déploiement

`docker compose config --quiet` valide le fichier Compose. Le démarrage ou la
reconstruction de l'image n'a pas pu être vérifié dans cette session : l'accès au
socket `/var/run/docker.sock` a répondu « permission denied », y compris lors de
la commande documentée `docker compose up -d --build --wait`. Le conteneur live
n'a donc pas été modifié et son état courant n'a pas pu être inspecté.

Pour reconstruire et démarrer avec les droits Docker de la machine :

```bash
cd /home/manu/projets/admin/ws-ps
sudo docker compose up -d --build --wait
sudo docker compose ps
curl http://localhost:8082/api/catalog
```

Après cela, ouvrir `http://192.168.1.106:8082` depuis le LAN (vérifier l'adresse
actuelle par `ip -4 addr`). Puis refaire `/health`; `/api/catalog` doit renvoyer
le catalogue, et `/` doit titrer « Autour du carré de Kaldor ».
