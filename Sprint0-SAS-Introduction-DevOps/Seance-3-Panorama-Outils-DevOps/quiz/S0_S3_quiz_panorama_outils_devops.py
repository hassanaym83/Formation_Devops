"""
Quiz Séance 3 - Validation des acquis
Panorama des Outils DevOps et Écosystème

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 20 minutes

Sprint 0 - Séance 3 - Panorama des Outils DevOps
"""

def run_quiz():
    """Execute le quiz de validation des concepts outils DevOps"""

    print("=" * 60)
    print("    QUIZ PANORAMA DES OUTILS DEVOPS")
    print("    25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - Écosystème DevOps
    print("\n1. Combien d'outils sont couramment utilisés dans l'écosystème DevOps ?")
    print("a) Plus de 500    b) Plus de 1000    c) Plus de 1500    d) Plus de 2000")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Plus de 1000 outils dans l'écosystème DevOps")

    # Question 2 - Classification outils
    print("\n2. Combien de catégories principales d'outils DevOps existent-il ?")
    print("a) 5 catégories    b) 7 catégories    c) 10 catégories    d) 12 catégories")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 10 catégories principales (Gestion de code, CI/CD, Tests, etc.)")

    # Question 3 - Gestion de code
    print("\n3. Quel est l'outil de versioning le plus populaire ?")
    print("a) SVN    b) Git    c) Mercurial    d) Bazaar")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Git - Standard de facto pour le versioning")

    # Question 4 - Plateformes Git
    print("\n4. Quelle plateforme Git est la plus utilisée pour les projets open source ?")
    print("a) GitLab    b) Bitbucket    c) GitHub    d) Azure DevOps")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) GitHub - Leader pour l'open source")

    # Question 5 - CI/CD Jenkins
    print("\n5. Quel est l'outil CI/CD open source le plus adopté ?")
    print("a) GitLab CI    b) Jenkins    c) GitHub Actions    d) TeamCity")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Jenkins - Leader historique du CI/CD")

    # Question 6 - Tests automatisés
    print("\n6. Quelle est la pyramide des tests de Mike Cohn ?")
    print("a) Unit > Integration > E2E    b) E2E > Integration > Unit")
    print("c) Integration > Unit > E2E    d) Unit > E2E > Integration")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Unit (base) > Integration > E2E (sommet)")

    # Question 7 - Quality Gates
    print("\n7. Quel outil est référence pour les quality gates et analyse de code ?")
    print("a) Checkmarx    b) SonarQube    c) Veracode    d) CodeClimate")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) SonarQube - Standard pour quality gates")

    # Question 8 - Containerisation
    print("\n8. Quel est l'outil de containerisation dominant ?")
    print("a) LXC    b) Docker    c) Podman    d) rkt")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Docker - Standard de facto des containers")

    # Question 9 - Orchestration
    print("\n9. Quelle plateforme d'orchestration est devenue le standard ?")
    print("a) Docker Swarm    b) Kubernetes    c) Mesos    d) Nomad")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Kubernetes - Standard orchestration containers")

    # Question 10 - Infrastructure as Code
    print("\n10. Quel est l'outil IaC le plus polyvalent multi-cloud ?")
    print("a) CloudFormation    b) ARM Templates    c) Terraform    d) Pulumi")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Terraform - Leader IaC multi-cloud")

    # Question 11 - Configuration Management
    print("\n11. Quels sont les 4 outils principaux de configuration management ?")
    print("a) Ansible, Puppet, Chef, SaltStack    b) Ansible, Docker, Terraform, Vagrant")
    print("c) Jenkins, Ansible, Docker, Git    d) Puppet, Chef, Docker, Kubernetes")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Ansible, Puppet, Chef, SaltStack")

    # Question 12 - Monitoring
    print("\n12. Quelle solution est référence pour les métriques et alerting ?")
    print("a) Nagios    b) Zabbix    c) Prometheus    d) Datadog")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Prometheus - Standard monitoring cloud-native")

    # Question 13 - Logging
    print("\n13. Quelle stack est populaire pour la gestion centralisée des logs ?")
    print("a) ELK Stack    b) TICK Stack    c) LAMP Stack    d) MEAN Stack")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) ELK Stack (Elasticsearch, Logstash, Kibana)")

    # Question 14 - Sécurité DevSecOps
    print("\n14. Quel concept intègre la sécurité dans DevOps ?")
    print("a) SecOps    b) DevSecOps    c) OpsSec    d) SecDev")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) DevSecOps - Security by Design")

    # Question 15 - Collaboration
    print("\n15. Quel type d'outil facilite la communication en équipe DevOps ?")
    print("a) Slack/Teams    b) ITSM    c) CRM    d) ERP")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Slack/Teams - Communication collaborative")

    # Question 16 - Chaînes d'outils
    print("\n16. Qu'est-ce qu'une toolchain DevOps ?")
    print("a) Une liste d'outils    b) Ensemble d'outils intégrés pour processus complet")
    print("c) Un seul outil    d) Une suite commerciale")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Ensemble d'outils intégrés couvrant processus complet")

    # Question 17 - Intégration toolchain
    print("\n17. Quel est le critère principal pour intégrer des outils dans une toolchain ?")
    print("a) Prix    b) Popularité    c) Compatibilité et APIs    d) Interface")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Compatibilité et APIs pour l'intégration")

    # Question 18 - Artifact Repository
    print("\n18. Quel type d'outil stocke les artefacts de build ?")
    print("a) Git Repository    b) Artifact Repository    c) Container Registry    d) Package Manager")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Artifact Repository (Nexus, Artifactory)")

    # Question 19 - Pipeline as Code
    print("\n19. Que signifie 'Pipeline as Code' ?")
    print("a) Code dans pipeline    b) Pipeline défini par code versionné")
    print("c) Code automatique    d) Pipeline manuel")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Pipeline défini par code versionné")

    # Question 20 - GitOps
    print("\n20. Quel principe définit GitOps ?")
    print("a) Git pour tout    b) Git comme source de vérité pour déploiements")
    print("c) Opérations Git    d) Git obligatoire")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Git comme source de vérité pour déploiements")

    # Question 21 - Observabilité 3 piliers
    print("\n21. Quels sont les 3 piliers de l'observabilité ?")
    print("a) Logs, Metrics, Traces    b) Monitoring, Logging, Alerting")
    print("c) CPU, Memory, Network    d) Applications, Infrastructure, Sécurité")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Logs, Metrics, Traces - 3 piliers observabilité")

    # Question 22 - Shift Left
    print("\n22. Que signifie 'Shift Left' en DevOps ?")
    print("a) Déplacer à gauche    b) Anticiper les tests et sécurité plus tôt")
    print("c) Changer d'équipe    d) Inverser le processus")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Anticiper tests et sécurité plus tôt dans le cycle")

    # Question 23 - Feature Flags
    print("\n23. À quoi servent les Feature Flags ?")
    print("a) Marquer le code    b) Activer/désactiver fonctionnalités sans redéploiement")
    print("c) Identifier bugs    d) Versionner features")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Activer/désactiver fonctionnalités sans redéploiement")

    # Question 24 - Blue/Green Deployment
    print("\n24. Qu'est-ce qu'un déploiement Blue/Green ?")
    print("a) Déploiement coloré    b) Deux environnements identiques, bascule instantanée")
    print("c) Tests bleus et verts    d) Environnements de couleur")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Deux environnements identiques avec bascule instantanée")

    # Question 25 - Cloud Native
    print("\n25. Que caractérise une application Cloud Native ?")
    print("a) Hébergée dans le cloud    b) Microservices, containers, orchestration")
    print("c) Application web    d) Sauvegarde cloud")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Microservices, containers, orchestration, APIs")

    # Résultats finaux
    print("\n" + "=" * 60)
    print("              RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez le panorama des outils DevOps")
        print("Vous pouvez passer à la séance suivante")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Écosystème DevOps et classification des outils")
            print("- Outils de gestion de code et versioning")
        if score < 15:
            print("- CI/CD et outils d'intégration continue")
            print("- Tests automatisés et quality gates")
        if score < 20:
            print("- Containerisation et orchestration")
            print("- Infrastructure as Code et configuration management")
        if score < 23:
            print("- Monitoring, logging et observabilité")
            print("- Sécurité DevSecOps et collaboration")
        print("Recommandation: Refaire les LABs et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Panorama des Outils DevOps")
    print("Sprint 0 - Séance 3")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 4 - Introduction Tests et Qualité")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")
