"""
Quiz Séance 1 - Validation des acquis
Linux Fondamentaux pour DevOps

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 1
"""

def run_quiz():
    """Execute le quiz de validation des fondamentaux Linux"""

    print("=" * 60)
    print("    QUIZ LINUX FONDAMENTAUX")
    print("    15 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 15

    # Question 1 - Navigation système
    print("\n1. Quelle commande permet d'afficher le répertoire de travail actuel ?")
    print("a) ls -la    b) pwd    c) cd .    d) whoami")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) pwd (Print Working Directory)")

    # Question 2 - Hiérarchie FHS
    print("\n2. Dans quel répertoire FHS trouve-t-on les fichiers de configuration système ?")
    print("a) /home    b) /var    c) /etc    d) /tmp")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) /etc contient les fichiers de configuration")

    # Question 3 - Permissions
    print("\n3. Que signifie la permission 755 en notation octale ?")
    print("a) rwxr-xr-x    b) rwxrwxrwx    c) rw-r--r--    d) rwx------")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) 755 = rwxr-xr-x (propriétaire: tout, groupe/autres: lecture+exécution)")

    # Question 4 - Commandes de base
    print("\n4. Quelle commande permet de créer un répertoire ?")
    print("a) touch    b) mkdir    c) cp    d) mv")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) mkdir (make directory)")

    # Question 5 - Affichage de fichiers
    print("\n5. Quelle commande affiche le contenu d'un fichier page par page ?")
    print("a) cat    b) head    c) tail    d) less")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) less permet la navigation page par page")

    # Question 6 - Processus
    print("\n6. Quelle commande affiche tous les processus en cours ?")
    print("a) ps aux    b) ls -la    c) top    d) who")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) ps aux affiche tous les processus avec détails")

    # Question 7 - Variables d'environnement
    print("\n7. Comment afficher la valeur de la variable PATH ?")
    print("a) $PATH    b) echo $PATH    c) path    d) show PATH")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) echo $PATH affiche le contenu de la variable")

    # Question 8 - Redirection
    print("\n8. Que fait la commande 'ls > fichier.txt' ?")
    print("a) Affiche le contenu de fichier.txt    b) Redirige la sortie de ls vers fichier.txt")
    print("c) Copie ls dans fichier.txt    d) Supprime fichier.txt")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) > redirige la sortie standard vers un fichier")

    # Question 9 - Recherche
    print("\n9. Quelle commande permet de rechercher un fichier par nom ?")
    print("a) grep    b) find    c) locate    d) search")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) find permet de rechercher des fichiers/dossiers")

    # Question 10 - Archives
    print("\n10. Quelle commande crée une archive tar.gz ?")
    print("a) tar -czf archive.tar.gz dossier/    b) zip archive.zip dossier/")
    print("c) gzip dossier/    d) compress dossier/")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) tar -czf crée une archive compressée")

    # Question 11 - Propriétés de fichiers
    print("\n11. Quelle commande change le propriétaire d'un fichier ?")
    print("a) chmod    b) chown    c) chgrp    d) usermod")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) chown (change owner)")

    # Question 12 - Liens
    print("\n12. Quelle différence entre un lien dur et un lien symbolique ?")
    print("a) Aucune différence    b) Le lien dur pointe vers l'inode, le symbolique vers le chemin")
    print("c) Le lien symbolique est plus rapide    d) Le lien dur ne fonctionne que sur ext4")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Lien dur = même inode, lien symbolique = référence au chemin")

    # Question 13 - Espace disque
    print("\n13. Quelle commande affiche l'espace disque utilisé par répertoire ?")
    print("a) df -h    b) du -h    c) free -h    d) fdisk -l")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) du -h (disk usage) affiche l'utilisation par répertoire")

    # Question 14 - Historique des commandes
    print("\n14. Comment exécuter la dernière commande commençant par 'git' ?")
    print("a) !git    b) history git    c) !!git    d) last git")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) !git recherche et exécute la dernière commande commençant par 'git'")

    # Question 15 - Texte et filtres
    print("\n15. Quelle commande compte le nombre de lignes dans un fichier ?")
    print("a) wc -l fichier    b) count fichier    c) lines fichier    d) nl fichier")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) wc -l (word count -lines)")

    # Résultats finaux
    print("\n" + "=" * 60)
    print("              RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les fondamentaux Linux pour DevOps")
        print("Vous pouvez passer à la séance suivante")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 5:
            print("- Navigation et structure FHS")
            print("- Commandes de base (ls, cd, pwd, mkdir)")
        if score < 8:
            print("- Permissions et propriétés de fichiers")
            print("- Redirection et pipes")
        if score < 11:
            print("- Processus et variables d'environnement")
            print("- Archives et recherche de fichiers")
        print("Recommandation: Refaire les LABs et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Linux Fondamentaux")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 1 - Semaine 1 - Séance 1")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 2 - Gestion des Processus et Services")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")