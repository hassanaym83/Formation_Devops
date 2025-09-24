# CORRECTION LAB 2 - Gestion d'erreurs et fichiers pour DevOps
# Fichier: S1_S2_S5_lab2_fichiers_logs_correction.py
# Auteur: Hassan ESSADIK
# Sprint 1 - Semaine 2 - Séance 5

"""
CORRECTION LAB 2 - Gestion d'erreurs et fichiers pour DevOps
Points: 5/30

Cette correction présente une implémentation professionnelle des concepts
avancés de gestion d'erreurs pour DevOps avec exceptions personnalisées,
gestionnaires de déploiement et monitoring automatique.
"""

import json
import subprocess
import time
import re
import random
import os
import shutil
from pathlib import Path
from contextlib import contextmanager
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DeploymentSystem')

# ====================
# CORRECTION EXERCICE 1 (2.5 points) - Exceptions personnalisées et hiérarchie
# ====================

class DeploymentError(Exception):
    """Exception de base pour les erreurs de déploiement"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
    
    def __str__(self):
        base_msg = super().__str__()
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{base_msg} (Details: {details_str})"
        return base_msg

class PreDeploymentError(DeploymentError):
    """Erreurs lors des vérifications pré-déploiement"""
    
    def __init__(self, message: str, check_failed: str = None, **kwargs):
        details = kwargs.get('details', {})
        if check_failed:
            details['failed_check'] = check_failed
        super().__init__(message, details)

class DeploymentExecutionError(DeploymentError):
    """Erreurs durant l'exécution du déploiement"""
    
    def __init__(self, message: str, step: str = None, **kwargs):
        details = kwargs.get('details', {})
        if step:
            details['failed_step'] = step
        super().__init__(message, details)

class PostDeploymentError(DeploymentError):
    """Erreurs lors des vérifications post-déploiement"""
    
    def __init__(self, message: str, verification: str = None, **kwargs):
        details = kwargs.get('details', {})
        if verification:
            details['failed_verification'] = verification
        super().__init__(message, details)

def validate_deployment_config(config: Dict[str, Any]) -> bool:
    """
    Valide une configuration de déploiement avec exceptions personnalisées
    
    Args:
        config (dict): Configuration de déploiement à valider
        
    Returns:
        bool: True si valide
        
    Raises:
        PreDeploymentError: Si la configuration est invalide
    """
    
    # Vérification app_name
    if 'app_name' not in config:
        raise PreDeploymentError(
            "Configuration invalide: 'app_name' manquant",
            check_failed='app_name_missing',
            details={'config_keys': list(config.keys())}
        )
    
    app_name = config['app_name']
    if not isinstance(app_name, str) or not app_name.strip():
        raise PreDeploymentError(
            f"app_name invalide: doit être une chaîne non vide, reçu: {repr(app_name)}",
            check_failed='app_name_invalid',
            details={'app_name_type': type(app_name).__name__, 'app_name_value': app_name}
        )
    
    # Validation version (format semver: x.y.z)
    if 'version' not in config:
        raise PreDeploymentError(
            "Configuration invalide: 'version' manquant",
            check_failed='version_missing'
        )
    
    version = config['version']
    semver_pattern = r'^\d+\.\d+\.\d+$'
    if not isinstance(version, str) or not re.match(semver_pattern, version):
        raise PreDeploymentError(
            f"Version invalide: doit respecter le format semver (x.y.z), reçu: {version}",
            check_failed='version_format',
            details={'version': version, 'expected_format': 'x.y.z'}
        )
    
    # Contrôle environment
    if 'environment' not in config:
        raise PreDeploymentError(
            "Configuration invalide: 'environment' manquant",
            check_failed='environment_missing'
        )
    
    environment = config['environment']
    valid_environments = ['dev', 'staging', 'prod']
    if environment not in valid_environments:
        raise PreDeploymentError(
            f"Environnement invalide: {environment}. Valeurs autorisées: {valid_environments}",
            check_failed='environment_invalid',
            details={'environment': environment, 'valid_environments': valid_environments}
        )
    
    # Vérification port
    if 'port' not in config:
        raise PreDeploymentError(
            "Configuration invalide: 'port' manquant",
            check_failed='port_missing'
        )
    
    port = config['port']
    if not isinstance(port, int):
        try:
            port = int(port)
        except (ValueError, TypeError):
            raise PreDeploymentError(
                f"Port invalide: doit être un entier, reçu: {repr(port)} ({type(port).__name__})",
                check_failed='port_type',
                details={'port_value': port, 'port_type': type(port).__name__}
            )
    
    if not (1 <= port <= 65535):
        raise PreDeploymentError(
            f"Port invalide: {port}. Doit être entre 1 et 65535",
            check_failed='port_range',
            details={'port': port, 'valid_range': '1-65535'}
        )
    
    logger.info(f"Configuration validée avec succès pour {app_name} v{version}")
    return True

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
    """
    
    prerequisites = {
        'disk_space': False,
        'network_connectivity': False,
        'write_permissions': False,
        'app_not_running': False
    }
    
    failed_checks = []
    
    try:
        # Vérification espace disque (>1GB requis)
        try:
            # Simulation - en réalité utiliser shutil.disk_usage()
            total, used, free = shutil.disk_usage('.')
            free_gb = free / (1024**3)
            
            if free_gb >= 1.0:
                prerequisites['disk_space'] = True
                logger.info(f"Espace disque OK: {free_gb:.2f}GB disponible")
            else:
                failed_checks.append(f"Espace disque insuffisant: {free_gb:.2f}GB < 1GB requis")
                
        except Exception as e:
            failed_checks.append(f"Erreur vérification espace disque: {e}")
        
        # Contrôle connectivité réseau (simulation)
        try:
            # En réalité: ping, ou connexion HTTP
            network_ok = random.choice([True, True, True, False])  # 75% de succès
            
            if network_ok:
                prerequisites['network_connectivity'] = True
                logger.info("Connectivité réseau OK")
            else:
                failed_checks.append("Connectivité réseau échouée")
                
        except Exception as e:
            failed_checks.append(f"Erreur test connectivité: {e}")
        
        # Validation permissions d'écriture
        try:
            test_file = Path(f".deployment_test_{app_name}")
            test_file.write_text("test")
            test_file.unlink()
            
            prerequisites['write_permissions'] = True
            logger.info("Permissions d'écriture OK")
            
        except Exception as e:
            failed_checks.append(f"Permissions d'écriture insuffisantes: {e}")
        
        # Vérification application pas déjà déployée
        try:
            # Simulation - en réalité vérifier processus, ports, etc.
            app_running = random.choice([False, False, False, True])  # 25% déjà en cours
            
            if not app_running:
                prerequisites['app_not_running'] = True
                logger.info(f"Application {app_name} pas en cours d'exécution")
            else:
                failed_checks.append(f"Application {app_name} déjà en cours d'exécution")
                
        except Exception as e:
            failed_checks.append(f"Erreur vérification application: {e}")
        
        # Vérification globale
        all_passed = all(prerequisites.values())
        
        if not all_passed:
            error_details = {
                'environment': environment,
                'failed_prerequisites': [k for k, v in prerequisites.items() if not v],
                'total_checks': len(prerequisites),
                'passed_checks': sum(prerequisites.values())
            }
            
            raise PreDeploymentError(
                f"Prérequis de déploiement non respectés pour {app_name} sur {environment}: " +
                ", ".join(failed_checks),
                check_failed='prerequisites',
                details=error_details
            )
        
        logger.info(f"Tous les prérequis validés pour {app_name} sur {environment}")
        return prerequisites
        
    except PreDeploymentError:
        raise
    except Exception as e:
        raise PreDeploymentError(
            f"Erreur inattendue lors de la vérification des prérequis: {e}",
            check_failed='unexpected_error',
            details={'error_type': type(e).__name__, 'error_message': str(e)}
        )

# ====================
# CORRECTION EXERCICE 2 (2.5 points) - Context Manager et gestionnaire de déploiement
# ====================

@contextmanager
def deployment_context(environment: str, app_name: str):
    """
    Context manager pour gérer le cycle de vie d'un déploiement
    
    Args:
        environment (str): Environnement de déploiement
        app_name (str): Nom de l'application
    """
    
    print(f"=== DEBUT DEPLOIEMENT {app_name} sur {environment.upper()} ===")
    start_time = time.time()
    resources_initialized = False
    deployment_lock = None
    
    try:
        # Setup des ressources
        logger.info(f"Initialisation des ressources pour {app_name}")
        
        # Création du répertoire de déploiement
        deployment_dir = Path(f"./deployments/{environment}/{app_name}")
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Création du lock de déploiement
        deployment_lock = deployment_dir / "deployment.lock"
        if deployment_lock.exists():
            raise DeploymentExecutionError(
                f"Déploiement déjà en cours pour {app_name} sur {environment}",
                step='resource_setup',
                details={'lock_file': str(deployment_lock)}
            )
        
        deployment_lock.write_text(f"Started: {datetime.now().isoformat()}")
        resources_initialized = True
        
        logger.info("Ressources initialisées avec succès")
        
        # Yield du contexte
        yield {
            'environment': environment,
            'app_name': app_name,
            'deployment_dir': deployment_dir,
            'start_time': start_time
        }
        
    except Exception as e:
        logger.error(f"ERREUR DURANT LE DEPLOIEMENT: {e}")
        
        # Tentative de rollback automatique
        try:
            logger.info("Tentative de rollback automatique...")
            perform_rollback(app_name, environment)
            logger.info("Rollback automatique réussi")
        except Exception as rollback_error:
            logger.error(f"ERREUR DE ROLLBACK: {rollback_error}")
        
        raise
        
    finally:
        # Nettoyage final
        logger.info("CLEANUP: Nettoyage des ressources")
        
        # Suppression du lock de déploiement
        if resources_initialized and deployment_lock and deployment_lock.exists():
            try:
                deployment_lock.unlink()
                logger.info("Lock de déploiement supprimé")
            except Exception as e:
                logger.warning(f"Impossible de supprimer le lock: {e}")
        
        # Nettoyage des fichiers temporaires
        try:
            temp_files = Path(".").glob(f"temp_{app_name}_*")
            for temp_file in temp_files:
                temp_file.unlink()
                logger.debug(f"Fichier temporaire supprimé: {temp_file}")
        except Exception as e:
            logger.warning(f"Erreur nettoyage fichiers temporaires: {e}")
        
        # Calcul et affichage durée
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
    """
    
    deployment_result = {
        'app_name': app_name,
        'version': version,
        'environment': environment,
        'status': 'unknown',
        'steps_completed': [],
        'errors': [],
        'rollback_performed': False,
        'start_time': time.time(),
        'end_time': None,
        'duration': None
    }
    
    try:
        with deployment_context(environment, app_name) as context:
            
            # ETAPE 1: Vérifications pré-déploiement
            try:
                logger.info("1. Vérifications pré-déploiement...")
                
                # Validation de la configuration
                validate_deployment_config(config)
                deployment_result['steps_completed'].append('config_validation')
                
                # Vérification des prérequis
                check_deployment_prerequisites(app_name, environment)
                deployment_result['steps_completed'].append('prerequisites_check')
                
                # Vérification de l'environnement
                check_environment_health(environment)
                deployment_result['steps_completed'].append('environment_check')
                
                logger.info("Vérifications pré-déploiement réussies")
                
            except Exception as e:
                raise PreDeploymentError(
                    f"Vérifications pré-déploiement échouées: {e}",
                    check_failed='pre_deployment',
                    details={'completed_steps': deployment_result['steps_completed']}
                )
            
            # ETAPE 2: Sauvegarde de l'état actuel
            try:
                logger.info("2. Sauvegarde de l'état actuel...")
                
                backup_result = backup_current_version(app_name, environment)
                deployment_result['backup_info'] = backup_result
                deployment_result['steps_completed'].append('backup')
                
                logger.info("Sauvegarde réussie")
                
            except Exception as e:
                raise DeploymentExecutionError(
                    f"Sauvegarde échouée: {e}",
                    step='backup',
                    details={'backup_attempted': True}
                )
            
            # ETAPE 3: Déploiement proprement dit
            try:
                logger.info("3. Déploiement de la nouvelle version...")
                
                # Arrêt des services
                stop_application_services(app_name, environment)
                deployment_result['steps_completed'].append('services_stopped')
                
                # Déploiement des fichiers
                deploy_application_files(app_name, version, environment)
                deployment_result['steps_completed'].append('files_deployed')
                
                # Mise à jour de la configuration
                update_application_config(app_name, environment, config)
                deployment_result['steps_completed'].append('config_updated')
                
                # Redémarrage des services
                start_application_services(app_name, environment)
                deployment_result['steps_completed'].append('services_started')
                
                logger.info("Déploiement réussi")
                
            except Exception as e:
                raise DeploymentExecutionError(
                    f"Déploiement échoué: {e}",
                    step='deployment',
                    details={
                        'completed_steps': deployment_result['steps_completed'],
                        'version': version
                    }
                )
            
            # ETAPE 4: Vérifications post-déploiement
            try:
                logger.info("4. Vérifications post-déploiement...")
                
                # Test de santé de l'application
                health_result = perform_health_checks(app_name, environment)
                deployment_result['health_check'] = health_result
                
                if not health_result['healthy']:
                    raise Exception(f"Tests de santé échoués: {health_result['errors']}")
                
                deployment_result['steps_completed'].append('health_checks')
                
                # Tests fonctionnels basiques
                smoke_test_result = run_smoke_tests(app_name, environment)
                deployment_result['smoke_tests'] = smoke_test_result
                deployment_result['steps_completed'].append('smoke_tests')
                
                logger.info("Vérifications post-déploiement réussies")
                
            except Exception as e:
                raise PostDeploymentError(
                    f"Vérifications post-déploiement échouées: {e}",
                    verification='post_deployment',
                    details={
                        'health_check_attempted': True,
                        'smoke_tests_attempted': True
                    }
                )
    
    except PreDeploymentError as e:
        deployment_result['status'] = 'failed_pre_deployment'
        deployment_result['errors'].append({
            'type': 'PreDeploymentError',
            'message': str(e),
            'details': e.details
        })
        logger.error(f"ECHEC PRE-DEPLOIEMENT: {e}")
    
    except DeploymentExecutionError as e:
        deployment_result['status'] = 'failed_execution'
        deployment_result['errors'].append({
            'type': 'DeploymentExecutionError',
            'message': str(e),
            'details': e.details
        })
        logger.error(f"ECHEC DEPLOIEMENT: {e}")
        
        # Tentative de rollback
        try:
            logger.info("Tentative de rollback...")
            rollback_result = perform_rollback(app_name, environment)
            deployment_result['rollback_performed'] = True
            deployment_result['rollback_info'] = rollback_result
            logger.info("Rollback réussi")
        except Exception as rollback_error:
            deployment_result['errors'].append({
                'type': 'RollbackError',
                'message': f"Rollback échoué: {rollback_error}",
                'details': {}
            })
            logger.error(f"ECHEC ROLLBACK: {rollback_error}")
    
    except PostDeploymentError as e:
        deployment_result['status'] = 'failed_post_deployment'
        deployment_result['errors'].append({
            'type': 'PostDeploymentError',
            'message': str(e),
            'details': e.details
        })
        logger.error(f"ECHEC POST-DEPLOIEMENT: {e}")
        
        # Décision de rollback pour échec post-déploiement
        if should_rollback_on_post_deployment_failure(e):
            try:
                rollback_result = perform_rollback(app_name, environment)
                deployment_result['rollback_performed'] = True
                deployment_result['rollback_info'] = rollback_result
            except Exception as rollback_error:
                deployment_result['errors'].append({
                    'type': 'RollbackError',
                    'message': f"Rollback échoué: {rollback_error}",
                    'details': {}
                })
    
    except Exception as e:
        deployment_result['status'] = 'failed_unexpected'
        deployment_result['errors'].append({
            'type': 'UnexpectedError',
            'message': f"Erreur inattendue: {e}",
            'details': {'error_type': type(e).__name__}
        })
        logger.error(f"ERREUR INATTENDUE: {e}")
    
    else:
        # Succès complet
        deployment_result['status'] = 'success'
        logger.info(f"DEPLOIEMENT REUSSI: {app_name} v{version} sur {environment}")
    
    finally:
        # Finalisation du rapport
        deployment_result['end_time'] = time.time()
        deployment_result['duration'] = deployment_result['end_time'] - deployment_result['start_time']
        
        # Génération du rapport final
        generate_deployment_report(deployment_result)
        
        # Nettoyage des artifacts
        cleanup_deployment_artifacts(app_name, version)
    
    return deployment_result

# ====================
# CORRECTION EXERCICE 3 (1 point) - Monitoring et récupération automatique
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
    """
    
    health_report = {
        'app_name': app_name,
        'environment': environment,
        'healthy': False,
        'attempts': 0,
        'recovery_actions': [],
        'errors': [],
        'last_check': time.time(),
        'response_times': [],
        'recovery_successful': False
    }
    
    for attempt in range(max_retries + 1):
        health_report['attempts'] = attempt + 1
        
        try:
            logger.info(f"Vérification santé #{attempt + 1} pour {app_name}")
            
            # Simulation health check HTTP
            start_time = time.time()
            
            # Simulation - en réalité: requête HTTP vers /health
            health_ok = random.choice([False, True, True])  # 66% de succès
            response_time = random.uniform(0.1, 2.0)
            
            health_report['response_times'].append(response_time)
            
            if health_ok and response_time < 1.5:
                health_report['healthy'] = True
                health_report['recovery_successful'] = True
                logger.info(f"Application {app_name} en bonne santé (temps: {response_time:.2f}s)")
                break
            
            else:
                # Application en mauvaise santé
                error_msg = f"Health check échoué (temps: {response_time:.2f}s, seuil: 1.5s)"
                health_report['errors'].append({
                    'attempt': attempt + 1,
                    'error': error_msg,
                    'response_time': response_time,
                    'timestamp': time.time()
                })
                
                logger.warning(error_msg)
                
                # Tentative de récupération si pas dernier essai
                if attempt < max_retries:
                    recovery_actions = attempt_recovery(app_name, environment, attempt + 1)
                    health_report['recovery_actions'].extend(recovery_actions)
                    
                    # Backoff exponentiel (1s, 2s, 4s...)
                    sleep_time = 2 ** attempt
                    logger.info(f"Attente de {sleep_time}s avant nouvelle tentative...")
                    time.sleep(sleep_time)
        
        except Exception as e:
            error_msg = f"Erreur lors du health check: {e}"
            health_report['errors'].append({
                'attempt': attempt + 1,
                'error': error_msg,
                'timestamp': time.time()
            })
            logger.error(error_msg)
            
            # Tentative de récupération d'urgence
            if attempt < max_retries:
                try:
                    emergency_recovery = perform_emergency_recovery(app_name, environment)
                    health_report['recovery_actions'].append({
                        'type': 'emergency_recovery',
                        'attempt': attempt + 1,
                        'action': 'emergency_restart',
                        'result': emergency_recovery,
                        'timestamp': time.time()
                    })
                except Exception as recovery_error:
                    logger.error(f"Récupération d'urgence échouée: {recovery_error}")
    
    # Calcul des métriques finales
    if health_report['response_times']:
        health_report['avg_response_time'] = sum(health_report['response_times']) / len(health_report['response_times'])
        health_report['max_response_time'] = max(health_report['response_times'])
    
    # Rapport final
    if health_report['healthy']:
        logger.info(f"Monitoring réussi pour {app_name} après {health_report['attempts']} tentative(s)")
    else:
        logger.error(f"Monitoring échoué pour {app_name} après {max_retries + 1} tentatives")
    
    return health_report

def attempt_recovery(app_name: str, environment: str, attempt: int) -> List[Dict]:
    """Tentatives de récupération automatique"""
    
    recovery_actions = []
    
    try:
        if attempt == 1:
            # Première tentative: redémarrage léger
            logger.info("Tentative de redémarrage léger...")
            action_result = restart_application_services(app_name, environment)
            recovery_actions.append({
                'type': 'soft_restart',
                'attempt': attempt,
                'action': 'restart_services',
                'result': action_result,
                'timestamp': time.time()
            })
            
        elif attempt == 2:
            # Deuxième tentative: nettoyage cache + redémarrage
            logger.info("Tentative de nettoyage cache et redémarrage...")
            
            clear_result = clear_application_cache(app_name, environment)
            restart_result = restart_application_services(app_name, environment)
            
            recovery_actions.extend([
                {
                    'type': 'cache_clear',
                    'attempt': attempt,
                    'action': 'clear_cache',
                    'result': clear_result,
                    'timestamp': time.time()
                },
                {
                    'type': 'restart',
                    'attempt': attempt,
                    'action': 'restart_services',
                    'result': restart_result,
                    'timestamp': time.time()
                }
            ])
            
        else:
            # Dernière tentative: redéploiement version précédente
            logger.info("Tentative de rollback vers version précédente...")
            rollback_result = perform_rollback(app_name, environment)
            recovery_actions.append({
                'type': 'rollback',
                'attempt': attempt,
                'action': 'rollback_previous_version',
                'result': rollback_result,
                'timestamp': time.time()
            })
    
    except Exception as e:
        recovery_actions.append({
            'type': 'recovery_failed',
            'attempt': attempt,
            'error': str(e),
            'timestamp': time.time()
        })
        logger.error(f"Récupération tentative #{attempt} échouée: {e}")
    
    return recovery_actions

# ====================
# FONCTIONS UTILITAIRES (Simulations pour la démonstration)
# ====================

def check_environment_health(environment: str) -> bool:
    """Vérification de la santé de l'environnement"""
    logger.info(f"Vérification santé environnement {environment}")
    return True

def backup_current_version(app_name: str, environment: str) -> Dict:
    """Sauvegarde de la version actuelle"""
    logger.info(f"Sauvegarde version actuelle de {app_name}")
    return {'backup_id': f"backup_{app_name}_{int(time.time())}", 'success': True}

def stop_application_services(app_name: str, environment: str):
    """Arrêt des services de l'application"""
    logger.info(f"Arrêt services {app_name}")
    time.sleep(0.1)  # Simulation

def deploy_application_files(app_name: str, version: str, environment: str):
    """Déploiement des fichiers de l'application"""
    logger.info(f"Déploiement fichiers {app_name} v{version}")
    time.sleep(0.2)  # Simulation

def update_application_config(app_name: str, environment: str, config: Dict):
    """Mise à jour de la configuration"""
    logger.info(f"Mise à jour configuration {app_name}")
    time.sleep(0.1)  # Simulation

def start_application_services(app_name: str, environment: str):
    """Démarrage des services de l'application"""
    logger.info(f"Démarrage services {app_name}")
    time.sleep(0.1)  # Simulation

def perform_health_checks(app_name: str, environment: str) -> Dict:
    """Tests de santé de l'application"""
    logger.info(f"Tests de santé {app_name}")
    # Simulation avec 80% de succès
    healthy = random.random() > 0.2
    return {
        'healthy': healthy,
        'errors': [] if healthy else ['Health endpoint not responding'],
        'response_time': random.uniform(0.1, 0.5)
    }

def run_smoke_tests(app_name: str, environment: str) -> Dict:
    """Tests fonctionnels basiques"""
    logger.info(f"Tests smoke {app_name}")
    return {'passed': True, 'tests_run': 5, 'failures': []}

def perform_rollback(app_name: str, environment: str) -> Dict:
    """Rollback vers version précédente"""
    logger.info(f"Rollback {app_name} sur {environment}")
    return {'success': True, 'previous_version': '1.0.0'}

def should_rollback_on_post_deployment_failure(error) -> bool:
    """Décision de rollback après échec post-déploiement"""
    return True  # Par défaut, rollback en cas d'échec post-déploiement

def generate_deployment_report(result: Dict):
    """Génération du rapport de déploiement"""
    logger.info("Génération rapport de déploiement")

def cleanup_deployment_artifacts(app_name: str, version: str):
    """Nettoyage des artifacts de déploiement"""
    logger.info("Nettoyage artifacts de déploiement")

def restart_application_services(app_name: str, environment: str) -> Dict:
    """Redémarrage des services"""
    logger.info(f"Redémarrage services {app_name}")
    return {'success': True}

def clear_application_cache(app_name: str, environment: str) -> Dict:
    """Nettoyage du cache"""
    logger.info(f"Nettoyage cache {app_name}")
    return {'success': True, 'cache_cleared': True}

def perform_emergency_recovery(app_name: str, environment: str) -> Dict:
    """Récupération d'urgence"""
    logger.info(f"Récupération d'urgence {app_name}")
    return {'success': True, 'recovery_type': 'emergency'}

# ====================
# DÉMONSTRATION COMPLÈTE
# ====================

def demonstration_complete():
    """Démonstration complète des concepts avancés"""
    
    print("=== DÉMONSTRATION GESTION D'ERREURS AVANCÉES ===\n")
    
    # Configuration de test
    valid_config = {
        'app_name': 'demo-app',
        'version': '2.1.0',
        'environment': 'staging',
        'port': 8080
    }
    
    invalid_config = {
        'app_name': '',
        'version': 'invalid-version',
        'environment': 'test',
        'port': 99999
    }
    
    # 1. Test des exceptions personnalisées
    print("1. Test exceptions personnalisées")
    print("-" * 40)
    
    try:
        print("✓ Validation config valide...")
        validate_deployment_config(valid_config)
        print("  Configuration validée avec succès")
    except Exception as e:
        print(f"✗ Erreur inattendue: {e}")
    
    try:
        print("✗ Test config invalide...")
        validate_deployment_config(invalid_config)
    except PreDeploymentError as e:
        print(f"  ✓ Exception capturée: {type(e).__name__}")
        print(f"  Message: {e}")
        print(f"  Détails: {e.details}")
    
    print()
    
    # 2. Test du gestionnaire de déploiement
    print("2. Test gestionnaire de déploiement")
    print("-" * 40)
    
    result = deploy_application_advanced(
        app_name='demo-app',
        version='2.1.0',
        environment='staging',
        config=valid_config
    )
    
    print(f"Statut: {result['status']}")
    print(f"Étapes complétées: {len(result['steps_completed'])}")
    print(f"Durée: {result['duration']:.2f}s")
    print(f"Rollback effectué: {result['rollback_performed']}")
    
    if result['errors']:
        print("Erreurs:")
        for error in result['errors']:
            print(f"  - {error['type']}: {error['message']}")
    
    print()
    
    # 3. Test du monitoring avec récupération
    print("3. Test monitoring et récupération")
    print("-" * 40)
    
    health_report = monitor_application_health(
        app_name='demo-app',
        environment='staging',
        max_retries=3
    )
    
    print(f"Application saine: {health_report['healthy']}")
    print(f"Tentatives: {health_report['attempts']}")
    print(f"Actions de récupération: {len(health_report['recovery_actions'])}")
    print(f"Récupération réussie: {health_report['recovery_successful']}")
    
    if health_report['response_times']:
        print(f"Temps de réponse moyen: {health_report.get('avg_response_time', 0):.2f}s")
    
    if health_report['errors']:
        print("Erreurs détectées:")
        for error in health_report['errors'][-2:]:  # Dernières 2 erreurs
            print(f"  - Tentative {error['attempt']}: {error['error']}")
    
    if health_report['recovery_actions']:
        print("Actions de récupération:")
        for action in health_report['recovery_actions']:
            print(f"  - {action['type']}: {action['action']}")

if __name__ == "__main__":
    demonstration_complete()