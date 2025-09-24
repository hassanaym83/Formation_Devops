# LAB 3 - Gestion d'erreurs et fichiers pour DevOps
# Fichier: S1_S2_S5_lab3_logging_monitoring.py
# Auteur: Hassan ESSADIK
# Sprint 1 - Semaine 2 - Séance 5

"""
LAB 3 - Gestion d'erreurs et fichiers pour DevOps
Points: 5/30
Durée estimée: 20 minutes

OBJECTIF:
Créer un système de logging basique pour applications DevOps
avec journalisation des événements et erreurs

CONTEXTE:
Vous devez implémenter un logging simple pour surveiller
les opérations et diagnostiquer les problèmes en production
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
 # TODO: Implémenter setup logging basique
 # - Créer un logger avec le nom du service
 # - Configurer niveau INFO
 # - Ajouter handler fichier ET console
 # - Format: timestamp - service - niveau - message
 # - Gérer les erreurs de création de fichier
 pass

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
 # TODO: Implémenter logging d'événements
 # - Selon event_type, utiliser le bon niveau de log
 # - start/success: INFO
 # - warning: WARNING 
 # - error: ERROR
 # - Formater les détails en message lisible
 pass

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
 # TODO: Implémenter logging opérations fichiers
 # - Si success=True: niveau INFO
 # - Si success=False: niveau ERROR avec error_msg
 # - Inclure timestamp et détails de l'opération
 pass

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
 # TODO: Implémenter analyse basique des logs
 # - Compter le nombre de lignes par niveau (INFO, WARNING, ERROR)
 # - Retourner un dictionnaire avec les statistiques
 # - Gérer le cas où le fichier n'existe pas
 # Format retour: {
 # 'total_lines': X,
 # 'info_count': Y,
 # 'warning_count': Z,
 # 'error_count': W
 # }
 pass

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
 print("LAB 3 - Logging fondamental DevOps")
 print("Objectif: Maîtriser le logging basique pour DevOps")
 print("-" * 60)
 
 # Exécuter les démonstrations
 demo_logging_system()
 simulate_production_scenario()
 
 print("\n" + "=" * 60)
 print("LAB 3 terminé !")
 print("Vérifiez les fichiers de log générés:")
 print("- deployment.log")
 print("- api.log")
 print("=" * 60)
