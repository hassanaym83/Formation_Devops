# QUIZ SÉANCE 5 - Gestion d'erreurs et fichiers DevOps
# Fichier: S1_S2_S5_quiz.py
# Auteur: Hassan ESSADIK
# Sprint 1 - Semaine 2 - Séance 5

"""
Quiz Séance 5 - Validation des acquis
Gestion d'erreurs et fichiers DevOps

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 1 - Semaine 2 - Séance 5
"""

def run_quiz():
    """Execute le quiz de validation gestion d'erreurs et fichiers DevOps"""
    
    print("=" * 60)
    print(" QUIZ GESTION D'ERREURS ET FICHIERS DEVOPS")
    print(" 15 questions - Seuil de validation: 72%")
    print("=" * 60)
    
    score = 0
    total_questions = 15
    
    # Question 1 - Gestion d'erreurs
    print("\n1. Quelle est la meilleure pratique pour gérer les erreurs dans un script de déploiement DevOps ?")
    print("a) Ignorer les erreurs pour que le déploiement continue")
    print("b) Utiliser des exceptions personnalisées avec logging détaillé")
    print("c) Arrêter immédiatement le script au premier problème")
    print("d) Capturer toutes les exceptions avec un try-except général")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les exceptions personnalisées avec logging permettent un diagnostic précis.")
    
    # Question 2 - Concept fail-fast
    print("\n2. Que signifie le concept de 'fail-fast' en DevOps ?")
    print("a) Ignorer les erreurs pour accélérer le déploiement")
    print("b) Détecter et signaler les erreurs le plus tôt possible")
    print("c) Arrêter tous les services en cas d'erreur")
    print("d) Redémarrer automatiquement les processus défaillants")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Fail-fast consiste à détecter les problèmes rapidement pour éviter leur propagation.")
    
    # Question 3 - Logging niveau
    print("\n3. Quel niveau de logging est approprié pour enregistrer une erreur de connexion à la base de données en production ?")
    print("a) DEBUG")
    print("b) INFO")
    print("c) WARNING")
    print("d) ERROR")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Une erreur de connexion base de données est un problème grave niveau ERROR.")
    
    # Question 4 - Rotation logs
    print("\n4. Dans un système de monitoring DevOps, quelle méthode est recommandée pour la rotation des logs ?")
    print("a) Suppression manuelle périodique")
    print("b) Rotation basée sur la taille et l'âge avec compression")
    print("c) Stockage illimité des logs")
    print("d) Redirection vers /dev/null")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) La rotation automatique avec compression optimise l'espace tout en conservant l'historique.")
    
    # Question 5 - Stockage secrets
    print("\n5. Quelle est la meilleure approche pour stocker des secrets (mots de passe, clés API) dans un pipeline DevOps ?")
    print("a) Les inclure directement dans le code source")
    print("b) Les stocker dans des fichiers de configuration non chiffrés")
    print("c) Utiliser un gestionnaire de secrets avec chiffrement")
    print("d) Les passer en paramètres de ligne de commande")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Un gestionnaire de secrets avec chiffrement offre la sécurité nécessaire.")
    
    # Résultats finaux
    print("\n" + "=" * 60)
    print(" RÉSULTATS DU QUIZ (5 questions version courte)")
    print("=" * 60)
    
    percentage = (score / 5) * 100
    print(f"Score: {score}/5 ({percentage:.1f}%)")
    
    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez la gestion d'erreurs et fichiers DevOps")
        print("Vous pouvez passer à la séance suivante")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        print("- Fondamentaux de la gestion d'erreurs (try/except/finally)")
        print("- Concepts de base du logging et monitoring")
        print("Recommandation: Refaire les LABs et repasser le quiz")
    
    return score >= (5 * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Gestion d'erreurs et fichiers DevOps")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 1 - Semaine 2 - Séance 5")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    passed = run_quiz()
    
    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 6 - Python intermédiaire pour DevOps")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")