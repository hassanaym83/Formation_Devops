#!/bin/bash

# =============================================================================
# CORRECTION LAB 1 - Concepts de base IP et CIDR
# =============================================================================

echo "=== CORRECTION LAB 1 - Concepts de base IP et CIDR ==="
echo ""

# =============================================================================
# RÉPONSES AU QUIZ
# =============================================================================

echo " RÉPONSES AU QUIZ :"
echo "===================="
echo ""

echo "Question 1 : Dans le réseau 192.168.1.0/24 :"
echo "--------------------------------------------"
ipcalc 192.168.1.0/24 2>/dev/null || echo " ipcalc requis"
echo ""
echo " Réponses :"
echo " a) 254 machines maximum (256 adresses - 2 réservées)"
echo " b) Première adresse utilisable : 192.168.1.1"
echo " c) Adresse de broadcast : 192.168.1.255"
echo ""

echo "Question 2 : Comparaison des tailles de réseaux :"
echo "------------------------------------------------"
echo ""
echo "a) 10.0.0.0/8 :"
ipcalc 10.0.0.0/8 2>/dev/null | grep "Hosts/Net" || echo "Hosts/Net: 16,777,214"
echo ""
echo "b) 192.168.1.0/24 :"
ipcalc 192.168.1.0/24 2>/dev/null | grep "Hosts/Net" || echo "Hosts/Net: 254"
echo ""
echo "c) 172.16.0.0/16 :"
ipcalc 172.16.0.0/16 2>/dev/null | grep "Hosts/Net" || echo "Hosts/Net: 65,534"
echo ""
echo " Réponse : a) 10.0.0.0/8 est le plus grand réseau"
echo ""

echo "Question 3 : Réseau optimal pour 10 machines :"
echo "----------------------------------------------"
echo ""
echo "/24 → 254 machines possibles (trop grand, gaspillage)"
echo "/28 → 14 machines possibles (parfait pour 10 machines)"
echo "/16 → 65,534 machines possibles (beaucoup trop grand)"
echo ""
echo "Vérification avec /28 :"
ipcalc 192.168.1.0/28 2>/dev/null || echo "Hosts/Net: 14"
echo ""
echo " Réponse : b) /28 est le meilleur choix"
echo ""

# =============================================================================
# VÉRIFICATION DES COMMANDES APPRISES
# =============================================================================

echo "VÉRIFICATION DES OUTILS ET COMMANDES :"
echo "========================================="
echo ""

echo "1. Vérification d'ipcalc :"
if command -v ipcalc >/dev/null 2>&1; then
 echo " ipcalc installé et fonctionnel"
 echo "Version : $(ipcalc --version 2>/dev/null || echo 'Version non disponible')"
else
 echo " ipcalc non installé"
 echo "Installation : sudo apt install ipcalc"
fi
echo ""

echo "2. Test des commandes réseau de base :"
echo "--------------------------------------"
echo ""
echo "Configuration réseau actuelle :"
echo "• Interfaces réseau :"
ip addr show | grep -E "(inet |UP,)" | head -5
echo ""
echo "• Table de routage :"
ip route show | head -3
echo ""

# =============================================================================
# EXEMPLES DÉTAILLÉS AVEC CALCULS
# =============================================================================

echo "EXEMPLES DÉTAILLÉS AVEC EXPLICATIONS :"
echo "=========================================="
echo ""

echo "Exemple 1 - Analyse complète d'un /24 :"
echo "---------------------------------------"
if command -v ipcalc >/dev/null 2>&1; then
 ipcalc 192.168.1.0/24
else
 echo "Network: 192.168.1.0/24"
 echo "Netmask: 255.255.255.0 = 24"
 echo "Broadcast: 192.168.1.255"
 echo "HostMin: 192.168.1.1"
 echo "HostMax: 192.168.1.254"
 echo "Hosts/Net: 254"
fi
echo ""
echo "Explication :"
echo " • 24 bits pour le réseau (192.168.1)"
echo " • 8 bits pour les machines (0-255)"
echo " • 2 adresses réservées (0=réseau, 255=broadcast)"
echo " • Donc 254 adresses utilisables (1-254)"
echo ""

echo "Exemple 2 - Analyse d'un /16 (plus grand) :"
echo "--------------------------------------------"
if command -v ipcalc >/dev/null 2>&1; then
 ipcalc 192.168.0.0/16
else
 echo "Network: 192.168.0.0/16"
 echo "Netmask: 255.255.0.0 = 16"
 echo "Broadcast: 192.168.255.255"
 echo "HostMin: 192.168.0.1"
 echo "HostMax: 192.168.255.254"
 echo "Hosts/Net: 65534"
fi
echo ""
echo "Explication :"
echo " • 16 bits pour le réseau (192.168)"
echo " • 16 bits pour les machines (0.0 à 255.255)"
echo " • 65,536 adresses totales - 2 réservées = 65,534 utilisables"
echo ""

echo "Exemple 3 - Analyse d'un /28 (plus petit) :"
echo "--------------------------------------------"
if command -v ipcalc >/dev/null 2>&1; then
 ipcalc 192.168.1.0/28
else
 echo "Network: 192.168.1.0/28"
 echo "Netmask: 255.255.255.240 = 28"
 echo "Broadcast: 192.168.1.15"
 echo "HostMin: 192.168.1.1"
 echo "HostMax: 192.168.1.14"
 echo "Hosts/Net: 14"
fi
echo ""
echo "Explication :"
echo " • 28 bits pour le réseau"
echo " • 4 bits pour les machines (16 adresses possibles)"
echo " • 16 - 2 réservées = 14 adresses utilisables"
echo ""

# =============================================================================
# POINTS CLÉS À RETENIR
# =============================================================================

echo "POINTS CLÉS À RETENIR :"
echo "=========================="
echo ""
echo "1. MASQUES CIDR COURANTS :"
echo " /8 = Classe A (16,777,214 hôtes) - Très grands réseaux"
echo " /16 = Classe B (65,534 hôtes) - Réseaux moyens"
echo " /24 = Classe C (254 hôtes) - Petits réseaux"
echo " /28 = Sous-réseau (14 hôtes) - Micro-réseaux"
echo ""

echo "2. RÈGLE DE CALCUL :"
echo " Nombre d'hôtes = 2^(32-masque) - 2"
echo " Exemple : /24 → 2^(32-24) - 2 = 2^8 - 2 = 256 - 2 = 254"
echo ""

echo "3. ADRESSES SPÉCIALES :"
echo " • X.X.X.0 = Adresse du réseau (non assignable)"
echo " • X.X.X.1 = Première adresse utilisable"
echo " • X.X.X.254 = Dernière adresse utilisable (pour /24)"
echo " • X.X.X.255 = Broadcast (diffusion vers tous)"
echo ""

echo "4. COMMANDES ESSENTIELLES :"
echo " • ipcalc X.X.X.X/YY = Calculer les infos d'un réseau"
echo " • ip addr show = Voir la config réseau locale"
echo " • ip route show = Voir la table de routage"
echo ""

# =============================================================================
# VALIDATION FINALE
# =============================================================================

echo " VALIDATION - TESTEZ VOTRE COMPRÉHENSION :"
echo "============================================"
echo ""

echo "Mini-exercice de validation :"
echo ""
echo "Calculez vous-même, puis vérifiez avec ipcalc :"
echo ""
echo "Réseau : 172.16.0.0/20"
echo ""
echo "À vous de deviner :"
echo "• Combien d'adresses au total ?"
echo "• Combien d'hôtes utilisables ?"
echo "• Quelle est l'adresse de broadcast ?"
echo ""
echo "Vérification avec ipcalc :"
if command -v ipcalc >/dev/null 2>&1; then
 ipcalc 172.16.0.0/20
else
 echo "Network: 172.16.0.0/20"
 echo "Netmask: 255.255.240.0 = 20"
 echo "Broadcast: 172.16.15.255"
 echo "HostMin: 172.16.0.1"
 echo "HostMax: 172.16.15.254"
 echo "Hosts/Net: 4094"
fi
echo ""
echo "Calcul : /20 → 2^(32-20) - 2 = 2^12 - 2 = 4096 - 2 = 4094 hôtes"
echo ""

echo "BRAVO ! Vous maîtrisez maintenant :"
echo "======================================"
echo " Les concepts d'adressage IP"
echo " La notation CIDR et les masques"
echo " L'utilisation d'ipcalc pour les calculs"
echo " Les commandes de diagnostic réseau de base"
echo " L'interprétation des informations réseau"
echo ""

echo "PROCHAINE ÉTAPE :"
echo "Vous êtes prêt pour le LAB 2 - Configuration et routage réseau"
echo ""

echo "=== FIN DE LA CORRECTION LAB 1 ==="
