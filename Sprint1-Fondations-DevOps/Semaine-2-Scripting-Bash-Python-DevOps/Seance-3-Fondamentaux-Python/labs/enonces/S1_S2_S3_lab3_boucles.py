"""
LAB 3 - Boucles avancées pour DevOps

Objectif : Maîtriser les boucles pour l'automatisation DevOps
Contexte : Automation de tâches répétitives sur infrastructure

Couverture : Section 5.2 - Boucles
- 5.2.1 Boucle for avec listes
- 5.2.2 Boucle for avec dictionnaires  
- 5.2.3 Boucles while et contrôle de flux

Instructions :
1. Parcourir des listes de serveurs et appliquer des opérations
2. Itérer sur des configurations dans des dictionnaires
3. Utiliser enumerate() et zip() pour des traitements avancés
4. Implémenter des boucles while pour monitoring continu
5. Gérer break et continue pour contrôler les flux

Points : 5/30
Durée estimée : 20 minutes
"""

# ===== PARTIE 1 : DONNÉES D'INFRASTRUCTURE =====

# Listes de serveurs par type
web_servers = ["web-01", "web-02", "web-03", "web-04"]
db_servers = ["db-primary", "db-replica-01", "db-replica-02"]  
cache_servers = ["redis-01", "redis-02", "memcached-01"]
all_servers = web_servers + db_servers + cache_servers

# Ports de services par serveur
server_ports = {
    "web-01": [80, 443, 22],
    "web-02": [80, 443, 22], 
    "db-primary": [3306, 22],
    "db-replica-01": [3306, 22],
    "redis-01": [6379, 22],
    "redis-02": [6379, 22]
}

# Métriques de performance (CPU, Memory, Disk)
server_metrics = {
    "web-01": {"cpu": 45, "memory": 67, "disk": 55},
    "web-02": {"cpu": 78, "memory": 82, "disk": 43},
    "db-primary": {"cpu": 89, "memory": 91, "disk": 76},
    "redis-01": {"cpu": 23, "memory": 34, "disk": 12}
}

# ===== PARTIE 2 : BOUCLES FOR AVEC LISTES =====

print("=" * 50)
print("        AUTOMATION INFRASTRUCTURE")
print("=" * 50)

print("\nPARTIE 1 : BOUCLES FOR AVEC LISTES")

# TODO: Parcourir tous les serveurs et afficher leur type
print("\nINVENTAIRE DES SERVEURS:")
for server in all_servers:
    # TODO: Déterminer le type de serveur selon son nom
    server_type = ""  # TODO: Logique pour identifier le type (web, db, cache)
    print(f"  - {server} ({server_type})")

# TODO: Utiliser enumerate() pour numéroter les serveurs
print("\nSERVEURS NUMÉROTÉS:")
for index, server in enumerate(all_servers):
    # TODO: Afficher index + 1 et nom du serveur
    print(f"  {index + 1}. {server}")

# TODO: Parcourir uniquement les serveurs web avec leur index
print("\nSERVEURS WEB AVEC INDEX:")
# TODO: Utiliser enumerate() sur web_servers

# ===== PARTIE 3 : BOUCLES FOR AVEC DICTIONNAIRES =====

print("\nPARTIE 2 : BOUCLES FOR AVEC DICTIONNAIRES")

# TODO: Parcourir les ports de chaque serveur
print("\nPORTS PAR SERVEUR:")
for server, ports in server_ports.items():
    # TODO: Afficher le serveur et ses ports
    print(f"  {server}: {ports}")
    
    # TODO: Sous-boucle pour vérifier chaque port
    for port in ports:
        # TODO: Simuler vérification de port (affichage simple)
        print(f"    - Port {port}: OK")

# TODO: Analyser les métriques avec nested loops
print("\nANALYSE DES MÉTRIQUES:")
for server, metrics in server_metrics.items():
    print(f"\n  {server}:")
    
    # TODO: Parcourir chaque métrique
    for metric_name, value in metrics.items():
        # TODO: Appliquer une règle simple selon la métrique
        if metric_name == "cpu":
            status = ""  # TODO: "HIGH" si > 80, "OK" sinon
        elif metric_name == "memory":
            status = ""  # TODO: "HIGH" si > 85, "OK" sinon
        else:  # disk
            status = ""  # TODO: "HIGH" si > 70, "OK" sinon
        
        print(f"    {metric_name}: {value}% ({status})")

# ===== PARTIE 4 : FONCTIONS AVANCÉES (ZIP, ENUMERATE) =====

print("\nPARTIE 3 : FONCTIONS AVANCÉES")

# TODO: Utiliser zip() pour combiner serveurs et types
server_types = ["web", "web", "web", "web", "db", "db", "db", "cache", "cache", "cache"]

print("\nSERVEURS AVEC TYPES (ZIP):")
# TODO: Utiliser zip(all_servers, server_types) pour combiner
for server, server_type in zip(all_servers, server_types):
    print(f"  {server} -> {server_type}")

# TODO: Créer des paires de serveurs pour backup
print("\nPAIRES DE BACKUP:")
for i in range(0, len(web_servers), 2):
    # TODO: Créer des paires (0-1, 2-3, etc.)
    if i + 1 < len(web_servers):
        primary = web_servers[i]
        backup = web_servers[i + 1]
    print(f"  Pair: {primary} <-> {backup}")

# ===== PARTIE 5 : BOUCLES WHILE ET CONTRÔLE =====

print("\nPARTIE 4 : BOUCLES WHILE ET CONTRÔLE")

# TODO: Simulation monitoring continu avec while
print("\nSIMULATION MONITORING (3 cycles):")
cycle = 0
max_cycles = 3

# TODO: Boucle while pour monitoring
while cycle < max_cycles:
    cycle += 1
    print(f"\n  Cycle de monitoring #{cycle}")
    
    # TODO: Vérifier les serveurs critiques seulement
    for server in ["db-primary", "web-01"]:
        if server in server_metrics:
            cpu = server_metrics[server]["cpu"]
            
            # TODO: Utiliser continue si serveur OK
            if cpu < 70:
                print(f"    {server}: OK (CPU: {cpu}%)")
                continue
            
            # TODO: Afficher alerte si problème
            print(f"    ATTENTION {server}: (CPU: {cpu}%)")
            
            # TODO: Utiliser break si critique
            if cpu > 85:
                print(f"    ARRET MONITORING - {server} critique!")
                break

# ===== PARTIE 6 : AUTOMATION BATCH =====

print("\nPARTIE 5 : AUTOMATION BATCH")

# TODO: Traitement par lots avec contrôle de flux
batch_size = 2
total_servers = len(all_servers)

print(f"\nTRAITEMENT PAR LOTS (taille: {batch_size}):")

# TODO: Boucle for avec range et step
for i in range(0, total_servers, batch_size):
    # TODO: Créer le batch actuel
    batch = all_servers[i:i + batch_size]
    batch_num = (i // batch_size) + 1
    
    print(f"\n  Batch #{batch_num}: {batch}")
    
    # TODO: Traiter chaque serveur du batch
    for server in batch:
        # TODO: Simuler une opération (mise à jour, backup, etc.)
        print(f"    Traitement {server}... OK")
        
        # TODO: Simuler échec sur db-primary
        if server == "db-primary":
            print(f"    Echec sur {server} - Skip batch")
            break  # Sort de la boucle interne
    else:
        # TODO: Ce bloc s'exécute si aucun break
        print(f"    Batch #{batch_num} terminé avec succès")

print("\nLAB 3 - Boucles avancées complété!")
print("Couverture: Section 5.2 - for, while, enumerate, zip, break, continue")

