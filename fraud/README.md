# Partie H — Data Science : détection de fraude bancaire

**Périmètre demandé :** classification binaire Python, analyse des valeurs manquantes et du déséquilibre, séparation stratifiée, pipeline d'imputation/encodage/standardisation, modèle simple, métriques et interprétation. Le déploiement du modèle **n'est pas demandé**.

## Résultats reproductibles sur le CSV remis

| Mesure | Résultat |
|---|---:|
| Lignes | 5 000 |
| Fraudes | 257 (5,14 %) |
| Train stratifié / test gelé | 3 750 / 1 250 |
| Comparaison des modèles | CV stratifiée 3 plis **sur le train** |
| Modèle choisi | Régression logistique pondérée |
| Average Precision sur le test | 0,1885 |
| Précision fraude, seuil 0,50 | 10,36 % |
| Rappel fraude, seuil 0,50 | 54,69 % |
| F1 fraude, seuil 0,50 | 0,1741 |
| Matrice test (VN, FP / FN, VP) | (883, 303 / 29, 35) |
| Tests unitaires Python | 6/6 réussis |

## Démarrer

Depuis le dossier `fraud/` :

```bash
python -m pip install -r requirements.txt
python train.py --csv data/bank_transactions.csv --out results
python -m pytest -q test_train.py
jupyter notebook Analyse_Fraude_ADRIA.ipynb
```

Le notebook Jupyter contient déjà les résultats de l'exécution réalisée sur le fichier fourni. Les graphiques et métriques ont été produits par le script, non dessinés manuellement. Le CSV est présent dans le ZIP mais exclu des commits Git par `.gitignore` : vérifier ses droits de partage avant de rendre le dépôt public.

## Preuves et résultats

- `results/metrics.json` : scores des trois méthodes (baseline, seuil 0,50, seuil optimisé **sur apprentissage**), AP, matrices de confusion, méthode de sélection.
- `results/comparaison_modeles_cv.csv` : résultats CV logistique / arbre / forêt (moyennes et écarts-types AP).
- `results/repartition_fraudes.png` et `results/valeurs_manquantes.png` : exploration sur le CSV.
- `results/confusion_matrix.png`, `results/precision_recall.png` : **jeu de test indépendant**.
- `results/analyse_seuil_sur_train.png` : exploration du seuil sur l'entraînement uniquement.
- `results/importance_variables.png` : permutation des variables sur le train, non interprétable causalement.
- `results/predictions_test.csv` : prédictions pour audit local, ignorées par Git.
- `results/fraud_pipeline.joblib` : pipeline sauvegardé, ignoré par Git ; ne jamais charger une sérialisation inconnue.

## À défendre au jury

1. **Baseline trompeuse :** prédire toujours « non-fraude » donne 94,88 % d'accuracy sur le test, mais aucun fraudeur n'est détecté.
2. **Choix du modèle :** 3 algorithmes testés en CV sur train, sélection par l'Average Precision (adaptée au déséquilibre).
3. **Aucune fuite :** imputation, OneHot et standardisation dans un `Pipeline`; ID exclus; seuil de 0,80 sélectionné avec probabilités hors-pli du train. Le test n'a servi qu'à l'évaluation finale.
4. **Compromis opérationnel :** seuil 0,50 = 35 fraudes détectées / 303 fausses alertes ; seuil 0,80 = 13 fraudes détectées / 43 fausses alertes. Coût d'une fraude non détectée versus coût d'une alerte injustifiée.
5. **Honnêteté méthodologique :** les métriques restent modestes (AP test 0,1885). Aucune date chronologique dans le CSV ; `hour` n'est **pas** un timestamp pour effectuer une validation temporelle. Les comptes peuvent se répéter entre les jeux. Pas de validation de la dérive ou de calibration en production.

## Mini-script de présentation (environ 2 minutes, à personnaliser)

« Pour la partie H, j'ai choisi de suivre une démarche Data Science reproductible. Le fichier contient 5 000 transactions, dont seulement 257 fraudes, soit 5,14 %. J'ai commencé par auditer les valeurs manquantes et à exclure les identifiants des variables explicatives. Puis j'ai isolé 25 % des données dans un test stratifié qui n'a servi ni à choisir le modèle ni à ajuster le seuil.

Sur le train, j'ai utilisé un pipeline scikit-learn pour l'imputation, le One-Hot Encoding et la standardisation, puis comparé trois modèles en validation croisée. La régression logistique pondérée obtient le meilleur Average Precision moyen sur les trois plis et a été retenue. Sur le test, l'Average Precision est 0,1885. Au seuil 0,50, 35 des 64 fraudes sont identifiées, mais 303 transactions légitimes déclenchent une fausse alerte. Un autre seuil étudié sur le train réduit ces fausses alertes, mais manque davantage de fraudes.

Cette expérience démontre l'importance de la précision, du rappel et du compromis métier, au-delà de l'accuracy. En amélioration, je demanderais des données horodatées pour une vraie validation temporelle, un historique plus riche, des coûts métier et une surveillance de la dérive. Le modèle reste volontairement hors des microservices, conformément à la consigne. »
