"""
Quiz 2 - Validation des acquis Kubernetes Basics
Objets et manifests niveau intermédiaire

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 20 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 1 - Kubernetes Basics
"""

def run_quiz():
    """Execute le quiz de validation des objets Kubernetes intermédiaires"""

    print("=" * 60)
    print(" QUIZ KUBERNETES BASICS - NIVEAU INTERMÉDIAIRE")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - Deployments
    print("\n1. Quelle stratégie RollingUpdate permet de contrôler les mises à jour ?")
    print("a) maxUnavailable et maxSurge  b) replicas et strategy  c) selector et template  d) minReadySeconds")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) maxUnavailable et maxSurge contrôlent le rythme des updates")

    # Question 2 - ConfigMaps injection
    print("\n2. Comment injecter une ConfigMap comme variable d'environnement ?")
    print("a) valueFrom.configMapKeyRef  b) envFrom.configMapRef  c) Les deux  d) volumeMounts")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Les deux méthodes permettent d'injecter des ConfigMaps")

    # Question 3 - Secrets vs ConfigMaps
    print("\n3. Principale différence entre Secrets et ConfigMaps ?")
    print("a) Taille  b) Encodage base64 des Secrets  c) Localisation  d) Performance")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les Secrets sont encodés en base64 (pas chiffrés)")

    # Question 4 - PV et PVC
    print("\n4. Quelle relation existe entre PV et PVC ?")
    print("a) PVC demande, PV fournit  b) PV demande, PVC fournit  c) Identiques  d) Aucune")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) PVC est une demande, PV est une ressource de stockage")

    # Question 5 - Service selectors
    print("\n5. Un Service utilise quoi pour sélectionner ses Pods ?")
    print("a) Annotations  b) Labels  c) Namespace  d) IP addresses")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les Services utilisent des labels selectors")

    # Question 6 - Ingress Controller
    print("\n6. Un Ingress nécessite quoi pour fonctionner ?")
    print("a) LoadBalancer  b) Ingress Controller  c) DNS externe  d) Certificats")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Un Ingress Controller implémente les règles Ingress")

    # Question 7 - Health checks
    print("\n7. Quelle probe redémarre un Pod défaillant ?")
    print("a) readinessProbe  b) livenessProbe  c) startupProbe  d) healthProbe")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) livenessProbe déclenche le redémarrage du conteneur")

    # Question 8 - Resources management
    print("\n8. Que se passe-t-il si un Pod dépasse ses limits CPU ?")
    print("a) Redémarrage  b) Throttling  c) Suppression  d) Rien")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Le CPU est throttlé (bridé) mais le Pod continue")

    # Question 9 - Volumes lifecycle
    print("\n9. Un volume emptyDir est supprimé quand ?")
    print("a) Redémarrage conteneur  b) Suppression Pod  c) Redémarrage node  d) Jamais")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) emptyDir suit le cycle de vie du Pod")

    # Question 10 - Multi-container Pods
    print("\n10. Dans un Pod multi-conteneurs, les conteneurs partagent :")
    print("a) Réseau seulement  b) Stockage seulement  c) Réseau et stockage  d) Rien")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Conteneurs d'un Pod partagent réseau et volumes")

    # Question 11 - Rolling updates
    print("\n11. Pour annuler un rolling update, quelle commande ?")
    print("a) kubectl rollout restart  b) kubectl rollout undo  c) kubectl rollback  d) kubectl revert")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) kubectl rollout undo annule le déploiement")

    # Question 12 - Service types
    print("\n12. NodePort expose l'application sur quel range de ports ?")
    print("a) 1-1023  b) 1024-32767  c) 30000-32767  d) 32768-65535")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) NodePort utilise la plage 30000-32767")

    # Question 13 - ConfigMap volumes
    print("\n13. Monter une ConfigMap comme volume permet de :")
    print("a) Créer des fichiers  b) Injecter variables  c) Les deux  d) Rien")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Volume ConfigMap crée des fichiers dans le conteneur")

    # Question 14 - Deployment history
    print("\n14. Comment voir l'historique des déploiements ?")
    print("a) kubectl get deployments  b) kubectl rollout history  c) kubectl describe  d) kubectl logs")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) kubectl rollout history montre les révisions")

    # Question 15 - Persistent Volume Claims
    print("\n15. Un PVC en statut Pending indique :")
    print("a) Erreur  b) Pas de PV disponible  c) En cours d'utilisation  d) Supprimé")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Pending signifie qu'aucun PV ne correspond à la demande")

    # Question 16 - Service discovery
    print("\n16. Format DNS complet d'un Service dans Kubernetes :")
    print("a) service.namespace  b) service.namespace.svc  c) service.namespace.svc.cluster.local  d) service.cluster.local")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Format complet : service.namespace.svc.cluster.local")

    # Question 17 - Init containers
    print("\n17. Les init containers s'exécutent :")
    print("a) Avant les conteneurs principaux  b) En parallèle  c) Après  d) En continu")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Init containers s'exécutent avant les conteneurs app")

    # Question 18 - Resource quotas
    print("\n18. Les ResourceQuota s'appliquent au niveau :")
    print("a) Cluster  b) Node  c) Namespace  d) Pod")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) ResourceQuota limite les ressources par namespace")

    # Question 19 - Endpoints
    print("\n19. Les endpoints d'un Service sont automatiquement :")
    print("a) Créés manuellement  b) Générés par labels  c) Configurés par DNS  d) Fixes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Endpoints générés automatiquement via label selectors")

    # Question 20 - Pod networking
    print("\n20. Chaque Pod reçoit :")
    print("a) IP partagée avec le node  b) IP unique dans le cluster  c) Pas d'IP  d) IP externe")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Chaque Pod a une IP unique routable dans le cluster")

    # Question 21 - Scaling
    print("\n21. Pour scaler un Deployment à 10 replicas :")
    print("a) kubectl scale deployment myapp --replicas=10  b) kubectl resize  c) kubectl expand  d) kubectl grow")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) kubectl scale modifie le nombre de replicas")

    # Question 22 - Ingress paths
    print("\n22. Dans Ingress, pathType: Prefix signifie :")
    print("a) Correspondance exacte  b) Correspondance préfixe  c) Regex  d) Wildcard")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Prefix matche tous les chemins commençant par le préfixe")

    # Question 23 - Secret types
    print("\n23. Le type kubernetes.io/tls est utilisé pour :")
    print("a) Mots de passe  b) Certificats SSL/TLS  c) Tokens  d) Clés SSH")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Type tls pour certificats et clés privées SSL/TLS")

    # Question 24 - Pod restart policy
    print("\n24. RestartPolicy: OnFailure redémarre le Pod :")
    print("a) Toujours  b) Jamais  c) Si exit code != 0  d) Si healthy")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) OnFailure redémarre uniquement en cas d'échec")

    # Question 25 - Storage classes
    print("\n25. StorageClass définit :")
    print("a) Taille du stockage  b) Type de stockage  c) Localisation  d) Permissions")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) StorageClass définit le type/qualité du stockage")

    # Résultats finaux
    print("\n" + "=" * 60)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les objets et manifests Kubernetes intermédiaires")
        print("Vous pouvez passer au Quiz 3 - Orchestration Avancée")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Deployments et stratégies de mise à jour")
            print("- ConfigMaps et Secrets avancés")
        elif score < 15:
            print("- Services et networking avancé")
            print("- Volumes et persistance")
        else:
            print("- Ingress et exposition externe")
            print("- Resource management et scaling")
        print("Recommandation: Refaire les LABs 4-8 et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Basics - Niveau Intermédiaire")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 1 - Kubernetes Basics")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 3 - Orchestration avancée")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")