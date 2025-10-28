"""
Quiz 3 - Validation des acquis Kubernetes Basics
Orchestration et production niveau avancé

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 25 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 1 - Kubernetes Basics
"""

def run_quiz():
    """Execute le quiz de validation de l'orchestration Kubernetes avancée"""

    print("=" * 60)
    print(" QUIZ KUBERNETES BASICS - NIVEAU AVANCÉ")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - DaemonSets
    print("\n1. DaemonSet garantit qu'un Pod s'exécute sur :")
    print("a) Un seul node  b) Tous les nodes  c) Master nodes seulement  d) Worker nodes seulement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) DaemonSet déploie un Pod sur chaque node du cluster")

    # Question 2 - StatefulSets
    print("\n2. StatefulSet garantit :")
    print("a) Identité réseau stable  b) Stockage persistant  c) Ordre de déploiement  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) StatefulSet garantit identité, persistance et ordre")

    # Question 3 - Jobs vs CronJobs
    print("\n3. CronJob diffère de Job par :")
    print("a) Persistance  b) Planification temporelle  c) Parallélisme  d) Stockage")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) CronJob ajoute la planification cron à Job")

    # Question 4 - HPA (Horizontal Pod Autoscaler)
    print("\n4. HPA scale basé sur :")
    print("a) CPU/Memory seulement  b) Métriques personnalisées seulement  c) Les deux  d) Temps")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) HPA peut utiliser métriques système et personnalisées")

    # Question 5 - Network Policies
    print("\n5. NetworkPolicy par défaut :")
    print("a) Bloque tout  b) Autorise tout  c) Dépend du CNI  d) Aucune règle")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Sans NetworkPolicy, tout trafic est autorisé")

    # Question 6 - Security Contexts
    print("\n6. SecurityContext au niveau Pod vs Container :")
    print("a) Pod override Container  b) Container override Pod  c) Aucune différence  d) Erreur")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) SecurityContext Container override celui du Pod")

    # Question 7 - RBAC
    print("\n7. Dans RBAC, ClusterRole diffère de Role par :")
    print("a) Permissions  b) Portée (cluster vs namespace)  c) Utilisateurs  d) Durée")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ClusterRole s'applique à tout le cluster")

    # Question 8 - Service Mesh concepts
    print("\n8. Service Mesh apporte principalement :")
    print("a) Performance  b) Observabilité et sécurité réseau  c) Stockage  d) Scheduling")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Service mesh gère observabilité, sécurité et trafic")

    # Question 9 - Taints et Tolerations
    print("\n9. Taint sur un node :")
    print("a) Attire les Pods  b) Repousse les Pods sans toleration  c) Supprime les Pods  d) Aucun effet")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Taint repousse les Pods sans toleration correspondante")

    # Question 10 - Custom Resources
    print("\n10. CRD (Custom Resource Definition) permet de :")
    print("a) Étendre l'API Kubernetes  b) Créer de nouveaux types d'objets  c) Les deux  d) Modifier les Pods")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) CRD étend l'API en créant de nouveaux types")

    # Question 11 - Operators
    print("\n11. Un Operator Kubernetes :")
    print("a) Gère seulement le déploiement  b) Encode la logique opérationnelle  c) Remplace kubectl  d) Surveille seulement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Operator encode la logique opérationnelle humaine")

    # Question 12 - Pod Disruption Budgets
    print("\n12. PodDisruptionBudget (PDB) contrôle :")
    print("a) Création de Pods  b) Interruptions volontaires  c) Performance  d) Stockage")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) PDB limite les interruptions volontaires (maintenance)")

    # Question 13 - Admission Controllers
    print("\n13. Admission Controllers interviennent :")
    print("a) Avant authentification  b) Après authentification, avant persistance  c) Après persistance  d) Pendant l'exécution")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Admission controllers valident/mutent avant stockage")

    # Question 14 - Multi-tenancy
    print("\n14. Pour isoler des équipes, meilleure approche :")
    print("a) Clusters séparés  b) Namespaces + RBAC + NetworkPolicy  c) Nodes dédiés  d) Pods séparés")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Namespaces + RBAC + NetworkPolicy pour multi-tenancy")

    # Question 15 - Helm Charts
    print("\n15. Helm Charts permettent :")
    print("a) Packaging d'applications  b) Templating de manifests  c) Versioning de releases  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Helm gère packaging, templating et versioning")

    # Question 16 - Monitoring stack
    print("\n16. Stack de monitoring standard Kubernetes :")
    print("a) ELK  b) Prometheus + Grafana  c) Nagios  d) Zabbix")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Prometheus + Grafana est le standard pour Kubernetes")

    # Question 17 - Resource Limits vs Requests
    print("\n17. Si CPU request > CPU limit :")
    print("a) Pod accepté  b) Pod rejeté  c) Warning seulement  d) Valeur corrigée")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Request ne peut pas être > limit, Pod rejeté")

    # Question 18 - Container runtimes
    print("\n18. CRI (Container Runtime Interface) standardise :")
    print("a) Images  b) Communication kubelet-runtime  c) Réseaux  d) Stockage")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) CRI standardise l'interface kubelet-container runtime")

    # Question 19 - Disaster Recovery
    print("\n19. Pour backup/restore etcd :")
    print("a) kubectl backup  b) etcdctl snapshot  c) helm backup  d) docker export")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) etcdctl snapshot save/restore pour backup etcd")

    # Question 20 - Cluster upgrades
    print("\n20. Stratégie recommandée pour upgrade cluster :")
    print("a) Upgrade tout simultanément  b) Upgrade master puis workers  c) Upgrade workers puis master  d) Rolling upgrade")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Upgrade master nodes avant worker nodes")

    # Question 21 - Service Account
    print("\n21. Service Account est utilisé par :")
    print("a) Utilisateurs humains  b) Pods/applications  c) Administrateurs  d) Outils externes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ServiceAccount pour l'identité des Pods")

    # Question 22 - CNI (Container Network Interface)
    print("\n22. CNI gère :")
    print("a) Storage  b) Networking des conteneurs  c) Security  d) Scheduling")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) CNI standardise le networking des conteneurs")

    # Question 23 - Resource contention
    print("\n23. Si un Pod dépasse memory limits :")
    print("a) Throttling  b) OOMKilled  c) Warning  d) Migration")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Dépassement memory limits = Pod tué (OOMKilled)")

    # Question 24 - GitOps principles
    print("\n24. GitOps utilise Git comme :")
    print("a) Stockage code  b) Source de vérité pour infrastructure  c) Backup  d) CI/CD")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) GitOps : Git comme source de vérité pour l'état désiré")

    # Question 25 - Production readiness
    print("\n25. Pour production Kubernetes, essentiel :")
    print("a) Monitoring + Backup + Security  b) Interface graphique  c) Développeurs admin  d) Cluster mono-node")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Production nécessite monitoring, backup et sécurité")

    # Résultats finaux
    print("\n" + "=" * 60)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez l'orchestration et les concepts avancés Kubernetes")
        print("Vous pouvez passer au Quiz 4 - Intégration et Synthèse")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- StatefulSets et DaemonSets")
            print("- RBAC et Security Contexts")
        elif score < 15:
            print("- Network Policies et Service Mesh")
            print("- HPA et Resource Management")
        else:
            print("- Operators et Custom Resources")
            print("- Production readiness et GitOps")
        print("Recommandation: Refaire les LABs 7-10 et approfondir la documentation")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Basics - Niveau Avancé")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 1 - Kubernetes Basics")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 4 - Intégration et synthèse finale")
    else:
        print("Direction: Révision approfondie et nouvelle tentative")
    print(f"{'='*60}")