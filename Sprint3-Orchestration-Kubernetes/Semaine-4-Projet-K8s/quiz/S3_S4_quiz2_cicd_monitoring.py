#!/usr/bin/env python3
"""
Quiz Interactif 2 - CI/CD et Monitoring
Semaine 4 - Projet Kubernetes
Framework DevOps Hassan - Sprint 3+
"""

import random
import time
from datetime import datetime
from typing import List, Dict, Tuple

class CICDMonitoringQuiz:
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
                "question": "Dans un pipeline GitLab CI/CD pour microservices, quelle stratégie est OPTIMALE pour le build ?",
                "options": [
                    "A) Build tous les services à chaque commit",
                    "B) Build uniquement les services modifiés",
                    "C) Build séquentiel service par service",
                    "D) Build manuel pour chaque service"
                ],
                "correct": "B",
                "explanation": "Le build conditionnel basé sur les changements optimise le temps et les ressources, évite les builds inutiles.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 2,
                "question": "Pour déployer des microservices dans Kubernetes, où doivent être stockées les images Docker ?",
                "options": [
                    "A) Directement dans les nodes Kubernetes",
                    "B) Sur le filesystem local du runner GitLab",
                    "C) Dans un Container Registry (GitLab, Docker Hub, ECR)",
                    "D) Dans un volume persistant Kubernetes"
                ],
                "correct": "C",
                "explanation": "Un Container Registry centralisé permet de distribuer les images vers tous les nodes du cluster de manière sécurisée.",
                "points": 2,
                "difficulty": "Fondamental"
            },
            {
                "id": 3,
                "question": "Quel avantage principal offre Kustomize pour les déploiements microservices multi-environnements ?",
                "options": [
                    "A) Compilation des images Docker",
                    "B) Gestion des configurations par overlay",
                    "C) Monitoring des performances",
                    "D) Test unitaire automatisé"
                ],
                "correct": "B",
                "explanation": "Kustomize permet de personnaliser les manifests Kubernetes par environnement (dev/staging/prod) sans duplication de code.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 4,
                "question": "Dans une architecture microservices, comment Prometheus découvre-t-il automatiquement les services à monitorer ?",
                "options": [
                    "A) Configuration manuelle des endpoints",
                    "B) Kubernetes Service Discovery",
                    "C) Parsing des logs d'application",
                    "D) Base de données de configuration"
                ],
                "correct": "B",
                "explanation": "Prometheus utilise l'API Kubernetes pour découvrir automatiquement les services et pods via les annotations.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 5,
                "question": "Quelles métriques sont ESSENTIELLES pour monitorer un microservice ? (Plusieurs réponses possibles)",
                "options": [
                    "A) Request rate (RPS)",
                    "B) Error rate (%)",
                    "C) Response time (latency)",
                    "D) Code coverage (%)",
                    "E) Memory usage"
                ],
                "correct": ["A", "B", "C", "E"],
                "explanation": "Les métriques RED (Rate, Errors, Duration) + ressources système sont fondamentales pour l'observabilité microservices.",
                "points": 2,
                "difficulty": "Intermédiaire",
                "type": "multiple"
            },
            {
                "id": 6,
                "question": """Analysez cette requête PromQL pour un dashboard Grafana. Que mesure-t-elle ?

```promql
rate(http_requests_total{status=~"5.."}[5m]) /
rate(http_requests_total[5m]) * 100
```""",
                "options": [
                    "A) Latence moyenne des requêtes HTTP",
                    "B) Nombre total de requêtes par seconde",
                    "C) Pourcentage d'erreurs serveur (5xx)",
                    "D) Utilisation CPU des services"
                ],
                "correct": "C",
                "explanation": "Cette requête calcule le ratio d'erreurs serveur (status 5xx) sur le total des requêtes, multiplié par 100 pour obtenir un pourcentage.",
                "points": 3,
                "difficulty": "Avancé"
            },
            {
                "id": 7,
                "question": "Pour une architecture microservices en production, quelle stratégie d'alerting est RECOMMANDÉE ?",
                "options": [
                    "A) Alertes uniquement sur les erreurs critiques",
                    "B) Alertes sur chaque métrique disponible",
                    "C) Alertes basées sur les SLIs (Service Level Indicators)",
                    "D) Alertes manuelles déclenchées par l'équipe"
                ],
                "correct": "C",
                "explanation": "Les alertes basées sur les SLIs permettent de se concentrer sur l'impact utilisateur réel et évitent la fatigue d'alertes.",
                "points": 3,
                "difficulty": "Avancé"
            }
        ]

    def display_header(self):
        """Affiche l'en-tête du quiz"""
        print("=" * 70)
        print("🔄 QUIZ INTERACTIF 2 - CI/CD ET MONITORING")
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
            print("⚠️  Question à choix multiples - Séparez vos réponses par des virgules (ex: A,B,C)")
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
        print("📊 RAPPORT FINAL - QUIZ CI/CD ET MONITORING")
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
            "GitLab CI/CD Strategies": [1],
            "Container Registry & Images": [2],
            "Kustomize & GitOps": [3],
            "Prometheus Service Discovery": [4],
            "Microservices Metrics": [5],
            "PromQL & Grafana": [6],
            "Alerting Strategies": [7]
        }
        
        for domain, question_ids in domains.items():
            domain_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
            domain_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
            domain_percentage = (domain_score / domain_total) * 100
            status = "✅" if domain_percentage >= 75 else "🔄" if domain_percentage >= 50 else "❌"
            print(f"  {status} {domain}: {domain_score}/{domain_total} ({domain_percentage:.0f}%)")
        
        print("\n📚 RECOMMANDATIONS:")
        if percentage >= 75:
            print("🎉 Excellente maîtrise du CI/CD et monitoring!")
            print("   → Prêt pour l'implémentation production")
            print("   → Explorez l'observabilité avancée (tracing, SLO)")
        else:
            print("📖 Révision recommandée sur:")
            weak_domains = []
            for domain, question_ids in domains.items():
                domain_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
                domain_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
                if (domain_score / domain_total) < 0.75:
                    weak_domains.append(domain)
            
            for domain in weak_domains:
                print(f"   • {domain}")
            
            if not weak_domains:
                print("   • Révision générale recommandée")
        
        print(f"\n💼 COMPÉTENCES PROFESSIONNELLES:")
        professional_skills = {
            "DevOps Pipeline Design": [1, 2, 3],
            "Observability Implementation": [4, 5, 6],
            "Production Monitoring": [7]
        }
        
        for skill, question_ids in professional_skills.items():
            skill_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
            skill_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
            skill_percentage = (skill_score / skill_total) * 100
            level = "Expert" if skill_percentage >= 90 else "Confirmé" if skill_percentage >= 75 else "Débutant"
            print(f"  📊 {skill}: {level} ({skill_percentage:.0f}%)")
        
        print(f"\n💯 CERTIFICATION:")
        if percentage >= 75:
            print(f"🏆 CERTIFIÉ - CI/CD et Monitoring Kubernetes")
            print(f"   Score: {percentage:.1f}% | Date: {datetime.now().strftime('%d/%m/%Y')}")
            print(f"   ✅ Compétent pour projets production")
        else:
            print(f"📚 Formation complémentaire recommandée")
            print(f"   Score actuel: {percentage:.1f}% | Objectif: 75%")
            print(f"   🎯 Focus: GitLab CI/CD, Prometheus, Grafana")
        
        print("=" * 70)

    def run_quiz(self):
        """Lance le quiz complet"""
        self.display_header()
        
        input("\n🚀 Appuyez sur Entrée pour commencer le quiz...")
        self.start_time = time.time()
        
        # Ordre des questions (peut être mélangé)
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
    print("🔧 Initialisation du Quiz CI/CD et Monitoring...")
    time.sleep(1)
    
    quiz = CICDMonitoringQuiz()
    
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