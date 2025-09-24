"""
LAB 1 - Fonctions de base pour DevOps - CORRECTION COMPLÈTE

Objectif : Créer des fonctions Python simples pour les tâches DevOps
Contexte : Scripts d'automatisation avec fonctions réutilisables

Cette correction démontre la création et l'utilisation de fonctions de base
pour des tâches DevOps courantes.
"""

def check_cpu():
    """Vérifie l'état du CPU"""
    print("Vérification CPU...")
    return "CPU: OK"

def check_service():
    """Vérifie si un service est actif"""
    print("Vérification service...")
    return True

def display_report():
    """Affiche un rapport de santé système"""
    print("=== RAPPORT DE SANTÉ SYSTÈME ===")
    print("Timestamp: 2024-01-15 14:30:00")
    print("Status: Système opérationnel")
    print("Services: Tous actifs")
    return "Rapport généré"

# Programme principal
if __name__ == "__main__":
    print("Démarrage monitoring système...")
    print()
    
    # Appel des fonctions de monitoring
    cpu_status = check_cpu()
    service_status = check_service()
    report_status = display_report()
    
    print()
    print("=== RÉSULTATS ===")
    print(f"CPU: {cpu_status}")
    print(f"Service actif: {service_status}")
    print(f"Rapport: {report_status}")
    
    print()
    print("Monitoring terminé avec succès!")