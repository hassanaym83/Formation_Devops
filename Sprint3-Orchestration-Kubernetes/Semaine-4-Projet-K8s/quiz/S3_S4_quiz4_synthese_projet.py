#!/usr/bin/env python3
"""
Quiz Interactif 4 - Synthèse Projet Microservices
Semaine 4 - Projet Kubernetes
Framework DevOps Hassan - Sprint 3+
"""

import random
import time
from datetime import datetime
from typing import List, Dict, Tuple

class ProjectSynthesisQuiz:
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
                "question": "Dans l'architecture DevOps Analytics Platform développée, quel service joue le rôle de point d'entrée principal ?",
                "options": [
                    "A) Auth Service",
                    "B) Metrics Collector",
                    "C) API Gateway (Nginx Ingress)",
                    "D) Alert Manager"
                ],
                "correct": "C",
                "explanation": "L'API Gateway (implémenté avec Nginx Ingress) centralise l'accès et route les requêtes vers les microservices appropriés selon les patterns établis.",
                "points": 2,
                "difficulty": "Fondamental"
            },
            {
                "id": 2,
                "question": "Dans la plateforme DevOps Analytics, quel est le flux de données CORRECT pour les métriques ?",
                "options": [
                    "A) Auth → Metrics Collector → TimescaleDB → Report Generator",
                    "B) Metrics Collector → PostgreSQL → Alert Manager → Reports",
                    "C) API Gateway → Auth → Redis → Reports",
                    "D) RabbitMQ → Alert Manager → PostgreSQL → Auth"
                ],
                "correct": "A",
                "explanation": "Le flux logique : authentification → collecte métriques → stockage time-series → génération de rapports analytiques.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 3,
                "question": "Pour gérer une charge 10x plus importante, quelle stratégie est PRIORITAIRE ?",
                "options": [
                    "A) Augmenter la taille des volumes persistants",
                    "B) Configurer HPA sur Metrics Collector",
                    "C) Ajouter plus de namespaces",
                    "D) Utiliser des images Docker plus petites"
                ],
                "correct": "B",
                "explanation": "Le Metrics Collector traite le plus gros volume de données et bénéficie le plus du scaling horizontal automatique via HPA.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 4,
                "question": "Quelle combinaison d'outils assure l'observabilité complète de la plateforme ?",
                "options": [
                    "A) Prometheus + Grafana + Logs",
                    "B) GitLab CI + Kubernetes Dashboard",
                    "C) Redis + RabbitMQ + PostgreSQL",
                    "D) Nginx + Docker + Helm"
                ],
                "correct": "A",
                "explanation": "Les 3 piliers de l'observabilité : métriques (Prometheus), visualisation (Grafana) et logs pour une vue complète du système.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 5,
                "question": "Pour déployer la plateforme en production, quelle séquence est CORRECTE ?",
                "options": [
                    "A) Services → Databases → Monitoring → CI/CD",
                    "B) Databases → Services → Monitoring → CI/CD",
                    "C) Monitoring → Databases → Services → CI/CD",
                    "D) CI/CD → Monitoring → Databases → Services"
                ],
                "correct": "B",
                "explanation": "Ordre logique de déploiement : infrastructure persistante (DB) → services applicatifs → observabilité → automatisation.",
                "points": 2,
                "difficulty": "Intermédiaire"
            },
            {
                "id": 6,
                "question": """Le service Alert Manager ne reçoit plus de métriques. Analysez cette sortie kubectl :

```bash
$ kubectl get pods -n microservices
NAME                            READY   STATUS    RESTARTS
auth-service-7d4b8f9c8d-xyz12   1/1     Running   0
metrics-collector-5c6d7e8f9-abc 0/1     Error     3
alert-manager-4b5c6d7e8f-def45  1/1     Running   0
```

Quelle est la cause PROBABLE ?""",
                "options": [
                    "A) Alert Manager est en panne",
                    "B) Metrics Collector ne peut pas démarrer",
                    "C) Auth Service bloque les métriques",
                    "D) Problème de réseau entre services"
                ],
                "correct": "B",
                "explanation": "Metrics Collector en Error avec 3 restarts indique un problème de démarrage du collecteur (config, connexion DB, ressources insuffisantes).",
                "points": 3,
                "difficulty": "Avancé"
            },
            {
                "id": 7,
                "question": "Pour faire évoluer la plateforme DevOps Analytics, quelles améliorations seraient PRIORITAIRES ? (Plusieurs réponses possibles)",
                "options": [
                    "A) Service Mesh (Istio) pour la sécurité avancée",
                    "B) Machine Learning pour l'analyse prédictive",
                    "C) Multi-cluster pour la haute disponibilité",
                    "D) Cache distribué pour les performances",
                    "E) Blockchain pour l'audit"
                ],
                "correct": ["A", "C", "D"],
                "explanation": "Service Mesh (sécurité/observabilité), multi-cluster (HA/DR) et cache distribué (performance) apportent des bénéfices opérationnels concrets et mesurables.",
                "points": 3,
                "difficulty": "Avancé",
                "type": "multiple"
            }
        ]

    def display_header(self):
        """Affiche l'en-tête du quiz"""
        print("=" * 70)
        print("🎯 QUIZ INTERACTIF 4 - SYNTHÈSE PROJET MICROSERVICES")
        print("   Semaine 4 - Projet Kubernetes | Framework DevOps Hassan")
        print("=" * 70)
        print("📋 Format: 7 questions | Durée: 15 min | Total: 16 points")
        print("🎯 Seuil de réussite: 12 points (75%)")
        print("🏆 Quiz final - Validation complète Semaine 4")
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
        print("📊 RAPPORT FINAL - QUIZ SYNTHÈSE PROJET MICROSERVICES")
        print("=" * 70)
        
        print(f"⏱️  Temps écoulé: {minutes:02d}:{seconds:02d}")
        print(f"📝 Questions répondues: {self.questions_answered}/{self.total_questions}")
        print(f"🎯 Score: {self.score}/16 points ({percentage:.1f}%)")
        print(f"🏅 Évaluation: {emoji} {grade}")
        
        print("\n📈 ANALYSE PAR COMPÉTENCE:")
        competency_areas = {
            "Architecture Système": [1, 2],
            "Scalabilité & Performance": [3, 4],
            "Déploiement Production": [5],
            "Troubleshooting": [6],
            "Vision Stratégique": [7]
        }
        
        for area, question_ids in competency_areas.items():
            area_score = sum(self.responses[qid-1]['points_earned'] for qid in question_ids)
            area_total = sum(self.questions[qid-1]['points'] for qid in question_ids)
            area_percentage = (area_score / area_total) * 100
            
            if area_percentage >= 80:
                status = "🌟 Maîtrisé"
            elif area_percentage >= 60:
                status = "✅ Acquis"
            elif area_percentage >= 40:
                status = "🔄 En cours"
            else:
                status = "❌ À revoir"
            
            print(f"  {status} {area}: {area_score}/{area_total} ({area_percentage:.0f}%)")
        
        print("\n🎓 ÉVALUATION SEMAINE 4 COMPLÈTE:")
        print("  📚 Quiz 1 - Architecture Microservices")
        print("  📚 Quiz 2 - CI/CD et Monitoring")
        print("  📚 Quiz 3 - Production et Sécurité")
        print(f"  🎯 Quiz 4 - Synthèse Projet: {self.score}/16 ({percentage:.0f}%)")
        print()
        print("  💼 Total Semaine 4: 64 points max")
        print("  🎯 Seuil certification: 48 points (75%)")
        
        print("\n🚀 COMPÉTENCES PROFESSIONNELLES:")
        if percentage >= 75:
            print("  🏆 Architecture de Solutions Microservices")
            print("  🥇 Déploiement Kubernetes Production")
            print("  🌟 Leadership Technique DevOps")
        elif percentage >= 60:
            print("  🥈 Développement Microservices")
            print("  📊 Opération Kubernetes")
            print("  🔧 Ingénierie DevOps")
        else:
            print("  📚 Fondamentaux Kubernetes")
            print("  🔧 Pratiques DevOps de base")
        
        print("\n🎯 PROCHAINES ÉTAPES:")
        if percentage >= 80:
            print("  🚀 Prêt pour projets enterprise complexes")
            print("  📈 Explorer Service Mesh et multi-cluster")
            print("  🎓 Préparer certifications avancées (CKS, CKA)")
        elif percentage >= 60:
            print("  📈 Approfondir troubleshooting production")
            print("  🔧 Pratiquer déploiements complexes")
            print("  📚 Étudier patterns microservices avancés")
        else:
            print("  📚 Réviser concepts fondamentaux")
            print("  🔧 Refaire les LABs pratiques")
            print("  👥 Demander accompagnement formateur")
        
        print("\n💯 CERTIFICATION FINALE:")
        if percentage >= 75:
            print(f"🏆 CERTIFIÉ - PROJET MICROSERVICES KUBERNETES")
            print(f"   Score final: {percentage:.1f}% | Date: {datetime.now().strftime('%d/%m/%Y')}")
            print(f"   ✅ Compétences validées niveau production")
            print(f"   🎯 Framework Hassan Sprint 3+ - RÉUSSI")
        else:
            print(f"📚 Certification en cours")
            print(f"   Score actuel: {percentage:.1f}% | Objectif: 75%")
            print(f"   🔄 Révision recommandée avant validation finale")
        
        print("\n🌟 MESSAGE FINAL:")
        if percentage >= 90:
            print("   Félicitations ! Maîtrise exceptionnelle des microservices")
            print("   Vous êtes prêt(e) pour les défis les plus complexes!")
        elif percentage >= 75:
            print("   Excellent travail ! Vous maîtrisez les concepts clés")
            print("   Prêt(e) pour l'application en contexte professionnel")
        else:
            print("   Continuez vos efforts ! Les bases sont posées")
            print("   La pratique vous mènera vers l'expertise")
        
        print("=" * 70)

    def run_quiz(self):
        """Lance le quiz complet"""
        self.display_header()
        
        input("\n🚀 Appuyez sur Entrée pour commencer le quiz final...")
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
    print("🔧 Initialisation du Quiz Final - Synthèse Projet...")
    time.sleep(1)
    
    quiz = ProjectSynthesisQuiz()
    
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