"""
Quiz Séance 3 - Validation des acquis
Fondamentaux IP et Architecture Réseau DevOps

15 questions - 1 point par question
Seuil de validation : 11/15 (72%)
Durée maximale : 15 minutes

Formateur: Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 3
"""

def run_quiz():
    """Execute le quiz de validation des fondamentaux réseau IP"""

    print("=" * 60)
    print("    QUIZ FONDAMENTAUX IP ET ARCHITECTURE RÉSEAU")
    print("    15 questions - Seuil de validation: 72%")
    print("=" * 60)

    score = 0
    total_questions = 15

    # Question 1 - Modèle TCP/IP
    print("\n1. Combien de couches compte le modèle TCP/IP ?")
    print("a) 3 couches    b) 4 couches    c) 5 couches    d) 7 couches")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Le modèle TCP/IP compte 4 couches : Application, Transport, Internet, Accès réseau")

    # Question 2 - Adresses privées
    print("\n2. Quelle plage d'adresses correspond aux adresses privées de classe A ?")
    print("a) 172.16.0.0/12    b) 192.168.0.0/16    c) 10.0.0.0/8    d) 127.0.0.0/8")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 10.0.0.0/8 est la plage privée de classe A (RFC 1918)")

    # Question 3 - Calcul CIDR
    print("\n3. Combien d'hôtes utilisables contient le réseau 192.168.10.0/26 ?")
    print("a) 64 hôtes    b) 62 hôtes    c) 32 hôtes    d) 30 hôtes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) /26 = 6 bits hôte = 2^6 - 2 = 62 hôtes utilisables")

    # Question 4 - Masque de sous-réseau
    print("\n4. Le masque 255.255.240.0 correspond à quelle notation CIDR ?")
    print("a) /20    b) /22    c) /24    d) /16")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) 255.255.240.0 = 20 bits de réseau = /20")

    # Question 5 - DNS
    print("\n5. Quel enregistrement DNS associe un nom de domaine à une adresse IPv4 ?")
    print("a) CNAME    b) MX    c) A    d) PTR")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) L'enregistrement A associe un nom à une adresse IPv4")

    # Question 6 - Routage
    print("\n6. Dans une table de routage, que représente la route 0.0.0.0/0 ?")
    print("a) Route locale    b) Route par défaut    c) Route multicast    d) Route statique")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 0.0.0.0/0 est la route par défaut (default gateway)")

    # Question 7 - VLSM
    print("\n7. Quel est l'avantage principal du VLSM (Variable Length Subnet Mask) ?")
    print("a) Sécurité accrue    b) Vitesse réseau    c) Optimisation adressage    d) Simplicité config")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) VLSM optimise l'utilisation de l'espace d'adressage")

    # Question 8 - Segmentation DevOps
    print("\n8. Pourquoi séparer les environnements Dev/Test/Prod en sous-réseaux distincts ?")
    print("a) Performance    b) Coût    c) Sécurité et isolation    d) Simplicité")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Séparation pour sécurité et isolation des environnements")

    # Question 9 - Adresse broadcast
    print("\n9. Quelle est l'adresse de broadcast du réseau 172.16.50.0/24 ?")
    print("a) 172.16.50.1    b) 172.16.50.254    c) 172.16.50.255    d) 172.16.51.0")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) L'adresse broadcast est la dernière du réseau : 172.16.50.255")

    # Question 10 - Protocole transport
    print("\n10. Quel protocole de transport utilise SSH pour ses connexions ?")
    print("a) UDP    b) TCP    c) ICMP    d) IP")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) SSH utilise TCP (port 22) pour garantir la fiabilité")

    # Question 11 - Classe IP
    print("\n11. À quelle classe traditionnelle appartient l'adresse 172.25.100.50 ?")
    print("a) Classe A    b) Classe B    c) Classe C    d) Classe D")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 172.x.x.x appartient à la classe B (128-191)")

    # Question 12 - Subdivision
    print("\n12. Pour créer 4 sous-réseaux à partir de 192.168.1.0/24, quel masque utiliser ?")
    print("a) /25    b) /26    c) /27    d) /28")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 4 sous-réseaux nécessitent 2 bits supplémentaires : /24 + 2 = /26")

    # Question 13 - Résolution inverse
    print("\n13. Quel enregistrement DNS permet la résolution inverse (IP vers nom) ?")
    print("a) A    b) AAAA    c) PTR    d) CNAME")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) L'enregistrement PTR permet la résolution inverse")

    # Question 14 - Couche réseau
    print("\n14. À quelle couche TCP/IP appartient le protocole ICMP (ping) ?")
    print("a) Application    b) Transport    c) Internet    d) Accès réseau")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) ICMP fait partie de la couche Internet (couche 3)")

    # Question 15 - Architecture DevOps
    print("\n15. Dans une architecture DevOps, quel environnement doit avoir l'accès réseau le plus restreint ?")
    print("a) Développement    b) Test    c) Staging    d) Production")
    answer = input("Réponse: ").lower()
    if answer == 'd':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: d) La Production doit avoir l'accès le plus restreint pour la sécurité")

    # Résultats finaux
    print("\n" + "=" * 60)
    print("              RÉSULTATS DU QUIZ")
    print("=" * 60)

    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage >= 72:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les fondamentaux réseau IP")
        print("Vous pouvez passer à la séance suivante")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        if score < 5:
            print("- Modèle TCP/IP et couches réseau")
            print("- Adresses IP et classes traditionnelles")
            print("- Calculs CIDR de base")
        elif score < 8:
            print("- Calculs de masques et VLSM")
            print("- DNS et résolution de noms")
            print("- Routage et tables de routage")
        elif score < 11:
            print("- Architecture réseau DevOps")
            print("- Segmentation et sécurité réseau")
            print("- Optimisations et best practices")
        print("Recommandation: Refaire les LABs et repasser le quiz")

    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Fondamentaux IP et Architecture Réseau")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 1 - Semaine 1 - Séance 3")
    print("\nAppuyez sur Entrée pour commencer...")
    input()

    passed = run_quiz()

    print(f"\n{'='*60}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 4 - Réseaux Interfaces et Configuration")
    else:
        print("Direction: Révision et nouvelle tentative")
    print(f"{'='*60}")
