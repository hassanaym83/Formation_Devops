"""
Quiz 2 - Helm Charts et GitOps
Déploiement et gestion d'applications avec Helm et ArgoCD

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 25 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 3 - Kubernetes Production
"""

def run_quiz():
    """Execute le quiz de validation des concepts Helm Charts et GitOps"""

    print("=" * 60)
    print(" QUIZ KUBERNETES PRODUCTION - HELM CHARTS ET GITOPS")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - Helm de base
    print("\n1. Qu'est-ce que Helm dans l'écosystème Kubernetes ?")
    print("a) Un orchestrateur  b) Un gestionnaire de packages")
    print("c) Un load balancer  d) Un système de monitoring")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Helm est le gestionnaire de packages pour Kubernetes")

    # Question 2 - Chart structure
    print("\n2. Quel fichier contient les métadonnées d'un Chart Helm ?")
    print("a) values.yaml  b) Chart.yaml  c) templates/  d) requirements.yaml")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Chart.yaml contient les métadonnées du chart")

    # Question 3 - Templates
    print("\n3. Les templates Helm utilisent quel langage de templating ?")
    print("a) Jinja2  b) Mustache  c) Go templates  d) ERB")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Helm utilise le système de templates de Go")

    # Question 4 - Values
    print("\n4. Comment passer des valeurs personnalisées lors de l'installation d'un chart ?")
    print("a) --set ou -f values.yaml  b) --config  c) --params  d) --env")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) --set pour valeurs individuelles, -f pour fichier de valeurs")

    # Question 5 - Release
    print("\n5. Qu'est-ce qu'une Release dans Helm ?")
    print("a) Une version du chart  b) Une instance déployée du chart")
    print("c) Un fichier de configuration  d) Un template")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Une Release est une instance déployée d'un chart avec un nom")

    # Question 6 - Repository
    print("\n6. Comment ajouter un repository Helm ?")
    print("a) helm add repo  b) helm repo add  c) helm install repo  d) helm create repo")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) helm repo add <nom> <url> ajoute un repository")

    # Question 7 - Dependencies
    print("\n7. Les dépendances d'un chart Helm sont définies dans :")
    print("a) values.yaml  b) Chart.yaml  c) requirements.yaml  d) dependencies.yaml")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les dépendances sont dans Chart.yaml (section dependencies)")

    # Question 8 - Hooks
    print("\n8. Les Helm hooks permettent de :")
    print("a) Connecter des services  b) Exécuter des actions à des moments spécifiques")
    print("c) Configurer le réseau  d) Gérer les volumes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les hooks exécutent des actions aux cycles de vie des releases")

    # Question 9 - GitOps concept
    print("\n9. GitOps est une méthodologie qui utilise Git comme :")
    print("a) Source de vérité pour l'infrastructure  b) Système de backup")
    print("c) Outil de monitoring  d) Load balancer")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) GitOps utilise Git comme source de vérité unique")

    # Question 10 - ArgoCD
    print("\n10. ArgoCD est un outil de :")
    print("a) Monitoring  b) Continuous Deployment GitOps")
    print("c) Load balancing  d) Backup")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ArgoCD implémente le déploiement continu GitOps")

    # Question 11 - Application ArgoCD
    print("\n11. Dans ArgoCD, une Application définit :")
    print("a) Un pod  b) La relation entre un repository Git et un cluster")
    print("c) Un service  d) Un volume")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Une Application ArgoCD lie un repository Git à un cluster destination")

    # Question 12 - Sync Policy
    print("\n12. La Sync Policy 'automated' dans ArgoCD :")
    print("a) Sauvegarde automatiquement  b) Synchronise automatiquement les changements Git")
    print("c) Redémarre les pods  d) Met à jour les images")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Automated sync déploie automatiquement les changements Git")

    # Question 13 - Helm template
    print("\n13. Que fait la commande 'helm template' ?")
    print("a) Crée un nouveau chart  b) Rend les templates sans les déployer")
    print("c) Met à jour un chart  d) Supprime un chart")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) helm template rend les templates localement sans déploiement")

    # Question 14 - Values precedence
    print("\n14. L'ordre de priorité des values Helm (du plus bas au plus haut) :")
    print("a) --set, -f, values.yaml  b) values.yaml, -f, --set")
    print("c) -f, values.yaml, --set  d) values.yaml, --set, -f")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) values.yaml < fichier -f < --set (du moins au plus prioritaire)")

    # Question 15 - Chart Museum
    print("\n15. Un Chart Museum est :")
    print("a) Un repository pour stocker les charts  b) Un outil de visualisation")
    print("c) Un système de backup  d) Un load balancer")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Chart Museum est un repository HTTP pour charts Helm")

    # Question 16 - ApplicationSet
    print("\n16. ApplicationSet dans ArgoCD permet de :")
    print("a) Sauvegarder des applications  b) Gérer plusieurs Applications avec des patterns")
    print("c) Monitorer les applications  d) Tester les applications")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ApplicationSet génère plusieurs Applications basées sur des templates")

    # Question 17 - Rollback
    print("\n17. Comment effectuer un rollback avec Helm ?")
    print("a) helm undo  b) helm rollback  c) helm revert  d) helm back")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) helm rollback <release> <revision> effectue un rollback")

    # Question 18 - Multi-tenancy
    print("\n18. Pour gérer plusieurs environnements avec ArgoCD, on utilise :")
    print("a) Multiple clusters  b) Projects et RBAC  c) Différents namespaces  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Toutes ces approches peuvent être utilisées pour la multi-tenancy")

    # Question 19 - Helm lint
    print("\n19. La commande 'helm lint' permet de :")
    print("a) Formater le code  b) Valider la syntaxe du chart")
    print("c) Compresser le chart  d) Publier le chart")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) helm lint valide la syntaxe et structure du chart")

    # Question 20 - ArgoCD CLI
    print("\n20. Comment se connecter à ArgoCD en CLI ?")
    print("a) argocd login  b) argocd connect  c) argocd auth  d) argocd signin")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) argocd login <server> pour s'authentifier")

    # Question 21 - Health Status
    print("\n21. Dans ArgoCD, un Health Status 'Degraded' signifie :")
    print("a) Application supprimée  b) Ressources en état anormal")
    print("c) Synchronisation en cours  d) Application saine")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Degraded indique que des ressources ne fonctionnent pas normalement")

    # Question 22 - Helm secrets
    print("\n22. Pour gérer les secrets dans Helm, on peut utiliser :")
    print("a) Helm secrets plugin  b) External Secrets Operator")
    print("c) Sealed Secrets  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Plusieurs solutions existent pour la gestion sécurisée des secrets")

    # Question 23 - Sync Window
    print("\n23. Les Sync Windows dans ArgoCD permettent de :")
    print("a) Contrôler quand les synchronisations peuvent avoir lieu")
    print("b) Monitorer les performances  c) Gérer les backups  d) Configurer le réseau")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Sync Windows définissent des fenêtres de déploiement autorisées")

    # Question 24 - Chart versioning
    print("\n24. Le versioning des charts Helm suit généralement :")
    print("a) Semantic Versioning  b) Date versioning  c) Sequential numbering  d) Random versioning")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Les charts Helm utilisent le Semantic Versioning (semver)")

    # Question 25 - GitOps benefits
    print("\n25. Le principal avantage de GitOps est :")
    print("a) Performance  b) Traçabilité et reproductibilité")
    print("c) Compression  d) Chiffrement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) GitOps assure traçabilité, reproductibilité et audit trail")

    # Résultats finaux
    print("\n" + "=" * 60)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez Helm Charts et les concepts GitOps")
        print("Vous pouvez passer au Quiz 3 - Monitoring et Observabilité")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Concepts de base Helm (Charts, Templates, Values)")
            print("- Principes GitOps et ArgoCD")
        elif score < 15:
            print("- Gestion avancée des charts et dépendances")
            print("- Configuration ArgoCD et Applications")
        else:
            print("- Concepts avancés GitOps et multi-environnements")
            print("- Sécurité et bonnes pratiques Helm/ArgoCD")
        print("Recommandation: Refaire les LABs 3-5 et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Production - Helm Charts et GitOps")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 3 - Kubernetes Production")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 3 - Monitoring et Observabilité")
    else:
        print("Direction: Révision LABs 3-5 et nouvelle tentative")
    print(f"{'='*60}")