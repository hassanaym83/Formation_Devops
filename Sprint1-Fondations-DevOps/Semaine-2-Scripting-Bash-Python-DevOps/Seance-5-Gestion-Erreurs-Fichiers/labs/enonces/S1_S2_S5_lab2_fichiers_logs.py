# LAB 2 - Gestion d'erreurs et fichiers pour DevOps
# Fichier: S1_S2_S5_lab2_fichiers_logs.py
# Auteur: Hassan ESSADIK
# Sprint 1 - Semaine 2 - Séance 5

"""
LAB 2 - Gestion d'erreurs et fichiers pour DevOps
Points: 5/30
Durée estimée: 25 minutes

OBJECTIF:
Maîtriser les concepts avancés de gestion d'erreurs pour DevOps avec 
exceptions personnalisées, gestionnaires de déploiement et context managers

CONTEXTE:
Vous devez développer un système de déploiement robuste avec gestion 
d'erreurs multicouche, rollback automatique et monitoring complet
"""

import json
import subprocess
import time
from pathlib import Path
from contextlib import contextmanager
from typing import Dict, List, Optional, Any

# ====================
# EXERCICE 1 (2.5 points) - Exceptions personnalisées et hiérarchie
# ====================

class DeploymentError(Exception):
    """TODO: Exception de base pour les erreurs de déploiement"""
    pass

class PreDeploymentError(DeploymentError):
    """TODO: Erreurs lors des vérifications pré-déploiement"""
    pass

class DeploymentExecutionError(DeploymentError):
    """TODO: Erreurs durant l'exécution du déploiement"""
    pass

class PostDeploymentError(DeploymentError):
    """TODO: Erreurs lors des vérifications post-déploiement"""
    pass

def validate_deployment_config(config: Dict[str, Any]) -> bool:
    """
    Valide une configuration de déploiement avec exceptions personnalisées
    
    Args:
        config (dict): Configuration de déploiement à valider
        
    Returns:
        bool: True si valide
        
    Raises:
        PreDeploymentError: Si la configuration est invalide
        
    Instructions:
        1. Vérifier que 'app_name' existe et n'est pas vide
        2. Valider 'version' (format semver: x.y.z)
        3. Contrôler 'environment' (dev, staging, prod uniquement)
        4. Vérifier 'port' (entre 1 et 65535)
        5. Utiliser des exceptions personnalisées avec messages détaillés
    """
    # TODO: Implémenter la validation complète avec exceptions personnalisées
    pass

def check_deployment_prerequisites(app_name: str, environment: str) -> Dict[str, bool]:
    """
    Vérifie les prérequis de déploiement avec gestion d'erreurs
    
    Args:
        app_name (str): Nom de l'application
        environment (str): Environnement cible
        
    Returns:
        dict: Statut des vérifications
        
    Raises:
        PreDeploymentError: Si les prérequis ne sont pas respectés
        
    Instructions:
        1. Vérifier l'espace disque disponible (>1GB requis)
        2. Contrôler la connectivité réseau
        3. Valider les permissions d'écriture
        4. Vérifier que l'application n'est pas déjà déployée
        5. Retourner un dictionnaire avec le statut de chaque vérification
    """
    # TODO: Implémenter les vérifications de prérequis
    pass

# ====================
# EXERCICE 2 (2.5 points) - Context Manager et gestionnaire de déploiement
# ====================

@contextmanager
def deployment_context(environment: str, app_name: str):
    """
    Context manager pour gérer le cycle de vie d'un déploiement
    
    Args:
        environment (str): Environnement de déploiement
        app_name (str): Nom de l'application
        
    Instructions:
        1. Afficher le début du déploiement avec timestamp
        2. Initialiser les ressources nécessaires
        3. Gérer les erreurs avec try/except dans le yield
        4. Nettoyer les ressources dans finally
        5. Calculer et afficher la durée totale
        6. En cas d'erreur, tenter un rollback automatique
    """
    # TODO: Implémenter le context manager complet
    print(f"=== DEBUT DEPLOIEMENT {app_name} sur {environment.upper()} ===")
    start_time = time.time()
    
    try:
        # TODO: Setup des ressources
        yield environment
        
    except Exception as e:
        # TODO: Gestion d'erreur avec rollback
        print(f"ERREUR DURANT LE DEPLOIEMENT: {e}")
        raise
        
    finally:
        # TODO: Nettoyage final et calcul durée
        duration = time.time() - start_time
        print(f"=== FIN DEPLOIEMENT ({duration:.2f}s) ===")

def deploy_application_advanced(app_name: str, version: str, environment: str, 
                               config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Déploie une application avec gestion d'erreurs complète et multicouche
    
    Args:
        app_name (str): Nom de l'application
        version (str): Version à déployer
        environment (str): Environnement cible
        config (dict): Configuration de déploiement
        
    Returns:
        dict: Résultat détaillé du déploiement
        
    Instructions:
        1. Utiliser le deployment_context
        2. Implémenter les 4 étapes avec gestion d'erreurs spécifiques:
           - Vérifications pré-déploiement (PreDeploymentError)
           - Sauvegarde état actuel (DeploymentExecutionError)
           - Déploiement proprement dit (DeploymentExecutionError)
           - Vérifications post-déploiement (PostDeploymentError)
        3. Traquer les étapes complétées dans le résultat
        4. Gérer les rollbacks selon le type d'erreur
        5. Retourner un rapport complet avec statut, erreurs, étapes
    """
    deployment_result = {
        'app_name': app_name,
        'version': version,
        'environment': environment,
        'status': 'unknown',
        'steps_completed': [],
        'errors': [],
        'rollback_performed': False,
        'start_time': time.time()
    }
    
    # TODO: Implémenter le déploiement complet avec context manager
    # et gestion d'erreurs multicouche
    pass

# ====================
# EXERCICE 3 (1 point) - Monitoring et récupération automatique
# ====================

def monitor_application_health(app_name: str, environment: str, 
                             max_retries: int = 3) -> Dict[str, Any]:
    """
    Surveille la santé d'une application avec récupération automatique
    
    Args:
        app_name (str): Nom de l'application
        environment (str): Environnement
        max_retries (int): Nombre maximum de tentatives de récupération
        
    Returns:
        dict: Rapport de santé avec actions entreprises
        
    Instructions:
        1. Vérifier la santé de l'application (HTTP health check simulé)
        2. En cas d'échec, tenter une récupération automatique
        3. Retry avec backoff exponentiel (1s, 2s, 4s...)
        4. Loguer chaque tentative et action
        5. Retourner un rapport détaillé des actions entreprises
    """
    health_report = {
        'app_name': app_name,
        'environment': environment,
        'healthy': False,
        'attempts': 0,
        'recovery_actions': [],
        'errors': [],
        'last_check': time.time()
    }
    
    # TODO: Implémenter le monitoring avec récupération automatique
    pass

# ====================
# INSTRUCTIONS SPÉCIALES
# ====================

"""
CONCEPTS AVANCÉS À MAÎTRISER:

1. HIÉRARCHIE D'EXCEPTIONS:
   - Exceptions personnalisées héritées
   - Messages d'erreur contextuels
   - Gestion spécifique par type d'erreur

2. CONTEXT MANAGERS:
   - @contextmanager decorator
   - Gestion automatique des ressources
   - Try/except/finally dans le context

3. GESTION D'ERREURS MULTICOUCHE:
   - Différents types d'erreurs selon les étapes
   - Rollback conditionnel selon le type d'erreur
   - Logging détaillé pour debugging

4. BONNES PRATIQUES DEVOPS:
   - Validation stricte des configurations
   - Vérifications de prérequis
   - Monitoring proactif avec récupération
   - Rapports détaillés pour audit

CRITÈRES D'ÉVALUATION:
- Exceptions personnalisées bien structurées
- Context manager correctement implémenté
- Gestion d'erreurs appropriée par étape
- Messages d'erreur informatifs
- Mécanismes de rollback et récupération
"""

if __name__ == "__main__":
    print("=== LAB 2 - Gestion d'erreurs - Concepts avancés ===")
    print("\nObjectifs:")
    print("1. Créer une hiérarchie d'exceptions personnalisées")
    print("2. Implémenter un gestionnaire de déploiement robuste")
    print("3. Développer un système de monitoring avec récupération")
    
    # Test de base - À compléter après implémentation
    print("\n=== TESTS DE BASE ===")
    try:
        # Test config invalide
        test_config = {
            'app_name': '',
            'version': 'invalid',
            'environment': 'test',
            'port': 99999
        }
        validate_deployment_config(test_config)
    except Exception as e:
        print(f"✓ Exception capturée comme attendu: {type(e).__name__}")
    
    print("\nImplémentez les fonctions pour voir les tests complets!")