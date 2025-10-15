#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz 1 - Validation des acquis
Pipelines et CI/CD Bases avec GitLab

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 2 - Semaine 3 - GitLab CI/CD
"""

def run_quiz():
    """Execute le quiz de validation des bases GitLab CI/CD"""
    
    print("=" * 65)
    print(" QUIZ PIPELINES ET CI/CD BASES GITLAB")
    print(" 15 questions - Seuil de validation: 72%")
    print("=" * 65)
    
    score = 0
    total_questions = 15
    
    # Question 1 - Définition CI
    print("\n1. Que signifie CI dans CI/CD ?")
    print("a) Container Integration")
    print("b) Continuous Integration")
    print("c) Code Integration")
    print("d) Cloud Integration")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Continuous Integration - Intégration Continue")
    
    # Question 2 - Fichier configuration
    print("\n2. Quel fichier configure les pipelines GitLab CI/CD ?")
    print("a) .gitlab.yml")
    print("b) .gitlab-ci.yml")
    print("c) gitlab-pipeline.yml")
    print("d) ci-config.yml")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) .gitlab-ci.yml à la racine du projet")
    
    # Question 3 - Syntaxe YAML
    print("\n3. GitLab CI utilise la syntaxe YAML qui est sensible à l'indentation. (Vrai/Faux)")
    print("a) Vrai")
    print("b) Faux")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Vrai - YAML est très sensible à l'indentation (espaces)")
    
    # Question 4 - Composants pipeline
    print("\n4. Quelle est l'unité de base d'un pipeline GitLab CI/CD ?")
    print("a) Stage")
    print("b) Job")
    print("c) Runner")
    print("d) Script")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Job - unité de base contenant scripts et configuration")
    
    # Question 5 - Stages par défaut
    print("\n5. Combien de stages sont définis par défaut dans GitLab CI ?")
    print("a) 3 stages")
    print("b) 4 stages")
    print("c) 5 stages")
    print("d) 6 stages")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 5 stages (.pre, build, test, deploy, .post)")
    
    # Question 6 - Ordre d'exécution
    print("\n6. Dans un même stage, les jobs s'exécutent :")
    print("a) Séquentiellement dans l'ordre de définition")
    print("b) En parallèle")
    print("c) Selon les dépendances")
    print("d) Aléatoirement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) En parallèle - tous les jobs d'un stage s'exécutent simultanément")
    
    # Question 7 - GitLab Runner
    print("\n7. Qu'est-ce qu'un GitLab Runner ?")
    print("a) Un utilisateur qui exécute les tests")
    print("b) Un agent qui exécute les jobs des pipelines")
    print("c) Un type de job spécial")
    print("d) Un outil de déploiement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Agent logiciel qui exécute les jobs sur différents environnements")
    
    # Question 8 - Types de runners
    print("\n8. Combien de types de runners principaux existe-t-il dans GitLab ?")
    print("a) 2 types")
    print("b) 3 types")
    print("c) 4 types")
    print("d) 5 types")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 3 types (Shared, Group, Specific/Project)")
    
    # Question 9 - Mot-clé script
    print("\n9. Le mot-clé 'script' dans un job est :")
    print("a) Optionnel")
    print("b) Obligatoire")
    print("c) Déprécié")
    print("d) Conditionnel")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Obligatoire - chaque job doit avoir au minimum un script")
    
    # Question 10 - Artifacts
    print("\n10. Les artifacts permettent de :")
    print("a) Stocker temporairement des fichiers entre jobs")
    print("b) Configurer les runners")
    print("c) Définir les variables")
    print("d) Créer des branches")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Partager fichiers/résultats entre jobs et stages")
    
    # Question 11 - Variables prédéfinies
    print("\n11. Quelle variable contient le nom de la branche ou du tag ?")
    print("a) CI_BRANCH_NAME")
    print("b) CI_REF_NAME")
    print("c) CI_COMMIT_REF_NAME")
    print("d) GITLAB_REF_NAME")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) CI_COMMIT_REF_NAME contient le nom de la branche/tag")
    
    # Question 12 - Before_script
    print("\n12. 'before_script' s'exécute :")
    print("a) Avant chaque job du pipeline")
    print("b) Avant chaque stage")
    print("c) Avant le script principal du job")
    print("d) Seulement dans le premier job")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Avant le script principal de chaque job qui le définit")
    
    # Question 13 - Cache
    print("\n13. Le cache GitLab CI permet de :")
    print("a) Stocker définitivement les résultats")
    print("b) Optimiser les performances en gardant des dépendances")
    print("c) Sauvegarder le code source")
    print("d) Créer des backups")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Garde dépendances (node_modules, etc.) entre exécutions")
    
    # Question 14 - Only/except
    print("\n14. Les mots-clés 'only' et 'except' permettent de :")
    print("a) Définir les permissions")
    print("b) Contrôler quand un job s'exécute")
    print("c) Configurer les artifacts")
    print("d) Gérer les erreurs")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Contrôler l'exécution conditionnelle des jobs")
    
    # Question 15 - Statuts pipeline
    print("\n15. Quand un job échoue, quel est le statut du pipeline ?")
    print("a) Pending")
    print("b) Running")
    print("c) Failed")
    print("d) Canceled")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Failed - échec d'un job = échec du pipeline entier")
    
    # Résultats finaux
    print("\n" + "=" * 65)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 65)
    
    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    
    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les bases de GitLab CI/CD")
        print("Vous pouvez passer au Quiz 2 : Configuration Avancée")
        
        if percentage >= 95:
            print("EXCELLENCE - Maîtrise parfaite des concepts de base!")
        elif percentage >= 85:
            print("TRÈS BIEN - Très bonne compréhension!")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        
        if score < 5:
            print("- Concepts fondamentaux CI/CD")
            print("- Structure et syntaxe YAML")
        if score < 8:
            print("- Components pipeline (jobs, stages, scripts)")
            print("- GitLab Runners et types")
        if score < 11:
            print("- Artifacts et cache")
            print("- Variables prédéfinies")
        if score < 13:
            print("- Contrôle d'exécution (only/except)")
            print("- Statuts et gestion d'erreurs")
        
        print("Recommandation: Revoir LABs 1-3 et concepts de base, puis repasser le quiz")
    
    # Concepts clés à retenir
    print(f"\n{'-'*65}")
    print("CONCEPTS CLÉS À RETENIR:")
    print(f"{'-'*65}")
    print("Configuration: .gitlab-ci.yml, syntaxe YAML, indentation")
    print("Structure: Jobs (unité de base), Stages (5 par défaut), Scripts")
    print("Exécution: Parallèle dans stage, séquentiel entre stages")
    print("Runners: Shared, Group, Specific - agents d'exécution")
    print("Partage: Artifacts (fichiers), Cache (dépendances)")
    print("Contrôle: only/except, variables, before_script, after_script")
    
    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz 1 - Pipelines et CI/CD Bases avec GitLab")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 2 - Semaine 3 - GitLab CI/CD")
    print("\nAssurez-vous d'avoir étudié le cours et fait les LABs 1-3")
    print("Durée recommandée: 15 minutes maximum")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    passed = run_quiz()
    
    print(f"\n{'='*65}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 2 - Configuration Avancée et Variables")
    else:
        print("Direction: Révision des concepts de base et nouvelle tentative")
    print(f"{'='*65}")