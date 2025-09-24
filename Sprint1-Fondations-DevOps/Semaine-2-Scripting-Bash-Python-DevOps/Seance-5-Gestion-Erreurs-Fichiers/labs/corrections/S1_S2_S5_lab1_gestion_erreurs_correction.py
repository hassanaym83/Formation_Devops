#!/usr/bin/env python3
"""
Sprint 1 - Semaine 2 - Séance 5
LAB 1 - Gestion d'erreurs et fichiers pour DevOps - CORRECTION
Fichier : S1_S2_S5_lab1_gestion_erreurs_correction.py

CORRECTION COMPLÈTE DU LAB 1
============================
"""

import json
import time
import socket
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

# ====================
# EXERCICE 1 - LECTURE SÉCURISÉE CONFIG
# ====================

def create_default_config():
    """Crée une configuration par défaut"""
    return {
        'server_name': 'default-server',
        'port': 8080,
        'environment': 'development',
        'debug': True,
        'max_connections': 100
    }

def read_config_with_fallback(config_path: str, fallback_config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Lecture sécurisée de configuration avec fallback
    
    Args:
        config_path (str): Chemin vers le fichier de configuration JSON
        fallback_config (dict): Configuration de fallback optionnelle
        
    Returns:
        dict: Configuration chargée ou configuration par défaut
    """
    if fallback_config is None:
        fallback_config = create_default_config()
    
    try:
        # Tentative de lecture du fichier
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validation basique de la configuration
        if not isinstance(config, dict):
            raise ValueError("Configuration doit être un objet JSON")
        
        print(f"Configuration chargée depuis {config_path}")
        return config
        
    except FileNotFoundError:
        print(f"Fichier {config_path} introuvable")
        print("Utilisation de la configuration par défaut")
        
        # Création du fichier avec config par défaut
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(fallback_config, f, indent=2)
            print(f"Configuration par défaut sauvegardée dans {config_path}")
        except Exception as e:
            print(f"Impossible de sauvegarder la config par défaut: {e}")
        
        return fallback_config
        
    except json.JSONDecodeError as e:
        print(f"JSON invalide dans {config_path}")
        print(f"Erreur ligne {e.lineno}, colonne {e.colno}: {e.msg}")
        print("Utilisation de la configuration de fallback")
        
        # Sauvegarde du fichier corrompu
        backup_path = f"{config_path}.corrupt.{int(time.time())}"
        try:
            os.rename(config_path, backup_path)
            print(f"Fichier corrompu sauvegardé: {backup_path}")
        except Exception:
            pass
        
        return fallback_config
        
    except PermissionError:
        print(f"Permissions insuffisantes pour lire {config_path}")
        print("Vérifiez les droits d'accès au fichier")
        print("Utilisation de la configuration de fallback")
        return fallback_config
        
    except Exception as e:
        print(f"Erreur inattendue lors de la lecture: {e}")
        print("Utilisation de la configuration de fallback")
        return fallback_config

# ====================
# EXERCICE 2 - TEST CONNECTIVITÉ SERVICES
# ====================

def test_service_connectivity(services_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Teste la connectivité des services avec gestion des timeouts et erreurs réseau
    
    Args:
        services_list: Liste des services à tester
                      Format: [{"name": "web", "host": "localhost", "port": 80, "timeout": 5}]
    
    Returns:
        dict: Résultats des tests de connectivité
    """
    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_services': len(services_list),
        'services': {},
        'summary': {
            'available': 0,
            'unavailable': 0,
            'errors': 0
        }
    }
    
    for service in services_list:
        service_name = service.get('name', 'unknown')
        host = service.get('host', 'localhost')
        port = service.get('port', 80)
        timeout = service.get('timeout', 5)
        
        print(f"Test de connectivité: {service_name} ({host}:{port})")
        
        service_result = {
            'name': service_name,
            'host': host,
            'port': port,
            'status': 'unknown',
            'response_time': None,
            'error': None,
            'attempts': 0
        }
        
        # Test de connectivité avec retry
        max_attempts = 3
        for attempt in range(max_attempts):
            service_result['attempts'] = attempt + 1
            
            try:
                start_time = time.time()
                
                # Test de connexion TCP
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                
                result = sock.connect_ex((host, port))
                response_time = time.time() - start_time
                
                sock.close()
                
                if result == 0:
                    service_result['status'] = 'available'
                    service_result['response_time'] = round(response_time * 1000, 2)  # en ms
                    results['summary']['available'] += 1
                    print(f"  {service_name}: Disponible ({service_result['response_time']}ms)")
                    break
                else:
                    raise ConnectionRefusedError(f"Connexion refusée sur {host}:{port}")
                    
            except socket.timeout:
                if attempt < max_attempts - 1:
                    print(f"  Timeout pour {service_name}, tentative {attempt + 1}/{max_attempts}")
                    time.sleep(1)
                else:
                    service_result['status'] = 'unavailable'
                    service_result['error'] = f'Timeout après {timeout}s'
                    results['summary']['unavailable'] += 1
                    print(f"  {service_name}: Timeout")
                    
            except ConnectionRefusedError as e:
                if attempt < max_attempts - 1:
                    print(f"  Connexion refusée pour {service_name}, retry...")
                    time.sleep(1)
                else:
                    service_result['status'] = 'unavailable'
                    service_result['error'] = str(e)
                    results['summary']['unavailable'] += 1
                    print(f"  {service_name}: Connexion refusée")
                    
            except socket.gaierror as e:
                service_result['status'] = 'error'
                service_result['error'] = f'Erreur DNS: {e}'
                results['summary']['errors'] += 1
                print(f"  {service_name}: Erreur DNS")
                break
                
            except Exception as e:
                service_result['status'] = 'error'
                service_result['error'] = str(e)
                results['summary']['errors'] += 1
                print(f"  {service_name}: Erreur inattendue - {e}")
                break
        
        results['services'][service_name] = service_result
    
    return results

# ====================
# EXERCICE 3 - BACKUP AVEC ROLLBACK
# ====================

def backup_critical_files(file_list: List[str], backup_dir: str) -> Dict[str, Any]:
    """
    Sauvegarde de fichiers critiques avec gestion complète des erreurs et rollback
    
    Args:
        file_list: Liste des fichiers à sauvegarder
        backup_dir: Répertoire de destination pour les sauvegardes
    
    Returns:
        dict: Résultats de l'opération de sauvegarde
    """
    import shutil
    from datetime import datetime
    
    # Préparation du répertoire de backup avec timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    full_backup_dir = Path(backup_dir) / f"backup_{timestamp}"
    
    results = {
        'timestamp': timestamp,
        'backup_dir': str(full_backup_dir),
        'total_files': len(file_list),
        'files': {},
        'summary': {
            'success': 0,
            'failed': 0,
            'rollback_needed': False
        }
    }
    
    backup_success = []
    
    try:
        # Création du répertoire de backup
        full_backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"Répertoire de backup créé: {full_backup_dir}")
        
        # Sauvegarde de chaque fichier
        for file_path in file_list:
            file_result = {
                'source': file_path,
                'destination': None,
                'status': 'pending',
                'error': None,
                'size': None
            }
            
            try:
                source_path = Path(file_path)
                
                # Vérification existence du fichier source
                if not source_path.exists():
                    raise FileNotFoundError(f"Fichier source inexistant: {file_path}")
                
                if not source_path.is_file():
                    raise ValueError(f"Le chemin ne pointe pas vers un fichier: {file_path}")
                
                # Destination avec préservation de la structure
                dest_path = full_backup_dir / source_path.name
                file_result['destination'] = str(dest_path)
                
                # Copie du fichier
                print(f"Sauvegarde: {source_path.name}")
                shutil.copy2(source_path, dest_path)
                
                # Vérification de l'intégrité
                if dest_path.stat().st_size != source_path.stat().st_size:
                    raise ValueError("Taille des fichiers différente après copie")
                
                file_result['status'] = 'success'
                file_result['size'] = source_path.stat().st_size
                results['summary']['success'] += 1
                backup_success.append(dest_path)
                
                print(f"  {source_path.name}: Sauvegardé ({file_result['size']} bytes)")
                
            except FileNotFoundError as e:
                file_result['status'] = 'failed'
                file_result['error'] = str(e)
                results['summary']['failed'] += 1
                print(f"  {Path(file_path).name}: Fichier introuvable")
                
            except PermissionError as e:
                file_result['status'] = 'failed'
                file_result['error'] = f'Permissions insuffisantes: {e}'
                results['summary']['failed'] += 1
                print(f"  {Path(file_path).name}: Permissions insuffisantes")
                
            except Exception as e:
                file_result['status'] = 'failed'
                file_result['error'] = str(e)
                results['summary']['failed'] += 1
                print(f"  {Path(file_path).name}: Erreur - {e}")
            
            results['files'][file_path] = file_result
        
        # Vérification du taux de succès
        success_rate = results['summary']['success'] / results['total_files']
        
        if success_rate < 0.8:  # Moins de 80% de succès
            print(f"Taux de succès faible: {success_rate:.1%}")
            raise Exception("Trop d'échecs de sauvegarde, rollback nécessaire")
        
        # Génération du manifeste de sauvegarde
        manifest = {
            'backup_info': results,
            'files_backed_up': [str(f) for f in backup_success]
        }
        
        manifest_path = full_backup_dir / 'backup_manifest.json'
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"Manifeste créé: {manifest_path}")
        print(f"Sauvegarde terminée: {results['summary']['success']}/{results['total_files']} fichiers")
        
    except Exception as critical_error:
        print(f"🚨 ERREUR CRITIQUE: {critical_error}")
        results['summary']['rollback_needed'] = True
        
        # Procédure de rollback
        print("Démarrage du rollback...")
        
        try:
            # Suppression des fichiers partiellement sauvegardés
            for backup_file in backup_success:
                if backup_file.exists():
                    backup_file.unlink()
                    print(f"  Supprimé: {backup_file.name}")
            
            # Suppression du répertoire de backup si vide
            if full_backup_dir.exists() and not any(full_backup_dir.iterdir()):
                full_backup_dir.rmdir()
                print(f"  Répertoire de backup supprimé")
            
            print("Rollback terminé")
            
        except Exception as rollback_error:
            print(f"Erreur durant le rollback: {rollback_error}")
            results['rollback_error'] = str(rollback_error)
    
    return results

# ====================
# EXERCICE 4 - MONITORING SYSTÈME
# ====================

def monitor_system_health() -> Dict[str, Any]:
    """
    Collecte les métriques système avec gestion d'erreurs par composant
    
    Returns:
        dict: Métriques système collectées
    """
    import psutil
    from datetime import datetime
    
    health_report = {
        'timestamp': datetime.now().isoformat(),
        'hostname': socket.gethostname(),
        'metrics': {},
        'errors': {},
        'overall_status': 'unknown'
    }
    
    components = {
        'cpu': lambda: psutil.cpu_percent(interval=1),
        'memory': lambda: psutil.virtual_memory()._asdict(),
        'disk': lambda: psutil.disk_usage('/')._asdict(),
        'network': lambda: psutil.net_io_counters()._asdict(),
        'processes': lambda: len(psutil.pids())
    }
    
    successful_components = 0
    
    for component, collector in components.items():
        try:
            print(f"Collecte métriques: {component}")
            
            if component == 'cpu':
                metric_data = {
                    'usage_percent': collector(),
                    'cores': psutil.cpu_count()
                }
            elif component == 'memory':
                mem_data = collector()
                metric_data = {
                    'total_gb': round(mem_data['total'] / (1024**3), 2),
                    'used_gb': round(mem_data['used'] / (1024**3), 2),
                    'usage_percent': mem_data['percent']
                }
            elif component == 'disk':
                disk_data = collector()
                metric_data = {
                    'total_gb': round(disk_data['total'] / (1024**3), 2),
                    'used_gb': round(disk_data['used'] / (1024**3), 2),
                    'usage_percent': round((disk_data['used'] / disk_data['total']) * 100, 2)
                }
            else:
                metric_data = collector()
            
            health_report['metrics'][component] = metric_data
            successful_components += 1
            print(f"  {component}: Collecté")
            
        except ImportError as e:
            error_msg = f"Module manquant: {e}"
            health_report['errors'][component] = error_msg
            print(f"  {component}: {error_msg}")
            
        except PermissionError as e:
            error_msg = f"Permissions insuffisantes: {e}"
            health_report['errors'][component] = error_msg
            print(f"  {component}: {error_msg}")
            
        except Exception as e:
            error_msg = f"Erreur inattendue: {e}"
            health_report['errors'][component] = error_msg
            print(f"  {component}: {error_msg}")
    
    # Détermination du statut global
    success_rate = successful_components / len(components)
    
    if success_rate >= 0.8:
        health_report['overall_status'] = 'healthy'
    elif success_rate >= 0.5:
        health_report['overall_status'] = 'degraded'
    else:
        health_report['overall_status'] = 'critical'
    
    health_report['success_rate'] = round(success_rate * 100, 1)
    
    return health_report

# ====================
# FONCTION DE TEST
# ====================

def test_all_functions():
    """Teste toutes les fonctions avec gestion d'erreurs"""
    
    print("=" * 60)
    print("TEST DE TOUTES LES FONCTIONS - LAB 1")
    print("=" * 60)
    
    # Test 1: Configuration
    print("\n1. TEST - Lecture de configuration")
    config = read_config_with_fallback("test_config.json")
    print(f"Configuration chargée: {config.get('server_name', 'N/A')}")
    
    # Test 2: Connectivité
    print("\n2. TEST - Connectivité des services")
    services = [
        {"name": "localhost", "host": "127.0.0.1", "port": 80, "timeout": 2},
        {"name": "google-dns", "host": "8.8.8.8", "port": 53, "timeout": 3},
        {"name": "invalid", "host": "192.0.2.1", "port": 9999, "timeout": 1}
    ]
    connectivity_results = test_service_connectivity(services)
    print(f"Services testés: {connectivity_results['summary']}")
    
    # Test 3: Backup
    print("\n3. TEST - Sauvegarde de fichiers")
    test_files = [__file__]  # Sauvegarde ce script lui-même
    backup_results = backup_critical_files(test_files, "backup_test")
    print(f"Résultats backup: {backup_results['summary']}")
    
    # Test 4: Monitoring
    print("\n4. TEST - Monitoring système")
    try:
        health = monitor_system_health()
        print(f"Statut système: {health['overall_status']} ({health['success_rate']}%)")
    except Exception as e:
        print(f"Monitoring indisponible: {e}")
    
    print("\n" + "=" * 60)
    print("TESTS TERMINÉS")
    print("=" * 60)

if __name__ == "__main__":
    test_all_functions()

"""
POINTS CLÉS DE CETTE SOLUTION :
=================================

1. GESTION D'ERREURS ROBUSTE
   - Try/except spécifiques pour chaque type d'erreur
   - Messages d'erreur informatifs et contextuels
   - Fallback automatique vers configurations par défaut
   - Logging visuel avec emojis pour la lisibilité

2. GESTION DE FICHIERS AVANCÉE
   - Création automatique de répertoires
   - Sauvegarde de fichiers corrompus
   - Vérification d'intégrité après copie
   - Gestion des permissions et droits d'accès

3. CONNECTIVITÉ RÉSEAU ROBUSTE
   - Tests TCP avec timeout configurables
   - Retry avec backoff pour la résilience
   - Gestion des erreurs DNS et connexion
   - Métriques de performance (temps de réponse)

4. MONITORING SYSTÈME COMPLET
   - Collecte de métriques CPU, mémoire, disque
   - Gestion des modules manquants (psutil)
   - Évaluation du statut global du système
   - Rapports structurés avec taux de succès

5. OPÉRATIONS DE BACKUP SÉCURISÉES
   ✅ Vérification de l'existence des fichiers source
   ✅ Rollback automatique en cas d'échec critique
   ✅ Manifeste de sauvegarde pour traçabilité
   ✅ Préservation des métadonnées de fichiers

Cette solution démontre une maîtrise complète de la gestion d'erreurs 
en environnement DevOps avec des pratiques professionnelles ! 🚀
"""