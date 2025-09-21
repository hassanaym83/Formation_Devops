"""
LAB 3 - Boucles avancées pour DevOps - CORRECTION

Objectif : Maîtriser les boucles pour l'automatisation DevOps
Contexte : Automation de tâches répétitives sur infrastructure

Couverture : Section 5.2 - Boucles
- 5.2.1 Boucle for avec listes
- 5.2.2 Boucle for avec dictionnaires  
- 5.2.3 Boucles while et contrôle de flux

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

# Parcourir tous les serveurs et afficher leur type
print("\nINVENTAIRE DES SERVEURS:")
for server in all_servers:
    # Déterminer le type de serveur selon son nom
    if server.startswith("web"):
        server_type = "Web Server"
    elif server.startswith("db"):
        server_type = "Database Server"
    elif server.startswith("redis") or server.startswith("memcached"):
        server_type = "Cache Server"
    else:
        server_type = "Unknown"
    
    print(f"  - {server} ({server_type})")

# Utiliser enumerate() pour numéroter les serveurs
print("\nSERVEURS NUMÉROTÉS:")
for index, server in enumerate(all_servers):
    print(f"  {index + 1}. {server}")

# Parcourir uniquement les serveurs web avec leur index
print("\nSERVEURS WEB AVEC INDEX:")
for index, server in enumerate(web_servers):
    print(f"  Web-{index + 1}: {server}")

# ===== PARTIE 3 : BOUCLES FOR AVEC DICTIONNAIRES =====

print("\nPARTIE 2 : BOUCLES FOR AVEC DICTIONNAIRES")

# Parcourir les ports de chaque serveur
print("\nPORTS PAR SERVEUR:")
for server, ports in server_ports.items():
    print(f"  {server}: {ports}")
    
    # Sous-boucle pour vérifier chaque port
    for port in ports:
        # Simuler vérification de port
        if port == 22:
            print(f"    - Port {port}: SSH OK")
        elif port in [80, 443]:
            print(f"    - Port {port}: HTTP/HTTPS OK")
        elif port == 3306:
            print(f"    - Port {port}: MySQL OK")
        elif port == 6379:
            print(f"    - Port {port}: Redis OK")
        else:
            print(f"    - Port {port}: OK")

# Analyser les métriques avec nested loops
print("\nANALYSE DES MÉTRIQUES:")
for server, metrics in server_metrics.items():
    print(f"\n  {server}:")
    
    # Parcourir chaque métrique
    for metric_name, value in metrics.items():
        # Appliquer une règle selon la métrique
        if metric_name == "cpu":
            status = "HIGH" if value > 80 else "OK"
        elif metric_name == "memory":
            status = "HIGH" if value > 85 else "OK"
        else:  # disk
            status = "HIGH" if value > 70 else "OK"
        
        print(f"    {metric_name}: {value}% ({status})")

# ===== PARTIE 4 : FONCTIONS AVANCÉES (ZIP, ENUMERATE) =====

print("\nPARTIE 3 : FONCTIONS AVANCÉES")

# Utiliser zip() pour combiner serveurs et types
server_types = ["web", "web", "web", "web", "db", "db", "db", "cache", "cache", "cache"]

print("\nSERVEURS AVEC TYPES (ZIP):")
for server, server_type in zip(all_servers, server_types):
    print(f"  {server} → {server_type}")

# Créer des paires de serveurs pour backup
print("\nPAIRES DE BACKUP:")
for i in range(0, len(web_servers), 2):
    # Créer des paires (0-1, 2-3, etc.)
    if i + 1 < len(web_servers):
        primary = web_servers[i]
        backup = web_servers[i + 1]
    print(f"  Pair: {primary} <-> {backup}")

# ===== PARTIE 5 : BOUCLES WHILE ET CONTRÔLE =====

print("\nPARTIE 4 : BOUCLES WHILE ET CONTRÔLE")

# Simulation monitoring continu avec while
print("\nSIMULATION MONITORING (3 cycles):")
cycle = 0
max_cycles = 3

# Boucle while pour monitoring
while cycle < max_cycles:
    cycle += 1
    print(f"\n  Cycle de monitoring #{cycle}")
    
    # Vérifier les serveurs critiques seulement
    for server in ["db-primary", "web-01"]:
        if server in server_metrics:
            cpu = server_metrics[server]["cpu"]
            
            # Utiliser continue si serveur OK
            if cpu < 70:
                print(f"    {server}: OK (CPU: {cpu}%)")
                continue
            
            # Afficher alerte si problème
            print(f"    ATTENTION {server}: (CPU: {cpu}%)")
            
            # Utiliser break si critique
            if cpu > 85:
                print(f"    ARRET MONITORING - {server} critique!")
                break
    else:
        # Ce bloc s'exécute si aucun break dans la boucle for
        print(f"    Cycle #{cycle} terminé - Tous serveurs vérifiés")

# ===== PARTIE 6 : AUTOMATION BATCH =====

print("\nPARTIE 5 : AUTOMATION BATCH")

# Traitement par lots avec contrôle de flux
batch_size = 2
total_servers = len(all_servers)

print(f"\nTRAITEMENT PAR LOTS (taille: {batch_size}):")

# Boucle for avec range et step
for i in range(0, total_servers, batch_size):
    # Créer le batch actuel
    batch = all_servers[i:i + batch_size]
    batch_num = (i // batch_size) + 1
    
    print(f"\n  Batch #{batch_num}: {batch}")
    
    # Traiter chaque serveur du batch
    for server in batch:
        # Simuler une opération (mise à jour, backup, etc.)
        print(f"    Traitement {server}... OK")
        
        # Simuler échec sur db-primary
        if server == "db-primary":
            print(f"    Echec sur {server} - Skip batch")
            break  # Sort de la boucle interne
    else:
        # Ce bloc s'exécute si aucun break
        print(f"    Batch #{batch_num} terminé avec succès")

# ===== PARTIE 7 : DÉMONSTRATION AVANCÉE =====

print("\nPARTIE 6 : TECHNIQUES AVANCÉES")

# List comprehensions avec boucles
print("\nLIST COMPREHENSIONS:")
web_server_names = [server for server in all_servers if server.startswith("web")]
print(f"  Serveurs web: {web_server_names}")

high_cpu_servers = [server for server, metrics in server_metrics.items() if metrics["cpu"] > 75]
print(f"  Serveurs CPU élevé: {high_cpu_servers}")

# Boucles imbriquées avec break/continue avancé
print("\nMAINTENANCE PROGRAMMÉE:")
maintenance_groups = [web_servers[:2], web_servers[2:], db_servers]

for group_index, group in enumerate(maintenance_groups):
    print(f"\n  Groupe de maintenance #{group_index + 1}: {group}")
    
    for server in group:
        # Skip si serveur critique
        if server in server_metrics and server_metrics[server]["cpu"] > 85:
            print(f"    SKIP {server}: CPU trop élevé pour maintenance")
            continue
        
        # Simuler maintenance
        print(f"    Maintenance {server}: En cours...")
        print(f"    Maintenance {server}: Terminée")
        
        # Arrêt de groupe si problème sur serveur primaire
        if server == "db-primary":
            print(f"    Problème détecté sur {server} - Arrêt groupe")
            break
    else:
        print(f"    Groupe #{group_index + 1}: Maintenance complète réussie")

print("\nLAB 3 - Boucles avancées complété!")
print("Couverture: Section 5.2 - for, while, enumerate, zip, break, continue")

# ===== STATISTIQUES FINALES =====
print(f"\nSTATISTIQUES FINALES:")
print(f"  Total serveurs traités: {len(all_servers)}")
print(f"  Serveurs web: {len(web_servers)}")
print(f"  Serveurs DB: {len(db_servers)}")
print(f"  Serveurs cache: {len(cache_servers)}")
print(f"  Serveurs avec métriques: {len(server_metrics)}")

# ===== COMMENTAIRES PÉDAGOGIQUES =====
"""
POINTS CLÉS DÉMONTRÉS :

1. BOUCLES FOR BASIQUES:
   - Itération sur listes simples
   - Logique conditionnelle dans les boucles
   - Classification et categorisation

2. ENUMERATE() ET INDEX:
   - Accès simultané index + valeur
   - Numérotation automatique
   - Traitement positionnel

3. BOUCLES AVEC DICTIONNAIRES:
   - Parcours de clés/valeurs avec .items()
   - Boucles imbriquées (nested loops)
   - Traitement de données structurées

4. ZIP() ET COMBINAISONS:
   - Combinaison de listes parallèles
   - Création de paires et associations
   - Traitement par groupes

5. BOUCLES WHILE:
   - Monitoring continu simulé
   - Conditions de sortie dynamiques
   - Compteurs et états

6. CONTRÔLE DE FLUX:
   - break: sortie anticipée
   - continue: passage à l'itération suivante
   - else avec boucles (exécution si pas de break)

7. RANGE() ET SLICING:
   - Traitement par lots (batches)
   - Pagination de données
   - Indexation avancée

APPLICATIONS DEVOPS ILLUSTRÉES:
   - Inventaire d'infrastructure
   - Vérification de ports et services
   - Analyse de métriques système
   - Monitoring continu automatisé
   - Maintenance programmée par groupes
   - Traitement par lots de serveurs

TECHNIQUES AVANCÉES:
   - List comprehensions
   - Boucles imbriquées complexes
   - Gestion d'erreurs dans les boucles
   - Patterns de traitement distribué
"""