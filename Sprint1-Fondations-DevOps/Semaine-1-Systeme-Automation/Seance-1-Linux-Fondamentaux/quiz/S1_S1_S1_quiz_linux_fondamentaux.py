#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 QUIZ - Linux Fondamentaux pour DevOps
Sprint 1 - Semaine 2 - Séance 1

Quiz interactif de validation des connaissances fondamentales Linux
dans le contexte DevOps.

Concepts évalués:
- Navigation système de fichiers
- Gestion fichiers et permissions
- Variables d'environnement 
- Commandes essentielles
- Bonnes pratiques DevOps

Format: QCM avec explications détaillées
Niveau: Débutant DevOps
"""

import random
import json
import os
from datetime import datetime

class LinuxDevOpsQuiz:
 """Quiz interactif Linux pour DevOps débutants"""
 
 def __init__(self):
 self.score = 0
 self.total_questions = 0
 self.questions_answered = []
 self.start_time = datetime.now()
 
 # Configuration couleurs pour terminal
 self.COLORS = {
 'HEADER': '\033[95m',
 'BLUE': '\033[94m',
 'GREEN': '\033[92m',
 'YELLOW': '\033[93m',
 'RED': '\033[91m',
 'BOLD': '\033[1m',
 'UNDERLINE': '\033[4m',
 'END': '\033[0m'
 }
 
 # Base de questions Linux DevOps
 self.questions = [
 {
 'id': 1,
 'category': 'Navigation système',
 'question': 'Quelle commande permet d\'afficher le répertoire de travail actuel ?',
 'options': [
 'ls -la',
 'pwd',
 'cd .',
 'whoami'
 ],
 'correct': 1,
 'explanation': 'pwd (Print Working Directory) affiche le chemin complet du répertoire actuel. Essential pour se repérer dans l\'arborescence système.'
 },
 {
 'id': 2,
 'category': 'Hiérarchie FHS',
 'question': 'Dans quelle hiérarchie FHS se trouvent généralement les logs système ?',
 'options': [
 '/etc/logs',
 '/home/logs',
 '/var/log',
 '/usr/log'
 ],
 'correct': 2,
 'explanation': '/var/log est le répertoire standard FHS pour les fichiers de logs. Crucial pour le monitoring en DevOps.'
 },
 {
 'id': 3,
 'category': 'Permissions Linux',
 'question': 'Que signifie la permission 755 sur un fichier ?',
 'options': [
 'rwxr-xr-x : propriétaire lecture/écriture/exécution, groupe et autres lecture/exécution',
 'rwx------ : seul le propriétaire a tous les droits',
 'rw-rw-rw- : tout le monde peut lire et écrire',
 'r--r--r-- : tout le monde peut seulement lire'
 ],
 'correct': 0,
 'explanation': '755 = rwxr-xr-x. Le propriétaire a tous les droits (7=rwx), groupe et autres ont lecture+exécution (5=r-x). Standard pour les scripts exécutables.'
 },
 {
 'id': 4,
 'category': 'Gestion fichiers',
 'question': 'Comment créer récursivement une structure de dossiers en une commande ?',
 'options': [
 'mkdir projet/config/env',
 'mkdir -p projet/config/env',
 'mkdir -r projet/config/env',
 'md projet/config/env'
 ],
 'correct': 1,
 'explanation': 'mkdir -p crée récursivement tous les dossiers parents nécessaires. Essentiel pour automatiser la création d\'arborescences projet.'
 },
 {
 'id': 5,
 'category': 'Variables environnement',
 'question': 'Comment définir une variable d\'environnement persistante pour tous les utilisateurs ?',
 'options': [
 'export VAR=valeur',
 'echo "export VAR=valeur" >> ~/.bashrc',
 'echo "export VAR=valeur" >> /etc/environment',
 'VAR=valeur'
 ],
 'correct': 2,
 'explanation': '/etc/environment définit des variables globales pour tous les utilisateurs. Méthode standard pour la configuration système en DevOps.'
 },
 {
 'id': 6,
 'category': 'Recherche fichiers',
 'question': 'Quelle commande trouve tous les fichiers .conf dans /etc et ses sous-dossiers ?',
 'options': [
 'ls /etc/*.conf',
 'find /etc -name "*.conf"',
 'grep .conf /etc',
 'locate /etc/*.conf'
 ],
 'correct': 1,
 'explanation': 'find /etc -name "*.conf" recherche récursivement tous les fichiers correspondant au motif. Crucial pour localiser les configurations système.'
 },
 {
 'id': 7,
 'category': 'Gestion processus',
 'question': 'Comment voir tous les processus en cours d\'exécution avec détails complets ?',
 'options': [
 'ps',
 'ps aux',
 'top',
 'htop'
 ],
 'correct': 1,
 'explanation': 'ps aux affiche tous les processus (a), utilisateurs (u) avec informations détaillées (x). Standard pour le monitoring système en DevOps.'
 },
 {
 'id': 8,
 'category': 'Redirection flux',
 'question': 'Comment rediriger à la fois stdout et stderr vers un fichier ?',
 'options': [
 'commande > fichier 2> fichier',
 'commande &> fichier',
 'commande >> fichier',
 'commande | tee fichier'
 ],
 'correct': 1,
 'explanation': '&> redirige stdout et stderr vers le même fichier. Essentiel pour capturer tous les outputs dans les scripts DevOps.'
 },
 {
 'id': 9,
 'category': 'Archives et compression',
 'question': 'Comment créer une archive tar.gz du dossier /var/www ?',
 'options': [
 'tar -cf backup.tar.gz /var/www',
 'tar -czf backup.tar.gz /var/www',
 'zip -r backup.tar.gz /var/www',
 'gzip /var/www'
 ],
 'correct': 1,
 'explanation': 'tar -czf crée (c) une archive compressée avec gzip (z) dans un fichier (f). Standard pour les sauvegardes en DevOps.'
 },
 {
 'id': 10,
 'category': 'Surveillance système',
 'question': 'Quelle commande affiche l\'utilisation des disques en format lisible ?',
 'options': [
 'ls -lh',
 'df -h',
 'du -sh',
 'free -h'
 ],
 'correct': 1,
 'explanation': 'df -h affiche l\'espace disque disponible en format human-readable. Crucial pour le monitoring d\'infrastructure en DevOps.'
 },
 {
 'id': 11,
 'category': 'Sécurité fichiers',
 'question': 'Comment changer le propriétaire d\'un fichier récursivement ?',
 'options': [
 'chmod -R user:group fichier',
 'chown -R user:group fichier',
 'chgrp -R user:group fichier',
 'usermod -R user:group fichier'
 ],
 'correct': 1,
 'explanation': 'chown -R change récursivement le propriétaire et groupe. Essentiel pour la gestion des permissions en déploiement DevOps.'
 },
 {
 'id': 12,
 'category': 'Monitoring temps réel',
 'question': 'Comment surveiller un fichier de log en temps réel ?',
 'options': [
 'cat /var/log/app.log',
 'tail -f /var/log/app.log',
 'head /var/log/app.log',
 'less /var/log/app.log'
 ],
 'correct': 1,
 'explanation': 'tail -f suit un fichier en temps réel, affichant les nouvelles lignes. Indispensable pour le debugging et monitoring en DevOps.'
 },
 {
 'id': 13,
 'category': 'Configuration réseau',
 'question': 'Comment vérifier les connexions réseau actives ?',
 'options': [
 'ping localhost',
 'netstat -an',
 'ifconfig',
 'route -n'
 ],
 'correct': 1,
 'explanation': 'netstat -an affiche toutes (-a) les connexions réseau avec adresses numériques (-n). Crucial pour le diagnostic réseau en DevOps.'
 },
 {
 'id': 14,
 'category': 'Gestion services',
 'question': 'Comment vérifier le statut d\'un service avec systemd ?',
 'options': [
 'service nginx status',
 'systemctl status nginx',
 '/etc/init.d/nginx status',
 'ps aux | grep nginx'
 ],
 'correct': 1,
 'explanation': 'systemctl status nginx affiche l\'état détaillé du service. Standard moderne pour la gestion des services en DevOps.'
 },
 {
 'id': 15,
 'category': 'Variables PATH',
 'question': 'Comment ajouter temporairement un répertoire au PATH ?',
 'options': [
 'PATH=$PATH:/nouveau/chemin',
 'export PATH=$PATH:/nouveau/chemin',
 'set PATH=$PATH:/nouveau/chemin',
 'PATH+=:/nouveau/chemin'
 ],
 'correct': 1,
 'explanation': 'export PATH=$PATH:/nouveau/chemin ajoute le chemin au PATH existant et l\'exporte pour les sous-processus. Essentiel pour les outils DevOps.'
 }
 ]
 
 def display_header(self):
 """Affiche l'en-tête du quiz"""
 print(f"\n{self.COLORS['HEADER']}{self.COLORS['BOLD']}")
 print("=" * 70)
 print(" QUIZ - LINUX FONDAMENTAUX POUR DEVOPS")
 print("Sprint 1 - Semaine 2 - Séance 1")
 print("=" * 70)
 print(f"{self.COLORS['END']}")
 print(f"{self.COLORS['BLUE']}Validation des connaissances Linux essentielles pour DevOps{self.COLORS['END']}")
 print(f"{self.COLORS['YELLOW']}Niveau: Débutant | Questions: {len(self.questions)} | Format: QCM{self.COLORS['END']}")
 print()
 
 def ask_question(self, question_data):
 """Pose une question et retourne si la réponse est correcte"""
 print(f"{self.COLORS['BOLD']}Question {self.total_questions + 1}{self.COLORS['END']}")
 print(f"{self.COLORS['BLUE']}Catégorie: {question_data['category']}{self.COLORS['END']}")
 print()
 print(f"{self.COLORS['BOLD']}{question_data['question']}{self.COLORS['END']}")
 print()
 
 # Affichage des options
 for i, option in enumerate(question_data['options']):
 print(f" {i + 1}. {option}")
 
 print()
 
 # Saisie de la réponse
 while True:
 try:
 response = input(f"{self.COLORS['YELLOW']}Votre réponse (1-{len(question_data['options'])}): {self.COLORS['END']}")
 choice = int(response) - 1
 
 if 0 <= choice < len(question_data['options']):
 break
 else:
 print(f"{self.COLORS['RED']}Veuillez choisir un nombre entre 1 et {len(question_data['options'])}{self.COLORS['END']}")
 except ValueError:
 print(f"{self.COLORS['RED']}Veuillez entrer un nombre valide{self.COLORS['END']}")
 
 # Vérification de la réponse
 is_correct = choice == question_data['correct']
 self.total_questions += 1
 
 if is_correct:
 self.score += 1
 print(f"\n{self.COLORS['GREEN']} Correct !{self.COLORS['END']}")
 else:
 correct_answer = question_data['options'][question_data['correct']]
 print(f"\n{self.COLORS['RED']} Incorrect{self.COLORS['END']}")
 print(f"{self.COLORS['GREEN']}Bonne réponse: {correct_answer}{self.COLORS['END']}")
 
 # Affichage de l'explication
 print(f"\n{self.COLORS['BLUE']} Explication:{self.COLORS['END']}")
 print(f"{question_data['explanation']}")
 
 # Enregistrement de la réponse
 self.questions_answered.append({
 'question_id': question_data['id'],
 'user_answer': choice,
 'correct_answer': question_data['correct'],
 'is_correct': is_correct,
 'category': question_data['category']
 })
 
 print("\n" + "-" * 70 + "\n")
 return is_correct
 
 def calculate_grade(self):
 """Calcule la note finale"""
 if self.total_questions == 0:
 return 0
 
 percentage = (self.score / self.total_questions) * 100
 
 if percentage >= 90:
 grade = "A"
 comment = "Excellent ! Maîtrise complète des fondamentaux Linux DevOps"
 elif percentage >= 80:
 grade = "B"
 comment = "Très bien ! Bonne compréhension des concepts essentiels"
 elif percentage >= 70:
 grade = "C"
 comment = "Bien ! Connaissances solides avec quelques lacunes à combler"
 elif percentage >= 60:
 grade = "D"
 comment = "Passable ! Révision recommandée des concepts fondamentaux"
 else:
 grade = "F"
 comment = "Insuffisant ! Étude approfondie nécessaire avant de continuer"
 
 return {
 'grade': grade,
 'percentage': percentage,
 'comment': comment
 }
 
 def display_results(self):
 """Affiche les résultats détaillés"""
 result = self.calculate_grade()
 duration = datetime.now() - self.start_time
 
 print(f"{self.COLORS['HEADER']}{self.COLORS['BOLD']}")
 print("=" * 70)
 print(" RÉSULTATS DU QUIZ")
 print("=" * 70)
 print(f"{self.COLORS['END']}")
 
 # Score global
 if result['percentage'] >= 70:
 color = self.COLORS['GREEN']
 elif result['percentage'] >= 60:
 color = self.COLORS['YELLOW']
 else:
 color = self.COLORS['RED']
 
 print(f"{self.COLORS['BOLD']}Score: {color}{self.score}/{self.total_questions} ({result['percentage']:.1f}%){self.COLORS['END']}")
 print(f"{self.COLORS['BOLD']}Note: {color}{result['grade']}{self.COLORS['END']}")
 print(f"{self.COLORS['BLUE']}{result['comment']}{self.COLORS['END']}")
 print(f"{self.COLORS['YELLOW']}Durée: {duration.total_seconds():.0f} secondes{self.COLORS['END']}")
 print()
 
 # Analyse par catégorie
 categories = {}
 for answer in self.questions_answered:
 cat = answer['category']
 if cat not in categories:
 categories[cat] = {'correct': 0, 'total': 0}
 categories[cat]['total'] += 1
 if answer['is_correct']:
 categories[cat]['correct'] += 1
 
 print(f"{self.COLORS['BOLD']}Analyse par domaine:{self.COLORS['END']}")
 for category, stats in categories.items():
 percentage = (stats['correct'] / stats['total']) * 100
 if percentage >= 80:
 color = self.COLORS['GREEN']
 elif percentage >= 60:
 color = self.COLORS['YELLOW']
 else:
 color = self.COLORS['RED']
 
 print(f" {category}: {color}{stats['correct']}/{stats['total']} ({percentage:.0f}%){self.COLORS['END']}")
 
 print()
 
 # Recommandations d'amélioration
 weak_categories = [cat for cat, stats in categories.items() 
 if (stats['correct'] / stats['total']) < 0.7]
 
 if weak_categories:
 print(f"{self.COLORS['YELLOW']} Domaines à approfondir:{self.COLORS['END']}")
 for category in weak_categories:
 print(f" • {category}")
 print()
 
 # Prochaines étapes
 print(f"{self.COLORS['BOLD']} Prochaines étapes recommandées:{self.COLORS['END']}")
 if result['percentage'] >= 80:
 print(" Prêt pour la Séance 2: Gestion des processus et services")
 print(" Continuer avec les LABs avancés Linux")
 elif result['percentage'] >= 60:
 print(" Réviser les concepts avec difficultés identifiées")
 print(" Repratiquer les LABs de cette séance")
 print(" Puis passer à la Séance 2")
 else:
 print(" Étude approfondie des fondamentaux Linux recommandée")
 print(" Pratiquer intensivement avec les LABs")
 print(" Reprendre le quiz après révision")
 
 print(f"\n{self.COLORS['GREEN']}Quiz terminé ! Continuez votre apprentissage DevOps.{self.COLORS['END']}")
 
 def save_results(self):
 """Sauvegarde les résultats dans un fichier JSON"""
 result = self.calculate_grade()
 
 results_data = {
 'quiz_info': {
 'title': 'Linux Fondamentaux pour DevOps',
 'session': 'Sprint 1 - Semaine 2 - Séance 1',
 'date': datetime.now().isoformat(),
 'duration_seconds': (datetime.now() - self.start_time).total_seconds()
 },
 'score': {
 'correct': self.score,
 'total': self.total_questions,
 'percentage': result['percentage'],
 'grade': result['grade']
 },
 'detailed_answers': self.questions_answered
 }
 
 filename = f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
 
 try:
 with open(filename, 'w', encoding='utf-8') as f:
 json.dump(results_data, f, indent=2, ensure_ascii=False)
 print(f"{self.COLORS['BLUE']} Résultats sauvegardés: {filename}{self.COLORS['END']}")
 except Exception as e:
 print(f"{self.COLORS['RED']}Erreur sauvegarde: {e}{self.COLORS['END']}")
 
 def run_quiz(self):
 """Lance le quiz complet"""
 self.display_header()
 
 # Instructions
 print(f"{self.COLORS['BLUE']} Instructions:{self.COLORS['END']}")
 print("• Lisez attentivement chaque question")
 print("• Choisissez la meilleure réponse parmi les options proposées")
 print("• Une explication détaillée suit chaque réponse")
 print("• Le quiz évalue vos connaissances Linux essentielles pour DevOps")
 print()
 
 input(f"{self.COLORS['YELLOW']}Appuyez sur Entrée pour commencer...{self.COLORS['END']}")
 print()
 
 # Mélange des questions pour variabilité
 questions_pool = self.questions.copy()
 random.shuffle(questions_pool)
 
 # Pose toutes les questions
 for question in questions_pool:
 self.ask_question(question)
 
 # Affichage des résultats
 self.display_results()
 
 # Sauvegarde optionnelle
 save_choice = input(f"\n{self.COLORS['YELLOW']}Sauvegarder les résultats ? (o/n): {self.COLORS['END']}").lower()
 if save_choice in ['o', 'oui', 'y', 'yes']:
 self.save_results()

def main():
 """Fonction principale"""
 try:
 quiz = LinuxDevOpsQuiz()
 quiz.run_quiz()
 except KeyboardInterrupt:
 print(f"\n\n{quiz.COLORS['YELLOW']}Quiz interrompu par l'utilisateur{quiz.COLORS['END']}")
 except Exception as e:
 print(f"\n{quiz.COLORS['RED']}Erreur inattendue: {e}{quiz.COLORS['END']}")

if __name__ == "__main__":
 main()
