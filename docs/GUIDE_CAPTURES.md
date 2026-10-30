# Guide captures - ADRIA / ENSET

**Ne pas présenter une maquette comme une exécution réelle.** Capturer les fenêtres du projet sur votre poste après démarrage effectif. Les références S01...S16 sont les mêmes que dans README et PDF.

## Préparation

1. Installer Java 21, Maven, Docker Desktop, Node et Python.
2. Créer `.env` avec des secrets personnels. En local, utiliser des comptes Keycloak de démonstration uniquement.
3. Exécuter `docker compose up -d --build` depuis la racine.
4. Suivre `docker compose ps` et `docker compose logs -f <service>` pour les problèmes de démarrage.
5. Sur Windows, `Win + Shift + S` puis enregistrer en `docs/captures/S01_...png`. Sur macOS `Cmd + Shift + 4`.

## Captures à prendre

- `S01_modules.png` : arborescence IntelliJ / VS Code, visible avec les 7 modules.
- `S02_tests_maven.png` : résultat réel de `mvn -B clean verify`.
- `S03_eureka.png` : http://localhost:8761, services enregistrés.
- `S04_config.png` : http://localhost:8888/transaction-service/default et max-amount 1000.
- `S05_account_swagger.png` : http://localhost:8081/swagger-ui/index.html.
- `S06_transaction_swagger.png` : http://localhost:8082/swagger-ui/index.html.
- `S07_transaction_postman.png` : création d'une transaction 250 EUR et après solde actualisé.
- `S08_business_rules.png` : deux erreurs significatives : montant 1001 EUR (400) et solde insuffisant (409).
- `S09_graphql.png` : POST `/graphql` avec la query des comptes.
- `S10_mcp_chat.png` : réponse réelle de l'agent utilisant les Tools MCP ; jamais afficher la clé OpenAI.
- `S11_kafka_consumer.png` : logs d'événement TransactionCreated, accountId comme clé.
- `S12_angular.png` : dashboard avec comptes et historique.
- `S13_keycloak.png` : écran de connexion ou compte utilisateur de démonstration, sans afficher de mot de passe.
- `S14_compose.png` : sortie `docker compose ps`.
- `S15_fraud.png` : **preuve réelle disponible dès maintenant**, ouvrir `fraud/results/metrics.json` et `fraud/results/confusion_matrix.png`, obtenus à partir du `bank_transactions.csv` fourni.
- `S17_notebook_fraud.png` : ouvrir `fraud/Analyse_Fraude_ADRIA.ipynb` dans Jupyter/VS Code avec les cellules déjà exécutées, montrer le tableau comparaison CV et les figures.
- `S18_eda.png` : ouvrir `fraud/results/repartition_fraudes.png` et `fraud/results/valeurs_manquantes.png`; figures réellement générées sur les 5 000 transactions.
- `S19_python_tests.png` : exécuter `cd fraud && python -m pytest -q test_train.py` et photographier la sortie locale (6 tests attendus).
- `S16_actions.png` : véritable pipeline GitHub Actions (après publication du repo).

**Aucune capture des services Java, Angular, Kafka ou Keycloak ne peut être revendiquée avant leur lancement réel.** Les PNG du dossier `fraud/results/` sont des résultats calculés, pas des captures simulées de logiciels.

## Ajouter les captures au rapport PDF

Le fichier `rapport/Compte_rendu_ADRIA.pdf` est généré comme **base de compte rendu** : ses captures réelles restent à insérer après tests. Ouvrir le générateur `tools/build_report.py` ou transmettre vos captures dans la conversation pour produire un rapport final actualisé.

**Important** : jamais de captures faisant apparaître un vrai token, secret, mot de passe, clé privée ou clé API.
