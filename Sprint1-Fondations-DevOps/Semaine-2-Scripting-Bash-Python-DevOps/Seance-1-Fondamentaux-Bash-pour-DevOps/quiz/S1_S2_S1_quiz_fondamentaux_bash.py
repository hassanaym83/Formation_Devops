#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz Séance 1 - Validation des acquis
Fondamentaux Bash pour DevOps

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 1 - Semaine 2 - Séance 1
"""

def run_quiz():
    """Execute le quiz de validation des fondamentaux Bash"""

    print("=" * 60)
    print("    QUIZ FONDAMENTAUX BASH DEVOPS")
    print("    15 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 15

    # Question 1 - Shebang et structure de base
    print("\n1. Quelle ligne doit être la première d'un script Bash ?")
    print("a) # Script Bash    b) #!/bin/bash    c) echo 'debut'    d) bash script")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Le shebang #!/bin/bash indique l'interpréteur à utiliser")

    # Question 2 - Variables
    print("\n2. Comment déclare-t-on une variable locale en Bash ?")
    print("a) $var=valeur    b) var=valeur    c) set var=valeur    d) declare $var=valeur")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) En Bash: nom_variable=valeur (sans espaces autour du =)")

    # Question 3 - Paramètres positionnels
    print("\n3. Dans un script, que contient la variable $1 ?")
    print("a) Le nom du script    b) Le premier paramètre    c) Nombre d'arguments    d) Tous les arguments")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) $1 contient le premier argument passé au script")

    # Question 4 - Tests de fichiers
    print("\n4. Quel opérateur teste l'existence d'un fichier régulier ?")
    print("a) -d    b) -e    c) -f    d) -r")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) L'opérateur -f teste l'existence d'un fichier régulier")

    # Question 5 - Conditions
    print("\n5. Quelle syntaxe est recommandée pour les tests en Bash moderne ?")
    print("a) if test    b) if [ ]    c) if [[ ]]    d) if command")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) [[ ]] est la syntaxe moderne recommandée en Bash")

    # Question 6 - Boucles for
    print("\n6. Comment parcourt-on tous les éléments d'un tableau 'services' ?")
    print('a) for i in services    b) for i in ${services}    c) for i in "${services[@]}"    d) for i in $services')
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print('Incorrect. Réponse: c) "${services[@]}" expanse tous les éléments du tableau')

    # Question 7 - Boucles while
    print("\n7. Une boucle while s'exécute tant que la condition est :")
    print("a) Fausse    b) Vraie    c) Nulle    d) Non définie")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) while continue tant que la condition est vraie")

    # Question 8 - Variables d'environnement
    print("\n8. Quelle variable contient le nom de l'utilisateur actuel ?")
    print("a) $HOME    b) $USER    c) $PWD    d) $SHELL")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) $USER contient le nom de l'utilisateur connecté")

    # Question 9 - Commandes système
    print("\n9. Quelle commande affiche l'espace disque disponible ?")
    print("a) du    b) df    c) free    d) ls")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) df affiche l'espace disque des systèmes de fichiers")

    # Question 10 - Redirection
    print("\n10. Que fait la redirection '>/dev/null 2>&1' ?")
    print("a) Affiche tout    b) Masque la sortie et les erreurs    c) Affiche erreurs seulement    d) Sauvegarde dans un fichier")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Redirige stdout et stderr vers /dev/null (masque tout)")

    # Question 11 - Comparaisons numériques
    print("\n11. Quel opérateur teste si un nombre est supérieur à un autre ?")
    print("a) -gt    b) -lt    c) -eq    d) -ne")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) -gt signifie 'greater than' (supérieur à)")

    # Question 12 - Exit codes
    print("\n12. Quel code de retour indique le succès d'une commande ?")
    print("a) 1    b) 0    c) -1    d) 255")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Le code 0 indique le succès, tout autre code indique une erreur")

    # Question 13 - Substitution de commande
    print("\n13. Comment capture-t-on le résultat d'une commande dans une variable ?")
    print("a) var=`commande`    b) var=$(commande)    c) var=commande    d) Les réponses a et b")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Backticks ` et $() fonctionnent, mais $() est recommandé")

    # Question 14 - Tests de chaînes
    print("\n14. Comment teste-t-on qu'une chaîne n'est pas vide ?")
    print("a) [[ -z $var ]]    b) [[ -n $var ]]    c) [[ $var ]]    d) Les réponses b et c")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) -n teste non-vide, et [[ $var ]] teste aussi non-vide")

    # Question 15 - Bonnes pratiques DevOps
    print("\n15. Dans quel contexte DevOps utilise-t-on principalement les scripts Bash ?")
    print("a) Développement web    b) Automation infrastructure    c) Bases de données    d) Interface graphique")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Bash est essentiel pour l'automation d'infrastructure DevOps")

    # Résultats finaux
    print("\n" + "=" * 60)
    print("              RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les fondamentaux Bash pour DevOps")
        print("Vous pouvez passer à la séance suivante : Bash Intermédiaire")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 5:
            print("- Structure de base des scripts (shebang, variables, commentaires)")
        if score < 8:
            print("- Structures de contrôle (conditions if/else)")
        if score < 11:
            print("- Structures répétitives (boucles for/while)")
        if score < 13:
            print("- Commandes système et administration")
        print("Recommandation: Refaire les LABs 1-4 et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Fondamentaux Bash pour DevOps")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 1 - Semaine 2 - Séance 1")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 2 - Bash Scripting Intermédiaire")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")