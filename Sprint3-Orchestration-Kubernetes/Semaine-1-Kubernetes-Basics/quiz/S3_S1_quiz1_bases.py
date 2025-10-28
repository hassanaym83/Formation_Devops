"""
Quiz 1 - Validation des acquis Kubernetes Basics
Concepts et architecture de base

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 20 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 1 - Kubernetes Basics
"""

def run_quiz():
    """Execute le quiz de validation des concepts Kubernetes de base"""

    print("=" * 60)
    print(" QUIZ KUBERNETES BASICS - CONCEPTS DE BASE")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - Architecture Kubernetes
    print("\n1. Quel composant du Control Plane stocke l'état du cluster ?")
    print("a) API Server  b) etcd  c) Scheduler  d) Controller Manager")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) etcd stocke toutes les données du cluster de manière persistante")

    # Question 2 - Pods
    print("\n2. Quelle est la plus petite unité déployable dans Kubernetes ?")
    print("a) Container  b) Node  c) Pod  d) Service")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Le Pod est l'unité atomique de déploiement")

    # Question 3 - Services
    print("\n3. Quel type de Service expose une application uniquement dans le cluster ?")
    print("a) NodePort  b) LoadBalancer  c) ClusterIP  d) ExternalName")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) ClusterIP est pour la communication interne")

    # Question 4 - kubectl
    print("\n4. Quelle commande affiche l'état des pods dans tous les namespaces ?")
    print("a) kubectl get pods  b) kubectl get pods -A  c) kubectl describe pods  d) kubectl list pods")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) -A ou --all-namespaces affiche toutes les ressources")

    # Question 5 - Manifests YAML
    print("\n5. Quel champ est obligatoire dans tous les manifests Kubernetes ?")
    print("a) metadata  b) spec  c) kind  d) Tous les précédents")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) apiVersion, kind, metadata et spec sont tous obligatoires")

    # Question 6 - Namespaces
    print("\n6. Quel namespace contient les composants système de Kubernetes ?")
    print("a) default  b) kube-system  c) kube-public  d) kube-node-lease")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) kube-system contient les pods système")

    # Question 7 - Réplication
    print("\n7. Quel objet gère directement les Pods dans un Deployment ?")
    print("a) Service  b) ReplicaSet  c) ConfigMap  d) Ingress")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Le ReplicaSet assure le nombre de replicas")

    # Question 8 - Networking
    print("\n8. Comment les Pods communiquent-ils entre eux par défaut ?")
    print("a) Via NAT  b) Directement par IP  c) Via proxy  d) Impossible")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Kubernetes utilise un réseau plat sans NAT")

    # Question 9 - Labels
    print("\n9. A quoi servent les labels dans Kubernetes ?")
    print("a) Documentation  b) Sélection d'objets  c) Versioning  d) Sécurité")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les labels permettent de sélectionner des ressources")

    # Question 10 - Volumes
    print("\n10. Quel type de volume partage des données entre conteneurs d'un même Pod ?")
    print("a) hostPath  b) persistentVolumeClaim  c) emptyDir  d) configMap")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) emptyDir est partagé entre conteneurs du Pod")

    # Question 11 - API Server
    print("\n11. Quel port utilise l'API Server Kubernetes par défaut ?")
    print("a) 8080  b) 6443  c) 8443  d) 9090")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 6443 est le port HTTPS standard de l'API Server")

    # Question 12 - Deployment strategy
    print("\n12. Quelle stratégie de déploiement évite les downtimes ?")
    print("a) Recreate  b) RollingUpdate  c) BlueGreen  d) Canary")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) RollingUpdate remplace progressivement les Pods")

    # Question 13 - ConfigMaps
    print("\n13. Les ConfigMaps peuvent stocker quels types de données ?")
    print("a) Données sensibles  b) Configuration non-sensible  c) Images  d) Certificats")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ConfigMaps pour configuration non-sensible uniquement")

    # Question 14 - Probes
    print("\n14. Quelle probe détermine si un Pod peut recevoir du trafic ?")
    print("a) livenessProbe  b) readinessProbe  c) startupProbe  d) healthProbe")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) readinessProbe contrôle l'ajout aux endpoints")

    # Question 15 - Resources
    print("\n15. Quelle différence entre requests et limits pour les ressources ?")
    print("a) Aucune  b) Requests=minimum, Limits=maximum  c) Requests=maximum  d) Limits=minimum")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Requests garantissent, Limits limitent les ressources")

    # Question 16 - Scheduler
    print("\n16. Le Scheduler Kubernetes place les Pods sur les nodes selon :")
    print("a) L'ordre  b) Resources disponibles  c) Le hasard  d) L'alphabet")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Le Scheduler optimise selon les ressources et contraintes")

    # Question 17 - Kubelet
    print("\n17. Kubelet s'exécute sur :")
    print("a) Master seulement  b) Workers seulement  c) Tous les nodes  d) Pods seulement")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Kubelet est l'agent présent sur tous les nodes")

    # Question 18 - Container Runtime
    print("\n18. Quel container runtime Kubernetes utilise-t-il par défaut ?")
    print("a) Docker  b) containerd  c) CRI-O  d) rkt")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) containerd est le runtime par défaut depuis v1.20")

    # Question 19 - DNS
    print("\n19. Comment un Pod accède-t-il à un Service nommé 'api' dans le même namespace ?")
    print("a) api  b) api.default  c) api.svc.cluster.local  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Toutes les formes de FQDN fonctionnent")

    # Question 20 - Annotations
    print("\n20. Les annotations Kubernetes servent à :")
    print("a) Sélectionner des objets  b) Stocker métadonnées  c) Router le trafic  d) Authentifier")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Annotations stockent des métadonnées non-sélectives")

    # Question 21 - Taints et Tolerations
    print("\n21. Les taints s'appliquent sur :")
    print("a) Pods  b) Nodes  c) Services  d) Namespaces")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les taints sont appliqués sur les nodes")

    # Question 22 - Controller Manager
    print("\n22. Le Controller Manager exécute :")
    print("a) Les Pods  b) Les boucles de contrôle  c) L'API  d) Le Scheduler")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Il maintient l'état désiré via des boucles de contrôle")

    # Question 23 - Ports
    print("\n23. Dans un Pod, targetPort fait référence au port :")
    print("a) Du Service  b) Du Node  c) Du conteneur  d) Du cluster")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) targetPort est le port d'écoute du conteneur")

    # Question 24 - Minikube
    print("\n24. Minikube est utilisé pour :")
    print("a) Production  b) Développement local  c) Cloud  d) Monitoring")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Minikube crée un cluster local pour développement")

    # Question 25 - Kube-proxy
    print("\n25. Kube-proxy gère :")
    print("a) L'authentification  b) Le load balancing  c) Le stockage  d) Les images")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Kube-proxy implémente le load balancing des Services")

    # Résultats finaux
    print("\n" + "=" * 60)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les concepts de base de Kubernetes")
        print("Vous pouvez passer au Quiz 2 - Niveau Intermédiaire")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Architecture Kubernetes (Control Plane et Worker Nodes)")
            print("- Concepts de base (Pods, Services, Namespaces)")
        elif score < 15:
            print("- Networking et DNS Kubernetes")
            print("- Manifests YAML et kubectl")
        else:
            print("- Configuration avancée et ressources")
            print("- Probes et gestion du cycle de vie")
        print("Recommandation: Refaire les LABs 1-5 et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Basics - Concepts de Base")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 1 - Kubernetes Basics")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 2 - Objets et manifests intermédiaires")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")