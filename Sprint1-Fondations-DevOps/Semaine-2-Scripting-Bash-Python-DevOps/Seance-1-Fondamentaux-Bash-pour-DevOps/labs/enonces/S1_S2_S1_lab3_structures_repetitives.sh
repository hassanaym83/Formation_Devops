#!/bin/bash

# S1_S2_S1_LAB3 - Structures répétitives pour DevOps
# DURÉE : 20 minutes

# OBJECTIF :
# Développez un script d'administration utilisant différents types de boucles pour automatiser 
# la surveillance et la maintenance d'infrastructure.

# CONTEXTE :
# Script de monitoring automatisé pour infrastructure de production

# CONSIGNES :
# 1. Créez une boucle for pour tester plusieurs services système
# 2. Implémentez une boucle while pour retry avec tentatives limitées
# 3. Utilisez une boucle for avec plage numérique pour rotation de fichiers
# 4. Combinez conditions et boucles pour logique avancée

# CRITÈRES D'ÉVALUATION :
# □ 3 types de boucles fonctionnelles (for tableau, while retry, for numérique)
# □ Logique de retry avec limite de tentatives
# □ Gestion d'erreurs dans les boucles
# □ Tests de services système
# □ Affichage formaté des résultats

# RÉSULTAT ATTENDU :
# Un script de monitoring qui teste des services, effectue des retry intelligents,
# et gère la rotation de fichiers automatiquement

# ====== TEMPLATE DE DÉPART ======

#!/bin/bash

echo "=== Script de monitoring infrastructure ==="

# TODO: Section 1 - Boucle for pour test de services
echo "1. Vérification des services critiques"

# TODO: Créez un tableau avec les services à vérifier
# services=("nginx" "docker" "ssh")

# TODO: Utilisez une boucle for pour tester chaque service
# for service in "${services[@]}"; do
#     # Testez si le service est actif avec systemctl
#     # Affichez ACTIF ou INACTIF selon le résultat
# done

echo ""

# TODO: Section 2 - Boucle while pour retry de connexion
echo "2. Test de connectivité avec retry"

# TODO: Configurez les variables de retry
# url_test="httpbin.org"  # URL à tester
# max_tentatives=3
# tentative=1

# TODO: Boucle while pour tentatives de ping
# while [[ $tentative -le $max_tentatives ]]; do
#     # Testez la connectivité avec ping
#     # Si succès : affichez "CONNEXION OK" et sortez (break)
#     # Si échec : affichez tentative échouée, sleep 2, incrémentez compteur
# done

# TODO: Vérifiez si toutes les tentatives ont échoué

echo ""

# TODO: Section 3 - Boucle for numérique pour rotation
echo "3. Simulation rotation de fichiers logs"

# TODO: Boucle for avec plage {1..5}
# for jour in {1..5}; do
#     # Simulez la vérification de fichiers logs
#     # fichier_log="/var/log/app_day_$jour.log"
#     # Affichez l'état du fichier (existant/manquant)
# done

echo "=== Monitoring terminé ==="

# ====== AIDE SUR LES BOUCLES ======
# Boucle for tableau : for item in "${array[@]}"; do ... done
# Boucle for numérique : for i in {1..10}; do ... done  
# Boucle while : while [[ condition ]]; do ... done
# Test de service : systemctl is-active --quiet service_name
# Test ping : ping -c 1 -W 2 hostname >/dev/null 2>&1
# Incrémentation : ((variable++))
# Sortie de boucle : break

# ====== COMMANDES UTILES ======
# systemctl is-active --quiet nginx    # Test service (retourne 0 si actif)
# ping -c 1 google.com >/dev/null     # Test ping silencieux
# [[ -f "/path/file" ]]               # Test existence fichier
# sleep 2                             # Pause 2 secondes

# ====== TESTS À EFFECTUER ======
# 1. Exécutez le script et observez les trois sections
# 2. Modifiez les services testés selon votre système  
# 3. Testez avec une URL inaccessible pour voir les retry
# 4. Vérifiez que la rotation simule bien 5 fichiers

# BONUS :
# Ajoutez des couleurs aux messages avec echo -e "\033[32mVERT\033[0m"