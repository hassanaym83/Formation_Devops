"""
LAB 2 - Structures conditionnelles pour DevOps

Objectif : Maîtriser les structures conditionnelles pour l'automatisation DevOps
Contexte : Système d'alertes et de prise de décision automatique

Couverture : Section 5.1 - Structures conditionnelles
- 5.1.1 if, elif, else
- 5.1.2 Conditions imbriquées
- 5.1.3 Opérateurs logiques dans conditions
- 5.1.4 Cas spéciaux et pièges

Instructions :
1. Créer un système d'alertes basé sur les métriques serveur avec conditions
2. Implémenter des niveaux d'alerte (OK, WARNING, CRITICAL) avec elif
3. Utiliser des conditions imbriquées pour des cas complexes
4. Appliquer des opérateurs logiques pour des conditions combinées
5. Gérer les cas spéciaux et éviter les pièges courants

Points : 5/30
Durée estimée : 20 minutes
"""

# ===== PARTIE 1 : DONNÉES DE TEST =====

# Données d'un serveur unique pour tests
server_data = {
    "name": "web-prod-01",
    "cpu": 0.0,      # TODO: Définir une valeur de test (ex: 45.2, 89.7, 95.2)
    "memory": 0.0,   # TODO: Définir une valeur de test (ex: 68.5, 92.1, 98.7)
    "disk": 0.0,     # TODO: Définir une valeur de test (ex: 75.0, 58.3, 92.1)
    "status": "",    # TODO: "running" ou "stopped"
    "environment": "",  # TODO: "production", "staging", "development"
    "service_type": ""  # TODO: "web", "database", "cache"
}

# Seuils d'alerte configurables
cpu_warning_threshold = 70
cpu_critical_threshold = 85
memory_warning_threshold = 80
memory_critical_threshold = 90
disk_warning_threshold = 75
disk_critical_threshold = 85

# ===== PARTIE 2 : STRUCTURES CONDITIONNELLES SIMPLES =====

print("=" * 60)
print("        SYSTÈME D'ALERTES CONDITIONNELLES")
print("=" * 60)

# TODO: Extraire les métriques du serveur
cpu = 0.0     # TODO: server_data["cpu"]
memory = 0.0  # TODO: server_data["memory"]
disk = 0.0    # TODO: server_data["disk"]
status = ""   # TODO: server_data["status"]

print(f"\nSERVEUR: {server_data['name']}")
print(f"   Status: {status}")
print(f"   CPU: {cpu}%")
print(f"   Memory: {memory}%")
print(f"   Disk: {disk}%")

# ===== PARTIE 3 : CONDITIONS SIMPLES (IF/ELIF/ELSE) =====

print("\nANALYSE CPU:")
# TODO: Implémenter la logique conditionnelle CPU
if True:  # TODO: Condition pour cpu >= cpu_critical_threshold
    cpu_level = "CRITICAL"
    cpu_action = "Redémarrage immédiat requis"
elif True:  # TODO: Condition pour cpu >= cpu_warning_threshold
    cpu_level = "WARNING"
    cpu_action = "Surveillance renforcée"
else:
    cpu_level = "OK"
    cpu_action = "Fonctionnement normal"

print(f"   Level: {cpu_level}")
print(f"   Action: {cpu_action}")

print("\nANALYSE MEMORY:")
# TODO: Implémenter la logique conditionnelle Memory
memory_level = "OK"    # TODO: Déterminer le niveau selon les seuils
memory_action = ""     # TODO: Déterminer l'action selon le niveau

print(f"   Level: {memory_level}")
print(f"   Action: {memory_action}")

print("\nANALYSE DISK:")
# TODO: Implémenter la logique conditionnelle Disk
disk_level = "OK"     # TODO: Déterminer le niveau selon les seuils
disk_action = ""      # TODO: Déterminer l'action selon le niveau

print(f"   Level: {disk_level}")
print(f"   Action: {disk_action}")

# ===== PARTIE 4 : CONDITIONS COMPLEXES (OPÉRATEURS LOGIQUES) =====

print("\nANALYSE GLOBALE:")

# TODO: Conditions combinées avec AND
is_system_critical = False  # TODO: cpu >= cpu_critical_threshold AND memory >= memory_critical_threshold

# TODO: Conditions combinées avec OR
has_any_warning = False     # TODO: cpu >= cpu_warning_threshold OR memory >= memory_warning_threshold OR disk >= disk_warning_threshold

# TODO: Conditions avec NOT
is_system_healthy = False   # TODO: NOT (has_any_warning)

print(f"   Système critique: {is_system_critical}")
print(f"   Alerte active: {has_any_warning}")
print(f"   Système sain: {is_system_healthy}")

# ===== PARTIE 5 : CONDITIONS IMBRIQUÉES =====

print("\nÉVALUATION SANTÉ GLOBALE:")

# TODO: Implémenter des conditions imbriquées
if True:  # TODO: status == "running"
    if True:  # TODO: is_system_critical
        if True:  # TODO: server_data["environment"] == "production"
            health_status = "URGENCE_PRODUCTION"
            recommended_action = "Escalade immédiate équipe production"
        else:
            health_status = "CRITIQUE_NON_PROD"
            recommended_action = "Intervention rapide équipe dev"
    elif True:  # TODO: has_any_warning
        health_status = "SURVEILLANCE"
        recommended_action = "Monitoring renforcé"
    else:
        health_status = "OPERATIONNEL"
        recommended_action = "Monitoring standard"
else:
    health_status = "HORS_SERVICE"
    recommended_action = "Redémarrage du service"

print(f"   Statut santé: {health_status}")
print(f"   Action recommandée: {recommended_action}")

# ===== PARTIE 6 : CAS SPÉCIAUX ET PIÈGES =====

print("\nGESTION DES CAS SPÉCIAUX:")

# TODO: Gestion des valeurs None/vides
if True:  # TODO: cpu is not None and memory is not None and disk is not None
    print("   Toutes les métriques sont disponibles")
else:
    print("   Métriques manquantes détectées")

# TODO: Gestion des valeurs aberrantes
if True:  # TODO: cpu > 100 or memory > 100 or disk > 100
    print("   Valeurs aberrantes détectées (>100%)")
elif True:  # TODO: cpu < 0 or memory < 0 or disk < 0
    print("   Valeurs négatives détectées")
else:
    print("   Toutes les valeurs sont dans les limites normales")

# TODO: Gestion des types de services spéciaux
service_type = ""  # TODO: server_data["service_type"]

if True:  # TODO: service_type == "database"
    # Base de données : seuils plus stricts
    db_cpu_critical = 70  # Plus strict que le général
    if True:  # TODO: cpu >= db_cpu_critical
        print("   Base de données : CPU critique (seuil strict appliqué)")
elif True:  # TODO: service_type == "cache"
    # Cache : tolérance plus élevée sur memory
    cache_memory_critical = 95  # Plus tolérant
    if True:  # TODO: memory >= cache_memory_critical
        print("   Cache : Memory dans les limites (seuil adapté)")
else:
    print("   Serveur standard : Seuils normaux appliqués")

# ===== PARTIE 7 : DÉCISIONS AUTOMATISÉES =====

print("\nDÉCISIONS AUTOMATISÉES:")

# TODO: Décision basée sur l'environnement et la criticité
environment = ""  # TODO: server_data["environment"]

if True:  # TODO: environment == "production"
    if True:  # TODO: health_status == "URGENCE_PRODUCTION"
        auto_action = "Basculement automatique sur serveur backup"
        notification_level = "CRITICAL"
    elif True:  # TODO: health_status == "SURVEILLANCE"
        auto_action = "Pré-positionnement équipe astreinte"
        notification_level = "WARNING"
    else:
        auto_action = "Monitoring continu"
        notification_level = "INFO"
elif True:  # TODO: environment == "staging"
    if True:  # TODO: health_status.startswith("CRITIQUE")
        auto_action = "Redémarrage automatique autorisé"
        notification_level = "WARNING"
    else:
        auto_action = "Tests automatiques de charge"
        notification_level = "INFO"
else:  # development
    auto_action = "Notifications développeur uniquement"
    notification_level = "DEBUG"

print(f"   Action automatique: {auto_action}")
print(f"   Niveau notification: {notification_level}")

# ===== PARTIE 8 : VALIDATION ET TESTS =====

print("\nVALIDATION DES CONDITIONS:")

# TODO: Tests de validation des conditions
test_results = []

# Test 1: Logique CPU
if True:  # TODO: cpu >= cpu_critical_threshold
    if cpu_level == "CRITICAL":
        test_results.append("Test CPU CRITICAL: OK")
    else:
        test_results.append("Test CPU CRITICAL: ÉCHEC")

# Test 2: Logique combinée
if True:  # TODO: has_any_warning
    test_results.append("Test alerte combinée: OK")
else:
    test_results.append("Test alerte combinée: ÉCHEC")

# Test 3: Conditions imbriquées
if True:  # TODO: status == "running" and environment == "production"
        if health_status in ["URGENCE_PRODUCTION", "CRITIQUE_NON_PROD", "SURVEILLANCE", "OPERATIONNEL"]:
            test_results.append("Test conditions imbriquées: OK")
        else:
            test_results.append("Test conditions imbriquées: ÉCHEC")

for result in test_results:
    print(f"   {result}")

print("\nLAB 2 - Structures conditionnelles complété!")
print("Couverture: Section 5.1 - if/elif/else, conditions imbriquées, opérateurs logiques")
