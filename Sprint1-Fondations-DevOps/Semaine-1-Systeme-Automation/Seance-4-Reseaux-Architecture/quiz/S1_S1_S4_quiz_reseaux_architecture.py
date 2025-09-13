"""
Quiz Séance 4 - Validation des acquis
Réseaux Architecture

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 4
"""

def run_quiz():
    """Execute le quiz de validation des concepts réseaux architecture"""

    print("=" * 60)
    print("    QUIZ RESEAUX ARCHITECTURE")
    print("    15 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 15

    # Question 1 - Concept adresse IP
    print("\n1. Qu'est-ce qu'une adresse IP ?")
    print("a) Un identifiant unique pour chaque machine sur un réseau")
    print("b) Un protocole de routage")
    print("c) Un type de câble réseau")
    print("d) Un logiciel de sécurité")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Une adresse IP identifie de manière unique chaque équipement réseau")

    # Question 2 - CIDR
    print("\n2. Que signifie le /24 dans 192.168.1.0/24 ?")
    print("a) 24 adresses disponibles")
    print("b) 24 bits pour la partie réseau")
    print("c) 24 bits pour la partie hôte")
    print("d) 24 sous-réseaux")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) /24 indique que 24 bits sont utilisés pour identifier le réseau")

    # Question 3 - Calcul sous-réseau
    print("\n3. Combien d'adresses utilisables dans un réseau /28 ?")
    print("a) 16")
    print("b) 14") 
    print("c) 28")
    print("d) 30")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) /28 = 16 adresses totales - 2 (réseau + broadcast) = 14 utilisables")

    # Question 4 - Commande Linux
    print("\n4. Quelle commande permet d'afficher la configuration IP sous Linux ?")
    print("a) ifconfig")
    print("b) ip addr show")
    print("c) ipconfig")
    print("d) netstat")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 'ip addr show' est la commande moderne pour afficher les IPs")

    # Question 5 - Outils réseau
    print("\n5. Quel outil permet de calculer rapidement un plan d'adressage ?")
    print("a) ping")
    print("b) traceroute")
    print("c) ipcalc")
    print("d) ssh")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) ipcalc calcule automatiquement les plages d'adresses et masques")

    # Question 6 - Segmentation
    print("\n6. À quoi sert la segmentation réseau ?")
    print("a) Augmenter la bande passante")
    print("b) Séparer les usages et renforcer la sécurité")
    print("c) Installer plus de serveurs")
    print("d) Remplacer les adresses IP")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) La segmentation isole les flux et améliore la sécurité")

    # Question 7 - Passerelle
    print("\n7. Quel est le rôle d'une passerelle par défaut ?")
    print("a) Fournir des adresses IP")
    print("b) Permettre la communication hors du réseau local")
    print("c) Sécuriser les connexions SSH")
    print("d) Gérer les VLANs")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) La passerelle route le trafic vers d'autres réseaux")

    # Question 8 - Routage
    print("\n8. Quelle commande affiche la table de routage ?")
    print("a) route -n")
    print("b) ip route show")
    print("c) netstat -rn")
    print("d) Toutes les réponses ci-dessus")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) Toutes ces commandes affichent les routes système")

    # Question 9 - VLANs
    print("\n9. Quel est l'intérêt d'utiliser des VLANs ?")
    print("a) Séparer logiquement les réseaux sur un même switch")
    print("b) Augmenter la vitesse du WiFi")
    print("c) Remplacer les adresses MAC")
    print("d) Installer des imprimantes")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Les VLANs créent des réseaux logiques séparés")

    # Question 10 - Planification
    print("\n10. Quelle est la première étape pour concevoir un plan d'adressage ?")
    print("a) Acheter du matériel")
    print("b) Analyser les besoins métier et le nombre d'équipements")
    print("c) Configurer le firewall")
    print("d) Installer un serveur DHCP")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) L'analyse des besoins précède toute conception technique")

    # Question 11 - Adresses privées
    print("\n11. Quelle plage d'adresses appartient aux réseaux privés RFC 1918 ?")
    print("a) 172.15.0.0/16")
    print("b) 172.16.0.0/12")
    print("c) 172.32.0.0/12")
    print("d) 172.15.0.0/12")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 172.16.0.0/12 (172.16.0.0 à 172.31.255.255) est une plage privée RFC 1918")

    # Question 12 - Masque de sous-réseau
    print("\n12. Quel masque correspond à un /26 ?")
    print("a) 255.255.255.192")
    print("b) 255.255.255.224") 
    print("c) 255.255.255.240")
    print("d) 255.255.255.248")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) /26 = 255.255.255.192 (26 bits à 1)")

    # Question 13 - Broadcast
    print("\n13. Quelle est l'adresse de broadcast pour le réseau 10.0.5.0/24 ?")
    print("a) 10.0.5.254")
    print("b) 10.0.5.255")
    print("c) 10.0.5.0")
    print("d) 10.0.6.0")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Dans un /24, l'adresse broadcast est toujours .255")

    # Question 14 - Architecture multi-sites
    print("\n14. Pour connecter 3 sites distants, quelle solution est recommandée ?")
    print("a) Câbles réseau très longs")
    print("b) VPN site-à-site")
    print("c) WiFi longue portée")
    print("d) Serveur FTP")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Les VPN site-à-site connectent de manière sécurisée des réseaux distants")

    # Question 15 - Évolutivité
    print("\n15. Pourquoi laisser des plages d'adresses libres dans un plan d'adressage ?")
    print("a) Pour économiser l'électricité")
    print("b) Pour permettre l'évolution future du réseau")
    print("c) Pour accélérer les connexions")
    print("d) Pour réduire les coûts")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Prévoir des plages libres permet d'ajouter facilement de nouveaux équipements")

    # Résultats finaux
    print("\n" + "=" * 60)
    print("              RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    
    print(f"Score obtenu: {score}/{total_questions} ({percentage:.1f}%)")
    print(f"Seuil requis: 11/15 (72%)")
    
    if score >= 11:
        print("\nFELICITATIONS! QUIZ VALIDE")
        print("Vous maîtrisez les concepts d'architecture réseau")
        print("Vous pouvez continuer vers la séance suivante")
    elif score >= 8:
        print("\nEN COURS D'ACQUISITION")
        print("Révisez les points faibles et recommencez")
        print("Consultez les corrections des LABs")
    else:
        print("\nA REPRENDRE") 
        print("Retravaillez le cours et les LABs avant de recommencer")
        print("N'hésitez pas à demander de l'aide au formateur")
    
    print("\n" + "=" * 60)
    print("Formateur: Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 4")

if __name__ == "__main__":
    run_quiz()
