"""
📝 LAB 4 - Challenge bibliothèque DevOps complète - CORRECTION COMPLÈTE

Objectif : Créer une bibliothèque d'outils DevOps complète et réutilisable
Contexte : Projet final intégrant tous les concepts pour usage en production

Cette correction démontre la création d'une bibliothèque DevOps professionnelle
avec structure modulaire, monitoring système et outils d'automation.
"""

import json
import datetime
import random
import os
from typing import Dict, List, Optional

# ========== PACKAGE DEVOPS_TOOLS ==========

# Fichier: devops_tools/__init__.py
"""
Bibliothèque d'outils DevOps Python
Version 1.0.0 - Hassan ESSADIK
"""

# Fichier: devops_tools/monitoring.py
class SystemMonitor:
    """Moniteur système avec historique et alertes"""
    
    def __init__(self, alert_thresholds: Optional[Dict] = None):
        self.alert_thresholds = alert_thresholds or {
            "cpu_percent": 80,
            "memory_percent": 85,
            "disk_percent": 90
        }
        self.history = []
    
    def collect_metrics(self) -> Dict:
        """Collecte les métriques système actuelles"""
        # Simulation de métriques réalistes
        metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "cpu_percent": round(random.uniform(10, 95), 1),
            "memory_percent": round(random.uniform(20, 90), 1),
            "disk_percent": round(random.uniform(30, 80), 1),
            "network_mbps": round(random.uniform(1, 100), 1),
            "processes_count": random.randint(50, 200),
            "load_average": round(random.uniform(0.5, 4.0), 2)
        }
        
        # Ajouter à l'historique
        self.history.append(metrics)
        if len(self.history) > 50:  # Garder 50 dernières mesures
            self.history = self.history[-50:]
        
        return metrics
    
    def check_alerts(self, metrics: Dict) -> List[Dict]:
        """Vérifie les seuils d'alerte"""
        alerts = []
        
        if metrics["cpu_percent"] > self.alert_thresholds["cpu_percent"]:
            alerts.append({
                "type": "CPU_HIGH",
                "value": metrics["cpu_percent"],
                "threshold": self.alert_thresholds["cpu_percent"],
                "severity": "CRITICAL" if metrics["cpu_percent"] > 95 else "WARNING"
            })
        
        if metrics["memory_percent"] > self.alert_thresholds["memory_percent"]:
            alerts.append({
                "type": "MEMORY_HIGH",
                "value": metrics["memory_percent"],
                "threshold": self.alert_thresholds["memory_percent"],
                "severity": "CRITICAL" if metrics["memory_percent"] > 95 else "WARNING"
            })
        
        if metrics["disk_percent"] > self.alert_thresholds["disk_percent"]:
            alerts.append({
                "type": "DISK_HIGH",
                "value": metrics["disk_percent"],
                "threshold": self.alert_thresholds["disk_percent"],
                "severity": "CRITICAL"
            })
        
        return alerts
    
    def generate_report(self, format_type: str = "json") -> str:
        """Génère un rapport complet"""
        if not self.history:
            return "Aucune donnée disponible"
        
        latest = self.history[-1]
        alerts = self.check_alerts(latest)
        
        # Calculs statistiques
        if len(self.history) > 1:
            cpu_avg = sum(m["cpu_percent"] for m in self.history) / len(self.history)
            memory_avg = sum(m["memory_percent"] for m in self.history) / len(self.history)
        else:
            cpu_avg = latest["cpu_percent"]
            memory_avg = latest["memory_percent"]
        
        report_data = {
            "report_timestamp": datetime.datetime.now().isoformat(),
            "current_metrics": latest,
            "statistics": {
                "cpu_average": round(cpu_avg, 2),
                "memory_average": round(memory_avg, 2),
                "samples_count": len(self.history)
            },
            "alerts": alerts,
            "system_health": "HEALTHY" if not alerts else "DEGRADED" if len(alerts) < 3 else "CRITICAL"
        }
        
        if format_type == "json":
            return json.dumps(report_data, indent=2)
        else:
            # Format texte
            report = f"""
=== RAPPORT SYSTÈME ===
Timestamp: {report_data['report_timestamp']}

MÉTRIQUES ACTUELLES:
- CPU: {latest['cpu_percent']}%
- Mémoire: {latest['memory_percent']}%
- Disque: {latest['disk_percent']}%
- Processus: {latest['processes_count']}

STATISTIQUES:
- CPU moyen: {cpu_avg:.1f}%
- Mémoire moyenne: {memory_avg:.1f}%
- Échantillons: {len(self.history)}

ALERTES ACTIVES: {len(alerts)}
{chr(10).join(f"- {alert['type']}: {alert['value']}% (seuil: {alert['threshold']}%)" for alert in alerts)}

SANTÉ SYSTÈME: {report_data['system_health']}
"""
            return report

# Fichier: devops_tools/automation.py
def deploy_application(app_name: str, environment: str = "production") -> Dict:
    """
    Déploie une application dans l'environnement spécifié
    
    Args:
        app_name: Nom de l'application
        environment: Environnement cible (dev/staging/production)
    
    Returns:
        Dict: Résultat du déploiement
    """
    valid_environments = ["development", "staging", "production"]
    if environment not in valid_environments:
        raise ValueError(f"Environnement invalide. Valeurs autorisées: {valid_environments}")
    
    # Simulation du déploiement
    print(f"Déploiement de {app_name} en {environment}...")
    
    # Configuration selon l'environnement
    config = {
        "app_name": app_name,
        "environment": environment,
        "deployment_time": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "status": "success",
        "resources": {
            "cpu": "500m" if environment == "production" else "200m",
            "memory": "1Gi" if environment == "production" else "512Mi"
        }
    }
    
    return config

def backup_database(db_name: str, backup_path: str = "/backup") -> Dict:
    """
    Effectue une sauvegarde de base de données
    
    Args:
        db_name: Nom de la base de données
        backup_path: Chemin de destination du backup
    
    Returns:
        Dict: Résultat de la sauvegarde
    """
    if not db_name:
        raise ValueError("Le nom de la base ne peut pas être vide")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_path}/{db_name}_backup_{timestamp}.sql"
    
    print(f"Sauvegarde de {db_name} vers {backup_file}...")
    
    return {
        "database": db_name,
        "backup_file": backup_file,
        "timestamp": timestamp,
        "size_mb": random.randint(100, 5000),
        "duration_seconds": random.randint(30, 300),
        "status": "success"
    }

def restart_service(service_name: str) -> Dict:
    """
    Redémarre un service système
    
    Args:
        service_name: Nom du service à redémarrer
    
    Returns:
        Dict: Résultat du redémarrage
    """
    print(f"Redémarrage du service {service_name}...")
    
    return {
        "service": service_name,
        "action": "restart",
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "previous_uptime": f"{random.randint(1, 30)} days",
        "pid": random.randint(1000, 9999)
    }

# Fichier: devops_tools/cli.py
class DevOpsCLI:
    """Interface ligne de commande pour outils DevOps"""
    
    def __init__(self):
        self.monitor = SystemMonitor()
    
    def show_menu(self):
        """Affiche le menu principal"""
        print("\n" + "="*50)
        print("    DEVOPS TOOLKIT - MENU PRINCIPAL")
        print("="*50)
        print("1. Monitoring système")
        print("2. Déploiement application")
        print("3. Backup base de données")
        print("4. Redémarrage service")
        print("5. Générer rapport complet")
        print("6. Export rapport (JSON)")
        print("7. Export rapport (Texte)")
        print("0. Quitter")
        print("="*50)
    
    def run_monitoring(self):
        """Execute le monitoring système"""
        print("\n📊 MONITORING SYSTÈME")
        metrics = self.monitor.collect_metrics()
        alerts = self.monitor.check_alerts(metrics)
        
        print(f"CPU: {metrics['cpu_percent']}%")
        print(f"Mémoire: {metrics['memory_percent']}%")
        print(f"Disque: {metrics['disk_percent']}%")
        print(f"Processus: {metrics['processes_count']}")
        
        if alerts:
            print(f"\n⚠️  {len(alerts)} alerte(s) active(s):")
            for alert in alerts:
                print(f"  - {alert['type']}: {alert['value']}% (seuil: {alert['threshold']}%)")
        else:
            print("\n✅ Aucune alerte active")
    
    def run_deployment(self):
        """Execute un déploiement"""
        print("\n🚀 DÉPLOIEMENT APPLICATION")
        app_name = input("Nom de l'application: ")
        environment = input("Environnement (dev/staging/production): ") or "production"
        
        try:
            result = deploy_application(app_name, environment)
            print(f"✅ Déploiement réussi:")
            print(f"  - Application: {result['app_name']}")
            print(f"  - Environnement: {result['environment']}")
            print(f"  - Version: {result['version']}")
        except ValueError as e:
            print(f"❌ Erreur: {e}")
    
    def run_backup(self):
        """Execute une sauvegarde"""
        print("\n💾 BACKUP BASE DE DONNÉES")
        db_name = input("Nom de la base: ")
        backup_path = input("Chemin backup [/backup]: ") or "/backup"
        
        try:
            result = backup_database(db_name, backup_path)
            print(f"✅ Backup réussi:")
            print(f"  - Base: {result['database']}")
            print(f"  - Fichier: {result['backup_file']}")
            print(f"  - Taille: {result['size_mb']} MB")
        except ValueError as e:
            print(f"❌ Erreur: {e}")
    
    def run_service_restart(self):
        """Execute un redémarrage de service"""
        print("\n🔄 REDÉMARRAGE SERVICE")
        service_name = input("Nom du service: ")
        
        result = restart_service(service_name)
        print(f"✅ Service redémarré:")
        print(f"  - Service: {result['service']}")
        print(f"  - Nouveau PID: {result['pid']}")
        print(f"  - Uptime précédent: {result['previous_uptime']}")
    
    def export_report(self, format_type: str):
        """Exporte un rapport"""
        print(f"\n📄 EXPORT RAPPORT ({format_type.upper()})")
        
        # Collecter quelques métriques pour le rapport
        for _ in range(3):
            self.monitor.collect_metrics()
        
        report = self.monitor.generate_report(format_type)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_report_{timestamp}.{format_type}"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Rapport exporté: {filename}")
        except Exception as e:
            print(f"❌ Erreur export: {e}")
            print("Rapport affiché à l'écran:")
            print(report)
    
    def run(self):
        """Lance l'interface CLI"""
        print("Démarrage DevOps Toolkit...")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nChoix: ").strip()
                
                if choice == "0":
                    print("Au revoir!")
                    break
                elif choice == "1":
                    self.run_monitoring()
                elif choice == "2":
                    self.run_deployment()
                elif choice == "3":
                    self.run_backup()
                elif choice == "4":
                    self.run_service_restart()
                elif choice == "5":
                    print("\n📋 RAPPORT COMPLET")
                    print(self.monitor.generate_report("text"))
                elif choice == "6":
                    self.export_report("json")
                elif choice == "7":
                    self.export_report("txt")
                else:
                    print("❌ Choix invalide")
                
                input("\nAppuyez sur Entrée pour continuer...")
                
            except KeyboardInterrupt:
                print("\n\nArrêt demandé par l'utilisateur")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")
                input("Appuyez sur Entrée pour continuer...")

# ========== SCRIPT PRINCIPAL ==========

def main():
    """Script principal démontrant la bibliothèque DevOps"""
    print("="*60)
    print("  DÉMONSTRATION BIBLIOTHÈQUE DEVOPS COMPLÈTE")
    print("  LAB 4 - Challenge Final")
    print("="*60)
    
    # 1. Monitoring système
    print("\n1. 📊 DÉMONSTRATION MONITORING")
    monitor = SystemMonitor()
    
    # Collecter quelques métriques
    for i in range(3):
        metrics = monitor.collect_metrics()
        alerts = monitor.check_alerts(metrics)
        print(f"  Mesure {i+1}: CPU {metrics['cpu_percent']}%, RAM {metrics['memory_percent']}%")
        if alerts:
            print(f"    ⚠️  {len(alerts)} alerte(s)")
    
    # 2. Automation
    print("\n2. 🚀 DÉMONSTRATION AUTOMATION")
    
    # Déploiement
    deploy_result = deploy_application("web-app", "production")
    print(f"  Déploiement: {deploy_result['app_name']} -> {deploy_result['status']}")
    
    # Backup
    backup_result = backup_database("prod_db")
    print(f"  Backup: {backup_result['database']} -> {backup_result['size_mb']} MB")
    
    # Redémarrage service
    restart_result = restart_service("nginx")
    print(f"  Restart: {restart_result['service']} -> PID {restart_result['pid']}")
    
    # 3. Rapport complet
    print("\n3. 📄 GÉNÉRATION RAPPORT")
    report_json = monitor.generate_report("json")
    print("  Rapport JSON généré ✅")
    
    report_text = monitor.generate_report("text")
    print("  Rapport texte généré ✅")
    
    # 4. Interface CLI (optionnelle)
    print("\n4. 🖥️  INTERFACE UTILISATEUR")
    print("  Interface CLI disponible avec DevOpsCLI().run()")
    
    print("\n" + "="*60)
    print("  DÉMONSTRATION TERMINÉE AVEC SUCCÈS")
    print("  Toutes les fonctionnalités ont été testées ✅")
    print("="*60)

# Programme principal
if __name__ == "__main__":
    print("LAB 4 - Challenge bibliothèque DevOps complète")
    print("Correction complète par Hassan ESSADIK")
    print()
    
    # Choix d'exécution
    print("Options disponibles:")
    print("1. Démonstration complète (recommandé)")
    print("2. Interface CLI interactive")
    print("3. Test des modules individuellement")
    
    choice = input("\nChoix [1]: ").strip() or "1"
    
    if choice == "1":
        main()
    elif choice == "2":
        cli = DevOpsCLI()
        cli.run()
    elif choice == "3":
        print("\n=== TEST MONITORING ===")
        monitor = SystemMonitor()
        metrics = monitor.collect_metrics()
        print(f"Métriques: {metrics}")
        
        print("\n=== TEST AUTOMATION ===")
        deploy_result = deploy_application("test-app", "staging")
        print(f"Déploiement: {deploy_result}")
        
        backup_result = backup_database("test_db")
        print(f"Backup: {backup_result}")
    else:
        print("Choix invalide, lancement de la démonstration...")
        main()