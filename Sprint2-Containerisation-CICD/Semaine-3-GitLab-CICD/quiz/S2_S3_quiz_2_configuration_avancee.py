#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz 2 - Validation des acquis
Configuration Avancée et Variables GitLab CI/CD

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 2 - Semaine 3 - GitLab CI/CD
"""

def run_quiz():
    """Execute le quiz de validation de la configuration avancée GitLab CI/CD"""
    
    print("=" * 65)
    print(" QUIZ CONFIGURATION AVANCÉE ET VARIABLES GITLAB")
    print(" 15 questions - Seuil de validation: 72%")
    print("=" * 65)
    
    score = 0
    total_questions = 15
    
    # Question 1 - Variables d'environnement
    print("\n1. Où peut-on définir des variables d'environnement dans GitLab CI/CD ? (Plusieurs réponses possibles)")
    print("a) Dans .gitlab-ci.yml uniquement")
    print("b) Dans l'interface GitLab (Settings > CI/CD)")
    print("c) Au niveau du job dans le fichier YAML")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Variables définissables à plusieurs niveaux")
    
    # Question 2 - Priorité des variables
    print("\n2. Quel est l'ordre de priorité des variables (de la plus haute à la plus basse) ?")
    print("a) Trigger > Job > Global > Group > Instance")
    print("b) Job > Trigger > Global > Group > Instance")
    print("c) Global > Job > Group > Trigger > Instance")
    print("d) Instance > Group > Global > Job > Trigger")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Trigger variables ont la priorité la plus haute")
    
    # Question 3 - Variables protégées
    print("\n3. Les variables 'Protected' ne sont disponibles que pour :")
    print("a) Les branches protégées")
    print("b) Les utilisateurs maintainers")
    print("c) Les pipelines manuels")
    print("d) Les jobs de déploiement")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Variables Protected limitées aux branches protégées")
    
    # Question 4 - Variables masquées
    print("\n4. Les variables 'Masked' sont :")
    print("a) Cryptées dans la base de données")
    print("b) Cachées dans les logs des jobs")
    print("c) Inaccessibles aux développeurs")
    print("d) Supprimées après utilisation")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Variables Masked masquées automatiquement dans les logs")
    
    # Question 5 - Include external
    print("\n5. Le mot-clé 'include' permet de :")
    print("a) Importer des fichiers de configuration externes")
    print("b) Inclure des dépendances")
    print("c) Ajouter des utilisateurs au projet")
    print("d) Intégrer des webhooks")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Include importe des fichiers .yml externes")
    
    # Question 6 - Types d'include
    print("\n6. Combien de types d'include existe-t-il dans GitLab CI ?")
    print("a) 3 types")
    print("b) 4 types")
    print("c) 5 types")
    print("d) 6 types")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 4 types (local, remote, template, project)")
    
    # Question 7 - Extends keyword
    print("\n7. Le mot-clé 'extends' permet de :")
    print("a) Étendre la durée d'exécution")
    print("b) Hériter de la configuration d'un autre job")
    print("c) Ajouter des runners")
    print("d) Créer des branches")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Extends permet l'héritage de configuration entre jobs")
    
    # Question 8 - Job templates
    print("\n8. Un job template (commençant par un point) est :")
    print("a) Exécuté automatiquement")
    print("b) Un job caché non exécuté directement")
    print("c) Un job de test")
    print("d) Un job d'erreur")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Jobs cachés (.job-name) pour héritage, non exécutés")
    
    # Question 9 - Rules vs only/except
    print("\n9. Les 'rules' remplacent 'only/except' et permettent :")
    print("a) Une logique conditionnelle plus complexe")
    print("b) Une meilleure performance")
    print("c) Plus de sécurité")
    print("d) Une syntaxe plus simple")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Rules offrent des conditions plus flexibles et complexes")
    
    # Question 10 - When conditions
    print("\n10. Dans les rules, 'when: manual' signifie :")
    print("a) Le job s'exécute automatiquement")
    print("b) Le job nécessite une intervention manuelle")
    print("c) Le job s'exécute seulement en cas d'erreur")
    print("d) Le job est désactivé")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Manual requiert déclenchement manuel par utilisateur")
    
    # Question 11 - Needs keyword
    print("\n11. Le mot-clé 'needs' permet de :")
    print("a) Définir les ressources nécessaires")
    print("b) Créer des dépendances entre jobs")
    print("c) Spécifier les permissions")
    print("d) Configurer les notifications")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Needs crée dépendances explicites entre jobs")
    
    # Question 12 - Parallel jobs
    print("\n12. 'parallel: 3' dans un job signifie :")
    print("a) Le job s'exécute 3 fois séquentiellement")
    print("b) Le job utilise 3 runners")
    print("c) Le job crée 3 instances parallèles")
    print("d) Le job a 3 tentatives")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Parallel crée plusieurs instances du même job")
    
    # Question 13 - Matrix builds
    print("\n13. Les matrix builds permettent de :")
    print("a) Tester différentes combinaisons de variables")
    print("b) Créer des matrices de permissions")
    print("c) Organiser les jobs visuellement")
    print("d) Calculer des métriques")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Matrix teste toutes combinaisons de variables définies")
    
    # Question 14 - Retry mechanism
    print("\n14. Le retry automatique d'un job peut être configuré avec :")
    print("a) retry: max: 2")
    print("b) retry: 2")
    print("c) Les deux syntaxes sont valides")
    print("d) retry: count: 2")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Syntaxe simple (retry: 2) et complexe (retry: max: 2)")
    
    # Question 15 - Resource group
    print("\n15. Les 'resource_group' permettent de :")
    print("a) Grouper les ressources système")
    print("b) Limiter l'exécution simultanée de jobs")
    print("c) Organiser les runners")
    print("d) Gérer les quotas")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Resource groups évitent exécution simultanée sur même environnement")
    
    # Résultats finaux
    print("\n" + "=" * 65)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 65)
    
    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    
    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez la configuration avancée GitLab CI/CD")
        print("Vous pouvez passer au Quiz 3 : Environnements et Déploiements")
        
        if percentage >= 95:
            print("EXCELLENCE - Expertise confirmée!")
        elif percentage >= 85:
            print("TRÈS BIEN - Solide maîtrise des concepts avancés!")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        
        if score < 5:
            print("- Variables d'environnement et priorités")
            print("- Variables protégées et masquées")
        if score < 8:
            print("- Include et extends")
            print("- Job templates et héritage")
        if score < 11:
            print("- Rules et conditions avancées")
            print("- Needs et dépendances")
        if score < 13:
            print("- Parallel et matrix builds")
            print("- Resource groups et retry")
        
        print("Recommandation: Revoir LABs 4-6 sur configuration avancée, puis repasser le quiz")
    
    # Concepts clés à retenir
    print(f"\n{'-'*65}")
    print("CONCEPTS CLÉS À RETENIR:")
    print(f"{'-'*65}")
    print("Variables: Priorités, Protected, Masked, niveaux de définition")
    print("Réutilisation: Include (local/remote/template/project), Extends")
    print("Templates: Jobs cachés (.template), héritage de configuration")
    print("Contrôle: Rules (vs only/except), when conditions, needs")
    print("Parallélisme: Parallel jobs, matrix builds")
    print("Ressources: Resource groups, retry, optimisations")
    
    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz 2 - Configuration Avancée et Variables GitLab CI/CD")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 2 - Semaine 3 - GitLab CI/CD")
    print("\nAssurez-vous d'avoir étudié le cours et fait les LABs 4-6")
    print("Durée recommandée: 15 minutes maximum")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    passed = run_quiz()
    
    print(f"\n{'='*65}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 3 - Environnements et Déploiements")
    else:
        print("Direction: Révision de la configuration avancée et nouvelle tentative")
    print(f"{'='*65}")