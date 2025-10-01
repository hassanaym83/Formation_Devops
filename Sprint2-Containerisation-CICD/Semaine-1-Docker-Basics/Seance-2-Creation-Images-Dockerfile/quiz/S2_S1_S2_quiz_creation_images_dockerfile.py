"""
Quiz Séance 2 - Validatio    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) ADD a des fonctionnalités supplémentaires") acquis
Création d'Images avec Dockerfile

18 questions - 1 point par question
Seuil de validation : 13/18 (72%)
Durée maximale : 18 minutes

Formateur: Hassan ESSADIK | Sprint 2 - Semaine 1 - Séance 2
"""

def run_quiz():
    """Execute le quiz de validation création d'images Dockerfile"""
    
    print("=" * 65)
    print("     QUIZ CRÉATION D'IMAGES AVEC DOCKERFILE")
    print("     18 questions - Seuil de validation: 72%")
    print("=" * 65)
    
    score = 0
    total_questions = 18
    questions_missed = []
    
    # Question 1 - Instructions de base
    print("\n1. Quelle est la différence principale entre COPY et ADD ?")
    print("   a) COPY et ADD sont identiques")
    print("   b) ADD peut extraire automatiquement les archives et télécharger des URLs")
    print("   c) COPY est plus rapide que ADD")
    print("   d) ADD ne peut copier que des fichiers locaux")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) ADD a des fonctionnalités supplémentaires")
        questions_missed.append(1)
    
    # Question 2 - Optimisation du cache
    print("\n2. Quel ordre d'instructions optimise le cache des couches ?")
    print("   a) FROM, COPY ., COPY package.json, RUN npm install")
    print("   b) FROM, COPY package.json, RUN npm install, COPY .")
    print("   c) COPY package.json, COPY ., RUN npm install, FROM")
    print("   d) FROM, COPY package.json, COPY ., RUN npm install")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) Dépendances d'abord, code ensuite")
        questions_missed.append(2)
    
    # Question 3 - Multi-stage builds
    print("\n3. Quel est l'avantage principal des builds multi-stage ?")
    print("   a) Permettre d'utiliser plusieurs images de base")
    print("   b) Réduire la taille de l'image finale en excluant les outils de build")
    print("   c) Accélérer le processus de build")
    print("   d) Permettre la parallélisation des builds")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) Séparation build/runtime pour optimisation")
        questions_missed.append(3)
    
    # Question 4 - Sécurité
    print("\n4. Quelle pratique de sécurité est essentielle dans un Dockerfile ?")
    print("   a) Utiliser l'utilisateur root par défaut")
    print("   b) Créer et utiliser un utilisateur non-root")
    print("   c) Exposer tous les ports nécessaires")
    print("   d) Installer tous les packages disponibles")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) Principe du moindre privilège")
        questions_missed.append(4)
    
    # Question 5 - BuildKit
    print("\n5. Quelle syntaxe BuildKit permet d'utiliser un cache mount ?")
    print("   a) RUN --cache /downloads wget file.tar.gz")
    print("   b) RUN --mount=type=cache,target=/downloads wget file.tar.gz")
    print("   c) RUN --volume=/downloads wget file.tar.gz")
    print("   d) RUN --cache-mount=/downloads wget file.tar.gz")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) Syntaxe --mount=type=cache,target=<path>")
        questions_missed.append(5)
    
    # Question 6 - Health checks
    print("\n6. Comment configurer un health check toutes les 30 secondes ?")
    print("   a) HEALTHCHECK CMD curl -f http://localhost/health")
    print("   b) HEALTHCHECK --interval=30s CMD curl -f http://localhost/health")
    print("   c) RUN healthcheck --interval=30s curl -f http://localhost/health")
    print("   d) CHECK --every=30s curl -f http://localhost/health")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) HEALTHCHECK avec --interval=30s")
        questions_missed.append(6)
    
    # Question 7 - Images de base
    print("\n7. Quelle image de base est recommandée pour la production ?")
    print("   a) ubuntu:latest")
    print("   b) alpine:3.14")
    print("   c) centos:8")
    print("   d) fedora:latest")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) Alpine - légère et sécurisée")
        questions_missed.append(7)
    
    # Question 8 - ENTRYPOINT vs CMD
    print("\n8. Quelle est la différence entre ENTRYPOINT et CMD ?")
    print("   a) ENTRYPOINT est remplaçable, CMD est fixe")
    print("   b) CMD est remplaçable, ENTRYPOINT est fixe")
    print("   c) Aucune différence fonctionnelle")
    print("   d) ENTRYPOINT pour les scripts, CMD pour les binaires")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) CMD peut être remplacé, ENTRYPOINT non")
        questions_missed.append(8)
    
    # Question 9 - Optimisation des couches
    print("\n9. Comment minimiser le nombre de couches dans une image ?")
    print("   a) Utiliser une instruction RUN par commande")
    print("   b) Combiner les commandes RUN avec && et \\")
    print("   c) Utiliser COPY pour chaque fichier séparément")
    print("   d) Éviter l'instruction FROM")
    answer = input("   Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("   Correct!")
    else:
        print("   Incorrect. Réponse: b) Combiner les commandes RUN")
        questions_missed.append(9)
    
    # Question 10 - Variables d'environnement
    print("\n10. Comment définir une variable d'environnement dans un Dockerfile ?")
    print("    a) SET VAR=value")
    print("    b) ENV VAR=value")
    print("    c) EXPORT VAR=value")
    print("    d) VAR=value")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: b) ENV VAR=value")
        questions_missed.append(10)
    
    # Question 11 - WORKDIR
    print("\n11. Quel est l'effet de l'instruction WORKDIR ?")
    print("    a) Créer un répertoire seulement")
    print("    b) Changer le répertoire courant seulement")
    print("    c) Créer ET définir comme répertoire de travail")
    print("    d) Supprimer le répertoire existant")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'c':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: c) Crée et définit le répertoire de travail")
        questions_missed.append(11)
    
    # Question 12 - .dockerignore
    print("\n12. À quoi sert le fichier .dockerignore ?")
    print("    a) Ignorer les erreurs de build")
    print("    b) Exclure des fichiers du contexte de build")
    print("    c) Ignorer les warnings de sécurité")
    print("    d) Exclure des couches de l'image")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: b) Exclut fichiers du contexte de build")
        questions_missed.append(12)
    
    # Question 13 - Multi-stage syntax
    print("\n13. Comment nommer un stage dans un build multi-stage ?")
    print("    a) FROM ubuntu:20.04 NAME builder")
    print("    b) FROM ubuntu:20.04 AS builder")
    print("    c) FROM ubuntu:20.04 STAGE builder")
    print("    d) FROM ubuntu:20.04 -> builder")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: b) FROM image AS nom_stage")
        questions_missed.append(13)
    
    # Question 14 - Copie depuis un stage
    print("\n14. Comment copier depuis un stage nommé 'builder' ?")
    print("    a) COPY --stage=builder /app/dist /app/")
    print("    b) COPY --from=builder /app/dist /app/")
    print("    c) COPY --source=builder /app/dist /app/")
    print("    d) COPY builder:/app/dist /app/")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: b) COPY --from=stage_name")
        questions_missed.append(14)
    
    # Question 15 - ARG vs ENV
    print("\n15. Quelle est la différence entre ARG et ENV ?")
    print("    a) ARG pour build-time, ENV pour runtime")
    print("    b) ENV pour build-time, ARG pour runtime")
    print("    c) Aucune différence")
    print("    d) ARG est plus sécurisé que ENV")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'a':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: a) ARG pendant build, ENV dans conteneur")
        questions_missed.append(15)
    
    # Question 16 - EXPOSE
    print("\n16. Que fait l'instruction EXPOSE dans un Dockerfile ?")
    print("    a) Publie automatiquement le port sur l'hôte")
    print("    b) Documente le port utilisé par l'application")
    print("    c) Ouvre le port dans le firewall")
    print("    d) Lie le port à l'interface réseau")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: b) Documentation, pas de publication")
        questions_missed.append(16)
    
    # Question 17 - Forme exec vs shell
    print("\n17. Quelle forme d'instruction est recommandée pour la sécurité ?")
    print("    a) RUN apt-get update")
    print("    b) RUN ['apt-get', 'update']")
    print("    c) Les deux sont équivalentes")
    print("    d) Dépend du package manager")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: b) Forme exec plus sécurisée")
        questions_missed.append(17)
    
    # Question 18 - BuildKit secrets
    print("\n18. Comment utiliser un secret BuildKit dans un RUN ?")
    print("    a) RUN --secret=id=token curl -H $token")
    print("    b) RUN --mount=type=secret,id=token curl -H $(cat /run/secrets/token)")
    print("    c) RUN --with-secret=token curl -H $token")
    print("    d) RUN curl -H $SECRET_TOKEN")
    answer = input("    Réponse: ").lower().strip()
    if answer == 'b':
        score += 1
        print("    Correct!")
    else:
        print("    Incorrect. Réponse: b) Mount secret et lecture depuis /run/secrets/")
        questions_missed.append(18)
    
    # Calcul du pourcentage
    percentage = (score / total_questions) * 100
    
    # Affichage des résultats
    print("\n" + "=" * 65)
    print(f"RÉSULTATS FINAUX")
    print("=" * 65)
    print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
    print(f"Seuil de validation: 13/18 (72%)")
    
    if score >= (total_questions * 0.72):
        print("\nVALIDATION RÉUSSIE!")
        print("Excellente maîtrise des concepts Dockerfile!")
        print("Vous pouvez passer à la séance suivante: Images et Registries")
        
        if percentage >= 90:
            print("\nPERFORMANCE EXCEPTIONNELLE!")
            print("Maîtrise parfaite des optimisations et bonnes pratiques")
        elif percentage >= 80:
            print("\nTRÈS BONNE PERFORMANCE!")
            print("Solide compréhension des concepts avancés")
    else:
        print("\nVALIDATION ÉCHOUÉE")
        print("Révisez les concepts suivants:")
        
        if score < 8:
            print("- Instructions de base Dockerfile (FROM, RUN, COPY, CMD)")
            print("- Optimisation du cache des couches")
        if score < 11:
            print("- Builds multi-stage et optimisation")
            print("- Sécurité et utilisateurs non-root")
        if score < 13:
            print("- BuildKit et fonctionnalités avancées")
            print("- Health checks et monitoring")
        
        print(f"\nQuestions ratées: {questions_missed}")
        print("Recommandation: Refaire les LABs 1-3 et repasser le quiz")
    
    print(f"\nProchaine séance: Images et Registries Docker")
    print("Focus: Distribution, versioning et registries privés")
    
    return score >= (total_questions * 0.72)

# Execution du quiz
if __name__ == "__main__":
    print("Quiz Création d'Images avec Dockerfile")
    print("Formateur: Hassan ESSADIK")
    print("Sprint 2 - Semaine 1 - Séance 2")
    print("\nAppuyez sur Entrée pour commencer...")
    input()
    
    passed = run_quiz()
    
    print(f"\n{'='*65}")
    print("Fin du quiz - Merci pour votre participation!")
    if passed:
        print("Direction: Séance 3 - Images et Registries")
    else:
        print("Direction: Révision et nouvelle tentative")