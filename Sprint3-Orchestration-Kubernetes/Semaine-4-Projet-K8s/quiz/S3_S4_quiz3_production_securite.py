#!/usr/bin/env python3
"""
Quiz Interactif 3 - Production et Sécurité
Semaine 4 - Projet Kubernetes
Framework DevOps Hassan - Sprint 3+
"""

import random
import time
from datetime import datetime
from typing import List, Dict, Tuple

class ProductionSecurityQuiz:
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
                "question": "Quelle métrique est PRINCIPALEMENT utilisée par le HPA Kubernetes pour décider du scaling ?",
                "options": [
                    "A) Nombre de connexions réseau",
                    "B) CPU et Memory utilization",
                    "C) Taille des logs générés",
                    "D) Nombre de requêtes totales"
                ],
                "correct": "B",
                "explanation": "Le HPA (Horizontal Pod Autoscaler) se base principalement sur l'utilisation CPU et mémoire, bien qu'il puisse aussi utiliser des métriques custom.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 2,
                "question": "Dans Kubernetes, quel est l'effet d'une NetworkPolicy sans règles ingress définies ?",
                "options": [
                    "A) Autorise tout le trafic entrant",
                    "B) Bloque tout le trafic entrant",
                    "C) Applique les règles par défaut du cluster",
                    "D) Ignore la politique réseau"
                ],
                "correct": "B",
                "explanation": "Une NetworkPolicy sans règles ingress bloque par défaut tout le trafic entrant vers les pods sélectionnés (deny-by-default).",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 3,
                "question": "Quel niveau de Pod Security Standard est RECOMMANDÉ pour des microservices en production ?",
                "options": [
                    "A) privileged",
                    "B) baseline",
                    "C) restricted",
                    "D) unrestricted"
                ],
                "correct": "C",
                "explanation": "Le niveau 'restricted' applique les meilleures pratiques de sécurité pour la production (non-root, read-only filesystem, etc.).",
                "points": 2,
                "difficulty": "Fondamental"
            },
            {
                "id": 4,
                "question": "Pour une stratégie de backup complète des microservices Kubernetes, que faut-il sauvegarder ?",
                "options": [
                    "A) Les pods en cours d'exécution uniquement",
                    "B) Les manifests Kubernetes et données persistantes",
                    "C) Les logs d'application uniquement",
                    "D) Les images Docker uniquement"
                ],
                "correct": "B",
                "explanation": "Il faut sauvegarder la configuration (manifests/YAML) et les données (volumes persistants) pour une recovery complète.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 5,
                "question": """Dans cet exemple RBAC, quelles permissions sont accordées ?

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: microservice-reader
rules:
  - apiGroups: ['']
    resources: ['configmaps', 'secrets']
    verbs: ['get', 'list']
```""",
                "options": [
                    "A) Lecture seule des ConfigMaps et Secrets",
                    "B) Écriture complète sur tous les objets",
                    "C) Administration du cluster",
                    "D) Accès aux logs des pods"
                ],
                "correct": "A",
                "explanation": "Ce rôle RBAC permet uniquement la lecture (get, list) des ConfigMaps et Secrets, suivant le principe du moindre privilège.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 6,
                "question": """Analysez cette configuration Velero. Quelle est la stratégie de rétention ?

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
spec:
  schedule: '0 2 * * *'
  template:
    ttl: 720h
    includedNamespaces:
      - microservices
```""",
                "options": [
                    "A) Backup quotidien gardé 720 jours",
                    "B) Backup quotidien gardé 30 jours",
                    "C) Backup hebdomadaire gardé 720 heures",
                    "D) Backup mensuel gardé 30 heures"
                ],
                "correct": "B",
                "explanation": "ttl: 720h = 30 jours (720÷24=30), avec schedule quotidien '0 2 * * *' (2h00 tous les jours).",
                "points": 3,
                "difficulty": "Avancé"
            },
            {
                "id": 7,
                "question": "Quelles mesures de sécurité sont CRITIQUES pour des microservices en production ? (Plusieurs réponses possibles)",
                "options": [
                    "A) Containers non-root users",
                    "B) Secrets management avec encryption",
                    "C) Network segmentation avec policies",
                    "D) Images de base Alpine Linux",
                    "E) Resource limits et quotas"
                ],
                "correct": ["A", "B", "C", "E"],
                "explanation": "Non-root users, secrets encryption, network policies et resource limits sont des mesures de sécurité critiques. Alpine est une bonne pratique mais pas critique.",
                "points": 3,
                "difficulty": "Avancé",
                "type": "multiple"
            }
        ]

    def display_header(self):
        """Affiche l'en-tête du quiz"""
        print("=" * 70)
        print("🔒 QUIZ INTERACTIF 3 - PRODUCTION ET SÉCURITÉ")
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
        print("📊 RAPPORT FINAL - QUIZ PRODUCTION ET SÉCURITÉ")
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
            "Autoscaling Production": [1],
            "Network Security": [2],
            "Pod Security Standards": [3],
            "Backup Strategies": [4],
            "RBAC & Permissions": [5],
            "Disaster Recovery": [6],
            "Security Best Practices": [7]
        }
        
        for domain, question_ids in domains.items():
            domain_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
            domain_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
            domain_percentage = (domain_score / domain_total) * 100
            status = "✅" if domain_percentage >= 75 else "🔄" if domain_percentage >= 50 else "❌"
            print(f"  {status} {domain}: {domain_score}/{domain_total} ({domain_percentage:.0f}%)")
        
        print("\n🔒 NIVEAU DE SÉCURITÉ:")
        security_score = 0
        security_total = 0
        security_questions = [2, 3, 5, 7]  # Questions liées à la sécurité
        
        for qid in security_questions:
            security_score += self.responses[qid-1]['points_earned']
            security_total += self.questions[qid-1]['points']
        
        security_percentage = (security_score / security_total) * 100
        
        if security_percentage >= 90:
            security_level = "🛡️  Expert Sécurité"
        elif security_percentage >= 75:
            security_level = "🔐 Sécurité Avancée"
        elif security_percentage >= 60:
            security_level = "🔒 Sécurité Intermédiaire"
        else:
            security_level = "⚠️  Sécurité à Renforcer"
        
        print(f"  {security_level}: {security_score}/{security_total} ({security_percentage:.0f}%)")
        
        print("\n📚 RECOMMANDATIONS:")
        if percentage >= 75:
            print("🎉 Excellente maîtrise de la sécurité production!")
            print("   → Prêt pour les déploiements critiques")
            print("   → Explorez les outils avancés (Falco, OPA Gatekeeper)")
        else:
            print("📖 Révision recommandée sur:")
            weak_domains = []
            for domain, question_ids in domains.items():
                domain_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
                domain_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
                if (domain_score / domain_total) < 0.75:
                    weak_domains.append(domain)
            
            for domain in weak_domains[:3]:  # Top 3 weak domains
                print(f"   • {domain}")
        
        print(f"\n🏢 CERTIFICATIONS SUGGÉRÉES:")
        if percentage >= 85:
            print("  🏆 Certified Kubernetes Security Specialist (CKS)")
            print("  🥇 AWS/Azure Security Certifications")
        elif percentage >= 70:
            print("  🥈 Certified Kubernetes Administrator (CKA)")
            print("  📚 Kubernetes Security Best Practices")
        else:
            print("  📖 Kubernetes Security Fundamentals")
            print("  🔧 Hands-on Security Labs")
        
        print(f"\n💯 CERTIFICATION:")
        if percentage >= 75:
            print(f"🏆 CERTIFIÉ - Production & Sécurité Kubernetes")
            print(f"   Score: {percentage:.1f}% | Date: {datetime.now().strftime('%d/%m/%Y')}")
            print(f"   ✅ Niveau production enterprise")
        else:
            print(f"📚 Formation sécurité recommandée")
            print(f"   Score actuel: {percentage:.1f}% | Objectif: 75%")
            print(f"   🎯 Focus: NetworkPolicies, RBAC, Pod Security")
        
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
    print("🔧 Initialisation du Quiz Production et Sécurité...")
    time.sleep(1)
    
    quiz = ProductionSecurityQuiz()
    
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