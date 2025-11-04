#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz 1 - Kubernetes Applications - Déploiement d'applications
Sprint 3 - Semaine 2 - Séance 1 & 2

Couvre : Application Deployment et Load Balancing/Ingress
"""

import random
import sys
from typing import List, Dict, Any

class QuizKubernetesApplications:
    def __init__(self):
        self.score = 0
        self.total_questions = 25
        self.questions = self._load_questions()
        self.seuil_validation = 0.72  # 72% requis pour validation Framework HASSAN
        
    def _load_questions(self) -> List[Dict[str, Any]]:
        """Charge les 25 questions du quiz"""
        return [
            {
                "question": "Quelle est la différence principale entre un Deployment et un Pod standalone ?",
                "options": [
                    "A) Un Deployment peut avoir plusieurs replicas",
                    "B) Un Pod standalone a une meilleure performance",
                    "C) Un Deployment assure la résilience et le scaling",
                    "D) Il n'y a pas de différence"
                ],
                "correct": "C",
                "explanation": "Un Deployment gère la résilience, le scaling, et les rolling updates via des ReplicaSets."
            },
            {
                "question": "Quel type de Service Kubernetes est recommandé pour une communication interne entre microservices ?",
                "options": [
                    "A) NodePort",
                    "B) LoadBalancer", 
                    "C) ClusterIP",
                    "D) ExternalName"
                ],
                "correct": "C",
                "explanation": "ClusterIP est optimal pour la communication interne car il fournit une IP stable accessible uniquement dans le cluster."
            },
            {
                "question": "Dans un manifeste Ingress, que fait l'annotation 'nginx.ingress.kubernetes.io/rate-limit: \"100\"' ?",
                "options": [
                    "A) Limite le nombre de connexions simultanées",
                    "B) Limite à 100 requêtes par minute par IP",
                    "C) Définit un timeout de 100 secondes",
                    "D) Configure 100 backends maximum"
                ],
                "correct": "B",
                "explanation": "Cette annotation limite le nombre de requêtes par minute par adresse IP source."
            },
            {
                "question": "Quelle est la fonction principale de cert-manager dans un cluster Kubernetes ?",
                "options": [
                    "A) Gérer les certificats SSL/TLS automatiquement",
                    "B) Chiffrer les communications inter-pods",
                    "C) Authentifier les utilisateurs",
                    "D) Gérer les secrets"
                ],
                "correct": "A",
                "explanation": "cert-manager automatise l'obtention et le renouvellement des certificats SSL/TLS, notamment via Let's Encrypt."
            },
            {
                "question": "Dans une architecture 3-tiers sur Kubernetes, comment doit-on exposer la base de données ?",
                "options": [
                    "A) Via un Service NodePort",
                    "B) Via un Service LoadBalancer",
                    "C) Via un Service ClusterIP uniquement",
                    "D) Directement via l'IP du Pod"
                ],
                "correct": "C",
                "explanation": "La base de données ne doit jamais être exposée à l'extérieur et doit utiliser ClusterIP pour l'accès interne."
            },
            {
                "question": "Quel est l'avantage principal d'utiliser des ConfigMaps plutôt que des variables d'environnement hardcodées ?",
                "options": [
                    "A) Meilleures performances",
                    "B) Sécurité renforcée",
                    "C) Séparation configuration/code et portabilité",
                    "D) Réduction de la taille des images"
                ],
                "correct": "C",
                "explanation": "Les ConfigMaps permettent de séparer la configuration du code, rendant l'application portable entre environnements."
            },
            {
                "question": "Dans un Ingress, que signifie 'pathType: Prefix' ?",
                "options": [
                    "A) Correspondance exacte du chemin",
                    "B) Correspondance du préfixe du chemin",
                    "C) Expression régulière",
                    "D) Redirection automatique"
                ],
                "correct": "B",
                "explanation": "pathType: Prefix fait correspondre toutes les URLs commençant par le chemin spécifié."
            },
            {
                "question": "Quelle est la meilleure pratique pour exposer une API backend dans une architecture microservices ?",
                "options": [
                    "A) Un Service NodePort par microservice",
                    "B) Un Ingress unique avec routage path-based",
                    "C) LoadBalancer pour chaque service",
                    "D) Accès direct aux Pods"
                ],
                "correct": "B",
                "explanation": "Un Ingress unique avec routage path-based centralise l'exposition et simplifie la gestion SSL/TLS."
            },
            {
                "question": "Comment peut-on implémenter un health check personnalisé pour une application web ?",
                "options": [
                    "A) Seulement via readinessProbe",
                    "B) Seulement via livenessProbe", 
                    "C) Via un endpoint HTTP dédié (/health)",
                    "D) Via les logs de l'application"
                ],
                "correct": "C",
                "explanation": "Un endpoint HTTP dédié comme /health permet des vérifications personnalisées de l'état applicatif."
            },
            {
                "question": "Dans quel cas utiliser un Service de type ExternalName ?",
                "options": [
                    "A) Pour exposer l'application à l'extérieur",
                    "B) Pour créer un alias vers un service externe",
                    "C) Pour équilibrer la charge",
                    "D) Pour la communication interne"
                ],
                "correct": "B",
                "explanation": "ExternalName crée un alias DNS vers un service externe au cluster (ex: base de données managée)."
            },
            {
                "question": "Quelle annotation Ingress permet de rediriger automatiquement HTTP vers HTTPS ?",
                "options": [
                    "A) nginx.ingress.kubernetes.io/ssl-redirect: \"true\"",
                    "B) nginx.ingress.kubernetes.io/force-ssl-redirect: \"true\"",
                    "C) nginx.ingress.kubernetes.io/redirect-to-https: \"true\"",
                    "D) nginx.ingress.kubernetes.io/tls-redirect: \"true\""
                ],
                "correct": "A",
                "explanation": "L'annotation ssl-redirect: \"true\" force la redirection automatique HTTP vers HTTPS."
            },
            {
                "question": "Comment configurer la persistance des données pour PostgreSQL dans Kubernetes ?",
                "options": [
                    "A) Utiliser un volume emptyDir",
                    "B) Utiliser un PersistentVolumeClaim",
                    "C) Stocker dans l'image Docker",
                    "D) Utiliser un volume hostPath"
                ],
                "correct": "B",
                "explanation": "PersistentVolumeClaim garantit la persistance des données même si le Pod est supprimé ou déplacé."
            },
            {
                "question": "Quel est le rôle du selector dans un Service Kubernetes ?",
                "options": [
                    "A) Définir le type de service",
                    "B) Identifier les Pods backend via leurs labels",
                    "C) Configurer le load balancing",
                    "D) Définir les ports d'écoute"
                ],
                "correct": "B",
                "explanation": "Le selector utilise les labels pour identifier quels Pods constituent les endpoints du Service."
            },
            {
                "question": "Dans une application multi-tiers, comment sécuriser la communication entre le frontend et l'API ?",
                "options": [
                    "A) Utiliser HTTPS seulement sur l'Ingress",
                    "B) Chiffrer avec TLS bout-en-bout",
                    "C) Utiliser des Network Policies",
                    "D) Toutes les réponses ci-dessus"
                ],
                "correct": "D",
                "explanation": "La sécurité en profondeur combine HTTPS, TLS interne, et Network Policies pour isolation réseau."
            },
            {
                "question": "Quelle est la différence entre startup, liveness et readiness probes ?",
                "options": [
                    "A) Elles ont toutes la même fonction",
                    "B) startup: démarrage lent, liveness: santé, readiness: prêt pour trafic",
                    "C) Elles ne sont utilisées que pour le debugging",
                    "D) startup et readiness sont identiques"
                ],
                "correct": "B",
                "explanation": "Chaque probe a un rôle spécifique dans le cycle de vie et la santé des Pods."
            },
            {
                "question": "Comment implémenter une stratégie de déploiement Blue/Green avec Kubernetes ?",
                "options": [
                    "A) Utiliser deux Deployments avec switch du Service selector",
                    "B) Utiliser un seul Deployment avec rolling update",
                    "C) Utiliser des DaemonSets",
                    "D) Modifier directement les Pods"
                ],
                "correct": "A",
                "explanation": "Blue/Green nécessite deux environnements complets avec basculement via modification du Service selector."
            },
            {
                "question": "Quel est l'avantage principal d'utiliser un Ingress Controller plutôt que des Services LoadBalancer ?",
                "options": [
                    "A) Meilleures performances",
                    "B) Un seul point d'entrée avec routage intelligent",
                    "C) Plus de sécurité",
                    "D) Support natif de Kubernetes"
                ],
                "correct": "B",
                "explanation": "Un Ingress centralise l'exposition avec routage avancé, SSL/TLS, et évite de multiplier les LoadBalancers."
            },
            {
                "question": "Comment partager une configuration commune entre plusieurs Deployments ?",
                "options": [
                    "A) Copier les variables dans chaque Deployment",
                    "B) Utiliser un ConfigMap partagé",
                    "C) Hardcoder dans les images",
                    "D) Utiliser des annotations"
                ],
                "correct": "B",
                "explanation": "Un ConfigMap peut être référencé par plusieurs Deployments pour partager la configuration."
            },
            {
                "question": "Dans un environnement de production, comment gérer les secrets de base de données ?",
                "options": [
                    "A) Les stocker en plain text dans ConfigMaps",
                    "B) Les hardcoder dans l'image Docker",
                    "C) Utiliser des Secrets Kubernetes avec RBAC",
                    "D) Les passer en paramètres de ligne de commande"
                ],
                "correct": "C",
                "explanation": "Les Secrets Kubernetes avec RBAC approprié offrent la meilleure sécurité pour les credentials."
            },
            {
                "question": "Quelle est la meilleure pratique pour gérer les logs d'une application multi-tiers ?",
                "options": [
                    "A) Stocker les logs dans des volumes locaux",
                    "B) Envoyer vers stdout/stderr pour collecte par Kubernetes",
                    "C) Écrire directement dans une base de données",
                    "D) Stocker dans des ConfigMaps"
                ],
                "correct": "B",
                "explanation": "Les logs vers stdout/stderr sont automatiquement collectés par Kubernetes et peuvent être centralisés."
            },
            {
                "question": "Comment s'assurer qu'un Pod ne reçoit du trafic qu'une fois complètement initialisé ?",
                "options": [
                    "A) Utiliser une livenessProbe",
                    "B) Utiliser une readinessProbe",
                    "C) Utiliser une startupProbe",
                    "D) Attendre un délai fixe"
                ],
                "correct": "B",
                "explanation": "La readinessProbe détermine si le Pod est prêt à recevoir du trafic via le Service."
            },
            {
                "question": "Dans une architecture microservices, comment gérer la découverte de services ?",
                "options": [
                    "A) Hardcoder les adresses IP",
                    "B) Utiliser des variables d'environnement",
                    "C) Utiliser le DNS interne de Kubernetes",
                    "D) Utiliser un registry externe"
                ],
                "correct": "C",
                "explanation": "Le DNS interne Kubernetes permet la découverte automatique via les noms de Services."
            },
            {
                "question": "Quel type de volume utiliser pour partager des fichiers entre conteneurs d'un même Pod ?",
                "options": [
                    "A) PersistentVolume",
                    "B) hostPath",
                    "C) emptyDir",
                    "D) configMap"
                ],
                "correct": "C",
                "explanation": "emptyDir est parfait pour partager des données temporaires entre conteneurs d'un même Pod."
            },
            {
                "question": "Comment implémenter un cache Redis partagé dans une architecture microservices ?",
                "options": [
                    "A) Un Redis par microservice",
                    "B) Un Deployment Redis avec Service ClusterIP",
                    "C) Redis en sidecar container",
                    "D) Redis directement dans l'image applicative"
                ],
                "correct": "B",
                "explanation": "Un Deployment Redis centralisé avec Service ClusterIP permet le partage entre tous les microservices."
            },
            {
                "question": "Quelle est la meilleure approche pour gérer les migrations de base de données dans Kubernetes ?",
                "options": [
                    "A) Les exécuter manuellement",
                    "B) Utiliser un Job Kubernetes pour les migrations",
                    "C) Les inclure dans le code applicatif",
                    "D) Utiliser un CronJob"
                ],
                "correct": "B",
                "explanation": "Un Job Kubernetes garantit l'exécution unique et contrôlée des migrations avant le déploiement applicatif."
            }
        ]
    
    def run_quiz(self):
        """Exécute le quiz complet"""
        print("=" * 80)
        print("🎯 QUIZ KUBERNETES APPLICATIONS - DÉPLOIEMENT")
        print("Sprint 3 - Semaine 2 - Séances 1 & 2")
        print("=" * 80)
        print(f"📋 {self.total_questions} questions - Seuil de validation: {self.seuil_validation:.0%}")
        print("=" * 80)
        
        # Mélanger les questions
        questions_melangees = random.sample(self.questions, self.total_questions)
        
        for i, q in enumerate(questions_melangees, 1):
            print(f"\n📝 Question {i}/{self.total_questions}")
            print("-" * 50)
            print(f"❓ {q['question']}")
            print()
            
            for option in q['options']:
                print(f"   {option}")
            
            reponse = input("\n👉 Votre réponse (A/B/C/D): ").strip().upper()
            
            if reponse == q['correct']:
                self.score += 1
                print("✅ Correct!")
            else:
                print(f"❌ Incorrect. La bonne réponse était: {q['correct']}")
            
            print(f"💡 Explication: {q['explanation']}")
            
            if i < self.total_questions:
                input("\n⏩ Appuyez sur Entrée pour continuer...")
        
        self._show_results()
    
    def _show_results(self):
        """Affiche les résultats finaux"""
        pourcentage = (self.score / self.total_questions) * 100
        
        print("\n" + "=" * 80)
        print("📊 RÉSULTATS DU QUIZ")
        print("=" * 80)
        print(f"📈 Score: {self.score}/{self.total_questions} ({pourcentage:.1f}%)")
        
        if pourcentage >= self.seuil_validation * 100:
            print("🎉 VALIDÉ! Vous maîtrisez le déploiement d'applications Kubernetes!")
            print("✅ Vous pouvez passer aux concepts de scaling et autoscaling.")
        else:
            print("📚 NON VALIDÉ. Révision recommandée sur:")
            print("   • Architecture multi-tiers sur Kubernetes")
            print("   • Configuration des Services et Ingress")
            print("   • Health checks et bonnes pratiques de déploiement")
            print("   • Gestion des ConfigMaps et Secrets")
        
        print("\n🎯 Concepts clés couverts:")
        print("   • Application Deployment et architecture 3-tiers")
        print("   • Services Kubernetes et découverte de services")
        print("   • Ingress Controllers et exposition externe")
        print("   • SSL/TLS automatique avec cert-manager")
        print("   • Health checks (startup, liveness, readiness)")
        print("   • Persistance des données et volumes")
        print("   • Sécurité et bonnes pratiques")
        
        print("=" * 80)

if __name__ == "__main__":
    quiz = QuizKubernetesApplications()
    try:
        quiz.run_quiz()
    except KeyboardInterrupt:
        print("\n\n⚠️  Quiz interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur durant le quiz: {e}")
        sys.exit(1)