#!/bin/bash

# =============================================================================
# LAB 3 - Planification d'architecture réseau simple
# =============================================================================
#
# Énoncé : Comprendre comment planifier un réseau pour différents services
#
# Objectif : Concevoir un plan d'adressage pour environnement d'entreprise
#
# Durée estimée : 25 minutes 
# Niveau de difficulté : Intermédiaire
# Prérequis : Connaissance de base des adresses IP et CIDR (LAB 1 et 2)
# =============================================================================

# =============================================================================
# PARTIE 1 - Pourquoi séparer les réseaux ?
# =============================================================================

echo "=== LAB 3 - Planification d'architecture réseau simple ==="
echo ""
echo "POURQUOI SÉPARER LES RÉSEAUX ?"
echo "================================="
echo ""
echo "Dans une entreprise, on sépare les réseaux pour :"
echo "• SÉCURITÉ : Isoler les serveurs importants"
echo "• ORGANISATION : Grouper les machines par fonction" 
echo "• PERFORMANCE : Éviter les embouteillages réseau"
echo "• MAINTENANCE : Faciliter la gestion et le diagnostic"
echo ""
echo "EXEMPLE CONCRET :"
echo "==================="
echo "Une école a besoin de :"
echo "• Réseau ADMINISTRATION (direction, comptabilité)"
echo "• Réseau ENSEIGNANTS (salles des profs, préparations)"
echo "• Réseau ÉTUDIANTS (salles de classe, WiFi public)"
echo "• Réseau SERVEURS (site web, fichiers partagés)"
echo ""
echo "Chaque réseau a ses propres règles et restrictions."
echo ""

# =============================================================================
# PARTIE 2 - Calculer les besoins en adresses
# =============================================================================

echo " EXERCICE 1 - Calculer les besoins :"
echo "======================================"
echo ""
echo "Imaginons une petite entreprise avec :"
echo "• 10 machines d'administration"
echo "• 25 postes d'employés"
echo "• 5 serveurs"
echo "• 50 appareils WiFi (invités, téléphones)"
echo ""
echo "CALCUL DES TAILLES DE RÉSEAU :"
echo ""
echo "Pour 10 machines d'administration :"
echo "• Besoin minimum : 10 adresses"
echo "• Avec marge de croissance : 20 adresses"
echo "• Réseau conseillé : /27 (30 adresses utilisables)"
echo ""
echo "Pour 25 postes d'employés :"
echo "• Besoin minimum : 25 adresses"
echo "• Avec marge de croissance : 50 adresses" 
echo "• Réseau conseillé : /26 (62 adresses utilisables)"
echo ""
echo "Pour 5 serveurs :"
echo "• Besoin minimum : 5 adresses"
echo "• Avec marge : 10 adresses"
echo "• Réseau conseillé : /28 (14 adresses utilisables)"
echo ""
echo "Pour 50 appareils WiFi :"
echo "• Besoin minimum : 50 adresses"
echo "• Avec marge : 100 adresses"
echo "• Réseau conseillé : /25 (126 adresses utilisables)"
echo ""

echo "VÉRIFICATION AVEC IPCALC :"
echo ""
echo "Vérifiez les capacités avec ipcalc :"
echo ""
echo "1. Réseau /27 pour l'administration :"
echo " ipcalc 192.168.10.0/27"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ipcalc 192.168.10.0/27 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""

echo "2. Réseau /26 pour les employés :"
echo " ipcalc 192.168.20.0/26"
echo "" 
echo "EXERCICE : Copiez et exécutez :"
echo ""
ipcalc 192.168.20.0/26 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""

# =============================================================================
# PARTIE 3 - Plan d'adressage complet
# =============================================================================

echo " EXERCICE 2 - Créer un plan d'adressage :"
echo "==========================================="
echo ""
echo "Créons un plan d'adressage pour notre entreprise :"
echo ""
echo "PLAN D'ADRESSAGE PROPOSÉ :"
echo "=============================="
echo ""
echo "┌─────────────────┬─────────────────┬─────────────┬──────────────┐"
echo "│ DÉPARTEMENT │ RÉSEAU CIDR │ NB ADRESSES │ UTILISATION │"
echo "├─────────────────┼─────────────────┼─────────────┼──────────────┤"
echo "│ Administration │ 192.168.10.0/27 │ 30 │ 10 machines │"
echo "│ Employés │ 192.168.20.0/26 │ 62 │ 25 postes │"
echo "│ Serveurs │ 192.168.30.0/28 │ 14 │ 5 serveurs │"
echo "│ WiFi Invités │ 192.168.40.0/25 │ 126 │ 50 appareils │"
echo "│ Imprimantes │ 192.168.50.0/28 │ 14 │ Équipements │"
echo "└─────────────────┴─────────────────┴─────────────┴──────────────┘"
echo ""

echo "VÉRIFICATION DU PLAN :"
echo "========================"
echo ""
echo "Vérifions chaque réseau de notre plan :"
echo ""

networks=("192.168.10.0/27" "192.168.20.0/26" "192.168.30.0/28" "192.168.40.0/25" "192.168.50.0/28")
departments=("Administration" "Employés" "Serveurs" "WiFi_Invités" "Imprimantes")

for i in "${!networks[@]}"; do
echo "${departments[$i]} : ${networks[$i]}"
if command -v ipcalc >/dev/null 2>&1; then
ipcalc "${networks[$i]}" | grep "Hosts/Net"
else
echo " (Utilisez ipcalc pour voir les détails)"
fi
echo ""
done

# =============================================================================
# PARTIE 4 - Règles de sécurité simple
# =============================================================================

echo "EXERCICE 3 - Définir des règles de sécurité :"
echo "==============================================="
echo ""
echo "Maintenant définissons qui peut communiquer avec qui :"
echo ""
echo "MATRICE DE COMMUNICATION :"
echo "============================="
echo ""
echo "┌─────────────┬─────┬─────┬─────┬─────┬─────┬─────────┐"
echo "│ DEPUIS \\ VERS │ ADM │ EMP │ SRV │ WIFI│ IMP │ INTERNET│"
echo "├─────────────┼─────┼─────┼─────┼─────┼─────┼─────────┤"
echo "│ Admin │ │ │ │ │ │ │"
echo "│ Employés │ │ │ │ │ │ │"
echo "│ Serveurs │ │ │ │ │ │ │"
echo "│ WiFi │ │ │ │ │ │ │"
echo "│ Imprimantes │ │ │ │ │ │ │"
echo "└─────────────┴─────┴─────┴─────┴─────┴─────┴─────────┘"
echo ""
echo "EXPLICATIONS :"
echo "• = Communication autorisée"
echo "• = Communication bloquée"
echo ""
echo "RÈGLES LOGIQUES :"
echo "• Admin peut accéder partout (maintenance)"
echo "• Employés peuvent utiliser serveurs et imprimantes"
echo "• Serveurs sont isolés (sécurité)"
echo "• WiFi invités limité à Internet et imprimantes"
echo "• Imprimantes n'ont pas besoin d'Internet"
echo ""

# =============================================================================
# PARTIE 5 - Simulation avec ping
# =============================================================================

echo "EXERCICE 4 - Simuler la connectivité :"
echo "========================================"
echo ""
echo "Testons notre réseau local pour comprendre :"
echo ""

echo "1. Voir notre réseau actuel :"
echo " ip route show | grep -E '192.168|10.0|172.16'"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip route show | grep -E '192.168|10.0|172.16'
echo ""

echo "2. Identifier notre sous-réseau :"
current_network=$(ip route show | grep -E "192.168\.[0-9]+\.[0-9]+/[0-9]+" | head -1 | awk '{print $1}')
if [ -n "$current_network" ]; then
echo "Votre réseau local actuel : $current_network"
echo ""
echo "Analyse avec ipcalc :"
ipcalc "$current_network" 2>/dev/null || echo "Utilisez ipcalc pour analyser ce réseau"
else
echo " Impossible de détecter automatiquement votre réseau local"
fi
echo ""

echo "3. Tester la connectivité dans votre réseau :"
gateway=$(ip route show default | awk '{print $3}' | head -1)
if [ -n "$gateway" ]; then
echo "Test vers votre passerelle ($gateway) :"
ping -c 2 "$gateway" || echo " Pas de réponse"
else
echo " Passerelle non détectée"
fi
echo ""

# =============================================================================
# PARTIE 6 - Créer votre propre plan
# =============================================================================

echo " EXERCICE 5 - Créer votre propre plan d'adressage :"
echo "===================================================="
echo ""
echo "À VOUS DE JOUER !"
echo ""
echo "Scénario : Vous devez planifier le réseau d'un café avec :"
echo "• 5 machines de caisse"
echo "• 20 places WiFi clients" 
echo "• 3 ordinateurs du personnel"
echo "• 1 serveur de fichiers"
echo ""
echo "QUESTIONS À RÉSOUDRE :"
echo "1. Combien de sous-réseaux créer ?"
echo "2. Quelle taille (/XX) pour chaque sous-réseau ?"
echo "3. Quelles adresses IP utiliser ?"
echo "4. Qui peut communiquer avec qui ?"
echo ""
echo "INDICES :"
echo "• Utilisez la plage 192.168.100.0/24 comme base"
echo "• Pensez à la sécurité (clients vs personnel)"
echo "• Prévoyez de la marge pour grandir"
echo "• Utilisez ipcalc pour vérifier vos calculs"
echo ""
echo "EXEMPLE DE DÉMARRAGE :"
echo "• Caisses : 192.168.100.0/28 (14 adresses pour 5 machines)"
echo "• WiFi clients : 192.168.100.32/27 (30 adresses pour 20 clients)"
echo "• Personnel : ?"
echo "• Serveur : ?"
echo ""
echo "Vérifiez le premier exemple :"
echo "ipcalc 192.168.100.0/28"
echo ""
ipcalc 192.168.100.0/28 2>/dev/null || echo " Installez ipcalc pour faire les calculs"
echo ""

# =============================================================================
# VALIDATION ET RÉCAPITULATIF 
# =============================================================================

echo " CRITÈRES DE RÉUSSITE :"
echo "========================"
echo ""
echo "Vous avez réussi si vous pouvez :"
echo "□ Estimer le nombre d'adresses IP nécessaires pour un usage"
echo "□ Choisir la taille appropriée de sous-réseau (/XX)"
echo "□ Utiliser ipcalc pour vérifier vos calculs"
echo "□ Créer un plan d'adressage organisé"
echo "□ Définir des règles de communication logiques"
echo "□ Comprendre les besoins de sécurité réseau"
echo ""

echo "CE QUE VOUS AVEZ APPRIS :"
echo "============================"
echo ""
echo "• Comment planifier l'adressage IP selon les besoins"
echo "• L'importance de prévoir une marge de croissance"
echo "• Les principes de base de la segmentation réseau"
echo "• Comment définir des règles de communication"
echo "• L'utilisation d'ipcalc pour valider les plans réseau"
echo "• Les concepts de sécurité par isolation réseau"
echo ""

echo "CONCEPTS AVANCÉS (pour plus tard) :"
echo "======================================="
echo ""
echo "Avec plus d'expérience, vous apprendrez :"
echo "• Les VLANs (réseaux virtuels)"
echo "• Les règles de firewall détaillées"
echo "• La haute disponibilité et redondance"
echo "• Les réseaux distribués et VPN"
echo "• L'automatisation de la configuration réseau"
echo ""

echo "PROJET PRATIQUE :"
echo "==================="
echo ""
echo "Pour consolider vos acquis, essayez de :"
echo "1. Planifier le réseau de votre maison/appartement"
echo "2. Dessiner un schéma avec les différentes zones"
echo "3. Calculer les besoins de chaque zone"
echo "4. Définir les règles de sécurité appropriées"
echo ""

echo "=== FIN DU LAB 3 - Planification d'architecture réseau simple ==="
