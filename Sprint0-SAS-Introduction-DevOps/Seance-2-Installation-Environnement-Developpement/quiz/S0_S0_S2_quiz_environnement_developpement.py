"""
Quiz Séance 2 - Validation des acquis
Installation Environnement de Développement DevOps

20 questions - 1 point par question
Seuil de validation : 14/20 (70%)
Durée maximale : 15 minutes

Sprint 0 - Séance 2 - Architecture, VirtualBox et Vagrant
Couvre les chapitres 1, 2, et 3 du cours
"""

def run_quiz():
    """Execute le quiz de validation des concepts d'environnement DevOps"""

    print("=" * 65)
    print("    QUIZ ENVIRONNEMENT DE DÉVELOPPEMENT DEVOPS")
    print("    20 questions - Seuil de validation: 70%")
    print("=" * 65)

    score = 0
    total_questions = 20

    # Question 1 - Architecture DevOps
    print("\n1. Quelles sont les 4 couches principales d'un environnement DevOps moderne ?")
    print("a) Web, App, DB, Cache")
    print("b) Virtualisation, Containerisation, Développement, Outils")
    print("c) Frontend, Backend, Database, API")
    print("d) Dev, Test, Stage, Prod")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Virtualisation, Containerisation, Développement, Outils")

    # Question 2 - VirtualBox
    print("\n2. Quel type d'hyperviseur est VirtualBox ?")
    print("a) Type 1 (bare metal)")
    print("b) Type 2 (hosted)")
    print("c) Hyperconvergé")
    print("d) Container-based")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Type 2 (hosted), s'exécute sur un OS hôte")

    # Question 3 - Chocolatey
    print("\n3. Que fait la commande PowerShell pour installer Chocolatey ?")
    print("a) Télécharge et installe automatiquement")
    print("b) Configure uniquement les variables d'environnement")
    print("c) Installe seulement les dépendances")
    print("d) Active le Windows Package Manager")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Télécharge et installe automatiquement Chocolatey")

    # Question 4 - Installation VirtualBox
    print("\n4. Quelle commande Chocolatey installe VirtualBox ?")
    print("a) choco get virtualbox")
    print("b) choco install virtualbox")
    print("c) choco add virtualbox")
    print("d) choco setup virtualbox")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) choco install virtualbox")

    # Question 5 - Configuration réseau NAT
    print("\n5. Quel est l'avantage principal du mode réseau NAT ?")
    print("a) Accès direct depuis le réseau local")
    print("b) Accès Internet pour la VM avec isolation")
    print("c) Communication entre VMs")
    print("d) Performance réseau maximale")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Accès Internet pour la VM avec isolation")

    # Question 6 - Port forwarding
    print("\n6. Que permet le port forwarding guest: 22, host: 2222 ?")
    print("a) SSH depuis la VM vers l'hôte sur le port 2222")
    print("b) SSH depuis l'hôte vers la VM via le port 2222")
    print("c) HTTP depuis la VM vers l'hôte")
    print("d) FTP depuis l'hôte vers la VM")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) SSH depuis l'hôte vers la VM via le port 2222")

    # Question 7 - Private Network
    print("\n7. Quelle est l'IP typique d'un réseau privé VirtualBox ?")
    print("a) 10.0.2.15")
    print("b) 172.16.0.10")
    print("c) 192.168.56.10")
    print("d) 127.0.0.1")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 192.168.56.10 (plage Host-Only par défaut)")

    # Question 8 - Bridged Adapter
    print("\n8. Que fait le mode Bridged Adapter ?")
    print("a) Isole complètement la VM")
    print("b) Connecte la VM directement au réseau physique")
    print("c) Crée un tunnel VPN")
    print("d) Partage la connexion Internet")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Connecte la VM directement au réseau physique")

    # Question 9 - Vagrant définition
    print("\n9. Qu'est-ce que Vagrant ?")
    print("a) Un hyperviseur de virtualisation")
    print("b) Un outil d'automatisation de VMs de développement")
    print("c) Un système d'exploitation pour conteneurs")
    print("d) Un gestionnaire de packages Linux")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Un outil d'automatisation de VMs de développement")

    # Question 10 - Vagrantfile
    print("\n10. Dans quel langage est écrit un Vagrantfile ?")
    print("a) YAML")
    print("b) JSON")
    print("c) Ruby")
    print("d) Python")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Ruby, utilise la syntaxe Ruby DSL")

    # Question 11 - Vagrant Box
    print("\n11. Qu'est-ce qu'une Vagrant Box ?")
    print("a) Un fichier de configuration")
    print("b) Un template de machine virtuelle pré-configuré")
    print("c) Un script de provisioning")
    print("d) Un plugin Vagrant")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Un template de machine virtuelle pré-configuré")

    # Question 12 - Commande vagrant up
    print("\n12. Que fait la commande 'vagrant up' ?")
    print("a) Met à jour Vagrant")
    print("b) Démarre et configure la VM selon le Vagrantfile")
    print("c) Supprime la VM")
    print("d) Sauvegarde l'état de la VM")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Démarre et configure la VM selon le Vagrantfile")

    # Question 13 - vagrant-vbguest plugin
    print("\n13. À quoi sert le plugin vagrant-vbguest ?")
    print("a) Gestion automatique des Guest Additions VirtualBox")
    print("b) Configuration du réseau")
    print("c) Partage de fichiers")
    print("d) Sauvegarde des VMs")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Gestion automatique des Guest Additions VirtualBox")

    # Question 14 - Source des boxes
    print("\n14. Où trouve-t-on les boxes Vagrant officielles ?")
    print("a) github.com/vagrant")
    print("b) app.vagrantup.com")
    print("c) vagrant.com/boxes")
    print("d) virtualbox.org/boxes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) app.vagrantup.com (Vagrant Cloud)")

    # Question 15 - Provisioning
    print("\n15. Qu'est-ce que le provisioning dans Vagrant ?")
    print("a) Installation du système d'exploitation")
    print("b) Configuration automatique après démarrage de la VM")
    print("c) Création du réseau virtuel")
    print("d) Allocation des ressources matérielles")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Configuration automatique après démarrage de la VM")

    # Question 16 - Commande vagrant ssh
    print("\n16. Que permet la commande 'vagrant ssh' ?")
    print("a) Configurer les clés SSH")
    print("b) Se connecter directement à la VM")
    print("c) Démarrer le service SSH")
    print("d) Générer une paire de clés")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Se connecter directement à la VM")

    # Question 17 - vagrant destroy
    print("\n17. Que fait 'vagrant destroy' ?")
    print("a) Arrête la VM")
    print("b) Supprime complètement la VM")
    print("c) Remet à zéro la configuration")
    print("d) Sauvegarde puis supprime")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Supprime complètement la VM")

    # Question 18 - Configuration mémoire
    print("\n18. Comment configurer 2GB de RAM dans un Vagrantfile ?")
    print("a) config.vm.memory = '2048'")
    print("b) vb.memory = '2048'")
    print("c) config.memory = 2048")
    print("d) vm.ram = '2GB'")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) vb.memory = '2048' dans le bloc provider")

    # Question 19 - Box CentOS recommandée
    print("\n19. Quelle box CentOS Stream 9 est recommandée ?")
    print("a) centos/stream9")
    print("b) generic/centos9s")
    print("c) redhat/centos9")
    print("d) official/centos-stream")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) generic/centos9s (maintenue par Generic)")

    # Question 20 - Avantages environnement multicouche
    print("\n20. Quel est le principal avantage d'un environnement DevOps multicouche ?")
    print("a) Réduction des coûts uniquement")
    print("b) Reproductibilité et isolation des projets")
    print("c) Performance maximale")
    print("d) Simplicité de configuration")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Reproductibilité et isolation des projets")

    # Calcul du score final
    percentage = (score / total_questions) * 100
    
    print("\n" + "=" * 50)
    print(f"RÉSULTAT FINAL: {score}/{total_questions} ({percentage:.1f}%)")
    
    if percentage >= 70:
        print("VALIDÉ! Excellent travail!")
        print("Vous maîtrisez les concepts d'environnement DevOps.")
    else:
        print("NON VALIDÉ")
        print("Seuil requis: 70% (14/20)")
        print("Révisez les chapitres 1, 2 et 3 du cours.")
    
    print("=" * 50)

    # Recommandations selon le score
    if percentage >= 90:
        print("\nPerformance exceptionnelle!")
        print("Vous êtes prêt pour les LABs pratiques.")
    elif percentage >= 70:
        print("\nBonne maîtrise des concepts!")
        print("Passez aux exercices pratiques.")
    else:
        print("\nPoints à réviser:")
        if score < 5:
            print("- Architecture environnement DevOps (chapitre 1)")
        if score < 10:
            print("- Installation et configuration VirtualBox (chapitre 2)")
        if score < 15:
            print("- Configuration Vagrant (chapitre 3)")
        print("- Relisez le cours et refaites le quiz.")

def main():
    """Point d'entrée principal du quiz"""
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")

if __name__ == "__main__":
    main()
