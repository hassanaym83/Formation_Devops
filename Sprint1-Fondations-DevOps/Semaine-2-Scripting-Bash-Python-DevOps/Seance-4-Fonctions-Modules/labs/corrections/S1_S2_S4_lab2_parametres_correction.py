"""
LAB 2 - Paramètres et valeurs de retour pour DevOps - CORRECTION COMPLÈTE

Objectif : Utiliser paramètres et retour de valeurs dans les fonctions DevOps
Contexte : Configuration de serveurs avec paramètres personnalisables

Cette correction montre l'utilisation de paramètres obligatoires, 
par défaut et le retour de valeurs pour la configuration de serveurs.
"""

def config_server(name, ip):
    """Configure les paramètres de base d'un serveur"""
    print(f"Configuration serveur: {name}")
    print(f"Adresse IP: {ip}")
    return f"Serveur {name} configuré sur {ip}"

def setup_web_server(name, port=80, ssl=False):
    """Configure un serveur web avec paramètres par défaut"""
    protocol = "HTTPS" if ssl else "HTTP"
    print(f"Configuration serveur web: {name}")
    print(f"Port: {port}")
    print(f"SSL activé: {ssl}")
    print(f"Protocole: {protocol}")
    return {
        "name": name,
        "port": port,
        "ssl": ssl,
        "protocol": protocol
    }

def calculate_resources(cpu_cores, memory_gb):
    """Calcule la capacité totale des ressources"""
    total_capacity = cpu_cores * memory_gb * 100  # Score arbitraire
    print(f"Calcul ressources: {cpu_cores} CPU cores, {memory_gb}GB RAM")
    print(f"Capacité totale calculée: {total_capacity}")
    return total_capacity

# Programme principal
if __name__ == "__main__":
    print("=== CONFIGURATION INFRASTRUCTURE ===")
    print()
    
    # Test fonction avec paramètres obligatoires
    print("1. Configuration serveur de base:")
    result1 = config_server("web-01", "192.168.1.10")
    print(f"Résultat: {result1}")
    print()
    
    # Test fonction avec paramètres par défaut
    print("2. Configuration serveur web (paramètres par défaut):")
    result2 = setup_web_server("web-01")
    print(f"Configuration: {result2}")
    print()
    
    # Test fonction avec paramètres personnalisés
    print("3. Configuration serveur web sécurisé:")
    result3 = setup_web_server("web-01", port=443, ssl=True)
    print(f"Configuration: {result3}")
    print()
    
    # Test fonction de calcul
    print("4. Calcul capacité serveur:")
    total = calculate_resources(8, 32)
    print(f"Capacité totale: {total}")
    print()
    
    print("Configuration infrastructure terminée!")