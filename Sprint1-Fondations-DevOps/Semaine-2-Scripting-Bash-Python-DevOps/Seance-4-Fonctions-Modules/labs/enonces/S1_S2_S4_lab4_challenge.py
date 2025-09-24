"""
📝 LAB 4 - Challenge bibliothèque DevOps complète

Objectif : Créer une bibliothèque d'outils DevOps complète et réutilisable
Contexte : Projet final intégrant tous les concepts pour usage en production

Instructions :
1. Créer un package devops_tools avec sous-modules
2. Implémenter une classe SystemMonitor avec collecte métriques
3. Créer des fonctions d'automation (déploiement, backup)
4. Développer interface utilisateur avec menu et export rapports

Points : 15/30
Durée estimée : 20 minutes
"""

# TODO: Créer la structure de package devops_tools/
# devops_tools/
# ├── __init__.py
# ├── monitoring.py
# ├── automation.py
# └── cli.py

# TODO: Dans monitoring.py, créer une classe SystemMonitor
# - Méthode collect_metrics() pour CPU, mémoire, disque
# - Méthode check_alerts() avec seuils configurables
# - Méthode generate_report() format JSON et texte

# TODO: Dans automation.py, créer des fonctions:
# - deploy_application(app_name, environment)
# - backup_database(db_name, backup_path)
# - restart_service(service_name)

# TODO: Dans cli.py, créer interface utilisateur:
# - Menu principal avec options
# - Export rapports (JSON/texte)
# - Gestion erreurs complète

# TODO: Dans __init__.py, exporter toutes les fonctions principales

# TODO: Créer script principal main.py qui utilise la bibliothèque
# pour démontrer toutes les fonctionnalités

# BONUS: Ajouter documentation complète avec docstrings
# BONUS: Gestion des logs avec module logging