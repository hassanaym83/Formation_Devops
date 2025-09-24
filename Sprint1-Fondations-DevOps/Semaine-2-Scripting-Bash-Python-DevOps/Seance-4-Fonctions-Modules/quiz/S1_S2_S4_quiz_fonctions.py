"""
Quiz Séance 4 - Validation des acquis
Fonctions et Modules Python pour DevOps

15 questions - 1 point par question - 15 points total
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 1 - Semaine 2 - Séance 4
Framework Hassan : Quiz conforme sans icônes interdites
"""

def run_quiz():
    """Execute le quiz de validation des fonctions et modules Python DevOps"""
    
    print("=" * 70)
    print("         QUIZ FONCTIONS ET MODULES PYTHON DEVOPS")
    print("    15 questions - Seuil de validation: 11/15 (72%)")
    print("=" * 70)
    
    score = 0
    total_questions = 15
    questions_missed = []
    
    # Question 1 - Définition fonction de base
    print("\n1. Comment définir une fonction Python pour script DevOps?")
    print("   a) function monitor_cpu():")
    print("   b) def monitor_cpu():")
    print("   c) func monitor_cpu():")
    print("   d) define monitor_cpu():")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: b) def monitor_cpu():")
        questions_missed.append(1)
    
    # Question 2 - Return dans contexte DevOps
    print("\n2. Que fait 'return' dans une fonction de monitoring?")
    print("   a) Affiche les métriques")
    print("   b) Retourne les données collectées")
    print("   c) Arrête le monitoring")
    print("   d) Crée un log")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: b) Retourne les données collectées")
        questions_missed.append(2)
    
    # Question 3 - Paramètres par défaut DevOps
    print("\n3. Dans 'def deploy(app, env='prod', replicas=1)', que signifie env='prod'?")
    print("   a) Variable globale")
    print("   b) Paramètre obligatoire")
    print("   c) Paramètre avec valeur par défaut")
    print("   d) Erreur de syntaxe")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'c':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: c) Paramètre avec valeur par défaut")
        questions_missed.append(3)
    
    # Question 4 - Appel fonction sans paramètres
    print("\n4. Comment appeler une fonction 'check_system_health()' sans paramètres?")
    print("   a) check_system_health")
    print("   b) check_system_health()")
    print("   c) call check_system_health")
    print("   d) run check_system_health()")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: b) check_system_health()")
        questions_missed.append(4)
    
    # Question 5 - Import module datetime
    print("\n5. Comment importer le module 'datetime' pour logs DevOps?")
    print("   a) import datetime")
    print("   b) from datetime")
    print("   c) include datetime")
    print("   d) load datetime")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'a':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: a) import datetime")
        questions_missed.append(5)
    
    # Question 6 - Import spécifique pour simulation
    print("\n6. Comment importer seulement 'randint' du module 'random'?")
    print("   a) import random.randint")
    print("   b) from random import randint")
    print("   c) import randint from random")
    print("   d) get randint from random")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: b) from random import randint")
        questions_missed.append(6)
    
    # Question 7 - Module pour timestamps
    print("\n7. Quel module Python est essentiel pour timestamps dans logs DevOps?")
    print("   a) time")
    print("   b) datetime")
    print("   c) clock")
    print("   d) calendar")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: b) datetime")
        questions_missed.append(7)
    
    # Question 8 - Module os pour système
    print("\n8. Le module 'os' en DevOps permet de:")
    print("   a) Calculer des métriques")
    print("   b) Interagir avec le système d'exploitation")
    print("   c) Générer des nombres aléatoires")
    print("   d) Gérer les dates uniquement")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: b) Interagir avec le système d'exploitation")
        questions_missed.append(8)
    
    # Question 9 - Fonction avec multiples paramètres
    print("\n9. Comment définir une fonction avec 2 paramètres en DevOps?")
    print("   a) def configure_server(name, ip):")
    print("   b) def configure_server(name) (ip):")
    print("   c) def configure_server[name, ip]:")
    print("   d) def configure_server{name, ip}:")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'a':
        score += 1
        print("   ✓ Correct!")
    else:
        print("   ✗ Incorrect. Réponse: a) def configure_server(name, ip):")
        questions_missed.append(9)
    
    # Question 10 - Organisation imports
    print("\n10. Où placer les imports dans un script DevOps Python?")
    print("    a) À la fin du fichier")
    print("    b) Au début du fichier")
    print("    c) Partout dans le code")
    print("    d) Après les fonctions principales")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    ✓ Correct!")
    else:
        print("    ✗ Incorrect. Réponse: b) Au début du fichier")
        questions_missed.append(10)
    
    # Question 11 - Main guard
    print("\n11. À quoi sert 'if __name__ == \"__main__\":' dans scripts DevOps?")
    print("    a) Teste le nom du fichier")
    print("    b) Exécute le code seulement si script lancé directement")
    print("    c) Importe le module principal")
    print("    d) Génère une erreur de syntaxe")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    ✓ Correct!")
    else:
        print("    ✗ Incorrect. Réponse: b) Exécute le code seulement si script lancé directement")
        questions_missed.append(11)
    
    # Question 12 - Docstrings DevOps
    print("\n12. À quoi servent les docstrings (\"\"\") dans fonctions DevOps?")
    print("    a) Commentaires temporaires")
    print("    b) Documentation des fonctions")
    print("    c) Variables de configuration")
    print("    d) Tests automatiques")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    ✓ Correct!")
    else:
        print("    ✗ Incorrect. Réponse: b) Documentation des fonctions")
        questions_missed.append(12)
    
    # Question 13 - Valeurs de retour multiples
    print("\n13. Comment retourner CPU et mémoire depuis une fonction?")
    print("    a) return cpu, memory")
    print("    b) return cpu; return memory")
    print("    c) return [cpu] [memory]")
    print("    d) return cpu + memory")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'a':
        score += 1
        print("    ✓ Correct!")
    else:
        print("    ✗ Incorrect. Réponse: a) return cpu, memory")
        questions_missed.append(13)
    
    # Question 14 - Module random pour tests
    print("\n14. Pourquoi utiliser le module 'random' en DevOps?")
    print("    a) Pour la sécurité")
    print("    b) Pour simuler des métriques de test")
    print("    c) Pour les calculs mathématiques")
    print("    d) Pour les dates aléatoires")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    ✓ Correct!")
    else:
        print("    ✗ Incorrect. Réponse: b) Pour simuler des métriques de test")
        questions_missed.append(14)
    
    # Question 15 - Avantages fonctions DevOps
    print("\n15. Pourquoi organiser le code DevOps en fonctions?")
    print("    a) C'est plus joli visuellement")
    print("    b) Réutilisabilité et maintenance du code")
    print("    c) Execution plus rapide")
    print("    d) Obligatoire en Python")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    ✓ Correct!")
    else:
        print("    ✗ Incorrect. Réponse: b) Réutilisabilité et maintenance du code")
        questions_missed.append(15)
    
    # Résultats finaux
    print("\n" + "=" * 70)
    print("                    RÉSULTATS DU QUIZ")
    print("=" * 70)
    
    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    print(f"Seuil de validation: 11/15 (72%)")
    
    if percentage >= 72:
        print("\n🎉 VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les fonctions et modules Python pour DevOps")
        print("✅ DIRECTION: Séance 5 - Gestion d'erreurs et fichiers")
        validation_status = "RÉUSSIE"
    else:
        print("\n❌ VALIDATION ÉCHOUÉE")
        print("Score insuffisant pour passer à la séance suivante")
        print("\nConcepts à réviser selon votre score:")
        
        if score < 6:
            print("📚 PRIORITÉ CRITIQUE - Revoir les bases:")
            print("   • Syntaxe des fonctions (def, return)")
            print("   • Appel de fonctions et paramètres")
            print("   • Concepts fondamentaux Python")
        
        if score < 10:
            print("📚 PRIORITÉ ÉLEVÉE - Renforcer:")
            print("   • Paramètres avec valeurs par défaut")
            print("   • Import et utilisation des modules")
            print("   • Organisation du code")
        
        if score < 13:
            print("📚 RÉVISION CIBLÉE:")
            print("   • Modules datetime, random, os")
            print("   • Docstrings et documentation")
            print("   • Bonnes pratiques DevOps")
        
        print("\n🔄 RECOMMANDATION:")
        print("   1. Réviser les concepts identifiés")
        print("   2. Refaire les LABs 1, 2, 3")
        print("   3. Repasser le quiz")
        validation_status = "ÉCHOUÉE"
    
    # Détail des erreurs si échec
    if questions_missed and len(questions_missed) > 3:
        print(f"\nQuestions manquées: {', '.join(map(str, questions_missed))}")
    
    print("\n" + "=" * 70)
    
    return score >= (total_questions * 0.72), score, percentage, validation_status

def generate_quiz_report(passed, score, percentage, status):
    """Génère un rapport détaillé du quiz"""
    from datetime import datetime
    
    report = f"""
RAPPORT DE QUIZ - SÉANCE 4
=====================================================
Étudiant: [À compléter]
Formateur: Hassan ESSADIK
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Séance: Sprint 1 - Semaine 2 - Séance 4

RÉSULTATS:
- Score: {score}/15 ({percentage:.1f}%)
- Statut: {status}
- Seuil requis: 11/15 (72%)

VALIDATION: {"✅ RÉUSSIE" if passed else "❌ ÉCHOUÉE"}

PROCHAINE ÉTAPE:
{f"Séance 5 - Gestion d'erreurs et fichiers" if passed else "Révision et nouvelle tentative"}

COMMENTAIRES FORMATEUR:
{f"Excellente maîtrise des concepts. Prêt pour la suite." if percentage >= 85 else
 f"Bonne compréhension générale. Quelques révisions recommandées." if passed else
 f"Révision nécessaire avant de continuer."}

Framework Hassan - Validation conforme
"""
    return report

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Fonctions et Modules Python DevOps")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 1 - Semaine 2 - Séance 4")
    print("Framework Hassan - Version conforme")
    
    print("\nCe quiz couvre tous les concepts de la séance:")
    print(" • Définition et appel de fonctions")
    print(" • Paramètres obligatoires et par défaut")
    print(" • Valeurs de retour et documentation")
    print(" • Modules standards (datetime, random, os)")
    print(" • Organisation et bonnes pratiques")
    
    print(f"\nConditions:")
    print(f" • 15 questions - 1 point chacune")
    print(f" • Durée maximum: 15 minutes")
    print(f" • Seuil validation: 11/15 (72%)")
    
    input("\nAppuyez sur Entrée pour commencer le quiz...")
    
    passed, score, percentage, status = run_quiz()
    
    # Génération du rapport
    report = generate_quiz_report(passed, score, percentage, status)
    
    # Sauvegarde du rapport
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quiz_S4_rapport_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nRapport sauvegardé: {filename}")
    except:
        print("\nImpossible de sauvegarder le rapport")
    
    print(f"\n{'='*70}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("🎯 Direction: Séance 5 - Gestion d'erreurs et fichiers")
    else:
        print("🔄 Direction: Révision et nouvelle tentative")
    print(f"{'='*70}")