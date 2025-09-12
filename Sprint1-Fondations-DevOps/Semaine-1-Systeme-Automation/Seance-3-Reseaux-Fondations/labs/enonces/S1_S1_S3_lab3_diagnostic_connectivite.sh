#!/bin/bash

# =============================================================================
# LAB 3 - Outils de diagnostic réseau de base
# =============================================================================
#
# Énoncé : Apprendre à utiliser les outils de base pour vérifier 
# la connectivité réseau sur Linux
#
# Objectif : Maîtriser les commandes essentielles de diagnostic réseau :
# ip, ping, ss et les commandes de base
#
# Contexte : Diagnostic simple de connectivité sans complexité avancée
#
# Durée estimée : 15 minutes
# Niveau de difficulté : Débutant/Intermédiaire (1-2/3)
# =============================================================================

echo "=== LAB 3 - Diagnostic de connectivité réseau ==="
echo "Date: $(date)"
echo "Utilisateur: $USER"
echo ""

# Rappel des outils de diagnostic de base
echo "OUTILS DE DIAGNOSTIC RESEAU DE BASE :"
echo "===================================="
echo "ip : Voir configuration réseau (remplace ifconfig)"
echo "ping : Tester la connectivité réseau"
echo "ss : Voir les connexions et ports (remplace netstat)"
echo ""
echo "METHODOLOGIE SIMPLE :"
echo "===================="
echo "1. Vérifier la configuration locale (ip)"
echo "2. Tester la connectivité (ping)"  
echo "3. Vérifier les services (ss)"
echo ""

# ETAPE 1 : Vérification de la configuration réseau
echo "ETAPE 1 - Configuration réseau locale :"
echo "======================================"
echo ""
echo "Voir toutes les interfaces réseau :"
echo "Commande : ip addr show"
ip addr show
echo ""

echo "Voir seulement les interfaces actives :"
echo "Commande : ip link show"
ip link show | grep "state UP"
echo ""

echo "Test de base - interface loopback :"
echo "Commande : ping -c 3 127.0.0.1"
ping -c 3 127.0.0.1
echo ""

# ETAPE 2 : Test de la passerelle (routeur)
echo "ETAPE 2 - Test de connectivité locale :"
echo "======================================"
echo ""
echo "Voir la route par défaut :"
echo "Commande : ip route show default"
ip route show default
echo ""

GATEWAY=$(ip route | grep default | awk '{print $3}' | head -1)
if [ -n "$GATEWAY" ]; then
    echo "Passerelle trouvée : $GATEWAY"
    echo "Test de connectivité vers la passerelle :"
    echo "Commande : ping -c 3 $GATEWAY"
    ping -c 3 $GATEWAY
    echo ""
else
    echo "ATTENTION : Aucune passerelle par défaut trouvée"
    echo "Cela peut indiquer un problème de configuration réseau"
fi
echo ""

# ETAPE 3 : Test de connectivité Internet
echo "ETAPE 3 - Test connectivité Internet :"
echo "====================================="
echo ""
echo "Test vers un serveur Internet (IP directe) :"
echo "Commande : ping -c 3 8.8.8.8"
ping -c 3 8.8.8.8
echo ""
echo "Note : 8.8.8.8 est un serveur DNS public de Google"
echo "Si ce test fonctionne, la connexion Internet de base est OK"
echo ""

# ETAPE 4 : Analyse des connexions et services
echo "ETAPE 4 - Services réseau actifs :"
echo "=================================="
echo ""
echo "Voir les ports en écoute (services actifs) :"
echo "Commande : ss -tuln"
ss -tuln | head -10
echo ""
echo "Explication :"
echo "- t = TCP, u = UDP, l = écoute, n = numérique"
echo "- Ces ports montrent quels services tournent"
echo ""

# ETAPE 5 : Résumé des informations réseau
echo "ETAPE 5 - Résumé de configuration :"
echo "==================================="
echo ""
echo "Résumé des adresses IP :"
echo "Commande : ip addr show | grep inet"
ip addr show | grep "inet " | grep -v "127.0.0.1"
echo ""

echo "Résumé des routes :"
echo "Commande : ip route"
ip route
echo ""

# SCRIPT DE TEST SIMPLE
echo "SCRIPT DE TEST AUTOMATIQUE :"
echo "============================"

# Fonction de test simple
test_network() {
    echo "=== TEST RESEAU SIMPLE ==="
    echo "Date: $(date)"
    echo "Machine: $(hostname)"
    echo ""
    
    # Test 1: Loopback
    echo "1. Test loopback :"
    if ping -c 1 127.0.0.1 >/dev/null 2>&1; then
        echo "   [OK] Système réseau de base fonctionne"
    else
        echo "   [ERREUR] Problème système de base"
    fi
    
    # Test 2: Passerelle
    echo "2. Test passerelle :"
    GATEWAY=$(ip route | grep default | awk '{print $3}' | head -1)
    if [ -n "$GATEWAY" ]; then
        if ping -c 2 -W 3 $GATEWAY >/dev/null 2>&1; then
            echo "   [OK] Passerelle $GATEWAY accessible"
        else
            echo "   [ERREUR] Passerelle $GATEWAY inaccessible"
        fi
    else
        echo "   [ERREUR] Pas de passerelle configurée"
    fi
    
    # Test 3: Internet
    echo "3. Test Internet :"
    if ping -c 2 8.8.8.8 >/dev/null 2>&1; then
        echo "   [OK] Connectivité Internet OK"
    else  
        echo "   [ERREUR] Pas de connectivité Internet"
    fi
    
    echo ""
    echo "=== RESUME DE CONFIGURATION ==="
    echo "Adresse IP principale :"
    ip addr show | grep "inet " | grep -v 127.0.0.1 | head -1
    echo "Route par défaut :"
    ip route | grep default
}

# Exécution du test
test_network

echo ""
echo "EXERCICES PRATIQUES :"
echo "===================="
echo ""
echo "1. Identifiez votre adresse IP principale"
echo "2. Trouvez votre passerelle par défaut"
echo "3. Testez la connectivité vers la passerelle"
echo "4. Listez les services en écoute sur votre machine"
echo "5. Vérifiez si Internet est accessible"
echo ""

echo "COMMANDES A RETENIR :"
echo "===================="
echo ""
echo "ip addr show     → Voir les adresses IP"
echo "ip link show     → Voir l'état des interfaces" 
echo "ip route         → Voir les routes"
echo "ping [adresse]   → Tester la connectivité"
echo "ss -tuln         → Voir les ports en écoute"
echo ""

echo "CRITERES DE VALIDATION :"
echo "[] Interface réseau active identifiée"
echo "[] Adresse IP locale trouvée"
echo "[] Passerelle accessible par ping"
echo "[] Test loopback réussi"
echo "[] Services en écoute listés"
echo "[] Connectivité Internet vérifiée"
echo ""

echo "=== FIN DU LAB 3 ==="
