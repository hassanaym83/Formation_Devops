# LAB 1 - Gestion d'erreurs et fichiers pour DevOps
# Fichier: S1_S2_S5_lab1_gestion_erreurs.py
# Auteur: Hassan ESSADIK
# Sprint 1 - Semaine 2 - Séance 5

"""
LAB 1 - Gestion d'erreurs et fichiers pour DevOps
Points: 5/30
Durée estimée: 20 minutes

OBJECTIF:
Créer des fonctions robustes avec gestion d'erreurs pour scripts DevOps
fiables et résistants aux pannes

CONTEXTE:
Vous développez des utilitaires DevOps qui doivent fonctionner
dans des environnements de production critiques
"""

# ====================
# EXERCICE 1 (1 point)
# ====================

def read_server_config(config_path):
 """
 Lecture sécurisée de configuration serveur
 
 Args:
 config_path (str): Chemin vers fichier de configuration
 
 Returns:
 dict: Configuration chargée ou configuration par défaut
 """
 # TODO: Implémenter la lecture sécurisée
 # - Gérer FileNotFoundError avec config par défaut
 # - Gérer json.JSONDecodeError avec message d'erreur
 # - Gérer PermissionError avec message approprié
 # - Retourner toujours un dictionnaire valide
 pass

def create_default_config():
 """Crée une configuration par défaut"""
 return {
 'server_name': 'default-server',
 'port': 8080,
 'environment': 'development',
 'debug': True,
 'max_connections': 100
 }

# ====================
# EXERCICE 2 (2 points)
# ====================

def ping_multiple_servers(server_list, timeout=5):
 """
 Ping multiple serveurs avec gestion d'erreurs
 
 Args:
 server_list (list): Liste des serveurs à tester
 timeout (int): Timeout en secondes
 
 Returns:
 dict: Résultats de ping pour chaque serveur
 """
 # TODO: Implémenter le ping multiple avec gestion d'erreurs
 # - Tester chaque serveur individuellement
 # - Gérer les timeouts et erreurs réseau
 # - Continuer même si un serveur échoue
 # - Retourner résultat détaillé pour chaque serveur
 pass

# ====================
# EXERCICE 3 (2 points)
# ====================

def backup_with_verification(source_path, backup_path):
 """
 Sauvegarde avec vérification et gestion d'erreurs
 
 Args:
 source_path (str): Chemin source à sauvegarder
 backup_path (str): Chemin de destination backup
 
 Returns:
 dict: Résultat de la sauvegarde avec détails
 """
 # TODO: Implémenter sauvegarde sécurisée
 # - Vérifier existence du source
 # - Créer répertoire backup si nécessaire
 # - Gérer erreurs d'espace disque
 # - Vérifier intégrité après copie
 # - Nettoyer en cas d'erreur (finally)
 pass

# ====================
# TESTS DE VALIDATION
# ====================

def tester_gestion_erreurs():
 """Tests de validation des exercices"""
 print("=== TESTS LAB 1 - Gestion d'erreurs ===")
 
 # Test Exercice 1
 print("\n--- Test Exercice 1: Lecture configuration ---")
 # Test fichier existant
 # Test fichier inexistant
 # Test fichier avec erreur JSON
 
 # Test Exercice 2
 print("\n--- Test Exercice 2: Ping multiple ---")
 # Test serveurs valides
 # Test serveurs invalides
 # Test timeouts
 
 # Test Exercice 3
 print("\n--- Test Exercice 3: Backup sécurisé ---")
 # Test backup normal
 # Test source inexistant
 # Test destination non accessible

if __name__ == "__main__":
 tester_gestion_erreurs()
