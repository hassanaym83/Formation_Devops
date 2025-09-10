#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QUIZ - Gestion des Processus et Services
Séance 2 - Sprint 1 - Fondations DevOps

Framework Hassan - Quiz de validation des connaissances
15 questions - Seuil de validation : 72% (11/15)
Durée recommandée : 20 minutes
"""

import random
import json
from datetime import datetime

class QuizProcessusServices:
    def __init__(self):
        self.score = 0
        self.total_questions = 15
        self.seuil_validation = 0.72
        self.questions = self.init_questions()
        self.reponses_utilisateur = []
        
    def init_questions(self):
        """
        Questions conformes au Framework Hassan
        Couvrent tous les concepts de la séance
        """
        return [
            {
                "id": 1,
                "question": "Quelle commande permet d'afficher tous les processus en cours d'exécution avec leurs détails ?",
                "options": [
                    "a) ps",
                    "b) ps aux",
                    "c) top",
                    "d) htop"
                ],
                "reponse_correcte": "b",
                "explication": "ps aux affiche tous les processus de tous les utilisateurs avec des informations détaillées",
                "niveau": "fondamental"
            },
            {
                "id": 2,
                "question": "Quel signal est envoyé par défaut avec la commande 'kill PID' ?",
                "options": [
                    "a) SIGKILL (9)",
                    "b) SIGTERM (15)",
                    "c) SIGSTOP (19)",
                    "d) SIGHUP (1)"
                ],
                "reponse_correcte": "b",
                "explication": "kill envoie par défaut SIGTERM (15) qui permet au processus de se terminer proprement",
                "niveau": "fondamental"
            },
            {
                "id": 3,
                "question": "Comment démarrer un service nginx avec systemctl ?",
                "options": [
                    "a) systemctl start nginx",
                    "b) service nginx start",
                    "c) systemctl begin nginx",
                    "d) start nginx"
                ],
                "reponse_correcte": "a",
                "explication": "systemctl start [service] est la commande standard pour démarrer un service systemd",
                "niveau": "fondamental"
            },
            {
                "id": 4,
                "question": "Que signifie un processus en état 'D' dans la sortie de ps ?",
                "options": [
                    "a) Processus dormant",
                    "b) Processus en attente d'I/O non interruptible",
                    "c) Processus terminé",
                    "d) Processus en cours d'exécution"
                ],
                "reponse_correcte": "b",
                "explication": "L'état D indique un processus en sommeil non interruptible, souvent en attente d'opérations I/O",
                "niveau": "intermediaire"
            },
            {
                "id": 5,
                "question": "Quelle commande permet de voir les logs d'un service spécifique ?",
                "options": [
                    "a) tail /var/log/service.log",
                    "b) journalctl -u service_name",
                    "c) cat /var/log/messages",
                    "d) systemctl logs service_name"
                ],
                "reponse_correcte": "b",
                "explication": "journalctl -u [service] affiche les logs spécifiques d'un service systemd",
                "niveau": "intermediaire"
            },
            {
                "id": 6,
                "question": "Comment configurer un service pour qu'il démarre automatiquement au boot ?",
                "options": [
                    "a) systemctl start service",
                    "b) systemctl enable service",
                    "c) systemctl boot service",
                    "d) systemctl autostart service"
                ],
                "reponse_correcte": "b",
                "explication": "systemctl enable configure le service pour démarrer automatiquement au boot",
                "niveau": "fondamental"
            },
            {
                "id": 7,
                "question": "Que représente le load average 1.50 sur un système à 2 cœurs ?",
                "options": [
                    "a) Système surchargé",
                    "b) Système normal",
                    "c) Système sous-utilisé",
                    "d) Erreur de mesure"
                ],
                "reponse_correcte": "b",
                "explication": "Load average de 1.50 sur 2 cœurs = 75% d'utilisation, ce qui est normal",
                "niveau": "intermediaire"
            },
            {
                "id": 8,
                "question": "Quelle commande permet de tuer brutalement un processus qui ne répond pas ?",
                "options": [
                    "a) kill PID",
                    "b) kill -9 PID",
                    "c) killall process",
                    "d) stop PID"
                ],
                "reponse_correcte": "b",
                "explication": "kill -9 envoie SIGKILL qui termine immédiatement le processus sans possibilité de nettoyage",
                "niveau": "fondamental"
            },
            {
                "id": 9,
                "question": "Comment afficher les processus consommant le plus de CPU ?",
                "options": [
                    "a) ps aux | sort -k3",
                    "b) ps aux --sort=-%cpu",
                    "c) top -cpu",
                    "d) ps -cpu"
                ],
                "reponse_correcte": "b",
                "explication": "ps aux --sort=-%cpu trie les processus par consommation CPU décroissante",
                "niveau": "intermediaire"
            },
            {
                "id": 10,
                "question": "Que fait la commande 'systemctl reload service' ?",
                "options": [
                    "a) Redémarre le service",
                    "b) Recharge la configuration sans arrêter le service",
                    "c) Arrête le service",
                    "d) Affiche le statut du service"
                ],
                "reponse_correcte": "b",
                "explication": "reload recharge la configuration du service sans l'arrêter (si supporté)",
                "niveau": "intermediaire"
            },
            {
                "id": 11,
                "question": "Comment suivre les logs d'un service en temps réel ?",
                "options": [
                    "a) journalctl -u service",
                    "b) journalctl -u service -f",
                    "c) tail -f /var/log/service",
                    "d) watch journalctl -u service"
                ],
                "reponse_correcte": "b",
                "explication": "L'option -f (follow) permet de suivre les logs en temps réel",
                "niveau": "intermediaire"
            },
            {
                "id": 12,
                "question": "Quelle est la différence entre 'systemctl stop' et 'systemctl kill' ?",
                "options": [
                    "a) Aucune différence",
                    "b) stop envoie SIGTERM, kill envoie SIGKILL",
                    "c) stop est plus lent que kill",
                    "d) kill désactive le service au boot"
                ],
                "reponse_correcte": "b",
                "explication": "stop permet un arrêt propre avec SIGTERM, kill force l'arrêt avec SIGKILL",
                "niveau": "avance"
            },
            {
                "id": 13,
                "question": "Comment voir les services qui ont échoué au démarrage ?",
                "options": [
                    "a) systemctl status",
                    "b) systemctl list-units --failed",
                    "c) systemctl error",
                    "d) journalctl --failed"
                ],
                "reponse_correcte": "b",
                "explication": "list-units --failed affiche uniquement les unités en état d'échec",
                "niveau": "intermediaire"
            },
            {
                "id": 14,
                "question": "Que signifie un processus 'zombie' ?",
                "options": [
                    "a) Processus utilisant beaucoup de CPU",
                    "b) Processus terminé mais dont l'entrée reste dans la table",
                    "c) Processus en erreur",
                    "d) Processus suspendu"
                ],
                "reponse_correcte": "b",
                "explication": "Un zombie est un processus terminé dont le processus parent n'a pas lu le code de sortie",
                "niveau": "avance"
            },
            {
                "id": 15,
                "question": "Comment limiter l'affichage de journalctl aux erreurs seulement ?",
                "options": [
                    "a) journalctl --error",
                    "b) journalctl -p err",
                    "c) journalctl --level=error",
                    "d) journalctl -e"
                ],
                "reponse_correcte": "b",
                "explication": "L'option -p err filtre les logs par niveau de priorité (erreur et plus grave)",
                "niveau": "avance"
            }
        ]
    
    def afficher_question(self, question):
        """Affiche une question avec ses options"""
        print(f"\n{'='*60}")
        print(f"Question {question['id']}/15 - Niveau: {question['niveau']}")
        print(f"{'='*60}")
        print(f"\n{question['question']}\n")
        
        for option in question['options']:
            print(f"  {option}")
        print()
    
    def obtenir_reponse(self):
        """Obtient la réponse de l'utilisateur"""
        while True:
            reponse = input("Votre réponse (a, b, c, d) : ").lower().strip()
            if reponse in ['a', 'b', 'c', 'd']:
                return reponse
            print("Veuillez entrer une réponse valide (a, b, c, ou d)")
    
    def evaluer_reponse(self, question, reponse_utilisateur):
        """Évalue la réponse et affiche le feedback"""
        correct = reponse_utilisateur == question['reponse_correcte']
        
        if correct:
            print("✅ CORRECT !")
            self.score += 1
        else:
            print("❌ INCORRECT")
            print(f"La bonne réponse était : {question['reponse_correcte']}")
        
        print(f"\n💡 Explication : {question['explication']}")
        
        self.reponses_utilisateur.append({
            'question_id': question['id'],
            'reponse_donnee': reponse_utilisateur,
            'reponse_correcte': question['reponse_correcte'],
            'correct': correct
        })
        
        return correct
    
    def executer_quiz(self):
        """Exécute le quiz complet"""
        print("🎯 QUIZ - GESTION DES PROCESSUS ET SERVICES")
        print("=" * 50)
        print(f"📚 15 questions à répondre")
        print(f"⏱️  Durée recommandée : 20 minutes")
        print(f"✅ Seuil de validation : {int(self.seuil_validation * 100)}% ({int(self.seuil_validation * self.total_questions)}/{self.total_questions})")
        print("\nBonne chance ! 🚀")
        
        input("\nAppuyez sur Entrée pour commencer...")
        
        # Mélanger les questions pour plus de variété
        questions_melangees = self.questions.copy()
        random.shuffle(questions_melangees)
        
        for i, question in enumerate(questions_melangees):
            self.afficher_question(question)
            reponse = self.obtenir_reponse()
            self.evaluer_reponse(question, reponse)
            
            if i < len(questions_melangees) - 1:
                input("\nAppuyez sur Entrée pour la question suivante...")
        
        self.afficher_resultats()
    
    def afficher_resultats(self):
        """Affiche les résultats finaux"""
        pourcentage = (self.score / self.total_questions) * 100
        validation = pourcentage >= (self.seuil_validation * 100)
        
        print("\n" + "="*60)
        print("🏁 RÉSULTATS DU QUIZ")
        print("="*60)
        print(f"📊 Score : {self.score}/{self.total_questions} ({pourcentage:.1f}%)")
        print(f"🎯 Seuil : {int(self.seuil_validation * 100)}%")
        
        if validation:
            print("🎉 FÉLICITATIONS ! Quiz validé !")
            print("✅ Vous maîtrisez les concepts de gestion des processus et services")
        else:
            print("⚠️  Quiz non validé")
            print("📚 Révisez les concepts et retentez le quiz")
        
        # Analyse par niveau
        print(f"\n📈 ANALYSE DÉTAILLÉE :")
        niveaux = {'fondamental': [], 'intermediaire': [], 'avance': []}
        
        for reponse in self.reponses_utilisateur:
            question = next(q for q in self.questions if q['id'] == reponse['question_id'])
            niveaux[question['niveau']].append(reponse['correct'])
        
        for niveau, resultats in niveaux.items():
            if resultats:
                score_niveau = sum(resultats)
                total_niveau = len(resultats)
                pct_niveau = (score_niveau / total_niveau) * 100
                print(f"  {niveau.capitalize()} : {score_niveau}/{total_niveau} ({pct_niveau:.1f}%)")
        
        # Questions à revoir
        questions_incorrectes = [r for r in self.reponses_utilisateur if not r['correct']]
        if questions_incorrectes:
            print(f"\n📝 QUESTIONS À REVOIR :")
            for reponse in questions_incorrectes:
                question = next(q for q in self.questions if q['id'] == reponse['question_id'])
                print(f"  Q{question['id']} : {question['question'][:50]}...")
        
        self.sauvegarder_resultats(pourcentage, validation)
    
    def sauvegarder_resultats(self, pourcentage, validation):
        """Sauvegarde les résultats dans un fichier JSON"""
        resultats = {
            'timestamp': datetime.now().isoformat(),
            'score': self.score,
            'total': self.total_questions,
            'pourcentage': pourcentage,
            'validation': validation,
            'seuil': self.seuil_validation * 100,
            'details': self.reponses_utilisateur
        }
        
        filename = f"quiz_resultats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(resultats, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Résultats sauvegardés : {filename}")
        except Exception as e:
            print(f"\n⚠️  Erreur sauvegarde : {e}")

def main():
    """Fonction principale"""
    print("Framework Hassan - Quiz de Validation")
    print("Séance 2 : Gestion des Processus et Services")
    print("-" * 50)
    
    quiz = QuizProcessusServices()
    quiz.executer_quiz()

if __name__ == "__main__":
    main()
