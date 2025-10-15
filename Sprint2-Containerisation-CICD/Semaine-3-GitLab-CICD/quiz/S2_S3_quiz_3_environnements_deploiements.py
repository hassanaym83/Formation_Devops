#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz 3 - Validation des acquis
Environnements et Déploiements GitLab CI/CD

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 2 - Semaine 3 - GitLab CI/CD
"""

def run_quiz():
    """Execute le quiz de validation des environnements et déploiements GitLab CI/CD"""
    
    print("=" * 65)
    print(" QUIZ ENVIRONNEMENTS ET DÉPLOIEMENTS GITLAB")
    print(" 15 questions - Seuil de validation: 72%")
    print("=" * 65)
    
    score = 0
    total_questions = 15
    
    # Question 1 - Définition environnement
    print("\n1. Dans GitLab CI/CD, un environnement représente :")
    print("a) Une machine virtuelle")
    print("b) Une configuration de déploiement nommée")
    print("c) Un type de runner")
    print("d) Un fichier de configuration")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Environnement = configuration de déploiement avec nom et URL")
    
    # Question 2 - Mot-clé environment
    print("\n2. Pour déclarer un environnement dans un job, on utilise :")
    print("a) deploy_to:")
    print("b) environment:")
    print("c) env:")
    print("d) target:")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) environment: avec name et url")
    
    # Question 3 - Types d'environnements
    print("\n3. Quels sont les environnements standards dans un workflow DevOps ?")
    print("a) dev, test, prod")
    print("b) development, staging, production")
    print("c) build, deploy, monitor")
    print("d) local, remote, cloud")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Development, Staging, Production (workflow standard)")
    
    # Question 4 - Environment URL
    print("\n4. L'URL d'environnement permet de :")
    print("a) Configurer le déploiement")
    print("b) Accéder directement à l'application déployée")
    print("c) Télécharger les logs")
    print("d) Gérer les permissions")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) URL fournit accès direct à l'app via interface GitLab")
    
    # Question 5 - Action stop
    print("\n5. L'action 'stop' d'un environnement permet de :")
    print("a) Arrêter le pipeline")
    print("b) Supprimer l'environnement et ses ressources")
    print("c) Mettre en pause le déploiement")
    print("d) Redémarrer l'application")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Stop permet cleanup des ressources d'environnement")
    
    # Question 6 - Review Apps
    print("\n6. Les Review Apps sont :")
    print("a) Des applications de révision de code")
    print("b) Des environnements temporaires pour chaque merge request")
    print("c) Des outils de test automatisé")
    print("d) Des tableaux de bord de monitoring")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Review Apps = environnements éphémères par MR")
    
    # Question 7 - Déploiement automatique
    print("\n7. Pour un déploiement automatique en production, on utilise généralement :")
    print("a) when: manual")
    print("b) when: always")
    print("c) when: on_success avec rules")
    print("d) when: delayed")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) on_success avec rules pour branches spécifiques")
    
    # Question 8 - Stratégies de déploiement
    print("\n8. La stratégie Blue-Green deployment consiste à :")
    print("a) Utiliser des codes couleur")
    print("b) Maintenir deux environnements identiques")
    print("c) Déployer par phases")
    print("d) Tester en parallèle")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Deux env identiques, switch instantané entre versions")
    
    # Question 9 - Canary deployment
    print("\n9. Le Canary deployment permet de :")
    print("a) Tester avec un échantillon d'utilisateurs")
    print("b) Déployer uniquement la nuit")
    print("c) Utiliser des containers jaunes")
    print("d) Automatiser les tests")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Exposition progressive nouvelle version à % utilisateurs")
    
    # Question 10 - Rolling deployment
    print("\n10. Le Rolling deployment :")
    print("a) Remplace toutes les instances simultanément")
    print("b) Met à jour les instances une par une")
    print("c) Crée de nouvelles instances")
    print("d) Sauvegarde puis restaure")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Mise à jour progressive instance par instance")
    
    # Question 11 - Environment variables deployment
    print("\n11. Les variables d'environnement pour le déploiement incluent :")
    print("a) CI_ENVIRONMENT_NAME")
    print("b) CI_ENVIRONMENT_URL")
    print("c) CI_ENVIRONMENT_SLUG")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Plusieurs variables automatiques pour environnements")
    
    # Question 12 - Environments protection
    print("\n12. La protection d'environnement peut inclure :")
    print("a) Restriction par utilisateurs/groupes")
    print("b) Restriction par horaires")
    print("c) Approbations requises")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Protections multiples disponibles (utilisateurs, horaires, approbations)")
    
    # Question 13 - Deployment boards
    print("\n13. Les Deployment boards montrent :")
    print("a) L'état des pods Kubernetes")
    print("b) Les métriques de performance")
    print("c) Les logs d'application")
    print("d) Les configurations réseau")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) État temps réel des pods/instances dans Kubernetes")
    
    # Question 14 - GitOps workflow
    print("\n14. Dans un workflow GitOps, les déploiements sont déclenchés par :")
    print("a) Des commandes manuelles")
    print("b) Des webhooks externes")
    print("c) Des commits sur le repository de configuration")
    print("d) Des timers automatiques")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) GitOps = déploiements via commits sur repo config")
    
    # Question 15 - Rollback
    print("\n15. Pour effectuer un rollback rapide, on peut utiliser :")
    print("a) Re-run du pipeline précédent")
    print("b) Redéploiement de la version antérieure")
    print("c) Les deux approches sont valides")
    print("d) Restauration depuis backup")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Re-run ou redéploiement selon contexte et stratégie")
    
    # Résultats finaux
    print("\n" + "=" * 65)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 65)
    
    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    
    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les environnements et déploiements GitLab CI/CD")
        print("Vous pouvez passer au Quiz 4 : Optimisation et Performance")
        
        if percentage >= 95:
            print("EXCELLENCE - Expertise en déploiement confirmée!")
        elif percentage >= 85:
            print("TRÈS BIEN - Solide compréhension des déploiements!")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        
        if score < 5:
            print("- Concepts d'environnements GitLab")
            print("- Configuration environment avec name/url")
        if score < 8:
            print("- Types d'environnements (dev/staging/prod)")
            print("- Review Apps et environnements temporaires")
        if score < 11:
            print("- Stratégies de déploiement (Blue-Green, Canary, Rolling)")
            print("- Variables d'environnement automatiques")
        if score < 13:
            print("- Protection d'environnements")
            print("- GitOps et workflows avancés")
        
        print("Recommandation: Revoir LABs 7-8 sur déploiements, puis repasser le quiz")
    
    # Concepts clés à retenir
    print(f"\n{'-'*65}")
    print("CONCEPTS CLÉS À RETENIR:")
    print(f"{'-'*65}")
    print("Environnements: Configuration avec name/url, protection")
    print("Types: Development, Staging, Production, Review Apps")
    print("Stratégies: Blue-Green, Canary, Rolling deployment")
    print("Variables: CI_ENVIRONMENT_NAME/URL/SLUG automatiques")
    print("Protection: Restrictions utilisateurs, horaires, approbations")
    print("GitOps: Déploiements déclaratifs via commits config")
    
    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz 3 - Environnements et Déploiements GitLab CI/CD")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 2 - Semaine 3 - GitLab CI/CD")
    print("\nAssurez-vous d'avoir étudié le cours et fait les LABs 7-8")
    print("Durée recommandée: 15 minutes maximum")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    passed = run_quiz()
    
    print(f"\n{'='*65}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Quiz 4 - Optimisation et Performance")
    else:
        print("Direction: Révision des environnements et nouvelle tentative")
    print(f"{'='*65}")