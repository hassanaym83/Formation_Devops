#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jeu de devinette de nombres - Formation DevOps
Un jeu simple pour démontrer la containerisation Python avec Docker

Règles du jeu:
- L'ordinateur génère un nombre aléatoire entre 1 et 99
- Le joueur doit deviner le nombre
- Le système indique si le nombre à deviner est plus grand ou plus petit
- Le score est basé sur le nombre de tentatives (moins = mieux)
- Un podium des 3 meilleurs scores est affiché à la fin

Auteur: Hassan ESSADIK - Formation DevOps Simplon Maghreb
"""

import random
import json
import os
from datetime import datetime

class NumberGuessingGame:
    def __init__(self):
        self.scores_file = "scores.json"
        self.players_scores = self.load_scores()
        
    def load_scores(self):
        """Charger les scores depuis le fichier JSON"""
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_scores(self):
        """Sauvegarder les scores dans le fichier JSON"""
        try:
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump(self.players_scores, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
    
    def display_welcome(self):
        """Afficher le message de bienvenue"""
        print("=" * 60)
        print("       JEU DE DEVINETTE DE NOMBRES")
        print("       Formation DevOps - Python Demo")
        print("=" * 60)
        print()
        print("Règles du jeu:")
        print("- Je vais générer un nombre entre 1 et 99")
        print("- Vous devez le deviner en un minimum de tentatives")
        print("- Je vous indiquerai si c'est plus grand ou plus petit")
        print("- Votre score sera le nombre de tentatives utilisées")
        print("- Moins de tentatives = meilleur score !")
        print()
    
    def play_round(self, player_name):
        """Jouer une manche complète pour un joueur"""
        print(f"\nC'est parti {player_name} !")
        print("-" * 40)
        
        # Génération du nombre secret
        secret_number = random.randint(1, 99)
        attempts = 0
        
        print("J'ai choisi un nombre entre 1 et 99.")
        print("À vous de le deviner !")
        print()
        
        while True:
            try:
                # Demander la tentative du joueur
                guess = input(f"Tentative #{attempts + 1} - Votre nombre: ")
                
                # Validation de l'entrée
                if not guess.strip():
                    print("Veuillez entrer un nombre valide.")
                    continue
                    
                guess = int(guess)
                
                if guess < 1 or guess > 99:
                    print("Le nombre doit être entre 1 et 99 !")
                    continue
                
                attempts += 1
                
                # Vérification de la réponse
                if guess == secret_number:
                    print()
                    print("=" * 50)
                    print(f"BRAVO {player_name.upper()} !")
                    print(f"Vous avez trouvé le nombre {secret_number}")
                    print(f"Nombre de tentatives: {attempts}")
                    
                    # Évaluation de la performance
                    if attempts == 1:
                        print("INCROYABLE ! Réussi du premier coup !")
                    elif attempts <= 3:
                        print("EXCELLENT ! Très peu de tentatives !")
                    elif attempts <= 6:
                        print("BIEN JOUÉ ! Bon score !")
                    elif attempts <= 10:
                        print("Pas mal ! Vous pouvez faire mieux !")
                    else:
                        print("Il y a de la place pour l'amélioration !")
                    
                    print("=" * 50)
                    print()
                    break
                    
                elif guess < secret_number:
                    print(f"[X] {guess} est trop PETIT ! Essayez un nombre plus GRAND.")
                else:
                    print(f"[X] {guess} est trop GRAND ! Essayez un nombre plus PETIT.")
                
            except ValueError:
                print("Erreur: Veuillez entrer un nombre entier valide.")
            except KeyboardInterrupt:
                print("\nJeu interrompu par l'utilisateur.")
                return None
        
        return attempts
    
    def add_score(self, player_name, attempts):
        """Ajouter le score d'un joueur"""
        score_entry = {
            "name": player_name,
            "attempts": attempts,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.players_scores.append(score_entry)
        self.save_scores()
        
        print(f"Score enregistré pour {player_name}: {attempts} tentatives")
    
    def display_podium(self):
        """Afficher le podium des 3 meilleurs scores"""
        if not self.players_scores:
            print("Aucun score enregistré pour le moment.")
            return
        
        # Trier par nombre de tentatives (croissant)
        sorted_scores = sorted(self.players_scores, key=lambda x: x["attempts"])
        
        print("\n" + "*" * 50)
        print("           PODIUM DES CHAMPIONS")
        print("*" * 50)
        print()
        
        podium_positions = ["[1] 1ère place", "[2] 2ème place", "[3] 3ème place"]
        
        for i, score in enumerate(sorted_scores[:3]):
            print(f"{podium_positions[i]}: {score['name']}")
            print(f"   Tentatives: {score['attempts']}")
            print(f"   Date: {score['date']}")
            print()
        
        # Statistiques globales
        total_games = len(self.players_scores)
        average_attempts = sum(score["attempts"] for score in self.players_scores) / total_games
        best_score = min(score["attempts"] for score in self.players_scores)
        
        print("-" * 40)
        print("STATISTIQUES GLOBALES:")
        print(f"Total de parties jouées: {total_games}")
        print(f"Moyenne de tentatives: {average_attempts:.1f}")
        print(f"Meilleur score: {best_score} tentative(s)")
        print("-" * 40)
    
    def get_player_name(self):
        """Demander le nom du joueur avec validation"""
        while True:
            name = input("Entrez votre nom: ").strip()
            if name:
                return name.title()  # Capitaliser la première lettre
            print("Le nom ne peut pas être vide. Veuillez réessayer.")
    
    def ask_continue(self):
        """Demander si un autre joueur veut jouer"""
        while True:
            response = input("\nUn autre joueur veut-il jouer ? (o/n): ").strip().lower()
            if response in ['o', 'oui', 'y', 'yes']:
                return True
            elif response in ['n', 'non', 'no']:
                return False
            print("Veuillez répondre par 'o' (oui) ou 'n' (non).")
    
    def run(self):
        """Lancer le jeu principal"""
        self.display_welcome()
        
        # Boucle principale du jeu
        while True:
            # Demander le nom du joueur
            player_name = self.get_player_name()
            
            # Jouer une manche
            attempts = self.play_round(player_name)
            
            # Si le jeu n'a pas été interrompu, enregistrer le score
            if attempts is not None:
                self.add_score(player_name, attempts)
            
            # Demander si un autre joueur veut jouer
            if not self.ask_continue():
                break
        
        # Afficher le podium final
        print("\n" + "=" * 60)
        print("           FIN DU JEU")
        print("=" * 60)
        self.display_podium()
        
        print("\nMerci d'avoir joué !")
        print("Formation DevOps - Simplon Maghreb")
        print("Conteneur Python démonstration")

def main():
    """Point d'entrée principal du programme"""
    try:
        game = NumberGuessingGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\nJeu interrompu. Au revoir !")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        print("Le jeu va se fermer.")

if __name__ == "__main__":
    main()