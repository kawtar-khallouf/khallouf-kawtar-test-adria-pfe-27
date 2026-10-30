#!/usr/bin/env python3
"""Generate the ADRIA PDF report from source and optional real screenshots.
Only existing Sxx PNG/JPG files under docs/captures are included; never fakes run evidence.
"""
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
import html, glob
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rapport'/'Compte_rendu_ADRIA.pdf'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if not Path(FONT).exists(): FONT='Helvetica';BOLD='Helvetica-Bold'
else:
 pdfmetrics.registerFont(TTFont('DejaVu',FONT));pdfmetrics.registerFont(TTFont('DejaVuBold',BOLD))
 FONT='DejaVu';BOLD='DejaVuBold'
NAVY=colors.HexColor('#173A68');BLUE=colors.HexColor('#266DC4');MUTED=colors.HexColor('#60728B');PALE=colors.HexColor('#ECF4FE');LINE=colors.HexColor('#D8E2EE');W=510
s={
 'title':ParagraphStyle('title',fontName=BOLD,fontSize=23,leading=30,textColor=NAVY,spaceAfter=14),
 'sub':ParagraphStyle('sub',fontName=FONT,fontSize=11.5,leading=18,textColor=MUTED,spaceAfter=11),
 'h1':ParagraphStyle('h1',fontName=BOLD,fontSize=14.5,leading=21,textColor=NAVY,spaceBefore=15,spaceAfter=8,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName=BOLD,fontSize=10.5,leading=16,textColor=BLUE,spaceBefore=10,spaceAfter=6,keepWithNext=True),
 'body':ParagraphStyle('body',fontName=FONT,fontSize=9,leading=15.3,textColor=colors.HexColor('#31435E'),spaceAfter=7),
 'small':ParagraphStyle('small',fontName=FONT,fontSize=7.7,leading=11.8,textColor=colors.HexColor('#31435E'),spaceAfter=5),
 'tiny':ParagraphStyle('tiny',fontName=FONT,fontSize=7.15,leading=10.9,textColor=colors.HexColor('#31435E')),
 'cover':ParagraphStyle('cover',fontName=FONT,fontSize=11.5,leading=19,textColor=BLUE),
 'footer':ParagraphStyle('footer',fontName=FONT,fontSize=7.3,leading=11,textColor=MUTED)
}
def p(txt,style='body'): return Paragraph(txt,s[style])
def h(txt):story.append(p(txt,'h1'))
def sub(txt):story.append(p(txt,'h2'))
def add(txt):story.append(p(txt))
def bullet(lines):
 for line in lines:story.append(p('&#8226; '+html.escape(line),'body'))
def img(path,width=W):
 from PIL import Image as PIL
 x=ROOT/path
 if not x.exists():return
 im=PIL.open(x);ratio=im.height/im.width
 if width*ratio>505: width=505/ratio
 story.append(Image(str(x),width=width,height=width*ratio))
 story.append(Spacer(1,10))
def tbl(rows,widths=None):
 data=[]
 for ri,row in enumerate(rows):
  data.append([p(html.escape(str(v)),'tiny') for v in row])
 table=Table(data,colWidths=widths or [W/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
 table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),NAVY),
 ('TEXTCOLOR',(0,0),(-1,0),colors.white),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7FB')]),
 ('GRID',(0,0),(-1,-1),.35,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
 ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
 # header paragraphs own font color: explicitly set header white text styles
 for c,txt in enumerate(rows[0]):
  data[0][c]=Paragraph(html.escape(str(txt)),ParagraphStyle('tablehead',parent=s['tiny'],fontName=BOLD,textColor=colors.white))
 story.append(table);story.append(Spacer(1,10))
def nextpage():story.append(PageBreak())

def footer(canvas,doc):
 canvas.saveState();width,height=A4
 canvas.setStrokeColor(LINE);canvas.line(42,38,width-42,38)
 canvas.setFont(FONT,7.5);canvas.setFillColor(MUTED)
 canvas.drawString(42,26,'ADRIA x ENSET | Compte rendu POC - version à valider par exécution')
 canvas.drawRightString(width-42,26,f'Page {doc.page}')
 canvas.restoreState()

story=[]
story.append(Spacer(1,73))
story.append(p('ÉPREUVE TECHNIQUE DE SÉLECTION','cover'))
story.append(p('Plateforme bancaire distribuée<br/>Spring Cloud, IA, Kafka &amp; Angular','title'))
story.append(HRFlowable(width='98%',thickness=2,color=BLUE,spaceBefore=7,spaceAfter=22))
story.append(p('<b>Priorité de candidature : Data Science (partie H) | Second choix : Full Stack</b>','sub'))
story.append(p('Rapport de conception, développement et résultats vérifiés de machine learning','cover'))
add('<b>Énoncé :</b> Test.pdf (4 pages) — architecture micro-services, IA et développement full-stack, durée annoncée : 3 heures.')
add('<b>Référence pédagogique :</b> Mohamed Youssfi, ENSET — architecture en couches, Spring Boot, Spring Cloud et pratiques Kafka.')
add('<b>Livrables :</b> backend Maven multi-modules, frontend Angular (partie G), Python et notebook Jupyter exécuté (partie H prioritaire), Docker Compose, diagrammes, README et procédures de captures.')
story.append(Spacer(1,23))
img('docs/architecture.png',width=480)
story.append(p('<b>VALIDATION :</b> Le fichier bank_transactions.csv fourni contient 5 000 lignes et 257 fraudes (5,14 %). Pipeline Python exécuté et évalué sur test indépendant, 6 tests pytest réussis. En revanche, aucune exécution Maven, Docker ou Angular n’est revendiquée sans preuve réelle.','small'))
nextpage()
h('1. Analyse du besoin et périmètre')
add('L’application bancaire a pour fonctions la consultation des comptes, l’enregistrement de transactions et les virements. Chaque transaction respecte le statut et la devise du compte, le solde disponible et le plafond bancaire partagé. Les événements de transaction doivent être publiés dans Kafka ; un assistant agentique utilise les outils exposés via MCP. Un modèle de fraude est étudié séparément en Python.')
sub('Correspondance avec les parties A à I de l’énoncé')
tbl([['Partie','Objectif','Implémentation / preuve'],['A','Remise, GitHub et rapport','README/PDF ; dépôt, Sheet, Classroom et commits à effectuer personnellement'],['B','Architecture et UML','Schémas PNG et sources DOT/SVG'],['C','Métier REST/GraphQL/MCP','Account, Transaction, OpenFeign, Resilience4j'],['D','Infrastructure Spring Cloud','Gateway, Eureka, Config Server ; max-amount = 1000'],['E','Agent conversationnel','Spring AI + client MCP, endpoint REST /api/chat'],['F','Événements Kafka','Outbox, topic, consumer de journalisation'],['G','Client web au choix','Dashboard Angular uniquement, sans Flutter'],['H (priorité 1)','Détection des fraudes','CSV fourni traité, 3 modèles en CV, résultats test, notebook exécuté'],['I','DevOps','Dockerfile, Compose, CI GitHub Actions, discussion de rollback']],widths=[45,137,328])
sub('Choix de réalisation')
add('Deux microservices <b>fonctionnels</b> : AccountService et TransactionService. Les composants Discovery, Config, Gateway, AI Agent et Audit Consumer sont <b>techniques</b>. L’application Angular et Keycloak sont des services d’intégration ; le modèle Python est volontairement hors du runtime Spring, conformément à la consigne.')
nextpage()
h('2. Architecture logique et UML')
img('docs/architecture.png',490)
add('Les clients passent par Gateway (8080), qui utilise Eureka (8761). Le Config Server (8888) centralise le plafond des transactions. TransactionService (8082) interroge AccountService (8081) à travers OpenFeign et un circuit breaker Resilience4j. AI Agent (8083) utilise les deux outils MCP. Kafka reçoit les événements du TransactionService et l’Audit Consumer (8084) les journalise. Le modèle Python de fraude n’est pas connecté au broker.')
img('docs/diagramme-classes.png',485)
add('Les classes BankTransaction et Account vivent dans deux bases séparées, reliées logiquement par accountId : UUID, pas par une jointure JPA. Cette isolation reprend le principe de responsabilité autonome de chaque microservice enseigné dans le cours.')
nextpage()
h('3. Implémentation et séparation des couches')
tbl([['Couche','Fichiers / rôle'],['domain/','Account, AccountStatus, BalanceOperation, BankTransaction, OutboxEvent'],['repository/','Spring Data JPA : AccountRepository, TransactionRepository, OutboxRepository'],['service/','AccountService, TransactionService, DTO et implémentations ; règles métier'],['web/rest/','API HTTP : CRUD comptes, transactions, virements'],['web/graphql/','QueryMapping et MutationMapping ; délègue à la même couche Service'],['mcp/','@Tool + ToolCallbackProvider ; délègue à la même couche Service'],['client/','OpenFeign, relais Bearer, Resilience4j pour accès distant']],widths=[132,378])
sub('Versions retenues')
add('Java 21 ; Spring Boot 3.4.2 ; Spring Cloud 2024.0.0 ; Spring AI 1.0.3 ; Springdoc 2.8.4 ; Angular 18. Ces versions suivent l’approche du professeur et la compatibilité nécessaire aux fonctionnalités AI/MCP. Dépendances Maven réparties dans les modules et versions gérées par les BOM du parent.')
sub('Contrats et endpoints métier')
tbl([['Service','Routes / fonctionnalités'],['Account','GET/POST /api/accounts ; GET/PATCH /api/accounts/{id} ; appels internes débit/crédit/virement'],['Transaction','GET/POST /api/transactions ; GET /api/transactions/{id} ; POST /api/transfers'],['GraphQL','POST /graphql/accounts et /graphql/transactions via Gateway, requêtes et mutations'],['Agent','POST /api/chat ; message et booléen confirmWrites'],['Swagger','/swagger-ui/index.html sur ports 8081 et 8082']],widths=[130,380])
sub('Vérification des règles métier')
add('Les validations imposent : montant strictement positif, maximum 1000, compte actif, devise égale, solde suffisant, deux comptes distincts. Les comptes sont verrouillés lors du débit/virement. Les identifiants d’opération sont uniques pour empêcher la répétition de mouvements sur un même operationId.')
nextpage()
h('4. Séquence de transaction et virement')
img('docs/sequence-transaction.png',490)
add('Après validation, le solde est débité dans AccountService ; TransactionService persiste localement la transaction et son événement Outbox dans la même transaction JPA. Une tâche planifiée publie ensuite l’événement dans Kafka. En cas de panne du broker, l’Outbox conserve l’événement à réessayer.')
img('docs/sequence-virement.png',490)
add('Le virement entre deux comptes est atomique dans la base de AccountService, après verrouillage de chaque compte. Les mouvements de transfert sont ensuite ajoutés à TransactionService. Une compensation best-effort tente le mouvement inverse si cet enregistrement échoue ; elle ne garantit pas une ACID globale entre services.')
sub('Communication et résilience')
add('OpenFeign identifie AccountService par son nom Eureka ; Resilience4j assure l’ouverture temporaire d’un circuit si le service distant est défaillant. Il ne faut jamais remplacer un solde réel indisponible par une valeur fictive de fallback. Les erreurs 4xx métier sont préservées lorsqu’elles proviennent du service distant.')
nextpage()
h('5. Intégration REST, GraphQL, MCP, IA et Keycloak')
sub('Trois accès, une seule logique métier')
add('REST, GraphQL et MCP utilisent les mêmes services applicatifs. REST est documenté par Springdoc ; les schémas GraphQL se trouvent dans src/main/resources/graphql ; Spring AI expose des outils @Tool via les serveurs MCP des modules métier. Le client MCP SSE de l’agent découvre les outils et les fournit au ChatClient.')
sub('Agent bancaire')
add('POST /api/chat reçoit un message et un booléen confirmWrites. Les outils d’écriture sont exclus si confirmWrites vaut false. Un modèle LLM est sollicité uniquement avec une clé fournie à travers OPENAI_API_KEY. Le chatbot doit utiliser les outils pour connaître les vrais soldes et ne pas inventer les résultats. Le test REST est le client choisi ; Telegram et Discord n’ont pas été développés.')
sub('Sécurité et autorisations')
add('Keycloak importe le realm bank et le client public bank-ui, qui emploie Authorization Code + PKCE. Les comptes de démonstration ont des rôles VIEWER et OPERATOR. Gateway et services métier disposent de la validation JWT. Les appels Feign relaient le Bearer token lorsqu’il existe ; le fallback service-to-service prévoit un client credentials. Les endpoints MCP SSE nécessitent un filtrage réseau rigoureux : ils ne doivent pas être publiés sans protections supplémentaires.')
sub('Tests attendus / captures')
add('Insérer des captures réelles de Swagger (S05-S06), GraphQL (S09), connexion Keycloak (S13), une conversation agentique (S10), et Angular (S12). Le présent rapport ne fabrique pas ces captures.')
nextpage()
h('6. Kafka et communication événementielle')
add('Topic : <b>bank.transactions.created</b>. La clé Kafka est <b>accountId</b>. Un événement TransactionCreated comprend eventId, eventType, transactionId, accountId, amount, currency et occurredAt. Une tâche Outbox réessaie les publications après panne de Kafka. Le consumer écrit une ligne de log de l’événement reçu et n’accède à aucune base de comptes ou transactions.')
tbl([['Champ','Type / exemple'],['eventId','UUID aléatoire'],['eventType','TransactionCreated'],['transactionId','UUID de la transaction persistée'],['accountId','UUID utilisé aussi comme clé Kafka'],['amount','250.00 (nombre)'],['currency','EUR'],['occurredAt','Instant UTC ISO-8601']],widths=[145,365])
sub('Limites et garanties')
add('L’Outbox évite la perte d’événement entre persistance JPA et Kafka, mais la livraison est de type at-least-once. Il faut dédupliquer les eventId côté consommateur en production ; les logs actuels sont uniquement des journaux pédagogiques. Référence de capture : S11 via docker compose logs event-consumer-service.')
nextpage()
h('7. PARTIE H — Data Science : données, méthode et résultats')
add('<b>Premier choix de stage : Data Science.</b> Cette section rend compte de résultats effectivement calculés à partir du fichier bank_transactions.csv fourni (5 000 lignes, 9 variables au total, 257 cas de fraude). Le modèle reste expérimental, hors microservices, conformément à l’énoncé. Les parties techniques conservent leur architecture Spring Cloud et le frontend G est uniquement Angular.')
sub('7.1 Profil des données : qualité et déséquilibre')
tbl([['Indicateur','Valeur observée'],['Transactions','5 000'],['Non fraudes','4 743 = 94,86 %'],['Fraudes','257 = 5,14 %'],['Attributs','9 dont is_fraud et deux identifiants'],['Valeurs manquantes','country : 66 ; merchant_category : 84 ; average_amount_last_7d : 75'],['IDs en double','0 identifiants transaction répétés']],widths=[160,350])
img('fraud/results/repartition_fraudes.png',345)
img('fraud/results/valeurs_manquantes.png',330)
nextpage()
h('7.2 Méthode anti-fuite et sélection en validation croisée')
img('docs/architecture-ml.png',490)
add('Le découpage stratifié, seed 42, réserve 3 750 transactions à l’entraînement et 1 250 au test (64 fraudes). Une chaîne scikit-learn impute les numériques par médiane et les catégories par mode, applique la standardisation et le OneHotEncoder. Chaque prétraitement est appris dans les seuls plis d’entraînement. Les identifiants transaction_id/account_id et la cible sont exclus des variables explicatives.')
sub('Comparaison des modèles : average precision en CV stratifiée 3 plis sur train')
tbl([['Modèle','AP moyenne train','Écart-type'],['Régression logistique pondérée','0,1833','0,0209'],['Random Forest pondérée','0,1131','0,0127'],['Arbre de décision pondéré','0,0935','0,0150']],widths=[270,125,115])
img('fraud/results/comparaison_modeles.png',405)
add('La régression logistique pondérée est sélectionnée sur le train uniquement. Le seuil fixe 0,50 est la référence ; le seuil secondaire 0,80 provient de la maximisation du F1 sur prédictions hors-pli du train. Aucun choix n’utilise les étiquettes du test.')
nextpage()
h('7.3 Évaluation indépendante sur les 1 250 transactions de test')
tbl([['Approche','Accuracy','Précision fraude','Rappel fraude','F1 fraude'],['Baseline non fraude','94,88 %','0 %','0 %','0'],['Modèle seuil 0,50','73,44 %','10,36 %','54,69 %','0,1741'],['Modèle seuil 0,80','92,48 %','23,21 %','20,31 %','0,2167']],widths=[155,88,93,88,86])
add('<b>Average Precision test : 0,1885.</b> Pour le seuil de 0,50 : 883 vrais négatifs, 303 faux positifs, 29 faux négatifs et 35 vrais positifs. Le modèle détecte 35/64 fraudes, mais produit 303 fausses alertes. Il ne peut pas être présenté comme prêt à déployer.')
img('fraud/results/confusion_matrix.png',405)
nextpage()
h('7.4 Courbe précision-rappel, seuil et interprétabilité')
img('fraud/results/precision_recall.png',415)
add('La performance doit être comparée à la prévalence de référence (environ 5,14 %). Average Precision = 0,1885 sur le test. Une courbe PR est plus informative qu’une accuracy globale dans le cas de fraude minoritaire.')
img('fraud/results/analyse_seuil_sur_train.png',390)
add('L’étude du seuil est calculée uniquement avec les probabilités hors-pli de l’entraînement. Le seuil choisi sur train est 0,80 ; sur le test il conduit à 43 fausses alertes contre 303 à 0,50, mais augmente les fraudes manquées de 29 à 51. Le compromis doit être défini selon les coûts métier.')
nextpage()
h('7.5 Importance des variables et questions d’analyse')
img('fraud/results/importance_variables.png',420)
add('L’importance par permutation est calculée sur le train, à des fins diagnostiques. Elle ne démontre pas de relation causale entre les variables et les fraudes.')
sub('Réponses aux quatre questions de l’épreuve')
add('<b>1. Accuracy insuffisante :</b> la stratégie toujours non-fraude donne 94,88 % d’accuracy mais ne détecte aucune des 64 fraudes du test. Considérer rappel, précision, F1 et AP.')
add('<b>2. Faux positifs et fraudes manquées :</b> seuil 0,50 = 303 fausses alertes et 29 fraudes manquées. Seuil 0,80 = 43 fausses alertes et 51 fraudes manquées. Aucun arbitrage sans coûts métier.')
add('<b>3. Diminution du seuil :</b> de 0,80 à 0,50, le rappel monte de 20,31 % à 54,69 %, mais les faux positifs augmentent de 43 à 303 sur le test.')
add('<b>4. Validation temporelle :</b> entraînement sur le passé et test sur le futur réduisent les fuites et mesurent mieux le déploiement. Le CSV n’a pas de timestamp complet, seulement hour ; la validation temporelle est donc impossible avec ces données. La stratification demandée est appliquée.')
sub('Livrables Data Science exécutés')
add('fraud/train.py ; fraud/Analyse_Fraude_ADRIA.ipynb (notebook avec sorties réelles) ; fraud/results/metrics.json, profile et figures ; 6 tests unitaires Python réussis. Ni service REST de modèle, ni intégration Kafka : non demandés par la partie H.')
nextpage()
h('8. DevOps et déploiement local')
sub('Docker Compose')
add('Le fichier compose.yml rassemble ZooKeeper, Kafka, Keycloak, Eureka, Config, Gateway, Account, Transaction, Audit Consumer, AI Agent et Angular. Un Dockerfile Maven multi-stage prend le paramètre MODULE et utilise Java 21. Les ports publics de développement sont associés à 127.0.0.1. Le démarrage de conteneurs ne prouve pas leur disponibilité : vérifier les health endpoints et les logs.')
sub('Pipeline CI/CD — GitHub Actions')
add('La CI exécute la compilation Maven, les tests unitaires, le build Angular, la construction des images et leur publication sur GitHub Container Registry avec un tag SHA. La phase de déploiement reste un exemple désactivé, car aucun déploiement cloud réel n’est exigé. Les variables de production doivent être créées dans GitHub Secrets / un gestionnaire de secrets.')
tbl([['Exigence DevOps','Réponse du projet'],['Secrets et configuration','Secrets via variables sécurisées / GitHub Secrets ; configuration partagée dans Spring Config, sans clé réelle dans Git.'],['Démarrage, disponibilité, vitalité','Actuator /actuator/health ; probes readiness/liveness à finaliser pour le runtime cible.'],['Logs, métriques, traces','Logs SLF4J + Actuator ; Prometheus/Grafana/OpenTelemetry recommandés pour la production.'],['Rollback','Images immuables SHA ; redéployer le digest de la dernière version saine.']],widths=[165,345])
nextpage()
h('9. Plan de tests, preuves et captures réelles')
add('Les tests Java nécessitent Maven et les dépendances réseau ; les tests de conteneurs nécessitent Docker et Keycloak. Ces exécutables ne sont pas disponibles ici. Le tableau indique les preuves <b>à produire par l’étudiant</b> après exécution locale, sans validation non observée.')
tbl([['Réf.','Capture / test attendu'],['S01 / S02','Arborescence Maven et résultat réel mvn clean verify'],['S03 / S04','Eureka et configuration transaction-service (1000)'],['S05 / S06','Swagger Account et Transaction'],['S07 / S08','Transaction valide, refus montant 1001, fonds insuffisants'],['S09 / S10','GraphQL, puis agent MCP avec clé LLM valide'],['S11 / S12','Log consumer Kafka et dashboard Angular'],['S13 / S14','Connexion Keycloak et docker compose ps'],['S15 / S16','Résultats Python réels fournis ; GitHub Actions à exécuter sur votre dépôt']],widths=[100,410])
sub('Protocole d’essai')
add('Commencer par une transaction nominale de 250 EUR sur un compte actif disposant d’un solde supérieur. Vérifier le nouveau solde, l’enregistrement dans TransactionService, puis l’événement consommé. Refaire avec 1001 EUR, une devise différente et un compte bloqué. Vérifier ensuite les virements, GraphQL, Keycloak et le chatbot. Le README détaille les URLs et commandes.')
# attach genuine available screenshots only
captures=sorted((ROOT/'docs'/'captures').glob('S*.png'))+sorted((ROOT/'docs'/'captures').glob('S*.jpg'))
if captures:
 nextpage();h('10. Captures réelles importées')
 for screenshot in captures[:12]:
  sub(screenshot.name)
  try:
   im=ImageReader(str(screenshot));iw,ih=im.getSize();width=min(W,480);height=width*ih/iw
   if height>450:width*=450/height;height=450
   story.append(Image(str(screenshot),width=width,height=height));story.append(Spacer(1,14))
  except Exception as ex:add(f'Capture non lisible : {html.escape(screenshot.name)}')
nextpage()
h('10. Conclusion, améliorations et limites')
add('Le projet propose un démonstrateur cohérent de système bancaire distribué : séparation des responsabilités, service Discovery, configuration centralisée, Gateway, règles métier, OpenFeign/Resilience4j, GraphQL/MCP, Spring AI, Kafka avec Outbox, sécurité Keycloak, Angular, ML Python et livrables CI/CD. Il suit l’approche en couches du cours et répond aux parties A à I du sujet par du code, des schémas et des procédures.')
sub('Limites à préciser au jury')
bullet([
 'Tests Java, build Angular et conteneurs non exécutés ici : effectuer ces vérifications sur votre poste. Tests Python sur scénarios artificiels : 6/6 réussis.',
 'Le CSV fourni a été évalué : AP test 0,1885 et rappel 54,69 % à seuil 0,50, mais 303 faux positifs. Modèle volontairement offline, sans déploiement.',
 'Solde stocké en double selon le modèle minimal ; recommander BigDecimal/DECIMAL en production.',
 'Pas de transaction distribuée ACID : compensation best-effort et besoin de Saga/réconciliation.',
 'Outbox et Kafka entraînent la possibilité de messages doublés ; déduplication par eventId à ajouter.',
 'MCP SSE, Keycloak et compte de service doivent être sécurisés/testés avant tout déploiement accessible.',
 'Comptes de démo et base H2 en mémoire : non destinés à des données bancaires réelles.'
])
sub('Actions de remise personnelles')
add('Créer un dépôt GitHub privé sous le nom indiqué dans l’énoncé ; remplir le Google Sheet ; réaliser des commits pendant l’épreuve à intervalles réguliers d’environ 15 minutes ; compléter ce rapport avec des captures réelles ; publier le dépôt seulement à la fin conformément aux consignes ; déposer dépôt et PDF sur Classroom. Aucun de ces actes externes n’a été exécuté automatiquement.')
sub('Références')
add('Mohamed Youssfi : Support Architectures Micro Services avec Spring Cloud ; dépôts github.com/mohamedYoussfi/micro-services-app et github.com/mohamedYoussfi/kafka-streams-spring-cloud-stream-bdcc-enset. Documentation officielle Spring Cloud, Spring AI MCP 1.0, Keycloak, Apache Kafka ; références et URLs détaillées dans le README.')

doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=49,bottomMargin=55,title='Compte rendu ADRIA - Plateforme bancaire distribuée',author='Projet académique ENSET',subject='Microservices, IA, Angular, Kafka, DevOps')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Created',OUT,OUT.stat().st_size)
