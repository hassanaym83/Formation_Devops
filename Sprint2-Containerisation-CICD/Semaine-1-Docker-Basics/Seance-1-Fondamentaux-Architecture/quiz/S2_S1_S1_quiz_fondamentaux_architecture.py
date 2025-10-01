#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz Séance 1 - Validation des acquis
Fondamentaux et Architecture Docker

18 questions - 1 point par question
Seuil de validation : 14/18 (78%)
Durée maximale : 18 minutes

Formateur: Hassan ESSADIK | Sprint 2 - Semaine 1 - Séance 1
"""

def run_quiz():
    """Execute le quiz de validation des fondamentaux Docker"""
    
    print("=" * 65)
    print(" QUIZ FONDAMENTAUX ET ARCHITECTURE DOCKER")
    print(" 18 questions - Seuil de validation: 78%")
    print("=" * 65)
    
    score = 0
    total_questions = 18
    
    # Question 1 - Images vs Conteneurs
    print("\n1. Quelle est la principale différence entre une image Docker et un conteneur Docker ?")
    print("a) Une image est exécutable, un conteneur est statique")
    print("b) Une image est un template en lecture seule, un conteneur est une instance exécutable d'une image")
    print("c) Une image contient des données persistantes, un conteneur est temporaire")
    print("d) Il n'y a pas de différence, ce sont des synonymes")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Image = template lecture seule, Conteneur = instance exécutable")
    
    # Question 2 - Architecture Docker
    print("\n2. Docker utilise une architecture client-serveur où le Docker Daemon gère les conteneurs et expose une API REST. (Vrai/Faux)")
    print("a) Vrai")
    print("b) Faux")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Vrai - Docker Client communique avec Docker Daemon via API REST")
    
    # Question 3 - Compatibilité OS
    print("\n3. Quelle est la principale différence entre conteneurs Linux et conteneurs Windows concernant la compatibilité ?")
    print("a) Les conteneurs Linux sont plus rapides")
    print("b) Les conteneurs Linux ne peuvent fonctionner que sur des hôtes Linux, les conteneurs Windows que sur des hôtes Windows")
    print("c) Les conteneurs Windows sont plus sécurisés")
    print("d) Il n'y a pas de différence de compatibilité")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Compatibilité dépend du noyau OS - Linux nécessite noyau Linux")
    
    # Question 4 - Commande pull
    print("\n4. Quelle commande permet de télécharger une image Docker sans créer de conteneur ?")
    print("a) docker get nginx")
    print("b) docker pull nginx")
    print("c) docker download nginx")
    print("d) docker fetch nginx")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 'docker pull' télécharge une image sans créer de conteneur")
    
    # Question 5 - Partage du noyau
    print("\n5. Les conteneurs Docker partagent le noyau du système d'exploitation hôte, contrairement aux machines virtuelles qui ont chacune leur propre OS. (Vrai/Faux)")
    print("a) Vrai")
    print("b) Faux")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Vrai - Les conteneurs partagent le noyau, contrairement aux VMs")
    
    # Question 6 - Isolation
    print("\n6. Quelle technologie Linux Docker utilise-t-il pour l'isolation des processus ?")
    print("a) Cgroups uniquement")
    print("b) Namespaces uniquement")
    print("c) Namespaces et Cgroups")
    print("d) SELinux uniquement")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Namespaces (isolation) + Cgroups (limitation ressources)")
    
    # Question 7 - Commande ps
    print("\n7. Quelle commande affiche les conteneurs en cours d'exécution ?")
    print("a) docker list")
    print("b) docker ps")
    print("c) docker show")
    print("d) docker containers")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 'docker ps' liste les conteneurs actifs")
    
    # Question 8 - Docker Desktop
    print("\n8. Docker Desktop résout l'incompatibilité des conteneurs Linux sur Windows/macOS en utilisant :")
    print("a) Une traduction des appels système en temps réel")
    print("b) Une machine virtuelle Linux cachée")
    print("c) Une émulation de noyau Linux")
    print("d) Un système de double boot automatique")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Docker Desktop utilise une VM Linux transparente")
    
    # Question 9 - Option detach
    print("\n9. Quelle option de la commande 'docker run' permet d'exécuter un conteneur en arrière-plan ?")
    print("a) -b ou --background")
    print("b) -d ou --detach")
    print("c) -bg ou --daemon")
    print("d) -f ou --fork")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) -d ou --detach pour exécution en arrière-plan")
    
    # Question 10 - Mapping de ports
    print("\n10. Comment mapper le port 8080 de l'hôte vers le port 80 du conteneur ?")
    print("a) docker run -p 80:8080 nginx")
    print("b) docker run -p 8080:80 nginx")
    print("c) docker run --port 8080:80 nginx")
    print("d) docker run --map 8080:80 nginx")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) Syntaxe: -p host_port:container_port")
    
    # Question 11 - Couches (layers)
    print("\n11. Les images Docker sont construites en couches (layers) qui peuvent être partagées entre différentes images. (Vrai/Faux)")
    print("a) Vrai")
    print("b) Faux")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Vrai - Les couches sont partagées pour optimiser l'espace")
    
    # Question 12 - Commande inspect
    print("\n12. Quelle commande permet d'inspecter les métadonnées d'un conteneur ?")
    print("a) docker info container-name")
    print("b) docker inspect container-name")
    print("c) docker describe container-name")
    print("d) docker metadata container-name")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 'docker inspect' affiche les métadonnées détaillées")
    
    # Question 13 - Registry
    print("\n13. Dans l'architecture Docker, quel composant stocke les images Docker ?")
    print("a) Docker Client")
    print("b) Docker Daemon")
    print("c) Docker Registry")
    print("d) Docker Engine")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) Docker Registry stocke les images (Docker Hub, registries privés)")
    
    # Question 14 - Commande exec
    print("\n14. La commande 'docker exec' permet d'exécuter des commandes dans un conteneur en cours d'exécution. (Vrai/Faux)")
    print("a) Vrai")
    print("b) Faux")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Vrai - 'docker exec' pour exécuter dans un conteneur actif")
    
    # Question 15 - Commande system prune
    print("\n15. Quelle commande supprime tous les conteneurs arrêtés, réseaux non utilisés et images danglings ?")
    print("a) docker cleanup")
    print("b) docker prune --all")
    print("c) docker system prune")
    print("d) docker remove --unused")
    answer = input("Réponse: ").lower()
    if answer == 'c':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: c) 'docker system prune' nettoie automatiquement")
    
    # Question 16 - PID Namespace
    print("\n16. Quel namespace Linux isole les processus de chaque conteneur ?")
    print("a) NET Namespace")
    print("b) PID Namespace")
    print("c) MNT Namespace")
    print("d) USER Namespace")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) PID Namespace isole les arbres de processus")
    
    # Question 17 - Copy-on-Write
    print("\n17. Grâce au mécanisme Copy-on-Write, les conteneurs partagent les couches en lecture seule et n'ont qu'une couche writable individuelle. (Vrai/Faux)")
    print("a) Vrai")
    print("b) Faux")
    answer = input("Réponse: ").lower()
    if answer == 'a':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: a) Vrai - Copy-on-Write optimise le partage des couches")
    
    # Question 18 - Commande history
    print("\n18. Quelle commande permet de voir l'historique des couches d'une image Docker ?")
    print("a) docker layers nginx")
    print("b) docker image history nginx")
    print("c) docker inspect --layers nginx")
    print("d) docker image layers nginx")
    answer = input("Réponse: ").lower()
    if answer == 'b':
        score += 1
        print("Correct!")
    else:
        print("Incorrect. Réponse: b) 'docker image history' montre les couches et leur historique")
    
    # Résultats finaux
    print("\n" + "=" * 65)
    print(" RÉSULTATS DU QUIZ")
    print("=" * 65)
    
    percentage = (score / total_questions) * 100
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    
    if percentage >= 78:
        print("VALIDATION RÉUSSIE!")
        print("Vous maîtrisez les fondamentaux et l'architecture Docker")
        print("Vous pouvez passer à la séance suivante : Création d'Images avec Dockerfile")
        
        if percentage >= 95:
            print("EXCELLENCE - Maîtrise parfaite des concepts!")
        elif percentage >= 85:
            print("TRÈS BIEN - Très bonne compréhension!")
    else:
        print("VALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        
        if score < 6:
            print("- Concepts fondamentaux (images vs conteneurs, architecture)")
            print("- Avantages des conteneurs vs VMs")
        if score < 10:
            print("- Isolation Linux (namespaces, cgroups)")
            print("- Compatibilité cross-platform et Docker Desktop")
        if score < 14:
            print("- Commandes Docker essentielles")
            print("- Structure en couches et Copy-on-Write")
        if score < 16:
            print("- Optimisations et bonnes pratiques")
        
        print("Recommandation: Revoir le cours et refaire les LABs 1-3, puis repasser le quiz")
    
    # Concepts clés à retenir
    print(f"\n{'-'*65}")
    print("CONCEPTS CLÉS À RETENIR:")
    print(f"{'-'*65}")
    print("Architecture: Client-serveur, Images, Conteneurs, Registry")
    print("Isolation: Namespaces (PID,NET,MNT,UTS,IPC,USER) + Cgroups")
    print("Conteneurs: Partage noyau, Copy-on-Write, couches partagées")
    print("Compatibilité: Linux/Linux, Windows/Windows + Docker Desktop")
    print("Commandes: pull, run, ps, exec, inspect, history, system prune")
    
    return score >= (total_questions * 0.78)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Fondamentaux et Architecture Docker")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 2 - Semaine 1 - Séance 1")
    print("\nAssurez-vous d'avoir étudié le cours et fait les LABs")
    print("Durée recommandée: 18 minutes maximum")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    passed = run_quiz()
    
    print(f"\n{'='*65}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 2 - Création d'Images avec Dockerfile")
    else:
        print("Direction: Révision des fondamentaux et nouvelle tentative")
    print(f"{'='*65}")