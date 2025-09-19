#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz Séance 2 - Automation et Monitoring DevOps
Durée : 15 minutes
Seuil de réussite : 72% (11/15 points minimum)
"""

import random
import time
from datetime import datetime

class QuizAutomationMonitoring:
 def __init__(self):
 self.questions = self._init_questions()
 self.score = 0
 self.total_questions = len(self.questions)
 self.responses = []
 self.start_time = None
 
 def _init_questions(self):
 """Initialise les 15 questions du quiz avec 4 choix chacune"""
 return [
 {
 "id": 1,
 "question": "Quel est l'objectif principal d'un script de déploiement multi-environnement ?",
 "choices": [
 "A) Automatiser uniquement les tests unitaires",
 "B) Gérer les déploiements vers différents environnements (dev, staging, production) de manière cohérente",
 "C) Surveiller les performances système en temps réel",
 "D) Créer des sauvegardes de base de données"
 ],
 "correct": "B",
 "explanation": "Un script de déploiement multi-environnement vise à automatiser et standardiser les déploiements vers différents environnements tout en maintenant la cohérence."
 },
 {
 "id": 2,
 "question": "Dans un contexte DevOps, que signifie 'rollback intelligent' ?",
 "choices": [
 "A) Supprimer définitivement la version qui pose problème",
 "B) Revenir automatiquement à la version précédente stable en cas d'échec, avec validation des dépendances",
 "C) Redémarrer tous les services simultanément",
 "D) Créer une nouvelle version corrective immédiatement"
 ],
 "correct": "B",
 "explanation": "Le rollback intelligent inclut la détection automatique d'échecs, la sélection de la version stable précédente et la validation des dépendances avant restauration."
 },
 {
 "id": 3,
 "question": "Quelle méthode bash permet de gérer proprement les erreurs dans un script critique ?",
 "choices": [
 "A) Ignorer les codes de retour avec || true",
 "B) Utiliser set -euo pipefail pour arrêter le script en cas d'erreur",
 "C) Capturer toutes les erreurs avec try/catch",
 "D) Rediriger stderr vers /dev/null"
 ],
 "correct": "B",
 "explanation": "set -euo pipefail active le mode strict : -e (exit on error), -u (error on undefined var), -o pipefail (exit on pipe failure)."
 },
 {
 "id": 4,
 "question": "Dans un système de monitoring, quel est le rôle des 'health checks' ?",
 "choices": [
 "A) Vérifier uniquement l'espace disque disponible",
 "B) Tester la disponibilité et le bon fonctionnement des services de manière proactive",
 "C) Analyser les logs d'erreurs passées",
 "D) Mesurer uniquement la charge CPU"
 ],
 "correct": "B",
 "explanation": "Les health checks permettent de détecter proactivement les problèmes de services (disponibilité, performance, fonctionnalité) avant qu'ils n'impactent les utilisateurs."
 },
 {
 "id": 5,
 "question": "Quelle approche est recommandée pour la collecte de métriques en monitoring DevOps ?",
 "choices": [
 "A) Collecter uniquement quand un problème est détecté",
 "B) Collecter en continu avec seuils d'alerte configurables et stockage temporisé",
 "C) Surveiller manuellement les indicateurs chaque heure",
 "D) Enregistrer seulement les erreurs critiques"
 ],
 "correct": "B",
 "explanation": "Le monitoring efficace nécessite une collecte continue, des seuils configurables pour déclencher des alertes et un stockage historique pour l'analyse de tendances."
 },
 {
 "id": 6,
 "question": "Dans une architecture REST API, quel mécanisme améliore les performances et réduit la charge serveur ?",
 "choices": [
 "A) Augmenter la fréquence des requêtes",
 "B) Implémenter du cache avec TTL et validation de fraîcheur des données",
 "C) Désactiver tous les logs d'accès",
 "D) Utiliser uniquement des requêtes POST"
 ],
 "correct": "B",
 "explanation": "Le cache avec TTL (Time To Live) permet de stocker temporairement les réponses, réduisant les appels serveur tout en maintenant la fraîcheur des données."
 },
 {
 "id": 7,
 "question": "Quel est l'avantage principal des webhooks dans l'intégration d'APIs ?",
 "choices": [
 "A) Permettre la communication asynchrone et événementielle entre services",
 "B) Chiffrer automatiquement tous les échanges de données",
 "C) Réduire la taille des réponses HTTP",
 "D) Remplacer complètement les requêtes GET"
 ],
 "correct": "A",
 "explanation": "Les webhooks permettent aux services de notifier automatiquement d'autres services lors d'événements, évitant le polling constant et améliorant la réactivité."
 },
 {
 "id": 8,
 "question": "Dans un script de monitoring, comment gérer efficacement les alertes pour éviter le spam ?",
 "choices": [
 "A) Envoyer une alerte pour chaque métrique collectée",
 "B) Implémenter des niveaux d'alerte (WARNING, CRITICAL) avec seuils différenciés et groupement",
 "C) Désactiver toutes les notifications automatiques",
 "D) Alerter seulement une fois par jour"
 ],
 "correct": "B",
 "explanation": "Un système d'alertes efficace utilise des niveaux hiérarchiques (WARNING, CRITICAL) avec seuils appropriés et peut grouper les alertes similaires pour éviter la surcharge."
 },
 {
 "id": 9,
 "question": "Quelle technique améliore la fiabilité d'un client REST API face aux erreurs réseau ?",
 "choices": [
 "A) Augmenter uniquement le timeout des requêtes",
 "B) Implémenter un mécanisme de retry avec backoff exponentiel",
 "C) Ignorer toutes les erreurs HTTP 5xx",
 "D) Utiliser exclusivement des connexions synchrones"
 ],
 "correct": "B",
 "explanation": "Le retry avec backoff exponentiel permet de retenter les requêtes échouées avec des délais croissants, améliorant les chances de succès sans surcharger le serveur."
 },
 {
 "id": 10,
 "question": "Dans l'orchestration de services, pourquoi la gestion des dépendances est-elle critique ?",
 "choices": [
 "A) Pour réduire l'utilisation mémoire des services",
 "B) Pour garantir l'ordre de démarrage et la cohérence du système complet",
 "C) Pour améliorer uniquement les performances de déploiement",
 "D) Pour simplifier les interfaces utilisateur"
 ],
 "correct": "B",
 "explanation": "La gestion des dépendances assure que les services démarrent dans le bon ordre (ex: DB avant API) et maintient la cohérence de l'architecture distribuée."
 },
 {
 "id": 11,
 "question": "Quel indicateur de performance est le plus pertinent pour évaluer la santé d'une API REST ?",
 "choices": [
 "A) Uniquement le nombre de requêtes par seconde",
 "B) La combinaison temps de réponse, taux d'erreur et disponibilité",
 "C) Seulement l'utilisation CPU du serveur",
 "D) Le nombre total de lignes de code"
 ],
 "correct": "B",
 "explanation": "La santé d'une API se mesure par plusieurs indicateurs complémentaires : temps de réponse (performance), taux d'erreur (fiabilité) et disponibilité (accessibilité)."
 },
 {
 "id": 12,
 "question": "Dans un système de déploiement automatisé, que permet la validation des seuils (thresholds) ?",
 "choices": [
 "A) Détecter automatiquement les anomalies et déclencher des actions correctives",
 "B) Calculer uniquement les coûts d'infrastructure",
 "C) Générer des rapports de conformité",
 "D) Optimiser la syntaxe du code source"
 ],
 "correct": "A",
 "explanation": "Les seuils permettent de détecter automatiquement quand les métriques dépassent des valeurs acceptables et de déclencher des actions (alertes, auto-remediation, etc.)."
 },
 {
 "id": 13,
 "question": "Quelle est la meilleure pratique pour sécuriser les webhooks en production ?",
 "choices": [
 "A) Utiliser uniquement des URLs publiques sans authentification",
 "B) Valider les signatures HMAC-SHA256 et vérifier l'origine des requêtes",
 "C) Accepter tous les payloads sans validation",
 "D) Stocker les secrets dans les URLs"
 ],
 "correct": "B",
 "explanation": "La sécurisation des webhooks nécessite la validation de signatures cryptographiques (HMAC-SHA256) et la vérification de l'origine pour éviter les attaques."
 },
 {
 "id": 14,
 "question": "Dans l'auto-remediation, quelle stratégie de recovery est la plus appropriée pour un service web surchargé ?",
 "choices": [
 "A) Redémarrer immédiatement tous les services",
 "B) Analyser la cause (CPU, mémoire, réseau) et appliquer la stratégie adaptée (restart, scale-up, load balancing)",
 "C) Ignorer le problème jusqu'à intervention manuelle",
 "D) Désactiver définitivement le service"
 ],
 "correct": "B",
 "explanation": "L'auto-remediation efficace nécessite d'abord un diagnostic de la cause racine, puis l'application de la stratégie appropriée selon le contexte (ressources, architecture, criticité)."
 },
 {
 "id": 15,
 "question": "Quel avantage apporte un dashboard de monitoring temps réel dans l'écosystème DevOps ?",
 "choices": [
 "A) Réduire uniquement les coûts opérationnels",
 "B) Fournir une visibilité immédiate sur l'état du système et faciliter la prise de décision rapide",
 "C) Remplacer complètement les tests automatisés",
 "D) Générer automatiquement du code de correction"
 ],
 "correct": "B",
 "explanation": "Un dashboard temps réel offre une visibilité instantanée sur les métriques critiques, permettant aux équipes DevOps de détecter rapidement les problèmes et prendre des décisions éclairées."
 }
 ]
 
 def display_welcome(self):
 """Affiche l'écran d'accueil du quiz"""
 print("=" * 60)
 print(" QUIZ SÉANCE 2 - AUTOMATION ET MONITORING DEVOPS")
 print("=" * 60)
 print(f" Questions : {self.total_questions}")
 print("⏱️ Durée recommandée : 15 minutes")
 print(" Seuil de réussite : 72% (11/15 points minimum)")
 print("=" * 60)
 print()
 
 input("Appuyez sur Entrée pour commencer le quiz...")
 print()
 self.start_time = time.time()
 
 def ask_question(self, question):
 """Pose une question et récupère la réponse"""
 print(f"Question {question['id']}/15")
 print("-" * 40)
 print(f"❓ {question['question']}")
 print()
 
 for choice in question['choices']:
 print(f" {choice}")
 print()
 
 while True:
 answer = input("Votre réponse (A, B, C, ou D) : ").upper().strip()
 if answer in ['A', 'B', 'C', 'D']:
 return answer
 print(" Veuillez entrer A, B, C ou D")
 
 def check_answer(self, question, user_answer):
 """Vérifie la réponse et affiche le résultat"""
 is_correct = user_answer == question['correct']
 
 if is_correct:
 print(" Correct !")
 self.score += 1
 else:
 print(f" Incorrect. La bonne réponse était : {question['correct']}")
 
 print(f" Explication : {question['explanation']}")
 print()
 
 self.responses.append({
 'question_id': question['id'],
 'user_answer': user_answer,
 'correct_answer': question['correct'],
 'is_correct': is_correct
 })
 
 input("Appuyez sur Entrée pour continuer...")
 print()
 
 def display_results(self):
 """Affiche les résultats finaux du quiz"""
 end_time = time.time()
 duration = int(end_time - self.start_time)
 percentage = round((self.score / self.total_questions) * 100, 1)
 
 print("=" * 60)
 print(" RÉSULTATS DU QUIZ")
 print("=" * 60)
 print(f"⏱️ Temps écoulé : {duration//60}m {duration%60}s")
 print(f" Score : {self.score}/{self.total_questions} ({percentage}%)")
 print()
 
 # Détermination du résultat
 if percentage >= 72:
 print(" FÉLICITATIONS ! Quiz réussi !")
 print(" Vous maîtrisez les concepts d'automation et monitoring DevOps")
 else:
 print("📚 Quiz non validé - Révision recommandée")
 print(" Concentrez-vous sur les domaines suivants :")
 self._display_improvement_areas()
 
 print()
 self._display_detailed_results()
 
 def _display_improvement_areas(self):
 """Affiche les domaines à améliorer basés sur les réponses incorrectes"""
 incorrect_areas = []
 
 for response in self.responses:
 if not response['is_correct']:
 question = next(q for q in self.questions if q['id'] == response['question_id'])
 if 'déploiement' in question['question'].lower() or 'rollback' in question['question'].lower():
 incorrect_areas.append("Déploiement et Rollback")
 elif 'monitoring' in question['question'].lower() or 'métriques' in question['question'].lower():
 incorrect_areas.append("Monitoring et Métriques")
 elif 'api' in question['question'].lower() or 'webhook' in question['question'].lower():
 incorrect_areas.append("Intégration APIs")
 elif 'orchestration' in question['question'].lower() or 'dépendances' in question['question'].lower():
 incorrect_areas.append("Orchestration")
 
 # Suppression des doublons et affichage
 unique_areas = list(set(incorrect_areas))
 for area in unique_areas:
 print(f" • {area}")
 
 def _display_detailed_results(self):
 """Affiche le détail des réponses"""
 print(" DÉTAIL DES RÉPONSES")
 print("-" * 40)
 
 for i, response in enumerate(self.responses, 1):
 status = "" if response['is_correct'] else ""
 print(f"{status} Q{response['question_id']:2d}: {response['user_answer']} "
 f"{'(correct)' if response['is_correct'] else f'(correct: {response['correct_answer']})'}")
 
 def run_quiz(self):
 """Exécute le quiz complet"""
 self.display_welcome()
 
 # Mélange des questions pour varier l'ordre
 random.shuffle(self.questions)
 
 # Pose toutes les questions
 for question in self.questions:
 user_answer = self.ask_question(question)
 self.check_answer(question, user_answer)
 
 # Affichage des résultats
 self.display_results()
 
 # Sauvegarde des résultats
 self._save_results()
 
 def _save_results(self):
 """Sauvegarde les résultats dans un fichier"""
 try:
 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
 filename = f"/tmp/quiz_s2_results_{timestamp}.txt"
 
 with open(filename, 'w', encoding='utf-8') as f:
 f.write(f"Quiz Séance 2 - Automation et Monitoring DevOps\n")
 f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
 f.write(f"Score: {self.score}/{self.total_questions} ({(self.score/self.total_questions)*100:.1f}%)\n")
 f.write(f"Résultat: {'RÉUSSI' if (self.score/self.total_questions)*100 >= 72 else 'NON VALIDÉ'}\n\n")
 
 f.write("Détail des réponses:\n")
 for response in self.responses:
 question = next(q for q in self.questions if q['id'] == response['question_id'])
 f.write(f"Q{response['question_id']}: {question['question']}\n")
 f.write(f" Réponse: {response['user_answer']} {'✓' if response['is_correct'] else '✗'}\n")
 if not response['is_correct']:
 f.write(f" Correct: {response['correct_answer']}\n")
 f.write("\n")
 
 print(f" Résultats sauvegardés : {filename}")
 
 except Exception as e:
 print(f" Erreur sauvegarde : {e}")

def main():
 """Fonction principale"""
 try:
 quiz = QuizAutomationMonitoring()
 quiz.run_quiz()
 
 except KeyboardInterrupt:
 print("\n\n⏸️ Quiz interrompu par l'utilisateur")
 except Exception as e:
 print(f"\n Erreur inattendue : {e}")

if __name__ == "__main__":
 main()

# ====== INFORMATIONS QUIZ ======
# 📚 DOMAINES COUVERTS :
# • Déploiement multi-environnement et rollback intelligent
# • Monitoring système et health checks
# • Collecte de métriques et alerting
# • Intégration REST APIs et webhooks
# • Orchestration de services et gestion dépendances
# • Auto-remediation et recovery strategies
# • Sécurité des webhooks et validation
# • Dashboard temps-réel et visibilité

# CRITÈRES DE RÉUSSITE :
# • 15 questions QCM (4 choix par question)
# • Seuil de validation : 72% (11 bonnes réponses minimum)
# • Durée recommandée : 15 minutes
# • Explications détaillées pour chaque réponse
# • Sauvegarde automatique des résultats

# PÉDAGOGIE :
# • Questions alignées sur les LABs pratiques
# • Contexte DevOps exclusif (conformité Framework Hassan)
# • Progression logique des concepts simples aux avancés
# • Feedback immédiat avec explications
# • Domaines d'amélioration identifiés automatiquement