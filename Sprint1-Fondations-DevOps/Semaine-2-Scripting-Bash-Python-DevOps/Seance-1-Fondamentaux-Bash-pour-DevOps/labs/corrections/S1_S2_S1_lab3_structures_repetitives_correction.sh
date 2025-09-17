#!/bin/bash

# S1_S2_S1_LAB3 - Structures répétitives pour DevOps - CORRECTION
#
# Cette correction présente une solution complète et optimisée.
#
# Concepts démontrés :
# - Boucle for pour itération sur tableaux
# - Boucle while avec logique de retry
# - Boucle for avec plages numériques {1..N}
# - Conditions if/else dans les boucles  
# - Tests de services système avec systemctl
# - Tests de connectivité réseau avec ping
# - Gestion des compteurs et limites
#
# Bonnes pratiques appliquées :
# - Tableaux pour données structurées
# - Variables de contrôle pour limites
# - Gestion des codes de retour
# - Affichage formaté et informatif
# - Combinaison logique conditions + boucles

#!/bin/bash

# Script de monitoring infrastructure avec boucles multiples
# Démontre l'usage des différents types de boucles en contexte DevOps

echo "=== Script de monitoring infrastructure ==="
echo "Démarré le: $(date)"
echo ""

# ====== SECTION 1 - Boucle for pour test de services ======

echo "1. Vérification des services critiques"
echo "--------------------------------------"

# Tableau des services à vérifier (adaptez selon votre système)
services=("ssh" "cron" "systemd-resolved")

# Compteurs pour statistiques
services_actifs=0
services_total=${#services[@]}

# Boucle for : parcourt chaque service du tableau
for service in "${services[@]}"; do
    echo -n "Service $service: "
    
    # Test si le service est actif (systemctl retourne 0 si actif)
    if systemctl is-active --quiet "$service" 2>/dev/null; then
        echo "ACTIF"
        ((services_actifs++))
    else
        echo "INACTIF"
    fi
done

echo "Résultat: $services_actifs/$services_total services actifs"
echo ""

# ====== SECTION 2 - Boucle while pour retry de connexion ======

echo "2. Test de connectivité avec retry"
echo "----------------------------------"

# Configuration des paramètres de retry
url_test="8.8.8.8"          # DNS Google (fiable pour test)
max_tentatives=3
tentative=1
connexion_ok=false

echo "Test de connectivité vers $url_test..."

# Boucle while : continue tant que tentative <= limite ET pas de succès
while [[ $tentative -le $max_tentatives ]] && [[ "$connexion_ok" == false ]]; do
    echo -n "Tentative $tentative/$max_tentatives: "
    
    # Test ping avec timeout court (-c 1 paquet, -W 2 secondes timeout)
    if ping -c 1 -W 2 "$url_test" >/dev/null 2>&1; then
        echo "CONNEXION OK"
        connexion_ok=true
        break  # Sortie immédiate si succès
    else
        echo "ÉCHEC"
        
        # Si ce n'est pas la dernière tentative, attendre avant retry
        if [[ $tentative -lt $max_tentatives ]]; then
            echo "  Attente 2 secondes avant nouvelle tentative..."
            sleep 2
        fi
        
        ((tentative++))  # Incrémentation du compteur
    fi
done

# Vérification finale du résultat
if [[ "$connexion_ok" == false ]]; then
    echo "ALERTE: Impossible de joindre $url_test après $max_tentatives tentatives"
else
    echo "Connectivité réseau: OK"
fi

echo ""

# ====== SECTION 3 - Boucle for numérique pour rotation ======

echo "3. Simulation rotation de fichiers logs"
echo "---------------------------------------"

# Configuration pour simulation
log_base_path="/var/log/myapp"
jours_retention=5

echo "Vérification des logs pour $jours_retention derniers jours:"

# Compteurs pour statistiques
fichiers_presents=0
fichiers_manquants=0

# Boucle for avec plage numérique : {1..5} génère 1, 2, 3, 4, 5
for jour in {1..5}; do
    # Construction du nom de fichier avec jour
    fichier_log="${log_base_path}_day_${jour}.log"
    
    echo -n "Jour $jour ($fichier_log): "
    
    # Test d'existence du fichier (-f = fichier régulier)
    if [[ -f "$fichier_log" ]]; then
        # Calcul de la taille du fichier
        taille=$(du -h "$fichier_log" 2>/dev/null | cut -f1)
        echo "PRÉSENT (${taille:-"inconnu"})"
        ((fichiers_presents++))
    else
        echo "MANQUANT"
        ((fichiers_manquants++))
    fi
done

echo "Statistiques: $fichiers_presents présents, $fichiers_manquants manquants"
echo ""

# ====== SECTION 4 - Boucle combinée avec conditions ======

echo "4. Analyse combinée (bonus)"
echo "---------------------------"

# Exemple de boucle for imbriquée avec conditions multiples
environnements=("dev" "staging")
services_env=("nginx" "mysql")

for env in "${environnements[@]}"; do
    echo "Environnement: $env"
    
    for service in "${services_env[@]}"; do
        echo -n "  $service: "
        
        # Simulation de test par environnement
        # En réalité, on testerait des services spécifiques à chaque env
        if systemctl is-active --quiet "$service" 2>/dev/null; then
            echo "ACTIF"
        else
            echo "NON INSTALLÉ/INACTIF"
        fi
    done
    echo ""
done

echo "=== Monitoring terminé ==="
echo "Rapport généré le: $(date)"

# ====== EXPLICATIONS TECHNIQUES ======

# 1. BOUCLE FOR AVEC TABLEAUX
#    for item in "${array[@]}"; do
#    "${array[@]}" expanse tous les éléments du tableau
#    Chaque élément est assigné à 'item' tour à tour

# 2. BOUCLE WHILE AVEC CONDITIONS MULTIPLES  
#    while [[ condition1 ]] && [[ condition2 ]]; do
#    Continue tant que TOUTES les conditions sont vraies
#    Utilise && (ET logique) ou || (OU logique)

# 3. BOUCLE FOR AVEC PLAGES
#    for i in {1..10}; do
#    {début..fin} génère une séquence numérique
#    {1..10..2} génère 1,3,5,7,9 (pas de 2)

# 4. CONTRÔLE DE BOUCLES
#    break    : sortie immédiate de la boucle
#    continue : passe à l'itération suivante
#    return   : sortie d'une fonction (si dans une fonction)

# 5. TESTS SYSTÈME COURANTS
#    systemctl is-active service  : teste si service actif (code retour 0/1)
#    ping -c 1 host              : teste connectivité (1 paquet)
#    [[ -f file ]]               : teste existence fichier
#    [[ -d dir ]]                : teste existence répertoire

# ====== VARIANTES ET AMÉLIORATIONS ======

# Test de service avec timeout :
# timeout 5 systemctl is-active service

# Boucle infinie avec break conditionnel :
# while true; do
#     # logique métier
#     [[ condition ]] && break
# done

# Boucle avec continue pour filtrage :
# for file in *; do
#     [[ ! -f "$file" ]] && continue  # Ignore si pas un fichier
#     # traiter le fichier
# done

# ====== USAGES DEVOPS RÉELS ======
# - Déploiement sur multiples serveurs (boucle for sur liste serveurs)
# - Attente démarrage service avec retry (boucle while)  
# - Rotation automatique logs/backups (boucle for numérique)
# - Health checks périodiques (boucle while infinie)
# - Validation multi-environnements (boucles imbriquées)