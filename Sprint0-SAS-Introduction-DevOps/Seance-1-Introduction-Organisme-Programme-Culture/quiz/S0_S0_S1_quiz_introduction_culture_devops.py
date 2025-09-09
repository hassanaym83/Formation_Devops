"""
Quiz Séance 1 - Validation des acquis
Introduction DevOps, Culture et Métriques

25 questions - 1 point par question
Seuil de validation : 18/25 (72%)
Durée maximale : 20 minutes

Sprint 0 - Séance 1 - Culture DevOps et Transformation Organisationnelle
"""

def run_quiz():
    """Execute le quiz de validation des concepts DevOps fondamentaux"""

    print("=" * 60)
    print("    QUIZ CULTURE DEVOPS ET TRANSFORMATION")
    print("    25 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 25

    # Question 1 - Définition DevOps
    print("\n1. Que signifie l'acronyme DevOps ?")
    print("a) Development Operations    b) Developer Optimization")
    print("c) Development + Operations    d) Device Operations")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Development + Operations")

    # Question 2 - Contexte historique
    print("\n2. Dans quelle période s'est déroulée la 'guerre Dev vs Ops' ?")
    print("a) 1995-2005    b) 2000-2008    c) 2005-2010    d) 2008-2015")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 2000-2008, période de conflits systémiques")

    # Question 3 - Standish Group
    print("\n3. Selon le rapport Standish CHAOS 2008, quel était le taux d'échec des projets IT ?")
    print("a) 58%    b) 68%    c) 78%    d) 88%")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 68% des projets IT en échec en 2008")

    # Question 4 - Objectif DevOps
    print("\n4. Quel est l'objectif principal de DevOps ?")
    print("a) Réduire les coûts    b) Livrer à haute vélocité avec qualité")
    print("c) Automatiser tout    d) Éliminer les tests")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Livrer applications à haute vélocité avec qualité")

    # Question 5 - Principe CALMS - Culture
    print("\n5. Que représente le 'C' dans l'acronyme CALMS ?")
    print("a) Code    b) Culture    c) Continuous    d) Cloud")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Culture - collaboration et responsabilité partagée")

    # Question 6 - Principe CALMS - Automation
    print("\n6. Que représente le 'A' dans l'acronyme CALMS ?")
    print("a) Agility    b) Automation    c) Architecture    d) Analytics")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Automation - automatisation des tâches répétitives")

    # Question 7 - Principe CALMS - Lean
    print("\n7. Combien de types de gaspillages identifie le principe Lean en DevOps ?")
    print("a) 5 types    b) 6 types    c) 7 types    d) 8 types")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 7 types de gaspillages (Transport, Inventaire, Mouvement, etc.)")

    # Question 8 - Psychological Safety
    print("\n8. Qui a développé le concept de Psychological Safety ?")
    print("a) Gene Kim    b) Amy Edmondson    c) Jez Humble    d) Patrick Debois")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Amy Edmondson (Harvard Business School)")

    # Question 9 - Psychological Safety niveaux
    print("\n9. Combien de niveaux de Psychological Safety existent-ils ?")
    print("a) 3 niveaux    b) 4 niveaux    c) 5 niveaux    d) 6 niveaux")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 4 niveaux (Inclusion, Learner, Contributor, Challenger)")

    # Question 10 - DORA origine
    print("\n10. Que signifie l'acronyme DORA ?")
    print("a) DevOps Research Assessment    b) DevOps Research and Assessment")
    print("c) Development Operations Research    d) DevOps Reliability Assessment")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) DevOps Research and Assessment")

    # Question 11 - Métriques DORA
    print("\n11. Combien de métriques principales compose le framework DORA ?")
    print("a) 3 métriques    b) 4 métriques    c) 5 métriques    d) 6 métriques")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 4 métriques DORA principales")

    # Question 12 - Deployment Frequency Elite
    print("\n12. Pour un niveau 'Elite' DORA, quelle est la fréquence de déploiement ?")
    print("a) Une fois par semaine    b) Une fois par jour")
    print("c) Plusieurs fois par jour    d) Une fois par mois")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Plusieurs fois par jour pour niveau Elite")

    # Question 13 - Lead Time Elite
    print("\n13. Pour un niveau 'Elite' DORA, quel est le Lead Time for Changes ?")
    print("a) < 1 heure    b) 1-24 heures    c) 1-7 jours    d) > 1 semaine")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) < 1 heure pour niveau Elite")

    # Question 14 - Change Failure Rate Elite
    print("\n14. Quel est le seuil 'Elite' pour Change Failure Rate ?")
    print("a) 0-15%    b) 16-30%    c) 31-45%    d) Plus de 45%")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) 0-15% pour niveau Elite")

    # Question 15 - Time to Restore Elite
    print("\n15. Pour un niveau 'Elite' DORA, quel est le Time to Restore Service ?")
    print("a) < 1 heure    b) 1-24 heures    c) 1-7 jours    d) > 1 semaine")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) < 1 heure pour niveau Elite")

    # Question 16 - Infrastructure as Code
    print("\n16. Que signifie Infrastructure as Code (IaC) ?")
    print("a) Code pour infrastructure    b) Gestion infrastructure par code")
    print("c) Infrastructure codée    d) Code d'infrastructure")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Gestion et provisioning infrastructure par code")

    # Question 17 - Continuous Integration
    print("\n17. Qu'est-ce que Continuous Integration (CI) ?")
    print("a) Déploiement continu    b) Fusion fréquente du code avec tests automatisés")
    print("c) Intégration manuelle    d) Tests continus")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Fusion fréquente du code avec builds et tests automatisés")

    # Question 18 - Microservices
    print("\n18. Qu'est-ce qu'une architecture microservices ?")
    print("a) Services très petits    b) Collection de services faiblement couplés")
    print("c) Services microscopiques    d) Services minimaux")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Collection de services faiblement couplés")

    # Question 19 - Site Reliability Engineering
    print("\n19. Que fait un Site Reliability Engineer (SRE) ?")
    print("a) Développe des sites web    b) Applique l'ingénierie logicielle aux opérations")
    print("c) Gère la sécurité    d) Optimise les performances")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Applique principes ingénierie logicielle aux opérations")

    # Question 20 - Team Topologies
    print("\n20. Combien de types d'équipes définit Team Topologies ?")
    print("a) 2 types    b) 3 types    c) 4 types    d) 5 types")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 4 types (Stream-aligned, Platform, Enabling, Complicated-subsystem)")

    # Question 21 - Technical Debt Ratio
    print("\n21. Quel est le seuil recommandé pour Technical Debt Ratio ?")
    print("a) < 3%    b) < 5%    c) < 10%    d) < 15%")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) < 5% selon SonarQube pour performance optimale")

    # Question 22 - Netflix déploiements
    print("\n22. Combien de déploiements par jour effectue Netflix ?")
    print("a) 100+    b) 500+    c) 1000+    d) 5000+")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 1000+ déploiements par jour")

    # Question 23 - Amazon déploiement
    print("\n23. Quelle est la fréquence de déploiement d'Amazon ?")
    print("a) Toutes les minutes    b) Toutes les 11.7 secondes")
    print("c) Toutes les heures    d) Toutes les 30 secondes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Toutes les 11.7 secondes")

    # Question 24 - ROI DevOps
    print("\n24. Quelle amélioration de fréquence de déploiement entre Low et Elite performers ?")
    print("a) 100x    b) 208x    c) 440x    d) 1000x")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 440x amélioration possible")

    # Question 25 - Observabilité
    print("\n25. Qu'est-ce que l'observabilité en DevOps ?")
    print("a) Observer les équipes    b) Comprendre l'état interne par les outputs externes")
    print("c) Surveillance simple    d) Monitoring basique")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Comprendre l'état interne par outputs externes (logs, métriques, traces)")

    # Résultats finaux
    print("\n" + "=" * 60)
    print("              RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les concepts fondamentaux DevOps")
        print("Vous pouvez passer à la séance suivante")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 8:
            print("- Contexte historique et définitions DevOps de base")
            print("- Problématiques traditionnelles Dev vs Ops")
        if score < 15:
            print("- Principes CALMS et culture DevOps")
            print("- Psychological Safety et transformation organisationnelle")
        if score < 20:
            print("- Métriques DORA et mesure de performance")
            print("- Concepts techniques (CI/CD, IaC, microservices)")
        if score < 23:
            print("- Exemples d'entreprises et ROI DevOps")
            print("- Team Topologies et observabilité")
        print("Recommandation: Refaire les LABs et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Culture DevOps et Transformation Organisationnelle")
    print("Sprint 0 - Séance 1")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 2 - Installation Environnement Développement")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")
