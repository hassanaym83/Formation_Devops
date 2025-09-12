#!/bin/bash

# =============================================================================
# CORRECTION LAB 3 - Outils de diagnostic réseau de base
# =============================================================================
#
# Cette correction présente les solutions pour les outils de diagnostic réseau
# selon le Framework Hassan Section A - Adaptabilité Pédagogique
#
# =============================================================================

echo "=== CORRECTION LAB 3 - Outils de diagnostic réseau de base ==="
echo "Date: $(date)"
echo "Formateur: Correction officielle"
echo ""

# Rappel des objectifs pédagogiques
echo "OBJECTIFS PEDAGOGIQUES RAPPEL :"
echo "==============================="
echo "1. Maîtriser les commandes ip, ping, ss"
echo "2. Diagnostiquer les problèmes de connectivité de base"
echo "3. Interpréter les résultats des outils réseau"
echo "4. Suivre une méthodologie simple de diagnostic"
echo ""

echo "SOLUTION DETAILLEE ETAPE PAR ETAPE :"
echo "===================================="
echo ""

echo "ETAPE 1 - VERIFICATION DE LA CONFIGURATION RESEAU :"
echo "==================================================="
echo ""
echo "Commande : ip addr show"
echo "Objectif : Voir toutes les interfaces et leurs adresses IP"
echo ""
echo "Résultat sur ce système :"
ip addr show
echo ""
echo "Analyse des résultats :"
LOCAL_IP=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -1)
if [ -n "$LOCAL_IP" ]; then
    echo "[OK] Adresse IP principale trouvée : $LOCAL_IP"
else
    echo "[PROBLEME] Aucune adresse IP configurée"
fi
echo ""

echo "Commande : ip link show"
echo "Objectif : Voir l'état des interfaces (UP/DOWN)"
echo ""
echo "État des interfaces :"
ip link show
echo ""
UP_COUNT=$(ip link show | grep -c "state UP")
echo "Nombre d'interfaces actives : $UP_COUNT"
echo ""

echo "ETAPE 2 - TEST DE CONNECTIVITE LOCALE :"
echo "======================================="
echo ""
echo "Commande : ping -c 3 127.0.0.1"
echo "Objectif : Test du système réseau local (loopback)"
echo ""
if ping -c 3 127.0.0.1 >/dev/null 2>&1; then
    echo "[OK] Test loopback réussi"
    ping -c 1 127.0.0.1 | head -2
else
    echo "[ERREUR] Test loopback échoué - problème système"
fi
echo ""

echo "ETAPE 3 - TEST DE LA PASSERELLE :"
echo "================================="
echo ""
echo "Commande : ip route show default"
echo "Objectif : Trouver la passerelle par défaut"
echo ""
echo "Routes actuelles :"
ip route show default
echo ""
GATEWAY=$(ip route | grep default | awk '{print $3}' | head -1)
if [ -n "$GATEWAY" ]; then
    echo "Passerelle détectée : $GATEWAY"
    echo ""
    echo "Test de connectivité vers la passerelle :"
    echo "Commande : ping -c 3 $GATEWAY"
    if ping -c 3 $GATEWAY >/dev/null 2>&1; then
        echo "[OK] Passerelle accessible"
        ping -c 1 $GATEWAY | head -2
    else
        echo "[PROBLEME] Passerelle inaccessible"
    fi
else
    echo "[PROBLEME] Aucune passerelle par défaut trouvée"
fi
echo ""

echo "ETAPE 4 - TEST DE CONNECTIVITE INTERNET :"
echo "========================================="
echo ""
echo "Commande : ping -c 3 8.8.8.8"
echo "Objectif : Tester l'accès Internet via IP directe"
echo ""
if ping -c 3 8.8.8.8 >/dev/null 2>&1; then
    echo "[OK] Connectivité Internet fonctionnelle"
    ping -c 1 8.8.8.8 | head -2
else
    echo "[PROBLEME] Pas d'accès Internet"
fi
echo ""
echo "Note : 8.8.8.8 est un serveur DNS public de Google"
echo "Si ce test fonctionne, la connexion Internet de base est OK"
echo ""

echo "ETAPE 5 - VERIFICATION DES SERVICES RESEAU :"
echo "============================================"
echo ""
echo "Commande : ss -tuln"
echo "Objectif : Lister les ports en écoute (services actifs)"
echo ""
echo "Services en écoute sur ce système :"
ss -tuln | head -10
echo ""
LISTEN_COUNT=$(ss -tuln | grep -c LISTEN)
echo "Nombre de services en écoute : $LISTEN_COUNT"
echo ""
echo "Explication des colonnes :"
echo "- Proto : Protocole (tcp/udp)"
echo "- Local Address : Adresse d'écoute"
echo "- State : État (LISTEN = en écoute)"
echo ""

echo "RESUME DE CONFIGURATION RESEAU :"
echo "==============================="
echo ""
echo "Configuration IP principale :"
ip addr show | grep "inet " | grep -v "127.0.0.1" | head -1
echo ""
echo "Route par défaut :"
ip route | grep default
echo ""
echo "Services réseau actifs :"
ss -tuln | grep LISTEN | wc -l | awk '{print $1 " services en écoute"}'
echo ""

echo "DIAGNOSTIC AUTOMATISE :"
echo "======================"
echo ""

# Script de diagnostic simple
diagnostic_simple() {
    echo "=== DIAGNOSTIC RESEAU RAPIDE ==="
    SCORE=0
    TOTAL=5
    
    # Test 1 : Loopback
    echo -n "1. Test loopback : "
    if ping -c 1 127.0.0.1 >/dev/null 2>&1; then
        echo "[OK]"
        ((SCORE++))
    else
        echo "[ERREUR]"
    fi
    
    # Test 2 : Interface UP
    echo -n "2. Interface active : "
    if [ $(ip link show | grep -c "state UP") -gt 0 ]; then
        echo "[OK]"
        ((SCORE++))
    else
        echo "[ERREUR]"
    fi
    
    # Test 3 : IP configurée
    echo -n "3. IP configurée : "
    if ip addr show | grep -q "inet.*scope global"; then
        echo "[OK]"
        ((SCORE++))
    else
        echo "[ERREUR]"
    fi
    
    # Test 4 : Passerelle
    echo -n "4. Passerelle accessible : "
    GATEWAY=$(ip route | grep default | awk '{print $3}' | head -1)
    if [ -n "$GATEWAY" ] && ping -c 1 -W 2 $GATEWAY >/dev/null 2>&1; then
        echo "[OK]"
        ((SCORE++))
    else
        echo "[ERREUR]"
    fi
    
    # Test 5 : Internet
    echo -n "5. Internet accessible : "
    if ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1; then
        echo "[OK]"
        ((SCORE++))
    else
        echo "[ERREUR]"
    fi
    
    echo ""
    echo "SCORE : $SCORE/$TOTAL"
    if [ $SCORE -eq $TOTAL ]; then
        echo "RESULTAT : EXCELLENT - Réseau complètement fonctionnel"
    elif [ $SCORE -ge 3 ]; then
        echo "RESULTAT : ACCEPTABLE - Quelques problèmes à résoudre"
    else
        echo "RESULTAT : PROBLEMATIQUE - Configuration à revoir"
    fi
}

diagnostic_simple

echo ""
echo "SOLUTIONS AUX PROBLEMES COURANTS :"
echo "================================="
echo ""
echo "Problème : Interface DOWN"
echo "Solution : sudo ip link set [interface] up"
echo ""
echo "Problème : Pas d'IP"
echo "Solution : Vérifier DHCP ou configurer IP statique"
echo ""
echo "Problème : Pas de passerelle"
echo "Solution : sudo ip route add default via [ip_passerelle]"
echo ""
echo "Problème : Pas d'Internet"
echo "Solution : Vérifier routage et configuration DNS"
echo ""

echo "CRITERES DE VALIDATION :"
echo "[] Interface réseau active identifiée avec ip link show"
echo "[] Adresse IP locale trouvée avec ip addr show"
echo "[] Passerelle accessible par ping"
echo "[] Test loopback réussi (ping 127.0.0.1)"
echo "[] Services en écoute listés avec ss -tuln"
echo "[] Connectivité Internet vérifiée (ping 8.8.8.8)"
echo ""

echo "COMMANDES A RETENIR :"
echo "===================="
echo "ip addr show        → Configuration IP des interfaces"
echo "ip link show        → État des interfaces (UP/DOWN)"
echo "ip route show       → Table de routage"
echo "ping [adresse]      → Test de connectivité"
echo "ss -tuln            → Ports en écoute"
echo "ss -tu              → Connexions actives"
echo ""

echo "=== FIN DE LA CORRECTION LAB 3 ==="
