"""
Quiz 4 - Performance et Concepts Avancés
HPA, VPA, Cluster Autoscaler, Disaster Recovery et Optimisation

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 25 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 3 - Kubernetes Production
"""

def run_quiz():
    """Execute le quiz de validation des concepts Performance et Avancés"""

    print("=" * 70)
    print(" QUIZ KUBERNETES PRODUCTION - PERFORMANCE ET CONCEPTS AVANCÉS")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 70)

    score = 0
    total_questions = 25

    # Question 1 - HPA
    print("\n1. HPA (Horizontal Pod Autoscaler) scale automatiquement :")
    print("a) Le nombre de nodes  b) Le nombre de pods")
    print("c) La taille des volumes  d) La bande passante")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) HPA ajuste le nombre de pods basé sur les métriques")

    # Question 2 - VPA
    print("\n2. VPA (Vertical Pod Autoscaler) ajuste :")
    print("a) Le nombre de pods  b) Les requests/limits CPU/Memory")
    print("c) Le nombre de nodes  d) La configuration réseau")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) VPA ajuste les ressources CPU/Memory des pods")

    # Question 3 - Cluster Autoscaler
    print("\n3. Cluster Autoscaler gère :")
    print("a) Les pods  b) Les services  c) Les nodes du cluster  d) Les volumes")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Cluster Autoscaler ajoute/supprime des nodes automatiquement")

    # Question 4 - Resource requests
    print("\n4. Les resource requests définissent :")
    print("a) Les ressources garanties  b) Les limites maximales")
    print("c) Les ressources recommandées  d) Les ressources par défaut")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Requests = ressources garanties pour le pod")

    # Question 5 - Resource limits
    print("\n5. Les resource limits définissent :")
    print("a) Les ressources minimales  b) Les ressources maximales")
    print("c) Les ressources moyennes  d) Les ressources recommandées")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Limits = plafond maximal de ressources")

    # Question 6 - QoS Classes
    print("\n6. Les classes QoS Kubernetes sont :")
    print("a) Guaranteed, Burstable, BestEffort  b) High, Medium, Low")
    print("c) Premium, Standard, Basic  d) Critical, Important, Normal")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) QoS: Guaranteed, Burstable, BestEffort")

    # Question 7 - Node Affinity
    print("\n7. Node Affinity permet de :")
    print("a) Contrôler où les pods sont schedulés")
    print("b) Gérer la bande passante  c) Configurer le stockage  d) Définir les services")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Node Affinity contraint le placement des pods")

    # Question 8 - Pod Disruption Budget
    print("\n8. Pod Disruption Budget (PDB) assure :")
    print("a) Le budget des pods  b) La disponibilité minimale pendant les maintenances")
    print("c) La performance  d) La sécurité")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) PDB maintient un minimum de pods disponibles")

    # Question 9 - Taints et Tolerations
    print("\n9. Taints et Tolerations permettent de :")
    print("a) Repousser certains pods des nodes")
    print("b) Améliorer les performances  c) Gérer le stockage  d) Configurer le réseau")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Taints repoussent les pods sans tolerations correspondantes")

    # Question 10 - Velero
    print("\n10. Velero est utilisé pour :")
    print("a) Monitoring  b) Backup et restore de cluster")
    print("c) Load balancing  d) Autoscaling")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Velero sauvegarde et restaure les ressources Kubernetes")

    # Question 11 - ETCD backup
    print("\n11. Sauvegarder etcd nécessite :")
    print("a) kubectl backup  b) etcdctl snapshot save")
    print("c) helm backup  d) docker backup")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) etcdctl snapshot save crée une sauvegarde etcd")

    # Question 12 - Network Policies performance
    print("\n12. Les Network Policies peuvent impacter :")
    print("a) La performance réseau  b) L'utilisation CPU")
    print("c) La latence  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Les Network Policies ont un coût en performance")

    # Question 13 - Resource Quotas
    print("\n13. Resource Quotas limitent :")
    print("a) Les ressources par namespace  b) Les ressources par pod")
    print("c) Les ressources par node  d) Les ressources par cluster")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Resource Quotas s'appliquent au niveau namespace")

    # Question 14 - Persistent Volume performance
    print("\n14. Pour optimiser les performances de stockage :")
    print("a) Utiliser SSD  b) Choisir la bonne StorageClass")
    print("c) Optimiser l'IOPS  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Plusieurs facteurs influencent les performances de stockage")

    # Question 15 - Container Image optimization
    print("\n15. Pour optimiser les images de containers :")
    print("a) Utiliser des images multi-stage  b) Minimiser les layers")
    print("c) Utiliser des images de base légères  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Toutes ces pratiques optimisent les images")

    # Question 16 - Kubernetes Scheduler
    print("\n16. Le scheduler Kubernetes peut être customisé via :")
    print("a) Scheduler Profiles  b) Scheduling Policies")
    print("c) Custom Schedulers  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Plusieurs méthodes de customisation du scheduler existent")

    # Question 17 - Multi-cluster management
    print("\n17. Pour gérer plusieurs clusters Kubernetes :")
    print("a) Kubectl contexts  b) Cluster API")
    print("c) Service mesh  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Plusieurs approches pour le multi-cluster management")

    # Question 18 - Probes optimization
    print("\n18. Pour optimiser les health checks :")
    print("a) Ajuster les timeouts  b) Utiliser des probes légères")
    print("c) Configurer les intervalles  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Toutes ces pratiques optimisent les probes")

    # Question 19 - Disaster Recovery strategy
    print("\n19. Une stratégie DR complète inclut :")
    print("a) Backup des données  b) Réplication multi-région")
    print("c) Tests de restore  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) DR nécessite une approche holistique")

    # Question 20 - Service Mesh benefits
    print("\n20. Un Service Mesh apporte :")
    print("a) Observabilité  b) Sécurité  c) Traffic management  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Service Mesh améliore observabilité, sécurité et gestion traffic")

    # Question 21 - Cost optimization
    print("\n21. Pour optimiser les coûts Kubernetes :")
    print("a) Right-sizing des ressources  b) Spot instances")
    print("c) Scaling automatique  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Plusieurs stratégies d'optimisation des coûts")

    # Question 22 - Chaos Engineering
    print("\n22. Chaos Engineering permet de :")
    print("a) Créer du chaos  b) Tester la résilience du système")
    print("c) Améliorer les performances  d) Gérer les déploiements")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Chaos Engineering teste la résilience par injection de pannes")

    # Question 23 - Custom Resource Definitions
    print("\n23. Les CRDs permettent de :")
    print("a) Créer de nouveaux types de ressources")
    print("b) Customiser les pods  c) Modifier l'API  d) Gérer les nodes")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) CRDs étendent l'API Kubernetes avec nouveaux types")

    # Question 24 - Admission Controllers
    print("\n24. Les Admission Controllers peuvent :")
    print("a) Valider les ressources  b) Muter les ressources")
    print("c) Refuser des créations  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Admission Controllers valident, mutent et contrôlent les ressources")

    # Question 25 - Production readiness
    print("\n25. Un cluster production-ready nécessite :")
    print("a) Monitoring complet  b) Backup/Restore testé")
    print("c) Sécurité renforcée  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Production readiness = monitoring + backup + sécurité + performance")

    # Résultats finaux
    print("\n" + "=" * 70)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 70)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les concepts avancés et la performance Kubernetes")
        print("Félicitations! Vous avez complété tous les quizzes de cette semaine")
        print("Vous êtes prêt pour les défis production Kubernetes!")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Concepts de base: HPA, VPA, Cluster Autoscaler")
            print("- Resource management et QoS")
        elif score < 15:
            print("- Optimisation des performances et placement des pods")
            print("- Strategies de backup et disaster recovery")
        else:
            print("- Concepts avancés: Service Mesh, Chaos Engineering")
            print("- Production readiness et cost optimization")
        print("Recommandation: Refaire les LABs 8-10 et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Production - Performance et Concepts Avancés")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 3 - Kubernetes Production")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*70}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Félicitations! Formation Kubernetes Production complétée!")
        print("Vous êtes maintenant prêt pour la production Kubernetes")
    else:
        print("Direction: Révision LABs 8-10 et nouvelle tentative")
    print(f"{'='*70}")