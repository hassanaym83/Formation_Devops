#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==================================================================================
Simplon Maghreb - Formation DevOps
Sprint 1 - Semaine 1 - Séance 6 
Quiz: Services avancés et automatisation
==================================================================================
Durée estimée: 15 minutes
Note de passage: 11/15 (72%)
Instructions: Choisissez la meilleure réponse pour chaque question
"""

import json
import os
from datetime import datetime
import random

class QuizSeance6:
    def __init__(self):
        self.questions = self.load_questions()
        self.score = 0
        self.total_questions = len(self.questions)
        self.user_answers = []
        self.start_time = datetime.now()
        
    def load_questions(self):
        """Questions sur les services avancés et l'automatisation"""
        return [
            {
                "id": 1,
                "question": "Quel est l'avantage principal d'utiliser systemd par rapport aux scripts init traditionnels?",
                "options": [
                    "A) Démarrage séquentiel plus rapide",
                    "B) Parallélisation du démarrage et gestion des dépendances",
                    "C) Moins d'utilisation mémoire",
                    "D) Compatible uniquement avec Ubuntu"
                ],
                "correct": "B",
                "explanation": "systemd permet le démarrage parallèle des services et gère automatiquement les dépendances entre services, accélérant le boot."
            },
            {
                "id": 2, 
                "question": "Dans un fichier service systemd, que signifie Type=forking?",
                "options": [
                    "A) Le service reste au premier plan",
                    "B) Le service se lance puis se met en arrière-plan",
                    "C) Le service s'exécute une seule fois",
                    "D) Le service redémarre automatiquement"
                ],
                "correct": "B",
                "explanation": "Type=forking indique que le processus principal va créer un processus enfant puis se terminer, laissant l'enfant en arrière-plan."
            },
            {
                "id": 3,
                "question": "Quelle directive systemd permet de redémarrer automatiquement un service en cas d'échec?",
                "options": [
                    "A) AutoRestart=yes",
                    "B) Restart=always", 
                    "C) RestartSec=10",
                    "D) FailureAction=restart"
                ],
                "correct": "B",
                "explanation": "Restart=always configure systemd pour redémarrer le service automatiquement en cas d'arrêt inattendu."
            },
            {
                "id": 4,
                "question": "Comment créer un timer systemd qui s'exécute toutes les heures?",
                "options": [
                    "A) OnCalendar=hourly",
                    "B) OnCalendar=*:00:00",
                    "C) OnCalendar=0/1:00",
                    "D) OnCalendar=every-hour"
                ],
                "correct": "A",
                "explanation": "OnCalendar=hourly est la syntaxe systemd pour une exécution toutes les heures (équivalent à *:00:00)."
            },
            {
                "id": 5,
                "question": "Quelle commande permet de voir les prochaines exécutions programmées des timers?",
                "options": [
                    "A) systemctl show-timers",
                    "B) systemctl list-timers",
                    "C) systemctl timer-status",
                    "D) systemctl get-timers"
                ],
                "correct": "B",
                "explanation": "systemctl list-timers affiche tous les timers actifs avec leurs prochaines exécutions et dernières exécutions."
            },
            {
                "id": 6,
                "question": "Dans systemd, que permet la directive WantedBy=multi-user.target?",
                "options": [
                    "A) Le service démarre seulement en mode graphique",
                    "B) Le service démarre automatiquement au démarrage système",
                    "C) Le service peut être utilisé par plusieurs utilisateurs",
                    "D) Le service nécessite plusieurs processeurs"
                ],
                "correct": "B",
                "explanation": "WantedBy=multi-user.target fait que le service sera démarré automatiquement quand le système atteint le niveau multi-utilisateur."
            },
            {
                "id": 7,
                "question": "Quel est l'avantage des systemd timers par rapport à cron?",
                "options": [
                    "A) Syntaxe plus courte",
                    "B) Intégration avec les logs systemd et gestion centralisée",
                    "C) Moins de consommation CPU", 
                    "D) Compatible avec tous les systèmes Unix"
                ],
                "correct": "B",
                "explanation": "Les timers systemd s'intègrent parfaitement avec journald pour les logs et permettent une gestion centralisée avec systemctl."
            },
            {
                "id": 8,
                "question": "Comment surveiller en temps réel les logs d'un service nommé 'myapp'?",
                "options": [
                    "A) tail -f /var/log/myapp.log",
                    "B) systemctl logs myapp -f",
                    "C) journalctl -u myapp -f",
                    "D) systemd-logs myapp --follow"
                ],
                "correct": "C",
                "explanation": "journalctl -u myapp -f suit en temps réel les logs du service 'myapp' via le système de logs systemd."
            },
            {
                "id": 9,
                "question": "Quelle méthode est recommandée pour automatiser la surveillance système?",
                "options": [
                    "A) Scripts shell avec cron uniquement",
                    "B) Combinaison de scripts, services systemd et timers",
                    "C) Applications GUI seulement", 
                    "D) Surveillance manuelle quotidienne"
                ],
                "correct": "B",
                "explanation": "L'approche moderne combine scripts automatisés, services systemd pour la gestion et timers pour la planification."
            },
            {
                "id": 10,
                "question": "Dans un script de monitoring, quel seuil CPU est généralement considéré comme critique?",
                "options": [
                    "A) 50%",
                    "B) 70%",
                    "C) 90%",
                    "D) 99%"
                ],
                "correct": "C",
                "explanation": "Un usage CPU de 90%+ est généralement considéré critique car il laisse peu de marge pour les pics d'activité."
            },
            {
                "id": 11,
                "question": "Quelle directive systemd permet de définir les dépendances d'un service?",
                "options": [
                    "A) Needs=",
                    "B) After=",
                    "C) Requires=", 
                    "D) DependsOn="
                ],
                "correct": "C",
                "explanation": "Requires= définit une dépendance forte: si le service requis échoue, le service courant s'arrête aussi."
            },
            {
                "id": 12,
                "question": "Comment redémarrer tous les services systemd après modification des fichiers?",
                "options": [
                    "A) systemctl restart-all",
                    "B) systemctl daemon-reload",
                    "C) systemctl refresh-services",
                    "D) systemctl reload-systemd"
                ],
                "correct": "B",
                "explanation": "systemctl daemon-reload recharge la configuration systemd et prend en compte les modifications des fichiers de service."
            },
            {
                "id": 13,
                "question": "Quel format de temps systemd permet d'exécuter une tâche tous les lundi à 9h?", 
                "options": [
                    "A) OnCalendar=Mon 09:00:00",
                    "B) OnCalendar=Monday-9:00",
                    "C) OnCalendar=weekly-monday-09",
                    "D) OnCalendar=1-09:00:00"
                ],
                "correct": "A",
                "explanation": "OnCalendar=Mon 09:00:00 utilise la syntaxe systemd pour programmer une exécution chaque lundi à 9h00."
            },
            {
                "id": 14,
                "question": "Dans l'automatisation DevOps, que permet principalement l'Infrastructure as Code (IaC)?",
                "options": [
                    "A) Écrire du code plus rapidement",
                    "B) Gérer l'infrastructure de façon reproductible et versionnée",
                    "C) Réduire les coûts de développement",
                    "D) Augmenter la sécurité automatiquement"
                ],
                "correct": "B",
                "explanation": "L'IaC permet de gérer l'infrastructure comme du code: versioning, reproductibilité, cohérence entre environnements."
            },
            {
                "id": 15,
                "question": "Quelle est la bonne pratique pour les logs d'automatisation?",
                "options": [
                    "A) Logs uniquement en cas d'erreur",
                    "B) Logs verbeux pour tout",
                    "C) Logs structurés avec niveaux (INFO, WARNING, ERROR)",
                    "D) Pas de logs pour éviter l'encombrement"
                ],
                "correct": "C", 
                "explanation": "Des logs structurés avec différents niveaux permettent un debugging efficace tout en évitant le spam inutile."
            }
        ]
    
    def display_question(self, q):
        """Affiche une question avec ses options"""
        print(f"\n" + "="*60)
        print(f"Question {q['id']}/{self.total_questions}")
        print("="*60)
        print(f"\n{q['question']}\n")
        
        for option in q['options']:
            print(f"  {option}")
        print()
    
    def get_user_answer(self):
        """Récupère la réponse de l'utilisateur"""
        while True:
            try:
                answer = input("Votre réponse (A, B, C, ou D): ").upper().strip()
                if answer in ['A', 'B', 'C', 'D']:
                    return answer
                else:
                    print("Veuillez entrer A, B, C ou D")
            except KeyboardInterrupt:
                print("\n\nQuiz interrompu par l'utilisateur.")
                return None
    
    def check_answer(self, question, user_answer):
        """Vérifie la réponse et affiche l'explication"""
        is_correct = user_answer == question['correct']
        
        if is_correct:
            print(f"Correct! Bonne réponse: {question['correct']}")
            self.score += 1
        else:
            print(f"Incorrect. Bonne réponse: {question['correct']}")
        
        print(f"Explication: {question['explanation']}")
        
        return is_correct
    
    def run_quiz(self):
        """Exécute le quiz complet"""
        print("=" * 70)
        print("QUIZ SÉANCE 6: SERVICES AVANCÉS ET AUTOMATISATION")
        print("=" * 70)
        print(f"Nombre de questions: {self.total_questions}")
        print(f"Temps estimé: 20 minutes")
        print(f"Note de passage: 12/{self.total_questions}")
        print("\nInstructions: Pour chaque question, choisissez la meilleure réponse (A, B, C ou D)")
        print("\nAppuyez sur Entrée pour commencer...")
        input()
        
        # Mélanger les questions pour éviter la mémorisation
        questions_shuffled = self.questions.copy()
        random.shuffle(questions_shuffled)
        
        # Poser chaque question
        for i, question in enumerate(questions_shuffled):
            self.display_question(question)
            user_answer = self.get_user_answer()
            
            if user_answer is None:  # Quiz interrompu
                return
            
            is_correct = self.check_answer(question, user_answer)
            
            # Sauvegarder la réponse
            self.user_answers.append({
                'question_id': question['id'],
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': question['correct'],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
            
            # Pause entre les questions
            if i < len(questions_shuffled) - 1:
                input("\nAppuyez sur Entrée pour la question suivante...")
        
        # Afficher les résultats
        self.show_results()
    
    def show_results(self):
        """Affiche les résultats finaux du quiz"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        percentage = (self.score / self.total_questions) * 100
        
        print("\n" + "="*70)
        print("RÉSULTATS DU QUIZ")
        print("="*70)
        
        print(f"\nScore final: {self.score}/{self.total_questions} ({percentage:.1f}%)")
        print(f"Temps écoulé: {duration.seconds//60}min {duration.seconds%60}s")
        
        # Déterminer le niveau
        if percentage >= 80:
            level = "Excellent"
            comment = "Parfaite maîtrise des services systemd et de l'automatisation!"
        elif percentage >= 60:
            level = "Bien" 
            comment = "Bonne compréhension, quelques révisions sur les points manqués."
        elif percentage >= 40:
            level = "Passable"
            comment = "Bases acquises mais nécessite plus de pratique."
        else:
            level = "Insuffisant"
            comment = "Il est recommandé de revoir le cours avant de continuer."
        
        print(f"\nNiveau: {level}")
        print(f"Commentaire: {comment}")
        
        # Note de passage
        if self.score >= 11:
            print("\nFélicitations! Vous avez réussi le quiz!")
            print("Vous pouvez passer à la séance suivante.")
        else:
            print(f"\nNote de passage non atteinte (minimum: 11/{self.total_questions})")
            print("Il est recommandé de réviser le cours et de refaire le quiz.")
        
        # Proposer la sauvegarde
        self.offer_save_results()
    
    def show_detailed_review(self):
        """Affiche une révision détaillée des réponses"""
        print("\n" + "="*70)
        print("RÉVISION DÉTAILLÉE")
        print("="*70)
        
        for i, answer in enumerate(self.user_answers, 1):
            status = "CORRECT" if answer['is_correct'] else "INCORRECT"
            print(f"\n{status} - Question {i}: {answer['question']}")
            print(f"   Votre réponse: {answer['user_answer']}")
            print(f"   Bonne réponse: {answer['correct_answer']}")
            if not answer['is_correct']:
                print(f"   Explication: {answer['explanation']}")
    
    def offer_save_results(self):
        """Propose de sauvegarder les résultats"""
        try:
            save = input("\nVoulez-vous sauvegarder vos résultats? (o/n): ").lower().strip()
            if save in ['o', 'oui', 'y', 'yes']:
                self.save_results()
            
            review = input("Voulez-vous voir la révision détaillée? (o/n): ").lower().strip()
            if review in ['o', 'oui', 'y', 'yes']:
                self.show_detailed_review()
                
        except KeyboardInterrupt:
            print("\nAu revoir!")
    
    def save_results(self):
        """Sauvegarde les résultats dans un fichier JSON"""
        try:
            results = {
                'date': self.start_time.isoformat(),
                'score': self.score,
                'total_questions': self.total_questions,
                'percentage': (self.score / self.total_questions) * 100,
                'duration_seconds': (datetime.now() - self.start_time).total_seconds(),
                'answers': self.user_answers
            }
            
            filename = f"quiz_seance6_results_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"Résultats sauvegardés dans: {filename}")
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")

def main():
    """Fonction principale"""
    try:
        quiz = QuizSeance6()
        quiz.run_quiz()
        
    except KeyboardInterrupt:
        print("\n\nQuiz interrompu. À bientôt!")
        
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        print("Veuillez relancer le quiz.")

if __name__ == "__main__":
    main()
