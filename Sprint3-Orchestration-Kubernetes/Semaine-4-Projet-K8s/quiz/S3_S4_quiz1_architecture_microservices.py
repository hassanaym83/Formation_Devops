#!/usr/bin/env python3
"""
Quiz Interactif 1 - Architecture Microservices
Semaine 4 - Projet Kubernetes
Framework DevOps Hassan - Sprint 3+
"""

import random
import time
from datetime import datetime
from typing import List, Dict, Tuple

class MicroservicesQuiz:
    def __init__(self):
        self.score = 0
        self.total_questions = 7
        self.questions_answered = 0
        self.start_time = None
        self.responses = []
        
        # 🎯 Questions avec réponses et explications
        self.questions = [
            {
                "id": 1,
                "question": "Quel pattern architectural est le PLUS adapté pour décomposer une application monolithique en microservices ?",
                "options": [
                    "A) Model-View-Controller (MVC)",
                    "B) Domain-Driven Design (DDD)",
                    "C) Model-View-ViewModel (MVVM)",
                    "D) Layered Architecture"
                ],
                "correct": "B",
                "explanation": "Le Domain-Driven Design permet d'identifier les bounded contexts qui deviennent naturellement des microservices.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 2,
                "question": "Dans une architecture microservices Kubernetes, quelle méthode de communication est RECOMMANDÉE pour les appels synchrones ?",
                "options": [
                    "A) Direct Pod IP calls",
                    "B) Kubernetes Service DNS",
                    "C) Node IP with NodePort",
                    "D) Container-to-container networking"
                ],
                "correct": "B",
                "explanation": "Les Services Kubernetes avec DNS offrent load balancing et service discovery automatiques.",
                "points": 2,
                "difficulty": "Fondamental"
            },
            {
                "id": 3,
                "question": "Selon les principes microservices, comment DOIT être gérée la persistance des données ?",
                "options": [
                    "A) Une base de données partagée pour tous les services",
                    "B) Chaque service a sa propre base de données",
                    "C) Base de données centralisée avec schémas séparés",
                    "D) Fichiers partagés sur volume persistant"
                ],
                "correct": "B",
                "explanation": "Le pattern 'Database per Service' garantit l'indépendance et l'évolutivité des microservices.",
                "points": 2,
                "difficulty": "Fondamental"
            },
            {
                "id": 4,
                "question": "Dans Kubernetes, quel mécanisme assure automatiquement le service discovery ?",
                "options": [
                    "A) ConfigMaps",
                    "B) Secrets",
                    "C) DNS internal et Services",
                    "D) Ingress Controllers"
                ],
                "correct": "C",
                "explanation": "Kubernetes DNS résout automatiquement les noms de services vers leurs endpoints.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 5,
                "question": "Quel avantage principal offre un API Gateway dans une architecture microservices ?",
                "options": [
                    "A) Améliore les performances des bases de données",
                    "B) Centralise l'authentification et le routage",
                    "C) Réduit la consommation mémoire des pods",
                    "D) Accélère les déploiements Kubernetes"
                ],
                "correct": "B",
                "explanation": "L'API Gateway centralise les préoccupations transversales (auth, routing, rate limiting).",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 6,
                "question": "Quels patterns sont ESSENTIELS pour la résilience d'une architecture microservices ? (Plusieurs réponses possibles)",
                "options": [
                    "A) Circuit Breaker",
                    "B) Singleton Pattern",
                    "C) Retry with Exponential Backoff",
                    "D) Bulkhead Isolation",
                    "E) Observer Pattern"
                ],
                "correct": ["A", "C", "D"],
                "explanation": "Circuit Breaker, Retry et Bulkhead sont des patterns de résilience fondamentaux pour éviter les cascading failures.",
                "points": 3,
                "difficulty": "Avancé",
                "type": "multiple"
            },
            {
                "id": 7,
                "question": """Analysez cette configuration Kubernetes. Quels éléments assurent la haute disponibilité ?

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    spec:
      containers:
        - name: auth
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
```""",
                "options": [
                    "A) replicas: 3 uniquement",
                    "B) rollingUpdate strategy uniquement",
                    "C) readinessProbe et livenessProbe uniquement",
                    "D) replicas: 3, rollingUpdate, et health probes"
                ],
                "correct": "D",
                "explanation": "La combinaison de réplication, rolling updates et health checks assure la haute disponibilité complète.",
                "points": 3,
                "difficulty": "Avancé"
            }
        ]

    def display_header(self):
        """Affiche l'en-tête du quiz"""
        print("=" * 70)
        print("🏗️  QUIZ INTERACTIF 1 - ARCHITECTURE MICROSERVICES")
        print("   Semaine 4 - Projet Kubernetes | Framework DevOps Hassan")
        print("=" * 70)
        print("📋 Format: 7 questions | Durée: 15 min | Total: 16 points")
        print("🎯 Seuil de réussite: 12 points (75%)")
        print("=" * 70)

    def display_question(self, question: Dict) -> str:
        """Affiche une question et récupère la réponse"""
        print(f"\n📝 QUESTION {question['id']}/{self.total_questions}")
        print(f"🔹 Difficulté: {question['difficulty']} | Points: {question['points']}")
        print("-" * 50)
        print(f"{question['question']}")
        print()
        
        for option in question['options']:
            print(f"   {option}")
        
        print("-" * 50)
        
        if question.get('type') == 'multiple':
            print("⚠️  Question à choix multiples - Séparez vos réponses par des virgules (ex: A,C,D)")
            answer = input("Votre réponse: ").strip().upper()
            return answer
        else:
            while True:
                answer = input("Votre réponse (A, B, C, D ou E): ").strip().upper()
                if answer in ['A', 'B', 'C', 'D', 'E']:
                    return answer
                print("❌ Réponse invalide. Veuillez entrer A, B, C, D ou E.")

    def check_answer(self, question: Dict, user_answer: str) -> Tuple[bool, int]:
        """Vérifie la réponse et retourne (correct, points_earned)"""
        if question.get('type') == 'multiple':
            # Question à choix multiples
            user_answers = [ans.strip() for ans in user_answer.split(',')]
            correct_answers = set(question['correct'])
            user_answers_set = set(user_answers)
            
            if user_answers_set == correct_answers:
                return True, question['points']
            elif user_answers_set & correct_answers:
                # Partial credit
                partial_points = int(question['points'] * len(user_answers_set & correct_answers) / len(correct_answers))
                return False, partial_points
            else:
                return False, 0
        else:
            # Question à choix unique
            if user_answer == question['correct']:
                return True, question['points']
            else:
                return False, 0

    def display_result(self, question: Dict, user_answer: str, is_correct: bool, points_earned: int):
        """Affiche le résultat de la question"""
        if is_correct:
            print("\n✅ CORRECT!")
            print(f"🎉 +{points_earned} points")
        else:
            if points_earned > 0:
                print(f"\n🟡 PARTIELLEMENT CORRECT (+{points_earned} points)")
            else:
                print("\n❌ INCORRECT")
            
            if question.get('type') == 'multiple':
                print(f"Réponse correcte: {', '.join(question['correct'])}")
            else:
                print(f"Réponse correcte: {question['correct']}")
        
        print(f"💡 Explication: {question['explanation']}")
        print("-" * 50)

    def calculate_grade(self) -> Tuple[str, str, float]:
        """Calcule la note finale"""
        percentage = (self.score / 16) * 100
        
        if percentage >= 90:
            grade = "Excellent"
            emoji = "🏆"
        elif percentage >= 75:
            grade = "Très Bien"
            emoji = "🥇"
        elif percentage >= 60:
            grade = "Bien"
            emoji = "🥈"
        elif percentage >= 50:
            grade = "Passable"
            emoji = "🥉"
        else:
            grade = "Insuffisant"
            emoji = "📚"
        
        return grade, emoji, percentage

    def display_final_report(self):
        """Affiche le rapport final détaillé"""
        duration = time.time() - self.start_time
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        grade, emoji, percentage = self.calculate_grade()
        
        print("\n" + "=" * 70)
        print("📊 RAPPORT FINAL - QUIZ ARCHITECTURE MICROSERVICES")
        print("=" * 70)
        
        print(f"⏱️  Temps écoulé: {minutes:02d}:{seconds:02d}")
        print(f"📝 Questions répondues: {self.questions_answered}/{self.total_questions}")
        print(f"🎯 Score: {self.score}/16 points ({percentage:.1f}%)")
        print(f"🏅 Évaluation: {emoji} {grade}")
        
        print("\n📈 DÉTAIL PAR DIFFICULTÉ:")
        difficulty_stats = {}
        for i, response in enumerate(self.responses):
            difficulty = self.questions[i]['difficulty']
            if difficulty not in difficulty_stats:
                difficulty_stats[difficulty] = {'correct': 0, 'total': 0, 'points': 0}
            
            difficulty_stats[difficulty]['total'] += 1
            difficulty_stats[difficulty]['points'] += response['points_earned']
            if response['correct']:
                difficulty_stats[difficulty]['correct'] += 1
        
        for difficulty, stats in difficulty_stats.items():
            success_rate = (stats['correct'] / stats['total']) * 100
            print(f"  {difficulty}: {stats['correct']}/{stats['total']} ({success_rate:.0f}%) - {stats['points']} points")
        
        print("\n🎯 DOMAINES DE COMPÉTENCE:")
        domains = {
            "Architecture Patterns": [1],
            "Communication & Service Discovery": [2, 4],
            "Data Management": [3],
            "API Gateway": [5],
            "Resilience Patterns": [6],
            "Kubernetes HA": [7]
        }
        
        for domain, question_ids in domains.items():
            domain_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
            domain_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
            domain_percentage = (domain_score / domain_total) * 100
            status = "✅" if domain_percentage >= 75 else "🔄" if domain_percentage >= 50 else "❌"
            print(f"  {status} {domain}: {domain_score}/{domain_total} ({domain_percentage:.0f}%)")
        
        print("\n📚 RECOMMANDATIONS:")
        if percentage >= 75:
            print("🎉 Excellente maîtrise de l'architecture microservices!")
            print("   → Prêt pour les défis de production")
            print("   → Approfondissez les patterns avancés")
        else:
            print("📖 Révision recommandée sur:")
            for domain, question_ids in domains.items():
                domain_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
                domain_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
                if (domain_score / domain_total) < 0.75:
                    print(f"   • {domain}")
        
        print(f"\n💯 CERTIFICATION:")
        if percentage >= 75:
            print(f"🏆 CERTIFIÉ - Architecture Microservices Kubernetes")
            print(f"   Score: {percentage:.1f}% | Date: {datetime.now().strftime('%d/%m/%Y')}")
        else:
            print(f"📚 Formation complémentaire recommandée")
            print(f"   Score actuel: {percentage:.1f}% | Objectif: 75%")
        
        print("=" * 70)

    def run_quiz(self):
        """Lance le quiz complet"""
        self.display_header()
        
        input("\n🚀 Appuyez sur Entrée pour commencer le quiz...")
        self.start_time = time.time()
        
        # Mélanger les questions (optionnel)
        questions_order = list(range(len(self.questions)))
        # random.shuffle(questions_order)  # Décommentez pour mélanger
        
        for i in questions_order:
            question = self.questions[i]
            user_answer = self.display_question(question)
            is_correct, points_earned = self.check_answer(question, user_answer)
            
            self.responses.append({
                'question_id': question['id'],
                'user_answer': user_answer,
                'correct': is_correct,
                'points_earned': points_earned
            })
            
            self.score += points_earned
            self.questions_answered += 1
            
            self.display_result(question, user_answer, is_correct, points_earned)
            
            if i < len(questions_order) - 1:
                input("Appuyez sur Entrée pour la question suivante...")
        
        self.display_final_report()

def main():
    """Fonction principale"""
    print("🔧 Initialisation du Quiz Architecture Microservices...")
    time.sleep(1)
    
    quiz = MicroservicesQuiz()
    
    try:
        quiz.run_quiz()
    except KeyboardInterrupt:
        print("\n\n⚠️  Quiz interrompu par l'utilisateur")
        print(f"Score partiel: {quiz.score} points")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        print("Veuillez relancer le quiz")

if __name__ == "__main__":
    main()