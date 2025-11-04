"""
Quiz 3 - Monitoring et Observabilité
Prometheus, Grafana, ELK Stack et pratiques d'observabilité

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 25 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 3 - Kubernetes Production
"""

def run_quiz():
    """Execute le quiz de validation des concepts Monitoring et Observabilité"""

    print("=" * 65)
    print(" QUIZ KUBERNETES PRODUCTION - MONITORING ET OBSERVABILITÉ")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 65)

    score = 0
    total_questions = 25

    # Question 1 - Observabilité concept
    print("\n1. L'observabilité repose sur trois piliers principaux :")
    print("a) Logs, Metrics, Traces  b) CPU, Memory, Storage")
    print("c) Pods, Services, Volumes  d) Frontend, Backend, Database")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Les trois piliers sont Logs, Metrics et Traces")

    # Question 2 - Prometheus
    print("\n2. Prometheus est :")
    print("a) Un orchestrateur  b) Un système de monitoring et d'alerting")
    print("c) Un load balancer  d) Un système de déploiement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Prometheus est un système de monitoring time-series")

    # Question 3 - Métriques Prometheus
    print("\n3. Les métriques Prometheus sont stockées au format :")
    print("a) JSON  b) XML  c) Time-series  d) CSV")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Prometheus utilise des time-series avec labels")

    # Question 4 - PromQL
    print("\n4. PromQL est :")
    print("a) Un langage de programmation  b) Le langage de requête de Prometheus")
    print("c) Un protocole réseau  d) Un format de données")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) PromQL est le langage de requête de Prometheus")

    # Question 5 - Node Exporter
    print("\n5. Node Exporter expose :")
    print("a) Métriques des applications  b) Métriques du système d'exploitation")
    print("c) Logs des pods  d) Configuration Kubernetes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Node Exporter collecte les métriques OS/hardware")

    # Question 6 - Grafana
    print("\n6. Grafana est principalement utilisé pour :")
    print("a) Stocker les métriques  b) Visualiser et créer des dashboards")
    print("c) Collecter les logs  d) Déployer des applications")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Grafana crée des visualisations et dashboards")

    # Question 7 - ServiceMonitor
    print("\n7. ServiceMonitor dans Prometheus Operator définit :")
    print("a) L'état d'un service  b) Comment scraper les métriques d'un service")
    print("c) Les alertes d'un service  d) La configuration réseau")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ServiceMonitor configure le scraping des métriques")

    # Question 8 - Alertmanager
    print("\n8. Alertmanager gère :")
    print("a) Les métriques  b) Les alertes et notifications")
    print("c) Les logs  d) Les traces")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Alertmanager route et envoie les notifications d'alertes")

    # Question 9 - ELK Stack
    print("\n9. ELK Stack est composé de :")
    print("a) Elasticsearch, Logstash, Kibana  b) Elastic, Linux, Kubernetes")
    print("c) Events, Logs, Kafka  d) Error, Latency, Kube")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) ELK = Elasticsearch, Logstash, Kibana")

    # Question 10 - Filebeat
    print("\n10. Filebeat est utilisé pour :")
    print("a) Gérer les fichiers  b) Collecter et transmettre les logs")
    print("c) Synchroniser les horloges  d) Compresser les données")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Filebeat collecte et transmet les logs vers Elasticsearch")

    # Question 11 - Kibana
    print("\n11. Kibana permet de :")
    print("a) Stocker les logs  b) Visualiser et analyser les logs")
    print("c) Compresser les logs  d) Chiffrer les logs")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Kibana visualise et analyse les données Elasticsearch")

    # Question 12 - Fluentd
    print("\n12. Fluentd est :")
    print("a) Un collecteur de logs unifié  b) Un système de monitoring")
    print("c) Un load balancer  d) Un orchestrateur")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Fluentd collecte, transforme et route les logs")

    # Question 13 - Jaeger
    print("\n13. Jaeger est utilisé pour :")
    print("a) Monitoring des métriques  b) Tracing distribué")
    print("c) Gestion des logs  d) Load balancing")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Jaeger implémente le tracing distribué OpenTelemetry")

    # Question 14 - Golden Signals
    print("\n14. Les 'Golden Signals' du SRE sont :")
    print("a) Latency, Traffic, Errors, Saturation  b) CPU, Memory, Disk, Network")
    print("c) Pods, Services, Volumes, Configs  d) Frontend, Backend, Database, Cache")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Les 4 Golden Signals: Latency, Traffic, Errors, Saturation")

    # Question 15 - Custom Metrics
    print("\n15. Pour exposer des métriques custom d'une application :")
    print("a) Utiliser l'endpoint /metrics  b) Créer un exporter")
    print("c) Instrumenter le code  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Toutes ces approches peuvent être utilisées")

    # Question 16 - Structured Logging
    print("\n16. Le structured logging utilise généralement :")
    print("a) Format JSON  b) Format texte libre  c) Format binaire  d) Format XML")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) JSON facilite l'indexation et la recherche")

    # Question 17 - SLI/SLO
    print("\n17. SLI et SLO signifient :")
    print("a) Service Level Indicator/Objective  b) System Load Indicator/Objective")
    print("c) Security Level Indicator/Objective  d) Service Link Indicator/Objective")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) SLI = Indicator, SLO = Objective pour la fiabilité")

    # Question 18 - MTTR/MTBF
    print("\n18. MTTR et MTBF mesurent :")
    print("a) Performance CPU  b) Fiabilité et temps de récupération")
    print("c) Utilisation mémoire  d) Bande passante réseau")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) MTTR = Mean Time To Recovery, MTBF = Mean Time Between Failures")

    # Question 19 - Log retention
    print("\n19. La rétention des logs dépend de :")
    print("a) Conformité réglementaire  b) Espace de stockage")
    print("c) Importance des données  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) La rétention dépend de plusieurs facteurs")

    # Question 20 - Distributed Tracing
    print("\n20. Le distributed tracing aide à :")
    print("a) Suivre les requêtes à travers les microservices")
    print("b) Monitorer les métriques  c) Gérer les logs  d) Configurer les alertes")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Le tracing suit le parcours des requêtes distribuées")

    # Question 21 - Blackbox monitoring
    print("\n21. Le blackbox monitoring teste :")
    print("a) Le code source  b) L'expérience utilisateur externe")
    print("c) Les métriques internes  d) La configuration")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Blackbox monitoring teste depuis l'extérieur")

    # Question 22 - Error budget
    print("\n22. Un error budget représente :")
    print("a) Le budget pour corriger les erreurs")
    print("b) Le niveau d'erreur acceptable selon les SLO")
    print("c) Le coût des pannes  d) Le temps de développement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Error budget = marge d'erreur autorisée par les SLO")

    # Question 23 - Metrics cardinality
    print("\n23. Une cardinalité élevée des métriques peut causer :")
    print("a) Problèmes de performance  b) Consommation mémoire")
    print("c) Coûts de stockage  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Haute cardinalité = plus de ressources et de coûts")

    # Question 24 - Runbook
    print("\n24. Un runbook contient :")
    print("a) Procédures de réponse aux incidents")
    print("b) Code de l'application  c) Configuration réseau  d) Schémas de données")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Runbook = procédures opérationnelles pour incidents")

    # Question 25 - Canary monitoring
    print("\n25. Le canary monitoring permet de :")
    print("a) Détecter les problèmes avant déploiement complet")
    print("b) Surveiller les oiseaux  c) Tester les performances  d) Gérer les versions")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Canary monitoring détecte les problèmes sur un sous-ensemble")

    # Résultats finaux
    print("\n" + "=" * 65)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 65)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez le monitoring et l'observabilité Kubernetes")
        print("Vous pouvez passer au Quiz 4 - Performance et Concepts Avancés")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Concepts de base: observabilité, métriques, logs, traces")
            print("- Stack Prometheus/Grafana et ELK")
        elif score < 15:
            print("- Configuration avancée Prometheus et Alertmanager")
            print("- Structured logging et distributed tracing")
        else:
            print("- SRE practices et SLI/SLO")
            print("- Optimisation performance et troubleshooting")
        print("Recommandation: Refaire les LABs 6-7 et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Production - Monitoring et Observabilité")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 3 - Kubernetes Production")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*65}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 4 - Performance et Concepts Avancés")
    else:
        print("Direction: Révision LABs 6-7 et nouvelle tentative")
    print(f"{'='*65}")