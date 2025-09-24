"""
LAB 3 - Modules standards pour DevOps - CORRECTION COMPLÈTE

Objectif : Utiliser les modules standards Python pour automatisation DevOps
Contexte : Script de monitoring avec timestamps et génération de données

Cette correction démontre l'utilisation des modules datetime, random et os
pour créer un système de monitoring réaliste.
"""

import datetime
import random
import os

def get_timestamp():
    """Retourne la date/heure actuelle formatée"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def generate_metrics():
    """Génère des métriques système simulées"""
    cpu_usage = random.randint(20, 90)
    memory_usage = random.randint(30, 85)
    disk_usage = random.randint(40, 95)
    
    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage
    }

def get_system_info():
    """Obtient les informations du système"""
    system_name = os.name
    try:
        hostname = os.uname().nodename if hasattr(os, 'uname') else "unknown"
    except:
        hostname = "windows-host"
    
    return {
        "os": system_name,
        "hostname": hostname
    }

def monitoring_report():
    """Génère un rapport de monitoring complet"""
    timestamp = get_timestamp()
    metrics = generate_metrics()
    system_info = get_system_info()
    
    print("=== RAPPORT DE MONITORING SYSTÈME ===")
    print(f"Timestamp: {timestamp}")
    print(f"Système: {system_info['os']}")
    print(f"Hostname: {system_info['hostname']}")
    print()
    print("=== MÉTRIQUES SYSTÈME ===")
    print(f"CPU: {metrics['cpu']}%")
    print(f"Mémoire: {metrics['memory']}%")
    print(f"Disque: {metrics['disk']}%")
    print()
    
    # Analyse automatique
    print("=== ANALYSE AUTOMATIQUE ===")
    if metrics['cpu'] > 80:
        print("ALERTE: CPU en surcharge")
    if metrics['memory'] > 80:
        print("ALERTE: Mémoire saturée")
    if metrics['disk'] > 90:
        print("CRITIQUE: Espace disque faible")
    
    if all(metric < 80 for metric in metrics.values()):
        print("STATUT: Système en bon état")
    
    return {
        "timestamp": timestamp,
        "metrics": metrics,
        "system": system_info
    }

# Programme principal
if __name__ == "__main__":
    print("Démarrage du monitoring système...")
    print()
    
    # Génération du rapport
    report_data = monitoring_report()
    
    print()
    print("=== DONNÉES BRUTES ===")
    print(f"Rapport complet: {report_data}")
    
    print()
    print("Monitoring terminé avec succès!")
    print(f"Prochain rapport dans 5 minutes...")