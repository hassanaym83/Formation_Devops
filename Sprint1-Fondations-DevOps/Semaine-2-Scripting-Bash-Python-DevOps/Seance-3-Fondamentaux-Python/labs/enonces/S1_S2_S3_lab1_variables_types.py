"""
LAB 1 - Variables, types et opérateurs pour DevOps

Objectif : Maîtriser les variables, types de données et opérateurs jusqu'aux opérateurs sur les chaînes
Contexte : Script de monitoring et gestion des serveurs de production

Couverture : Sections 3 à 3.4
- 3. Variables et types de données
- 3.1 Variables en Python  
- 3.2 Types de données fondamentaux
- 3.3 Opérateurs arithmétiques
- 3.4 Opérateurs sur les chaînes

Instructions :
1. Définir les variables serveur avec différents types de données
2. Manipuler les types numériques et chaînes de caractères
3. Utiliser les opérateurs arithmétiques pour des calculs DevOps
4. Appliquer les opérateurs sur les chaînes pour formater les données
5. Créer un système de nommage et d'identification automatique

Points : 5/30
Durée estimée : 25 minutes
"""

# ===== PARTIE 1 : VARIABLES ET TYPES DE DONNÉES =====

# 1.1 Variables serveur (chaînes de caractères)
server_name = "web-prod-01"
server_ip = "192.168.1.10"
server_location = "datacenter-paris"
environment = "production"

# 1.2 Variables numériques (différents types)
# Types entiers (int)
port_http = 80
port_https = 443
max_connections = 1000
server_id = 101

# Types décimaux (float)
cpu_usage = 0.0  # TODO: Définir l'utilisation CPU actuelle (ex: 45.8)
memory_total_gb = 16.0
disk_total_tb = 2.5
response_time_ms = 0.0  # TODO: Définir le temps de réponse (ex: 125.6)

# 1.3 Variables booléennes
is_production = True
ssl_enabled = True
maintenance_mode = False
backup_completed = False  # TODO: Définir l'état du backup

# 1.4 Collections de base
supported_protocols = ["HTTP", "HTTPS", "SSH", "FTP"]
open_ports = [22, 80, 443, 3306]

server_config = {
    "hostname": server_name,
    "ip": server_ip,
    "environment": environment,
    "ssl": ssl_enabled
}

# ===== PARTIE 2 : OPÉRATEURS ARITHMÉTIQUES =====

# 2.1 Variables métriques pour calculs
memory_used_gb = 0.0  # TODO: Définir la mémoire utilisée (ex: 12.3)
disk_used_tb = 0.0    # TODO: Définir l'espace disque utilisé (ex: 1.8)
requests_per_minute = 0  # TODO: Définir le nombre de requêtes (ex: 1250)

# 2.2 Calculs avec opérateurs arithmétiques
# Addition et soustraction
memory_free_gb = 0.0  # TODO: Calculer memory_total_gb - memory_used_gb
disk_free_tb = 0.0    # TODO: Calculer disk_total_tb - disk_used_tb

# Multiplication et division
memory_percent = 0.0  # TODO: Calculer (memory_used_gb / memory_total_gb) * 100
disk_percent = 0.0    # TODO: Calculer (disk_used_tb / disk_total_tb) * 100
requests_per_second = 0.0  # TODO: Calculer requests_per_minute / 60

# Division entière et modulo
memory_used_mb = 0  # TODO: Calculer memory_used_gb * 1024 (conversion en MB)
storage_blocks = 0  # TODO: Calculer disk_used_tb * 1024 // 4 (blocs de 4GB)

# Puissance
memory_bytes = 0  # TODO: Calculer memory_used_gb * (1024 ** 3) (conversion en bytes)

# ===== PARTIE 3 : OPÉRATEURS SUR LES CHAÎNES =====

# 3.1 Concaténation de chaînes
# Concaténation simple
full_server_name = ""  # TODO: Concatener server_name + "-" + environment
server_endpoint = ""   # TODO: Concatener "http://" + server_ip

# 3.2 Formatage avec f-strings
# Messages de monitoring
cpu_status_message = ""  # TODO: f"CPU utilization: {cpu_usage}% on {server_name}"
memory_status_message = ""  # TODO: f"Memory: {memory_used_gb}/{memory_total_gb} GB ({memory_percent:.1f}%)"
disk_status_message = ""    # TODO: f"Disk space: {disk_free_tb:.2f} TB free of {disk_total_tb} TB"

# URL et identifiants
api_url = ""  # TODO: f"https://{server_ip}:{port_https}/api/v1/status"
log_filename = ""  # TODO: f"{server_name}_{environment}_{server_id}.log"

# 3.3 Répétition de chaînes
separator_line = ""  # TODO: Créer une ligne de 50 caractères "-"
header_decoration = ""  # TODO: Créer une ligne de 20 caractères "="

# 3.4 Opérations avancées sur chaînes
# Transformation du nom serveur
server_name_upper = ""  # TODO: Mettre server_name en majuscules
server_name_underscore = ""  # TODO: Remplacer les "-" par "_" dans server_name

# Construction de noms de services
service_prefix = "svc"
service_name = ""  # TODO: f"{service_prefix}_{server_name.replace('-', '_')}"

# Tags et labels pour DevOps
environment_tag = ""  # TODO: f"env:{environment}"
location_tag = ""     # TODO: f"location:{server_location.split('-')[1]}"  # Extraire "paris"

# ===== PARTIE 4 : AFFICHAGE ET VALIDATION =====

# 4.1 Rapport de monitoring formaté
print("=" * 60)
print("          RAPPORT MONITORING SERVEUR")
print("=" * 60)

# TODO: Afficher les informations serveur
print("\nINFORMATIONS SERVEUR:")
# TODO: Afficher server_name, server_ip, environment, location avec f-strings

print("\nMÉTRIQUES SYSTÈME:")
# TODO: Afficher CPU, mémoire, disque avec pourcentages calculés

print("\nCONNECTIVITÉ:")
# TODO: Afficher les ports, protocoles supportés, endpoints

print("\nTAGS ET LABELS:")
# TODO: Afficher environment_tag, location_tag, service_name

print("\n" + "=" * 60)

# 4.2 Tests de validation
print("\nTESTS DE VALIDATION:")

# TODO: Vérifier que les calculs sont corrects
print(f"Test memory_percent calculation: {memory_percent}")
print(f"Test disk_percent calculation: {disk_percent}")

# TODO: Vérifier les opérations sur chaînes
print(f"Test server name formatting: {server_name_upper}")
print(f"Test service name generation: {service_name}")

# TODO: Vérifier les f-strings
print(f"Test API URL generation: {api_url}")
print(f"Test log filename: {log_filename}")

print("\nLAB 1 - Variables, types et opérateurs complété!")
print("Couverture: Sections 3 à 3.4 - Variables, types, opérateurs arithmétiques et sur chaînes")
