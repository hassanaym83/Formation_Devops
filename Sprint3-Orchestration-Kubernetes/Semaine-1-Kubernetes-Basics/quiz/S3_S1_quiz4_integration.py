"""
Quiz 4 - Validation des acquis Kubernetes Basics
Intégration et synthèse finale

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 30 minutes

Formateur: Hassan ESSADIK | Sprint 3 - Semaine 1 - Kubernetes Basics
"""

def run_quiz():
    """Execute le quiz final d'intégration Kubernetes"""

    print("=" * 60)
    print(" QUIZ KUBERNETES BASICS - INTÉGRATION FINALE")
    print(" 25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - Architecture complète
    print("\n1. Dans une architecture 3-tiers sur Kubernetes, ordre recommandé des Services :")
    print("a) Frontend->Backend->Database  b) Database->Backend->Frontend  c) Simultané  d) Backend->Frontend->Database")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Frontend expose Backend qui accède Database")

    # Question 2 - Choix de workload
    print("\n2. Pour une base de données, quel workload choisir ?")
    print("a) Deployment  b) DaemonSet  c) StatefulSet  d) Job")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) StatefulSet pour données persistantes et identité stable")

    # Question 3 - Debugging production
    print("\n3. Pod en CrashLoopBackOff, première action :")
    print("a) kubectl delete pod  b) kubectl logs  c) kubectl scale --replicas=0  d) kubectl restart")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) kubectl logs pour comprendre la cause du crash")

    # Question 4 - Configuration management
    print("\n4. Séparer config de l'application, meilleure pratique :")
    print("a) Variables dans image  b) ConfigMaps + Secrets  c) Annotations  d) Labels")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ConfigMaps (config) + Secrets (données sensibles)")

    # Question 5 - Exposer application web
    print("\n5. Exposer une app web avec SSL terminaison :")
    print("a) NodePort + SSL dans app  b) LoadBalancer + certificats externes  c) Ingress + TLS  d) ClusterIP seulement")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Ingress gère SSL/TLS terminaison et routing")

    # Question 6 - Health checks stratégie
    print("\n6. Stratégie complète health checks :")
    print("a) liveness seulement  b) readiness seulement  c) liveness + readiness  d) liveness + readiness + startup")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Trio complet : startup, liveness, readiness")

    # Question 7 - Gestion des ressources
    print("\n7. Production : relation requests/limits recommandée :")
    print("a) requests = limits  b) requests < limits  c) pas de limits  d) requests > limits")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) requests < limits permet burst tout en garantissant minimum")

    # Question 8 - Rolling update stratégie
    print("\n8. Zero-downtime deployment, paramètres optimaux :")
    print("a) maxUnavailable=0, maxSurge=1  b) maxUnavailable=100%, maxSurge=0  c) Les deux  d) Aucun")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) maxUnavailable=0 garantit zéro interruption")

    # Question 9 - Monitoring intégré
    print("\n9. Métriques natives exposées par Kubernetes :")
    print("a) Prometheus format  b) /metrics endpoint  c) cAdvisor integration  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) K8s expose métriques Prometheus via /metrics")

    # Question 10 - Sécurité multicouche
    print("\n10. Sécurité defense-in-depth Kubernetes :")
    print("a) RBAC seulement  b) NetworkPolicy seulement  c) RBAC + NetworkPolicy + SecurityContext  d) Firewall externe")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Sécurité multicouche : RBAC + Network + Container")

    # Question 11 - Persistence patterns
    print("\n11. Pattern de persistance pour applications stateless :")
    print("a) PVC par Pod  b) Shared PVC  c) emptyDir  d) hostPath")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Applications stateless peuvent partager stockage")

    # Question 12 - Service discovery pattern
    print("\n12. Communication inter-services recommandée :")
    print("a) IP addresses  b) Service DNS names  c) NodePort  d) hostNetwork")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) DNS names des Services pour découverte automatique")

    # Question 13 - Troubleshooting réseau
    print("\n13. Pod ne peut pas joindre Service, vérifier :")
    print("a) Labels selector  b) Endpoints  c) DNS resolution  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Vérifier labels, endpoints et DNS pour networking")

    # Question 14 - Backup strategy
    print("\n14. Sauvegarde complète cluster Kubernetes :")
    print("a) etcd snapshot seulement  b) PVC backup seulement  c) etcd + PVC + configs  d) Docker images")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Backup complet : etcd + données + configurations")

    # Question 15 - Scaling patterns
    print("\n15. Auto-scaling complet d'une application :")
    print("a) HPA seulement  b) VPA seulement  c) HPA + VPA  d) Manual scaling")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) HPA (horizontal) + VPA (vertical) pour scaling optimal")

    # Question 16 - CI/CD integration
    print("\n16. Deploy depuis CI/CD, méthode recommandée :")
    print("a) kubectl apply direct  b) Helm charts  c) GitOps (ArgoCD/Flux)  d) Scripts manuels")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) GitOps pour déploiements déclaratifs et auditable")

    # Question 17 - Multi-environment
    print("\n17. Gérer dev/staging/prod sur même cluster :")
    print("a) Namespaces séparés  b) ResourceQuota  c) NetworkPolicy  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Isolation complète : namespaces + quota + network")

    # Question 18 - Performance optimization
    print("\n18. Optimiser performance Pods :")
    print("a) Resource limits élevées  b) Node affinity appropriée  c) QoS classe Guaranteed  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Performance : resources + placement + QoS")

    # Question 19 - Observability stack
    print("\n19. Stack observabilité complète :")
    print("a) Logs seulement  b) Metrics seulement  c) Traces seulement  d) Logs + Metrics + Traces")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Observabilité = trois piliers : logs, metrics, traces")

    # Question 20 - Disaster recovery
    print("\n20. RTO/RPO pour application critique :")
    print("a) Ignorer  b) Multi-AZ deployment  c) Cross-region replication  d) Dépend des besoins")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) DR strategy dépend des objectifs métier RTO/RPO")

    # Question 21 - Security scanning
    print("\n21. Sécuriser images conteneurs :")
    print("a) Scanner vulnérabilités  b) Images minimales  c) Non-root user  d) Toutes les réponses")
    backup = input("Réponse: ").lower()
    if backup == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Sécurité images : scan + minimal + non-root")

    # Question 22 - Cost optimization
    print("\n22. Optimiser coûts Kubernetes :")
    print("a) Right-sizing resources  b) Spot instances  c) Resource cleanup  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Cost optimization : sizing + instances + cleanup")

    # Question 23 - Compliance
    print("\n23. Audit et compliance Kubernetes :")
    print("a) Audit logs  b) RBAC policies  c) Security policies  d) Toutes les réponses")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Compliance : audit + RBAC + security policies")

    # Question 24 - Migration strategy
    print("\n24. Migrer app legacy vers Kubernetes :")
    print("a) Lift-and-shift direct  b) Containerisation d'abord  c) Refactoring complet  d) Étapes progressives")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Migration progressive : containerisation puis orchestration")

    # Question 25 - Synthèse finale
    print("\n25. Kubernetes apporte principalement :")
    print("a) Containerisation  b) Orchestration et automation  c) Développement  d) Stockage")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Kubernetes = orchestration et automation des conteneurs")

    # Résultats finaux
    print("\n" + "=" * 60)
    print(" RÉSULTATS DU QUIZ FINAL")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("🎓 VALIDATION RÉUSSIE - SEMAINE 1 COMPLÈTE!")
        print("Vous maîtrisez les fondamentaux Kubernetes et leur intégration")
        print("Compétences validées :")
        print("✓ Architecture et composants Kubernetes")
        print("✓ Gestion des workloads et objets")
        print("✓ Networking et services")
        print("✓ Stockage et persistance")
        print("✓ Sécurité et production")
        print("✓ Monitoring et troubleshooting")
        print("✓ Bonnes pratiques DevOps")
        print("\n🚀 Vous êtes prêt pour la Semaine 2 - Applications Kubernetes")
    else:
        print("❌ VALIDATION ÉCHOUÉE")
        print("Score insuffisant pour valider la semaine")
        print("Plan de remédiation :")
        if score < 10:
            print("📚 Révision complète nécessaire")
            print("- Reprendre le cours depuis le début")
            print("- Refaire tous les LABs avec attention")
            print("- Repasser les 4 quiz progressivement")
        elif score < 18:
            print("🔄 Révision ciblée recommandée")
            print("- Approfondir les concepts avancés")
            print("- Refaire LABs 7-10 avec corrections")
            print("- Étudier patterns de production")
        else:
            print("🎯 Révision finale")
            print("- Réviser intégration et synthèse")
            print("- Pratiquer troubleshooting")
            print("- Nouvelle tentative possible")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Kubernetes Basics - Intégration Finale")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 3 - Semaine 1 - Kubernetes Basics")
    print("\n" + "="*60)
    print("QUIZ FINAL DE VALIDATION")
    print("Ce quiz synthétise tous les concepts de la semaine")
    print("Réussite = maîtrise complète des fondamentaux K8s")
    print("="*60)
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du parcours Semaine 1 - Kubernetes Basics")
    if passed:
        print("🎉 FÉLICITATIONS - Objectifs atteints!")
        print("Direction: Sprint 3 - Semaine 2 - Applications Kubernetes")
    else:
        print("📖 Révision nécessaire avant progression")
        print("Consultez le plan de remédiation ci-dessus")
    print(f"{'='*60}")