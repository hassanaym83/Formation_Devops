# LAB 3 - Gestion d'erreurs et fichiers pour DevOps - CORRECTION
# Fichier: S1_S2_S5_lab3_logging_monitoring_correction.py
# Auteur: Hassan ESSADIK
# Sprint 1 - Semaine 2 - Séance 5

"""
LAB 3 - Gestion d'erreurs et fichiers pour DevOps - CORRECTION
Points: 5/30
Durée estimée: 20 minutes

Solution complète pour système de logging basique DevOps
"""

import logging
import os
from datetime import datetime

# ====================
# EXERCICE 1 (2 points)
# ====================

def setup_basic_logging(service_name, log_file="app.log"):
 """
 Configuration logging basique pour services DevOps
 
 Args:
 service_name (str): Nom du service
 log_file (str): Nom du fichier de log
 
 Returns:
 logging.Logger: Logger configuré
 """
 try:
 # Créer le logger avec le nom du service
 logger = logging.getLogger(service_name)
 logger.setLevel(logging.INFO)
 
 # Éviter les doublons de handlers
 if logger.handlers:
 logger.handlers.clear()
 
 # Format des messages
 formatter = logging.Formatter(
 '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 datefmt='%Y-%m-%d %H:%M:%S'
 )
 
 # Handler pour fichier
 try:
 file_handler = logging.FileHandler(log_file, encoding='utf-8')
 file_handler.setLevel(logging.INFO)
 file_handler.setFormatter(formatter)
 logger.addHandler(file_handler)
 except (PermissionError, OSError) as e:
 print(f"Erreur création fichier log {log_file}: {e}")
 # Utiliser un fichier temporaire
 temp_log = f"temp_{service_name}.log"
 file_handler = logging.FileHandler(temp_log, encoding='utf-8')
 file_handler.setLevel(logging.INFO)
 file_handler.setFormatter(formatter)
 logger.addHandler(file_handler)
 
 # Handler pour console
 console_handler = logging.StreamHandler()
 console_handler.setLevel(logging.WARNING) # Seulement warnings et erreurs en console
 console_handler.setFormatter(formatter)
 logger.addHandler(console_handler)
 
 return logger
 
 except Exception as e:
 print(f"Erreur configuration logger: {e}")
 return None

# ====================
# EXERCICE 2 (2 points)
# ====================

def log_deployment_event(logger, event_type, details):
 """
 Enregistre un événement de déploiement
 
 Args:
 logger: Logger configuré
 event_type (str): Type d'événement (start, success, error, warning)
 details (dict): Détails de l'événement
 """
 if not logger:
 print("Logger non disponible")
 return
 
 # Formater les détails en message lisible
 if isinstance(details, dict):
 details_str = " | ".join([f"{k}: {v}" for k, v in details.items()])
 else:
 details_str = str(details)
 
 message = f"Déploiement [{event_type.upper()}] - {details_str}"
 
 # Utiliser le bon niveau selon le type d'événement
 if event_type.lower() in ['start', 'success']:
 logger.info(message)
 elif event_type.lower() == 'warning':
 logger.warning(message)
 elif event_type.lower() == 'error':
 logger.error(message)
 else:
 logger.info(f"Événement inconnu: {message}")

def log_file_operation(logger, operation, filename, success=True, error_msg=None):
 """
 Enregistre une opération sur fichier
 
 Args:
 logger: Logger configuré
 operation (str): Type d'opération (read, write, delete, copy)
 filename (str): Nom du fichier
 success (bool): Si l'opération a réussi
 error_msg (str): Message d'erreur si échec
 """
 if not logger:
 print("Logger non disponible")
 return
 
 timestamp = datetime.now().strftime('%H:%M:%S')
 
 if success:
 message = f"Opération fichier réussie [{operation.upper()}] - {filename} à {timestamp}"
 logger.info(message)
 else:
 error_detail = f" - {error_msg}" if error_msg else ""
 message = f"Opération fichier échouée [{operation.upper()}] - {filename}{error_detail}"
 logger.error(message)

# ====================
# EXERCICE 3 (1 point)
# ====================

def create_log_summary(log_file):
 """
 Génère un résumé des logs
 
 Args:
 log_file (str): Chemin vers le fichier de log
 
 Returns:
 dict: Statistiques des logs
 """
 summary = {
 'total_lines': 0,
 'info_count': 0,
 'warning_count': 0,
 'error_count': 0
 }
 
 try:
 if not os.path.exists(log_file):
 print(f"Fichier de log {log_file} introuvable")
 return summary
 
 with open(log_file, 'r', encoding='utf-8') as f:
 for line in f:
 line = line.strip()
 if line:
 summary['total_lines'] += 1
 
 # Compter par niveau
 if ' - INFO - ' in line:
 summary['info_count'] += 1
 elif ' - WARNING - ' in line:
 summary['warning_count'] += 1
 elif ' - ERROR - ' in line:
 summary['error_count'] += 1
 
 return summary
 
 except Exception as e:
 print(f"Erreur lecture fichier log: {e}")
 return summary

# ====================
# TESTS ET DÉMONSTRATION
# ====================

def demo_logging_system():
 """Démonstration du système de logging"""
 
 print("=== DÉMONSTRATION LOGGING DEVOPS ===\n")
 
 # Test 1: Setup du logging
 print("1. Configuration du logging...")
 logger = setup_basic_logging("web-deployment", "deployment.log")
 
 if logger:
 print(" Logger configuré avec succès")
 else:
 print(" Erreur de configuration du logger")
 return
 
 # Test 2: Événements de déploiement
 print("\n2. Simulation d'événements de déploiement...")
 
 # Début de déploiement
 log_deployment_event(logger, "start", {
 "app": "web-app",
 "version": "1.2.3", 
 "environment": "production"
 })
 
 # Opérations sur fichiers
 log_file_operation(logger, "read", "config.json", success=True)
 log_file_operation(logger, "write", "backup.tar.gz", success=True)
 log_file_operation(logger, "delete", "temp_file.tmp", success=False, 
 error_msg="Fichier introuvable")
 
 # Événements variés
 log_deployment_event(logger, "warning", {
 "message": "Mémoire faible détectée",
 "memory_usage": "85%"
 })
 
 log_deployment_event(logger, "success", {
 "message": "Déploiement terminé",
 "duration": "2m 34s"
 })
 
 # Test 3: Analyse des logs
 print("\n3. Génération du résumé des logs...")
 summary = create_log_summary("deployment.log")
 
 if summary:
 print(f" Total lignes: {summary.get('total_lines', 0)}")
 print(f" INFO: {summary.get('info_count', 0)}")
 print(f" WARNING: {summary.get('warning_count', 0)}")
 print(f" ERROR: {summary.get('error_count', 0)}")
 else:
 print(" Erreur lors de l'analyse des logs")

def simulate_production_scenario():
 """Simule un scénario de production réaliste"""
 
 print("\n=== SCÉNARIO PRODUCTION ===\n")
 
 # Configuration pour service API
 api_logger = setup_basic_logging("api-server", "api.log")
 
 if not api_logger:
 print("Erreur: Impossible de configurer le logger API")
 return
 
 # Simulation d'événements API
 events = [
 ("start", {"message": "Démarrage serveur API", "port": 8080}),
 ("success", {"message": "Base de données connectée"}),
 ("warning", {"message": "Limite de connexions atteinte", "connections": 95}),
 ("error", {"message": "Échec authentification", "user": "admin", "ip": "192.168.1.100"}),
 ("success", {"message": "Cache actualisé", "cache_size": "245MB"})
 ]
 
 print("Simulation d'événements API en cours...")
 for event_type, details in events:
 log_deployment_event(api_logger, event_type, details)
 
 # Opérations fichiers
 file_ops = [
 ("read", "users.db", True, None),
 ("write", "session.cache", True, None),
 ("backup", "api.backup", False, "Espace disque insuffisant"),
 ("read", "config.ini", True, None)
 ]
 
 print("Simulation d'opérations fichiers...")
 for op, filename, success, error in file_ops:
 log_file_operation(api_logger, op, filename, success, error)
 
 # Analyse finale
 print("\nAnalyse des logs API:")
 api_summary = create_log_summary("api.log")
 if api_summary:
 for key, value in api_summary.items():
 print(f" {key}: {value}")

if __name__ == "__main__":
 print("LAB 3 - Logging fondamental DevOps - CORRECTION")
 print("Solution complète du système de logging basique")
 print("-" * 60)
 
 # Exécuter les démonstrations
 demo_logging_system()
 simulate_production_scenario()
 
 print("\n" + "=" * 60)
 print("RÉSULTATS LAB 3:")
 print("- Configuration logging: Implémentée avec handlers fichier/console")
 print("- Événements déploiement: Journalisés par niveau approprié")
 print("- Opérations fichiers: Tracées avec succès/échec")
 print("- Analyse logs: Statistiques générées")
 print("- Gestion erreurs: Robuste avec fallbacks")
 print("=" * 60)
