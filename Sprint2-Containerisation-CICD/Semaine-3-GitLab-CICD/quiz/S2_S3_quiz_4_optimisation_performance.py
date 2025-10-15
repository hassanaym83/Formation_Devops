#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz 4 - Validation des acquis
Optimisation et Performance GitLab CI/CD

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 2 - Semaine 3 - GitLab CI/CD
"""

def run_quiz():
    """Execute le quiz de validation de l'optimisation et performance GitLab CI/CD"""
    
    print("=" * 65)
    print(" QUIZ OPTIMISATION ET PERFORMANCE GITLAB")
    print(" 15 questions - Seuil de validation: 72%")
    print("=" * 65)
    
    score = 0
    total_questions = 15
    
    # Question 1 - Cache intelligent
    print("\n1. Le cache intelligent GitLab utilise :")
    print("a) Les hash des fichiers pour détecter les changements")
    print("b) La date de modification")
    print("c) La taille des fichiers")
    print("d) Le nom des fichiers")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Hash SHA pour détecter changements réels")
    
    # Question 2 - Cache policy
    print("\n2. La policy 'pull-push' pour le cache signifie :")
    print("a) Télécharger seulement")
    print("b) Télécharger et uploader le cache")
    print("c) Uploader seulement")
    print("d) Ignorer le cache")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Pull-push = télécharger en début, uploader en fin")
    
    # Question 3 - Parallelisation jobs
    print("\n3. Pour optimiser la vitesse, on peut paralléliser :")
    print("a) Les jobs d'un même stage")
    print("b) Les tests unitaires")
    print("c) Les builds multi-architectures")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Parallelisation possible à plusieurs niveaux")
    
    # Question 4 - Pipeline DAG
    print("\n4. Le DAG (Directed Acyclic Graph) permet de :")
    print("a) Visualiser les dépendances entre jobs")
    print("b) Optimiser l'ordre d'exécution")
    print("c) Identifier les goulots d'étranglement")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) DAG optimise orchestration et visualisation")
    
    # Question 5 - Docker layer caching
    print("\n5. Le Docker Layer Caching (DLC) améliore les performances en :")
    print("a) Réutilisant les couches Docker identiques")
    print("b) Compressant les images")
    print("c) Supprimant les couches inutiles")
    print("d) Parallelisant les builds")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) DLC réutilise couches inchangées entre builds")
    
    # Question 6 - Shared runners optimization
    print("\n6. Pour optimiser l'utilisation des shared runners :")
    print("a) Utiliser des tags spécifiques")
    print("b) Limiter les jobs concurrents")
    print("c) Préférer les specific runners pour les gros projets")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Stratégies multiples pour optimiser runners")
    
    # Question 7 - Interruptible jobs
    print("\n7. Les jobs 'interruptible' permettent de :")
    print("a) Interrompre automatiquement en cas d'erreur")
    print("b) Annuler les jobs redondants des anciennes pipelines")
    print("c) Limiter la durée d'exécution")
    print("d) Prioriser les jobs importants")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Interruption automatique jobs anciens lors nouveaux commits")
    
    # Question 8 - Artifacts optimization
    print("\n8. Pour optimiser les artifacts :")
    print("a) Définir une expire_in appropriée")
    print("b) Exclure les fichiers temporaires")
    print("c) Compresser si nécessaire")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Optimisation artifacts sur multiple aspects")
    
    # Question 9 - Pipeline efficiency
    print("\n9. L'efficacité d'un pipeline se mesure par :")
    print("a) Le temps total d'exécution")
    print("b) Le taux de succès")
    print("c) La parallélisation effective")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Métriques multiples pour évaluer efficacité")
    
    # Question 10 - Resource monitoring
    print("\n10. Le monitoring des ressources inclut :")
    print("a) CPU/Memory des jobs")
    print("b) Temps d'attente des runners")
    print("c) Utilisation du cache")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Monitoring complet ressources et performances")
    
    # Question 11 - Conditional execution
    print("\n11. L'exécution conditionnelle avec 'changes' permet de :")
    print("a) Exécuter seulement si certains fichiers ont changé")
    print("b) Modifier la configuration dynamiquement")
    print("c) Changer l'ordre des jobs")
    print("d) Adapter les ressources automatiquement")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Changes: exécution selon modifications fichiers spécifiques")
    
    # Question 12 - Pipeline scheduling
    print("\n12. Les pipelines programmés (scheduled) sont utiles pour :")
    print("a) Tests de régression nocturnes")
    print("b) Builds périodiques de sécurité")
    print("c) Maintenance automatisée")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Pipelines programmés pour automatisation périodique")
    
    # Question 13 - Fast feedback
    print("\n13. Pour un feedback rapide, on privilégie :")
    print("a) Tests rapides en premier")
    print("b) Parallélisation des vérifications")
    print("c) Fail-fast strategy")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Stratégies multiples pour feedback rapide")
    
    # Question 14 - Retry strategy
    print("\n14. Une stratégie de retry intelligente inclut :")
    print("a) Retry seulement sur erreurs transitoires")
    print("b) Backoff exponentiel")
    print("c) Limite du nombre de tentatives")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Retry intelligent avec multiples stratégies")
    
    # Question 15 - Performance metrics
    print("\n15. Les métriques clés de performance incluent :")
    print("a) MTTR (Mean Time To Recovery)")
    print("b) Pipeline duration et success rate")
    print("c) Resource utilization efficiency")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Métriques complètes pour suivi performance")
    
    # Résultats finaux
    print("\n" + "=" * 65)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 65)
    
    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    
    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez l'optimisation et la performance GitLab CI/CD")
        print("Félicitations! Vous avez terminé tous les quiz GitLab CI/CD")
        
        if percentage >= 95:
            print("EXCELLENCE - Expertise complète confirmée!")
        elif percentage >= 85:
            print("TRÈS BIEN - Excellente maîtrise de l'optimisation!")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        
        if score < 5:
            print("- Cache intelligent et policies")
            print("- Parallelisation et DAG")
        if score < 8:
            print("- Docker Layer Caching")
            print("- Optimisation des runners")
        if score < 11:
            print("- Jobs interruptibles et artifacts")
            print("- Monitoring des ressources")
        if score < 13:
            print("- Exécution conditionnelle")
            print("- Stratégies de retry et feedback")
        
        print("Recommandation: Revoir LABs 9-10 sur optimisation, puis repasser le quiz")
    
    # Concepts clés à retenir
    print(f"\n{'-'*65}")
    print("CONCEPTS CLÉS À RETENIR:")
    print(f"{'-'*65}")
    print("Cache: Intelligent hashing, policies pull/push/pull-push")
    print("Parallelisation: Jobs, tests, builds multi-arch")
    print("Optimisation: DAG, DLC, runners spécifiques")
    print("Efficacité: Interruptible jobs, artifacts optimisés")
    print("Monitoring: Ressources, métriques performance")
    print("Stratégies: Conditional execution, fast feedback, retry intelligent")
    
    # Message de fin de formation
    print(f"\n{'='*65}")
    print("🎉 FORMATION GITLAB CI/CD TERMINÉE 🎉")
    print("Vous avez acquis les compétences pour :")
    print("- Créer et configurer des pipelines GitLab CI/CD")
    print("- Optimiser les performances et la sécurité")
    print("- Gérer les déploiements multi-environnements")
    print("- Implémenter les meilleures pratiques DevOps")
    print("Prochaine étape : Mise en pratique sur vos projets!")
    print(f"{'='*65}")
    
    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz 4 - Optimisation et Performance GitLab CI/CD")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 2 - Semaine 3 - GitLab CI/CD")
    print("\nAssurez-vous d'avoir étudié le cours et fait les LABs 9-10")
    print("Durée recommandée: 15 minutes maximum")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    passed = run_quiz()
    
    print(f"\n{'='*65}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("🎯 FORMATION GITLAB CI/CD COMPLÉTÉE AVEC SUCCÈS!")
        print("Direction: Application pratique sur projets réels")
    else:
        print("Direction: Révision de l'optimisation et nouvelle tentative")
    print(f"{'='*65}")