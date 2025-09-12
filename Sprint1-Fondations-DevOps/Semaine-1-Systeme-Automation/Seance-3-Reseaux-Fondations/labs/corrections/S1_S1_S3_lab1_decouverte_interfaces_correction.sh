#!/bin/bash

# =============================================================================
# CORRECTION LAB 1 - Découverte des interfaces réseau Linux
# =============================================================================
#
# Correction simplifiée pour niveau débutant - Focus sur l'interprétation
# des commandes de base sans scripting avancé
#
# =============================================================================

echo "=== CORRECTION LAB 1 - Découverte des interfaces réseau Linux ==="
echo "Date: $(date)"
echo "Formateur: Correction officielle"
echo ""

echo "OBJECTIFS PEDAGOGIQUES ATTEINTS :"
echo "================================="
echo "1. Exécuter les commandes réseau de base (ip link, ip addr, ip route)"
echo "2. Interpréter les résultats selon les éléments du cours (UP, IP/24, MTU)"
echo "3. Identifier l'interface principale via route par défaut"
echo "4. Compléter un tableau d'analyse simple"
echo ""

echo "SOLUTION ÉTAPE PAR ÉTAPE :"
echo "========================="
echo ""

echo "ÉTAPE 1 - Commande : ip link show"
echo "================================="
echo "Cette commande montre toutes les interfaces et leur état :"
echo ""
ip link show
echo ""
echo "ANALYSE ATTENDUE :"
echo "- Rechercher les mots 'UP' ou 'DOWN' dans la sortie"
echo "- Identifier les noms d'interfaces (lo, eth0, enp0s*, etc.)"
echo "- Noter le MTU (généralement 1500 pour Ethernet)"
echo ""

echo "ÉTAPE 2 - Commande : ip addr show"
echo "================================="
echo "Cette commande ajoute les adresses IP et MAC :"
echo ""
ip addr show
echo ""
echo "ANALYSE ATTENDUE selon Section 4.2 du cours :"
echo "- Chercher les adresses IP au format X.X.X.X/24"
echo "- Identifier l'adresse MAC (6 groupes de 2 caractères séparés par :)"
echo "- Vérifier la cohérence avec l'état UP/DOWN de l'étape 1"
echo ""

echo "ÉTAPE 3 - Commande : ip route show default"
echo "=========================================="
echo "Cette commande montre l'interface principale (route par défaut) :"
echo ""
ip route show default
echo ""
echo "ANALYSE ATTENDUE :"
echo "- Identifier le nom de l'interface après 'dev' (ex: eth0, enp0s3)"
echo "- Cette interface est celle qui connecte au réseau principal"
echo "- Elle doit correspondre à une interface UP de l'étape 1"
echo ""

echo "EXEMPLE DE COMPLETION DU TABLEAU :"
echo "=================================="
echo "| Interface | État UP/DOWN | A une IP | Type (physique/virtuelle) |"
echo "|-----------|--------------|----------|---------------------------|"
echo "| lo        | UP           | Oui      | virtuelle (loopback)      |"
echo "| eth0      | UP           | Oui      | physique (principale)     |"
echo "|           |              |          |                           |"
echo ""

echo "REPONSES AUX QUESTIONS D'ANALYSE :"
echo "=================================="
echo "- Combien d'interfaces UP ? → Compter celles avec 'UP' dans ip link show"
echo "- Interface avec IP 192.168.x.x ? → Chercher dans ip addr show" 
echo "- Interface 'lo' avec 127.0.0.1 ? → Oui, toujours présente"
echo "- Interface principale ? → Celle indiquée par 'ip route show default'"
echo ""

echo "CRITERES DE VALIDATION :"
echo "[] Exécution réussie des 3 commandes principales"
echo "[] Identification des interfaces UP et DOWN"
echo "[] Relevé d'au moins une adresse IP et une adresse MAC"
echo "[] Compréhension du rôle de la route par défaut"
echo "[] Documentation basique de la configuration réseau"
echo ""

echo "=== FIN DE LA CORRECTION LAB 1 ==="
