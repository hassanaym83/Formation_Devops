#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz GitLab CI/CD - Sprint 2 Semaine 3 Séance 1
Cours: Introduction GitLab CI/CD
Questions: 50 questions couvrant tous les concepts du cours
Seuil de validation: 72% (Framework HASSAN)
"""

import random
import time
import json
from typing import List, Dict, Tuple

class GitLabCIQuiz:
    """Quiz interactif sur GitLab CI/CD avec 50 questions"""
    
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        self.user_answers = []
        self.start_time = None
        
        # Base de données des questions
        self.questions = [
            # Chapitre 1: Introduction CI/CD et GitLab (10 questions)
            {
                "id": 1,
                "chapter": "Introduction CI/CD",
                "question": "Que signifie CI/CD ?",
                "options": [
                    "Continuous Integration / Continuous Deployment",
                    "Code Integration / Code Deployment", 
                    "Container Integration / Container Development",
                    "Client Integration / Client Development"
                ],
                "correct": 0,
                "explanation": "CI/CD signifie Continuous Integration (Intégration Continue) et Continuous Deployment (Déploiement Continu)."
            },
            {
                "id": 2,
                "chapter": "Introduction CI/CD",
                "question": "Quel est l'objectif principal de l'intégration continue ?",
                "options": [
                    "Intégrer et tester automatiquement les changements de code",
                    "Déployer uniquement en production",
                    "Créer des branches multiples",
                    "Supprimer les tests unitaires"
                ],
                "correct": 0,
                "explanation": "L'intégration continue vise à intégrer et tester automatiquement chaque changement de code pour détecter rapidement les problèmes."
            },
            {
                "id": 3,
                "chapter": "Introduction CI/CD",
                "question": "Quel avantage GitLab CI/CD offre-t-il par rapport à Jenkins ?",
                "options": [
                    "Configuration plus complexe",
                    "Support uniquement pour Java",
                    "Interface en ligne de commande uniquement",
                    "Intégration native avec GitLab sans outil externe"
                ],
                "correct": 3,
                "explanation": "GitLab CI/CD est intégré nativement dans GitLab, éliminant le besoin d'outils externes comme Jenkins."
            },
            {
                "id": 4,
                "chapter": "Introduction CI/CD",
                "question": "Dans l'architecture GitLab CI/CD, quel composant exécute les jobs ?",
                "options": [
                    "GitLab Engine",
                    "GitLab Runners",
                    "Container Registry",
                    "Git Repository"
                ],
                "correct": 1,
                "explanation": "Les GitLab Runners sont les agents qui exécutent les jobs définis dans les pipelines."
            },
            {
                "id": 5,
                "chapter": "Introduction CI/CD",
                "question": "Quel fichier configure un pipeline GitLab CI/CD ?",
                "options": [
                    ".gitlab-pipeline.yml",
                    ".ci-config.yml",
                    ".gitlab-ci.yml", 
                    ".pipeline.yml"
                ],
                "correct": 2,
                "explanation": "Le fichier .gitlab-ci.yml à la racine du projet configure le pipeline GitLab CI/CD."
            },
            {
                "id": 6,
                "chapter": "Introduction CI/CD",
                "question": "Quelle est la différence entre CI et CD ?",
                "options": [
                    "Aucune différence",
                    "CI compile seulement, CD teste seulement",
                    "CI est manuel, CD est automatique",
                    "CI teste le code, CD le déploie"
                ],
                "correct": 3,
                "explanation": "CI (Continuous Integration) se concentre sur les tests automatisés, CD (Continuous Deployment) sur le déploiement automatisé."
            },
            {
                "id": 7,
                "chapter": "Introduction CI/CD",
                "question": "Quel composant GitLab stocke les images Docker ?",
                "options": [
                    "GitLab Runner",
                    "GitLab Engine",
                    "Container Registry",
                    "Git Repository"
                ],
                "correct": 2,
                "explanation": "Le Container Registry GitLab stocke et gère les images Docker pour les déploiements."
            },
            {
                "id": 8,
                "chapter": "Introduction CI/CD",
                "question": "Dans un workflow DevOps, à quelle étape intervient GitLab CI/CD ?",
                "options": [
                    "Entre le commit et le déploiement",
                    "Uniquement au développement",
                    "Seulement en production",
                    "Uniquement pour les tests"
                ],
                "correct": 0,
                "explanation": "GitLab CI/CD automatise le processus entre le commit du code et son déploiement en production."
            },
            {
                "id": 9,
                "chapter": "Introduction CI/CD",
                "question": "Quel est l'avantage de 'Configuration as Code' ?",
                "options": [
                    "Configuration impossible à modifier",
                    "Versioning et traçabilité de la configuration",
                    "Configuration plus complexe",
                    "Nécessite plus d'outils"
                ],
                "correct": 1,
                "explanation": "Configuration as Code permet de versionner, tracer et collaborer sur la configuration comme le code source."
            },
            {
                "id": 10,
                "chapter": "Introduction CI/CD",
                "question": "Quel déclencheur automatique lance un pipeline GitLab ?",
                "options": [
                    "Redémarrage du serveur",
                    "Connexion utilisateur",
                    "Push d'un commit",
                    "Mise à jour GitLab"
                ],
                "correct": 2,
                "explanation": "Un pipeline GitLab se déclenche automatiquement lors du push d'un commit vers le repository."
            },
            
            # Chapitre 2: Premier pipeline GitLab CI/CD (8 questions)
            {
                "id": 11,
                "chapter": "Premier pipeline",
                "question": "Quelle est la syntaxe correcte pour définir des stages ?",
                "options": [
                    "steps: [build, test, deploy]",
                    "stages: [build, test, deploy]",
                    "phases: [build, test, deploy]",
                    "pipeline: [build, test, deploy]"
                ],
                "correct": 1,
                "explanation": "La directive 'stages:' définit l'ordre des étapes dans un pipeline GitLab CI/CD."
            },
            {
                "id": 12,
                "chapter": "Premier pipeline",
                "question": "Comment spécifier l'image Docker pour un job ?",
                "options": [
                    "docker: node:18",
                    "container: node:18",
                    "runtime: node:18",
                    "image: node:18"
                ],
                "correct": 3,
                "explanation": "La directive 'image:' spécifie l'image Docker à utiliser pour exécuter le job."
            },
            {
                "id": 13,
                "chapter": "Premier pipeline",
                "question": "Que contient la section 'script:' d'un job ?",
                "options": [
                    "Les commandes à exécuter",
                    "La configuration du runner",
                    "Les variables d'environnement",
                    "Les artifacts à conserver"
                ],
                "correct": 0,
                "explanation": "La section 'script:' contient la liste des commandes shell à exécuter dans le job."
            },
            {
                "id": 14,
                "chapter": "Premier pipeline",
                "question": "Comment limiter l'exécution d'un job à certaines branches ?",
                "options": [
                    "branches: [main]",
                    "only: [main]",
                    "filter: [main]",
                    "when: main"
                ],
                "correct": 1,
                "explanation": "La directive 'only:' limite l'exécution du job aux branches spécifiées."
            },
            {
                "id": 15,
                "chapter": "Premier pipeline",
                "question": "Quelle directive permet l'exécution manuelle d'un job ?",
                "options": [
                    "manual: true",
                    "trigger: manual",
                    "when: manual",
                    "mode: manual"
                ],
                "correct": 2,
                "explanation": "La directive 'when: manual' nécessite une intervention manuelle pour déclencher le job."
            },
            {
                "id": 16,
                "chapter": "Premier pipeline",
                "question": "Comment définir des variables globales dans un pipeline ?",
                "options": [
                    "variables:",
                    "env:",
                    "globals:",
                    "config:"
                ],
                "correct": 0,
                "explanation": "La section 'variables:' au niveau global définit des variables disponibles pour tous les jobs."
            },
            {
                "id": 17,
                "chapter": "Premier pipeline",
                "question": "Que se passe-t-il si un job échoue dans un stage ?",
                "options": [
                    "Le pipeline continue normalement",
                    "Seul ce job s'arrête",
                    "Le repository est verrouillé",
                    "Les stages suivants ne s'exécutent pas"
                ],
                "correct": 3,
                "explanation": "Si un job échoue, GitLab arrête l'exécution des stages suivants pour éviter les déploiements défaillants."
            },
            {
                "id": 18,
                "chapter": "Premier pipeline",
                "question": "Quel est l'ordre d'exécution correct de ces stages ?",
                "options": [
                    "deploy, build, test",
                    "build, test, deploy",
                    "test, build, deploy",
                    "build, deploy, test"
                ],
                "correct": 1,
                "explanation": "L'ordre logique est: build (construction), test (vérification), deploy (déploiement)."
            },
            
            # Chapitre 3: Jobs, stages et artifacts (10 questions)
            {
                "id": 19,
                "chapter": "Jobs et stages",
                "question": "Que sont les artifacts dans GitLab CI/CD ?",
                "options": [
                    "Des fichiers conservés entre jobs",
                    "Des erreurs de compilation",
                    "Des variables d'environnement",
                    "Des logs d'exécution"
                ],
                "correct": 0,
                "explanation": "Les artifacts sont des fichiers générés par un job et conservés pour être utilisés par d'autres jobs."
            },
            {
                "id": 20,
                "chapter": "Jobs et stages",
                "question": "Comment spécifier une durée d'expiration pour les artifacts ?",
                "options": [
                    "timeout: 1 week",
                    "duration: 1 week",
                    "lifetime: 1 week",
                    "expire_in: 1 week"
                ],
                "correct": 3,
                "explanation": "La directive 'expire_in:' définit la durée de conservation des artifacts."
            },
            {
                "id": 21,
                "chapter": "Jobs et stages",
                "question": "Quelle directive permet de récupérer des artifacts spécifiques ?",
                "options": [
                    "needs:",
                    "artifacts:",
                    "dependencies:",
                    "requires:"
                ],
                "correct": 2,
                "explanation": "La directive 'dependencies:' spécifie quels jobs fournissent les artifacts nécessaires."
            },
            {
                "id": 22,
                "chapter": "Jobs et stages",
                "question": "Comment configurer le cache pour optimiser les performances ?",
                "options": [
                    "optimize: [node_modules/]",
                    "cache: { paths: [node_modules/] }",
                    "store: [node_modules/]",
                    "persist: [node_modules/]"
                ],
                "correct": 1,
                "explanation": "La section 'cache:' avec 'paths:' définit les dossiers à mettre en cache entre les exécutions."
            },
            {
                "id": 23,
                "chapter": "Jobs et stages",
                "question": "Quelle est la différence entre artifacts et cache ?",
                "options": [
                    "Aucune différence",
                    "Cache: entre jobs, Artifacts: entre pipelines",
                    "Artifacts: temporaires, Cache: permanents",
                    "Artifacts: entre jobs, Cache: entre pipelines"
                ],
                "correct": 3,
                "explanation": "Les artifacts passent des données entre jobs du même pipeline, le cache optimise entre différents pipelines."
            },
            {
                "id": 24,
                "chapter": "Jobs et stages",
                "question": "Comment exécuter des jobs en parallèle ?",
                "options": [
                    "parallel: true",
                    "concurrent: true",
                    "Les placer dans le même stage",
                    "async: true"
                ],
                "correct": 2,
                "explanation": "Les jobs placés dans le même stage s'exécutent automatiquement en parallèle."
            },
            {
                "id": 25,
                "chapter": "Jobs et stages",
                "question": "Que fait la directive 'allow_failure: true' ?",
                "options": [
                    "Empêche l'échec du job",
                    "Relance automatiquement le job",
                    "Ignore complètement le job",
                    "Permet au pipeline de continuer malgré l'échec"
                ],
                "correct": 3,
                "explanation": "allow_failure: true permet au pipeline de continuer même si ce job échoue."
            },
            {
                "id": 26,
                "chapter": "Jobs et stages",
                "question": "Comment spécifier qu'un job doit toujours s'exécuter ?",
                "options": [
                    "always: true",
                    "when: always",
                    "force: true",
                    "mandatory: true"
                ],
                "correct": 1,
                "explanation": "La directive 'when: always' force l'exécution du job indépendamment des échecs précédents."
            },
            {
                "id": 27,
                "chapter": "Jobs et stages",
                "question": "Quel format d'artifact est recommandé pour les rapports de tests ?",
                "options": [
                    "TXT",
                    "CSV",
                    "JUnit XML",
                    "PDF"
                ],
                "correct": 2,
                "explanation": "Le format JUnit XML est standard pour les rapports de tests et s'intègre nativement dans GitLab."
            },
            {
                "id": 28,
                "chapter": "Jobs et stages",
                "question": "Comment optimiser un pipeline avec de nombreux jobs ?",
                "options": [
                    "Tout mettre dans un seul job",
                    "Supprimer les tests",
                    "Exécuter séquentiellement",
                    "Utiliser cache et artifacts intelligemment"
                ],
                "correct": 3,
                "explanation": "L'optimisation passe par l'usage intelligent du cache et des artifacts pour minimiser les transferts."
            },
            
            # Chapitre 4: GitLab Runners (6 questions)
            {
                "id": 29,
                "chapter": "GitLab Runners",
                "question": "Quels sont les types de runners disponibles ?",
                "options": [
                    "Shared, Group, Project",
                    "Public, Private, Protected",
                    "Local, Remote, Cloud",
                    "Fast, Standard, Secure"
                ],
                "correct": 0,
                "explanation": "GitLab propose des Shared Runners (partagés), Group Runners (niveau groupe) et Project Runners (spécifiques)."
            },
            {
                "id": 30,
                "chapter": "GitLab Runners",
                "question": "Quel exécuteur est recommandé pour l'isolation maximale ?",
                "options": [
                    "Shell Executor",
                    "Docker Executor",
                    "SSH Executor",
                    "VirtualBox Executor"
                ],
                "correct": 1,
                "explanation": "Le Docker Executor offre l'isolation maximale en exécutant chaque job dans un container séparé."
            },
            {
                "id": 31,
                "chapter": "GitLab Runners",
                "question": "Comment spécifier un runner particulier pour un job ?",
                "options": [
                    "tags: [specific-runner]",
                    "runner: specific-runner",
                    "executor: specific-runner",
                    "node: specific-runner"
                ],
                "correct": 0,
                "explanation": "La directive 'tags:' permet de cibler des runners spécifiques ayant ces tags."
            },
            {
                "id": 32,
                "chapter": "GitLab Runners",
                "question": "Quel service Docker peut être ajouté pour les bases de données ?",
                "options": [
                    "database: postgres:13",
                    "containers: [postgres:13]",
                    "depends_on: [postgres:13]",
                    "services: [postgres:13]"
                ],
                "correct": 3,
                "explanation": "La section 'services:' permet d'ajouter des containers de services comme PostgreSQL."
            },
            {
                "id": 33,
                "chapter": "GitLab Runners",
                "question": "Quelle commande installe un GitLab Runner ?",
                "options": [
                    "Both methods are correct",
                    "curl -L | sudo bash",
                    "apt install gitlab-runner",
                    "npm install gitlab-runner"
                ],
                "correct": 0,
                "explanation": "GitLab Runner peut être installé via les dépôts APT ou via le script d'installation officiel."
            },
            {
                "id": 34,
                "chapter": "GitLab Runners",
                "question": "Quel avantage offre le Kubernetes Executor ?",
                "options": [
                    "Simplicité de configuration",
                    "Coût réduit",
                    "Auto-scaling et isolation",
                    "Compatibilité Windows"
                ],
                "correct": 2,
                "explanation": "Le Kubernetes Executor offre l'auto-scaling automatique et une isolation forte via les pods."
            },
            
            # Chapitre 5: Variables et secrets (8 questions)
            {
                "id": 35,
                "chapter": "Variables et secrets",
                "question": "Comment définir une variable d'environnement dans un job ?",
                "options": [
                    "variables: MY_VAR: value",
                    "env: MY_VAR=value",
                    "export MY_VAR=value",
                    "set MY_VAR=value"
                ],
                "correct": 0,
                "explanation": "La section 'variables:' dans un job définit des variables d'environnement spécifiques."
            },
            {
                "id": 36,
                "chapter": "Variables et secrets",
                "question": "Quelle variable prédéfinie contient le SHA du commit ?",
                "options": [
                    "$CI_COMMIT_SHA",
                    "$CI_COMMIT_ID",
                    "$CI_COMMIT_HASH",
                    "$CI_COMMIT_REF"
                ],
                "correct": 0,
                "explanation": "$CI_COMMIT_SHA contient le SHA complet du commit qui a déclenché le pipeline."
            },
            {
                "id": 37,
                "chapter": "Variables et secrets",
                "question": "Comment sécuriser une variable sensible ?",
                "options": [
                    "La marquer comme 'Protected' et 'Masked'",
                    "La préfixer par SECRET_",
                    "L'encoder en base64",
                    "La stocker dans un fichier"
                ],
                "correct": 0,
                "explanation": "Les variables 'Protected' et 'Masked' dans GitLab assurent la sécurité des données sensibles."
            },
            {
                "id": 38,
                "chapter": "Variables et secrets",
                "question": "Quel est l'ordre de priorité des variables ?",
                "options": [
                    "Global > Job > Runner",
                    "Runner > Job > Global",
                    "Job > Runner > Global",
                    "Job > Global > Runner"
                ],
                "correct": 3,
                "explanation": "L'ordre de priorité est: Job (highest) > Global > Runner (lowest)."
            },
            {
                "id": 39,
                "chapter": "Variables et secrets",
                "question": "Comment utiliser un fichier de variables ?",
                "options": [
                    "include: variables.env",
                    "variables: file: variables.env",
                    "source variables.env",
                    "Variables File dans l'interface GitLab"
                ],
                "correct": 3,
                "explanation": "L'interface GitLab permet d'uploader des fichiers de variables pour les configurations complexes."
            },
            {
                "id": 40,
                "chapter": "Variables et secrets",
                "question": "Quelle variable indique l'environnement de déploiement ?",
                "options": [
                    "$CI_DEPLOY_TARGET",
                    "$CI_ENVIRONMENT_NAME",
                    "$CI_STAGE",
                    "$CI_ENVIRONMENT_URL"
                ],
                "correct": 1,
                "explanation": "$CI_ENVIRONMENT_NAME contient le nom de l'environnement de déploiement défini."
            },
            {
                "id": 41,
                "chapter": "Variables et secrets",
                "question": "Comment éviter qu'une variable apparaisse dans les logs ?",
                "options": [
                    "hidden: true",
                    "secret: true",
                    "masked: true",
                    "private: true"
                ],
                "correct": 2,
                "explanation": "L'option 'Masked' dans GitLab empêche l'affichage de la variable dans les logs."
            },
            {
                "id": 42,
                "chapter": "Variables et secrets",
                "question": "Quelle variable contient l'URL du registry Docker ?",
                "options": [
                    "$CI_DOCKER_REGISTRY",
                    "$CI_REGISTRY",
                    "$CI_CONTAINER_REGISTRY",
                    "$CI_IMAGE_REGISTRY"
                ],
                "correct": 1,
                "explanation": "$CI_REGISTRY contient l'URL du Container Registry GitLab pour le projet."
            },
            
            # Chapitre 6: Intégration Docker (4 questions)
            {
                "id": 43,
                "chapter": "Intégration Docker",
                "question": "Quel service est nécessaire pour construire des images Docker ?",
                "options": [
                    "docker:20.10.16-dind",
                    "docker:latest",
                    "docker-compose:latest",
                    "buildkit:latest"
                ],
                "correct": 0,
                "explanation": "docker:20.10.16-dind (Docker-in-Docker) permet de construire des images dans GitLab CI/CD."
            },
            {
                "id": 44,
                "chapter": "Intégration Docker",
                "question": "Comment se connecter au GitLab Container Registry ?",
                "options": [
                    "docker auth $CI_REGISTRY",
                    "docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY",
                    "gitlab-ci login",
                    "docker connect gitlab"
                ],
                "correct": 1,
                "explanation": "La commande docker login avec les variables prédéfinies GitLab permet l'authentification."
            },
            {
                "id": 45,
                "chapter": "Intégration Docker",
                "question": "Quelle variable contient l'image du projet dans le registry ?",
                "options": [
                    "CI_REGISTRY_IMAGE",
                    "CI_PROJECT_IMAGE",
                    "CI_CONTAINER_IMAGE",
                    "CI_DOCKER_IMAGE"
                ],
                "correct": 0,
                "explanation": "$CI_REGISTRY_IMAGE contient le chemin complet de l'image dans le registry GitLab."
            },
            {
                "id": 46,
                "chapter": "Intégration Docker",
                "question": "Comment optimiser le build d'images Docker ?",
                "options": [
                    "Utiliser des images de base lourdes",
                    "Ignorer le .dockerignore",
                    "Multi-stage builds et cache layers",
                    "Rebuilder complètement à chaque fois"
                ],
                "correct": 2,
                "explanation": "Les multi-stage builds et le cache des layers Docker optimisent significativement les builds."
            },
            
            # Chapitre 7: Triggers et automatisation (4 questions)  
            {
                "id": 47,
                "chapter": "Triggers et automatisation",
                "question": "Comment configurer un pipeline programmé ?",
                "options": [
                    "Dans le fichier .gitlab-ci.yml",
                    "Avec un cron job système",
                    "Via l'interface GitLab CI/CD Schedules",
                    "Par email à GitLab"
                ],
                "correct": 2,
                "explanation": "Les pipelines programmés se configurent via l'interface GitLab dans CI/CD > Schedules."
            },
            {
                "id": 48,
                "chapter": "Triggers et automatisation",
                "question": "Comment déclencher un pipeline d'un autre projet ?",
                "options": [
                    "curl vers l'API GitLab",
                    "Les deux méthodes sont correctes",
                    "trigger: project: group/project",
                    "webhook externe"
                ],
                "correct": 1,
                "explanation": "On peut déclencher via la directive 'trigger:' ou via l'API REST GitLab."
            },
            {
                "id": 49,
                "chapter": "Triggers et automatisation",
                "question": "Quelle directive évite l'exécution sur des merge requests ?",
                "options": [
                    "except: merge_requests",
                    "when: never si $CI_MERGE_REQUEST_ID",
                    "only: [branches]",
                    "rules avec conditions"
                ],
                "correct": 3,
                "explanation": "Les 'rules:' avec des conditions offrent le contrôle le plus fin des déclencheurs."
            },
            {
                "id": 50,
                "chapter": "Triggers et automatisation",
                "question": "Comment implémenter un rollback automatique ?",
                "options": [
                    "rollback: auto",
                    "auto_rollback: true",
                    "when: on_failure dans un job de rollback",
                    "C'est impossible"
                ],
                "correct": 2,
                "explanation": "Un job avec 'when: on_failure' peut implémenter la logique de rollback automatique."
            }
        ]
        
        # Statistiques par chapitre
        self.chapter_stats = {}
        
    def display_welcome(self):
        """Affiche le message de bienvenue"""
        print("="*80)
        print("            QUIZ GITLAB CI/CD - SPRINT 2 SEMAINE 3 SÉANCE 1")
        print("="*80)
        print("Cours: Introduction GitLab CI/CD")
        print("Questions: 50 questions couvrant tous les concepts")
        print("Temps recommandé: 25-30 minutes")
        print("Chapitres couverts:")
        print("   • Introduction CI/CD et GitLab")
        print("   • Premier pipeline GitLab CI/CD") 
        print("   • Jobs, stages et artifacts")
        print("   • GitLab Runners et exécuteurs")
        print("   • Variables et secrets")
        print("   • Intégration Docker")
        print("   • Triggers et automatisation")
        print("="*80)
        print()
        
    def display_question(self, question: Dict, question_num: int) -> int:
        """Affiche une question et récupère la réponse"""
        print(f"Question {question_num}/50 - Chapitre: {question['chapter']}")
        print(f"{question['question']}")
        print()
        
        for i, option in enumerate(question['options']):
            print(f"  {chr(65+i)}. {option}")
        print()
        
        while True:
            try:
                answer = input("Votre réponse (A, B, C, D): ").upper().strip()
                if answer in ['A', 'B', 'C', 'D']:
                    return ord(answer) - ord('A')
                else:
                    print("Veuillez saisir A, B, C ou D")
            except KeyboardInterrupt:
                print("\n\nQuiz interrompu par l'utilisateur")
                exit(0)
    
    def check_answer(self, question: Dict, user_answer: int) -> bool:
        """Vérifie la réponse et affiche l'explication"""
        correct = question['correct']
        is_correct = user_answer == correct
        
        if is_correct:
            print("Correct!")
            self.score += 1
        else:
            print(f"Incorrect. La bonne réponse était {chr(65 + correct)}.")
        
        print(f"{question['explanation']}")
        print("-" * 80)
        print()
        
        # Mise à jour des statistiques par chapitre
        chapter = question['chapter']
        if chapter not in self.chapter_stats:
            self.chapter_stats[chapter] = {'correct': 0, 'total': 0}
        
        self.chapter_stats[chapter]['total'] += 1
        if is_correct:
            self.chapter_stats[chapter]['correct'] += 1
            
        return is_correct
    
    def display_progress(self, current: int, total: int):
        """Affiche la progression"""
        if current % 10 == 0 and current > 0:
            progress = (current / total) * 100
            print(f"Progression: {current}/{total} questions ({progress:.0f}%)")
            print(f"Score actuel: {self.score}/{current} ({(self.score/current)*100:.1f}%)")
            print()
    
    def calculate_grade(self) -> Tuple[str, str]:
        """Calcule la note et l'appréciation"""
        percentage = (self.score / len(self.questions)) * 100
        
        if percentage >= 90:
            return "A+", "Excellent! Maîtrise parfaite de GitLab CI/CD"
        elif percentage >= 80:
            return "A", "Très bien! Très bonne compréhension des concepts"
        elif percentage >= 70:
            return "B+", "Bien! Bonne maîtrise avec quelques points à revoir"
        elif percentage >= 60:
            return "B", "Assez bien! Compréhension correcte mais à approfondir"
        elif percentage >= 50:
            return "C", "Passable! Révision nécessaire des concepts de base"
        else:
            return "D", "Insuffisant! Révision complète du cours recommandée"
    
    def display_chapter_stats(self):
        """Affiche les statistiques par chapitre"""
        print("STATISTIQUES PAR CHAPITRE")
        print("="*60)
        
        for chapter, stats in self.chapter_stats.items():
            percentage = (stats['correct'] / stats['total']) * 100
            status = "OK" if percentage >= 70 else "Attention" if percentage >= 50 else "A revoir"
            print(f"{status} {chapter:<35} {stats['correct']}/{stats['total']} ({percentage:.1f}%)")
        print()
    
    def display_recommendations(self):
        """Affiche des recommandations personnalisées"""
        print("RECOMMANDATIONS PERSONNALISÉES")
        print("="*50)
        
        weak_chapters = []
        for chapter, stats in self.chapter_stats.items():
            percentage = (stats['correct'] / stats['total']) * 100
            if percentage < 70:
                weak_chapters.append(chapter)
        
        if not weak_chapters:
            print("Excellente maîtrise sur tous les chapitres!")
            print("Vous êtes prêt(e) pour les LABs pratiques")
        else:
            print("Chapitres à réviser en priorité:")
            for chapter in weak_chapters:
                print(f"   • {chapter}")
            
            print("\nRessources recommandées:")
            if "Introduction CI/CD" in weak_chapters:
                print("   • Revoir les concepts fondamentaux du CI/CD")
                print("   • Comprendre l'architecture GitLab")
            if "Premier pipeline" in weak_chapters:
                print("   • Pratiquer la syntaxe YAML")
                print("   • Réaliser le LAB 1")
            if "Jobs et stages" in weak_chapters:
                print("   • Comprendre les artifacts et le cache")
                print("   • Réaliser le LAB 2")
            if "GitLab Runners" in weak_chapters:
                print("   • Étudier les différents types de runners")
                print("   • Comprendre les exécuteurs Docker")
            if "Variables et secrets" in weak_chapters:
                print("   • Maîtriser la gestion des variables")
                print("   • Comprendre la sécurité des secrets")
            if "Intégration Docker" in weak_chapters:
                print("   • Pratiquer Docker-in-Docker")
                print("   • Réaliser le LAB 3")
            if "Triggers et automatisation" in weak_chapters:
                print("   • Comprendre les déclencheurs")
                print("   • Étudier l'automatisation avancée")
        print()
    
    def save_results(self):
        """Sauvegarde les résultats du quiz"""
        results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'score': self.score,
            'total': len(self.questions),
            'percentage': (self.score / len(self.questions)) * 100,
            'duration': time.time() - self.start_time,
            'chapter_stats': self.chapter_stats,
            'user_answers': self.user_answers
        }
        
        try:
            with open('S2_S3_S1_quiz_introduction_gitlab_ci_results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print("Résultats sauvegardés dans S2_S3_S1_quiz_introduction_gitlab_ci_results.json")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
    
    def run_quiz(self, randomize: bool = True):
        """Lance le quiz complet"""
        self.display_welcome()
        
        # Demander à l'utilisateur ses préférences
        mode = input("Mode de quiz:\n1. Questions aléatoires (recommandé)\n2. Ordre des chapitres\nVotre choix (1 ou 2): ").strip()
        randomize = mode != "2"
        
        if randomize:
            print("Mode aléatoire activé")
            random.shuffle(self.questions)
        else:
            print("Mode séquentiel par chapitre")
        
        input("\nAppuyez sur Entrée pour commencer le quiz...")
        print("\n" + "="*80)
        
        self.start_time = time.time()
        
        # Boucle principale du quiz
        for i, question in enumerate(self.questions, 1):
            self.display_progress(i-1, len(self.questions))
            
            user_answer = self.display_question(question, i)
            is_correct = self.check_answer(question, user_answer)
            
            # Sauvegarder la réponse
            self.user_answers.append({
                'question_id': question['id'],
                'user_answer': user_answer,
                'correct_answer': question['correct'],
                'is_correct': is_correct
            })
            
            # Pause entre les questions (sauf la dernière)
            if i < len(self.questions):
                input("Appuyez sur Entrée pour la question suivante...")
                print()
        
        # Affichage des résultats finaux
        self.display_final_results()
    
    def display_final_results(self):
        """Affiche les résultats finaux"""
        duration = time.time() - self.start_time
        percentage = (self.score / len(self.questions)) * 100
        grade, appreciation = self.calculate_grade()
        
        print("="*80)
        print("                            RÉSULTATS FINAUX")
        print("="*80)
        print(f"Score: {self.score}/{len(self.questions)} ({percentage:.1f}%)")
        print(f"Note: {grade}")
        print(f"Appréciation: {appreciation}")
        print(f"Temps total: {duration//60:.0f}m {duration%60:.0f}s")
        print()
        
        # Seuil de validation Framework HASSAN
        if percentage >= 72:
            print("VALIDATION RÉUSSIE! (Seuil: 72%)")
            print("Vous maîtrisez les concepts de GitLab CI/CD")
            print("Vous pouvez passer à la séance suivante")
        else:
            print("VALIDATION ÉCHOUÉE (Seuil: 72%)")
            print("Révisez les concepts suivants et refaites le quiz")
        print()
        
        self.display_chapter_stats()
        self.display_recommendations()
        
        # Sauvegarde
        save_option = input("Souhaitez-vous sauvegarder vos résultats? (o/n): ").lower().strip()
        if save_option in ['o', 'oui', 'y', 'yes']:
            self.save_results()
        
        print("\n🎓 Merci d'avoir participé au quiz GitLab CI/CD!")
        print("N'hésitez pas à refaire le quiz pour améliorer votre score!")
        print("Prochaine étape: Réalisez les LABs pratiques!")

def main():
    """Fonction principale"""
    try:
        quiz = GitLabCIQuiz()
        quiz.run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrompu. À bientôt!")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        print("Veuillez relancer le quiz.")

if __name__ == "__main__":
    main()