"""
Quiz Séance 5 - Validation des acquis
Réseaux - Sécurité et Monitoring

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 5
"""

def run_quiz():
    """Execute le quiz de validation sécurité réseau et monitoring"""

    print("=" * 60)
    print("    QUIZ RÉSEAUX - SÉCURITÉ ET MONITORING")
    print("    15 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 15

    # Question 1 - UFW politique par défaut
    print("\n1. Quelle politique UFW est recommandée pour un serveur de production ?")
    print("a) default allow incoming    b) default deny incoming    c) default reject incoming    d) default drop all")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) default deny incoming applique le principe de moindre privilège")

    # Question 2 - UFW autorisation SSH
    print("\n2. Avant d'activer UFW, que faut-il IMPÉRATIVEMENT faire pour éviter la coupure d'accès ?")
    print("a) Redémarrer le serveur    b) Autoriser SSH    c) Désactiver iptables    d) Configurer le DNS")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Autoriser SSH est critique pour éviter la coupure d'accès distant")

    # Question 3 - SSH sécurisé port
    print("\n3. Pourquoi utiliser un port SSH non-standard (ex: 2222) ?")
    print("a) Performance améliorée    b) Sécurité par obscurité    c) Compatibilité    d) Obligation légale")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Utiliser un port non-standard réduit les scans automatisés")

    # Question 4 - SSH PermitRootLogin
    print("\n4. Que fait la directive 'PermitRootLogin no' dans /etc/ssh/sshd_config ?")
    print("a) Désactive SSH    b) Interdit les connexions root directes    c) Change le port SSH    d) Active les clés SSH")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) PermitRootLogin no interdit les connexions root directes pour la sécurité")

    # Question 5 - Outil ss moderne
    print("\n5. Quel outil moderne remplace netstat pour analyser les connexions réseau ?")
    print("a) tcpdump    b) ss    c) nmap    d) wireshark")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ss est l'outil moderne recommandé pour remplacer netstat")

    # Question 6 - tcpdump capture HTTP
    print("\n6. Quelle commande tcpdump capture uniquement le trafic HTTP ?")
    print("a) tcpdump http    b) tcpdump port 80    c) tcpdump -p 80    d) tcpdump protocol http")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) tcpdump port 80 capture le trafic sur le port HTTP")

    # Question 7 - Logs authentification
    print("\n7. Dans quel fichier trouve-t-on les tentatives de connexion SSH échouées ?")
    print("a) /var/log/syslog    b) /var/log/auth.log    c) /var/log/ssh.log    d) /var/log/security.log")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) /var/log/auth.log contient les logs d'authentification SSH")

    # Question 8 - UFW règles numérotées
    print("\n8. Quelle commande affiche les règles UFW avec leur numéro pour la suppression ?")
    print("a) ufw list    b) ufw status numbered    c) ufw show rules    d) ufw display all")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ufw status numbered affiche les règles avec numérotation")

    # Question 9 - SSH MaxAuthTries
    print("\n9. À quoi sert la directive 'MaxAuthTries 3' dans SSH ?")
    print("a) Limite le nombre d'utilisateurs    b) Limite les tentatives d'authentification")
    print("c) Change le timeout    d) Active l'authentification à facteurs")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) MaxAuthTries limite le nombre de tentatives d'authentification par connexion")

    # Question 10 - fail2ban protection
    print("\n10. À quoi sert fail2ban dans la sécurité SSH ?")
    print("a) Chiffrement des connexions    b) Protection contre les attaques par force brute")
    print("c) Génération de clés SSH    d) Configuration automatique")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) fail2ban protège contre les attaques par force brute en bannissant les IPs")

    # Question 11 - ss connexions établies
    print("\n11. Quelle commande ss affiche uniquement les connexions établies ?")
    print("a) ss -established    b) ss -tu state established    c) ss -connected    d) ss -active")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ss -tu state established filtre les connexions dans l'état established")

    # Question 12 - Monitoring automatisé
    print("\n12. Quel service Linux permet de programmer l'exécution de scripts de monitoring ?")
    print("a) systemd    b) cron    c) NetworkManager    d) ufw")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) cron permet de programmer l'exécution automatique de tâches")

    # Question 13 - UFW logs
    print("\n13. Dans quel fichier UFW enregistre-t-il les connexions bloquées ?")
    print("a) /var/log/ufw.log    b) /var/log/firewall.log    c) /var/log/iptables.log    d) /var/log/blocked.log")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) /var/log/ufw.log contient les logs du pare-feu UFW")

    # Question 14 - SSH ClientAliveInterval
    print("\n14. À quoi sert 'ClientAliveInterval 300' dans la configuration SSH ?")
    print("a) Change le port SSH    b) Déconnecte les sessions inactives après 5 minutes")
    print("c) Limite les utilisateurs    d) Active le chiffrement")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) ClientAliveInterval 300 déconnecte les sessions inactives après 300 secondes")

    # Question 15 - Principe sécurité
    print("\n15. Quel principe de sécurité applique-t-on avec 'ufw default deny incoming' ?")
    print("a) Défense en profondeur    b) Principe de moindre privilège    c) Chiffrement bout en bout    d) Authentification forte")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Le principe de moindre privilège : bloquer par défaut, autoriser seulement le nécessaire")

    # Calcul du résultat
    percentage = (score / total_questions) * 100
    print(f"\n" + "=" * 50)
    print(f"RÉSULTAT FINAL")
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    
    if percentage >= 72:
        print(" VALIDATION RÉUSSIE ! Compétences sécurité réseau et monitoring acquises.")
        print("\nPoints forts démontrés:")
        if score >= 13:
            print("- Maîtrise excellente de la sécurisation UFW")
            print("- Expertise durcissement SSH pour production")  
            print("- Compétences monitoring réseau avancées")
        elif score >= 11:
            print("- Bonne compréhension des pare-feu Linux")
            print("- Configuration SSH sécurisée maîtrisée")
            print("- Bases du monitoring réseau solides")
    else:
        print(" Validation non atteinte. Révision nécessaire.")
        print("\nÀ revoir en priorité:")
        print("- Configuration UFW et politiques de sécurité")
        print("- Durcissement SSH et bonnes pratiques")
        print("- Outils de monitoring (ss, tcpdump)")
        print("- Analyse des logs de sécurité")
    
    print(f"\nSeuil de validation: 72% | Votre score: {percentage:.1f}%")
    return score >= (total_questions * 0.72)

if __name__ == "__main__":
    run_quiz()
