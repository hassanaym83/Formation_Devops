"""
LAB 1 - Variables, types et opérateurs pour DevOps - CORRECTION

Objectif : Maîtriser les variables, types de données et opérateurs jusqu'aux opérateurs sur les chaînes
Contexte : Script de monitoring et gestion des serveurs de production

Couverture : Sections 3 à 3.4
- 3. Variables et types de données
- 3.1 Variables en Python  
- 3.2 Types de données fondamentaux
- 3.3 Opérateurs arithmétiques
- 3.4 Opérateurs sur les chaînes

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
cpu_usage = 45.8  # Utilisation CPU actuelle en pourcentage
memory_total_gb = 16.0
disk_total_tb = 2.5
response_time_ms = 125.6  # Temps de réponse en millisecondes

# 1.3 Variables booléennes
is_production = True
ssl_enabled = True
maintenance_mode = False
backup_completed = True  # État du backup

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
memory_used_gb = 12.3  # Mémoire utilisée en GB
disk_used_tb = 1.8     # Espace disque utilisé en TB
requests_per_minute = 1250  # Nombre de requêtes par minute

# 2.2 Calculs avec opérateurs arithmétiques
# Addition et soustraction
memory_free_gb = memory_total_gb - memory_used_gb  # 16.0 - 12.3 = 3.7
disk_free_tb = disk_total_tb - disk_used_tb        # 2.5 - 1.8 = 0.7

# Multiplication et division
memory_percent = (memory_used_gb / memory_total_gb) * 100  # (12.3/16.0)*100 = 76.875
disk_percent = (disk_used_tb / disk_total_tb) * 100       # (1.8/2.5)*100 = 72.0
requests_per_second = requests_per_minute / 60            # 1250/60 = 20.833...

# Division entière et modulo
memory_used_mb = memory_used_gb * 1024              # 12.3 * 1024 = 12595.2
storage_blocks = disk_used_tb * 1024 // 4          # 1.8 * 1024 // 4 = 460

# Puissance
memory_bytes = memory_used_gb * (1024 ** 3)        # Conversion en bytes

# ===== PARTIE 3 : OPÉRATEURS SUR LES CHAÎNES =====

# 3.1 Concaténation de chaînes
# Concaténation simple
full_server_name = server_name + "-" + environment      # "web-prod-01-production"
server_endpoint = "http://" + server_ip                 # "http://192.168.1.10"

# 3.2 Formatage avec f-strings
# Messages de monitoring
cpu_status_message = f"CPU utilization: {cpu_usage}% on {server_name}"
memory_status_message = f"Memory: {memory_used_gb}/{memory_total_gb} GB ({memory_percent:.1f}%)"
disk_status_message = f"Disk space: {disk_free_tb:.2f} TB free of {disk_total_tb} TB"

# URL et identifiants
api_url = f"https://{server_ip}:{port_https}/api/v1/status"
log_filename = f"{server_name}_{environment}_{server_id}.log"

# 3.3 Répétition de chaînes
separator_line = "-" * 50      # "---...---" (50 caractères)
header_decoration = "=" * 20   # "===...===" (20 caractères)

# 3.4 Opérations avancées sur chaînes
# Transformation du nom serveur
server_name_upper = server_name.upper()                    # "WEB-PROD-01"
server_name_underscore = server_name.replace("-", "_")     # "web_prod_01"

# Construction de noms de services
service_prefix = "svc"
service_name = f"{service_prefix}_{server_name.replace('-', '_')}"  # "svc_web_prod_01"

# Tags et labels pour DevOps
environment_tag = f"env:{environment}"                              # "env:production"
location_tag = f"location:{server_location.split('-')[1]}"         # "location:paris"

# ===== PARTIE 4 : AFFICHAGE ET VALIDATION =====

# 4.1 Rapport de monitoring formaté
print("=" * 60)
print("          RAPPORT MONITORING SERVEUR")
print("=" * 60)

# Affichage des informations serveur
print("\nINFORMATIONS SERVEUR:")
print(f"   Nom: {server_name}")
print(f"   IP: {server_ip}")
print(f"   Environnement: {environment}")
print(f"   Localisation: {server_location}")
print(f"   SSL activé: {ssl_enabled}")
print(f"   Mode maintenance: {maintenance_mode}")

print("\nMÉTRIQUES SYSTÈME:")
print(f"   CPU: {cpu_usage}%")
print(f"   Mémoire: {memory_used_gb}/{memory_total_gb} GB ({memory_percent:.1f}%)")
print(f"   Disque: {disk_used_tb}/{disk_total_tb} TB ({disk_percent:.1f}%)")
print(f"   Temps de réponse: {response_time_ms} ms")
print(f"   Requêtes/seconde: {requests_per_second:.1f}")

print("\nCONNECTIVITÉ:")
print(f"   Ports ouverts: {open_ports}")
print(f"   Protocoles: {supported_protocols}")
print(f"   Endpoint HTTP: {server_endpoint}")
print(f"   API URL: {api_url}")

print("\nTAGS ET LABELS:")
print(f"   Service: {service_name}")
print(f"   Environment: {environment_tag}")
print(f"   Location: {location_tag}")
print(f"   Log file: {log_filename}")

print("\n" + "=" * 60)

# 4.2 Tests de validation
print("\nTESTS DE VALIDATION:")

# Vérification des calculs
print(f"Test memory_percent calculation: {memory_percent:.2f}% (attendu: 76.88%)")
print(f"Test disk_percent calculation: {disk_percent:.2f}% (attendu: 72.00%)")
print(f"Test requests_per_second: {requests_per_second:.2f} (attendu: 20.83)")

# Vérification des opérations sur chaînes
print(f"Test server name formatting: {server_name_upper} (attendu: WEB-PROD-01)")
print(f"Test service name generation: {service_name} (attendu: svc_web_prod_01)")

# Vérification des f-strings
print(f"Test API URL generation: {api_url}")
print(f"Test log filename: {log_filename}")

# Vérifications techniques avancées
print(f"\nVÉRIFICATIONS TECHNIQUES:")
print(f"   Memory en MB: {memory_used_mb:.1f} MB")
print(f"   Storage blocks: {storage_blocks} blocs")
print(f"   Memory en bytes: {memory_bytes:,.0f} bytes")
print(f"   Separator line length: {len(separator_line)} chars")

print("\nLAB 1 - Variables, types et opérateurs complété!")
print("Couverture: Sections 3 à 3.4 - Variables, types, opérateurs arithmétiques et sur chaînes")

# ===== VÉRIFICATION DES TYPES =====
print(f"\nTYPES PYTHON UTILISÉS:")
print(f"server_name: {type(server_name).__name__}")
print(f"cpu_usage: {type(cpu_usage).__name__}")
print(f"memory_total_gb: {type(memory_total_gb).__name__}")
print(f"is_production: {type(is_production).__name__}")
print(f"open_ports: {type(open_ports).__name__}")
print(f"server_config: {type(server_config).__name__}")

# ===== COMMENTAIRES PÉDAGOGIQUES =====
"""
POINTS CLÉS DÉMONTRÉS :

1. VARIABLES ET TYPES (Section 3.1-3.2):
   - Types primitifs : int, float, str, bool
   - Collections : list, dict
   - Nommage et conventions Python

2. OPÉRATEURS ARITHMÉTIQUES (Section 3.3):
   - Addition, soustraction, multiplication, division
   - Division entière (//) et modulo (%)
   - Puissance (**)
   - Ordre des opérations

3. OPÉRATEURS SUR CHAÎNES (Section 3.4):
   - Concaténation avec +
   - Formatage avec f-strings
   - Répétition avec *
   - Méthodes : upper(), replace(), split()

APPLICATIONS DEVOPS ILLUSTRÉES :
   - Monitoring de système
   - Configuration management
   - Génération d'URLs et noms de fichiers
   - Tags et labels pour containers/services
   - Calculs de métriques et pourcentages

BONNES PRATIQUES :
   - Variables explicites et bien nommées
   - Formatage professionnel avec f-strings
   - Validation des résultats
   - Documentation claire du code
"""

