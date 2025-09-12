#!/bin/bash

# =============================================================================
# CORRECTION LAB 2 - Configuration NetworkManager
# =============================================================================
#
# Cette correction présente la solution détaillée avec analyse théorique
# selon le Framework Hassan Section A - Adaptabilité Pédagogique
#
# =============================================================================

echo "=== CORRECTION LAB 2 - Configuration NetworkManager ==="
echo "Date: $(date)"
echo "Formateur: Correction officielle"
echo ""

# Rappel des objectifs pédagogiques
echo "OBJECTIFS PEDAGOGIQUES RAPPEL :"
echo "==============================="
echo "1. Identifier les devices et connexions NetworkManager"
echo "2. Configurer une IP statique avec nmcli"
echo "3. Tester la configuration avec des commandes de base"
echo "4. Comprendre la persistance des configurations"
echo ""

echo "RAPPEL THEORIQUE - NETWORKMANAGER :"
echo "===================================="
echo "Device vs Connection :"
echo "- DEVICE : Interface physique (eth0, wlan0)"
echo "- CONNECTION : Profil de configuration (peut avoir plusieurs par device)"
echo ""
echo "Configuration statique vs DHCP :"
echo "- STATIQUE : IP fixe, configuration manuelle"
echo "- DHCP : IP automatique du serveur"
echo ""
echo "Utilisation nmcli :"
echo "- nmcli device : Gérer les interfaces physiques"
echo "- nmcli connection : Gérer les profils de configuration"
echo ""

echo "SOLUTION DETAILLEE ETAPE PAR ETAPE :"
echo "===================================="
echo ""

echo "ETAPE 1 - Vérification préalable de NetworkManager :"
echo "----------------------------------------------------"
echo "Commande : systemctl status NetworkManager"
echo ""
echo "Sortie attendue :"
echo "Active: active (running) since..."
echo ""
echo "Si inactive :"
echo "  sudo systemctl enable NetworkManager"
echo "  sudo systemctl start NetworkManager"
echo ""

echo "État actuel sur ce système :"
systemctl status NetworkManager --no-pager -l | head -3
echo ""

echo "ETAPE 2 - Analyse du réseau existant :"
echo "--------------------------------------"
echo "Identification du réseau local actuel :"
CURRENT_GW=$(ip route | grep default | awk '{print $3}' | head -1)
CURRENT_IF=$(ip route | grep default | awk '{print $5}' | head -1)
CURRENT_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '{print $7}' | head -1)

if [ -n "$CURRENT_GW" ] && [ -n "$CURRENT_IP" ]; then
    echo "Interface active : $CURRENT_IF"
    echo "IP actuelle : $CURRENT_IP"
    echo "Passerelle : $CURRENT_GW"
    
    # Détection de la plage réseau
    NETWORK_BASE=$(echo $CURRENT_IP | cut -d. -f1-3)
    echo "Réseau détecté : ${NETWORK_BASE}.0/24"
    
    # Classification RFC 1918
    if [[ $CURRENT_IP =~ ^192\.168\. ]]; then
        echo "Type réseau : RFC 1918 Classe C (domestique/PME)"
        echo "Plage disponible : 192.168.x.2 à 192.168.x.254"
        SUGGESTED_IP="${NETWORK_BASE}.100"
    elif [[ $CURRENT_IP =~ ^10\. ]]; then
        echo "Type réseau : RFC 1918 Classe A (entreprise)"
        echo "Plage disponible : 10.x.x.2 à 10.x.x.254"
        SUGGESTED_IP="${NETWORK_BASE}.100"
    elif [[ $CURRENT_IP =~ ^172\.1[6-9]\.|^172\.2[0-9]\.|^172\.3[01]\. ]]; then
        echo "Type réseau : RFC 1918 Classe B (cloud)"
        echo "Plage disponible : 172.x.x.2 à 172.x.x.254"
        SUGGESTED_IP="${NETWORK_BASE}.100"
    else
        echo "ATTENTION : Réseau public ou non-standard"
        SUGGESTED_IP="${NETWORK_BASE}.100"
    fi
    
    echo "IP statique suggérée : $SUGGESTED_IP/24"
else
    echo "ATTENTION : Pas de réseau configuré actuellement"
    SUGGESTED_IP="192.168.1.100"
    CURRENT_GW="192.168.1.1"
    CURRENT_IF="eth0"
fi
echo ""

echo "ETAPE 3 - Création de la connexion statique :"
echo "---------------------------------------------"
echo "Commande de création (adaptée à votre réseau) :"
echo ""
echo "sudo nmcli connection add type ethernet \\"
echo "     con-name 'lab-static-devops' \\"
echo "     ifname $CURRENT_IF \\"
echo "     ip4 $SUGGESTED_IP/24 \\"
echo "     gw4 $CURRENT_GW"
echo ""
echo "Explication des paramètres :"
echo "- type ethernet : Interface Ethernet physique (couche 2)"
echo "- con-name : Nom de la connexion NetworkManager"
echo "- ifname : Interface physique cible"
echo "- ip4 : Adresse IPv4 statique avec masque CIDR"
echo "- gw4 : Passerelle par défaut (route 0.0.0.0/0)"
echo ""

echo "ETAPE 4 - Vérification de la connexion :"
echo "----------------------------------------"
echo "Lister les connexions disponibles :"
echo "nmcli connection show"
echo ""
echo "Voir les détails de notre connexion :"
echo "nmcli connection show 'lab-static-devops'"
echo ""

echo "ETAPE 5 - Activation et test :"
echo "------------------------------"
echo "Activation de la connexion :"
echo "sudo nmcli connection up 'lab-static-devops'"
echo ""
echo "Vérification immédiate :"
echo "ip addr show $CURRENT_IF | grep inet"
echo ""

echo "TESTS DE VALIDATION BASIQUES :"
echo "=============================="
echo ""

echo "Test 1 - Vérification de l'interface :"
echo "ip addr show $CURRENT_IF"
CURRENT_TEST_IP=$(ip addr show $CURRENT_IF 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -1)
if [ -n "$CURRENT_TEST_IP" ]; then
    echo "RESULTAT : IP configurée - $CURRENT_TEST_IP"
else
    echo "PROBLEME : Aucune IP configurée"
fi
echo ""

echo "Test 2 - Test de connectivité locale :"
echo "ping -c 2 $CURRENT_GW"
if ping -c 2 -W 3 $CURRENT_GW >/dev/null 2>&1; then
    echo "RESULTAT : Passerelle accessible"
else
    echo "PROBLEME : Passerelle inaccessible"
fi
echo ""

echo "Test 3 - Vérification du statut NetworkManager :"
echo "nmcli device status"
nmcli device status 2>/dev/null
echo ""

echo "GESTION BASIQUE DES CONNEXIONS :"
echo "==============================="
echo ""
echo "Lister toutes les connexions :"
echo "nmcli connection show"
nmcli connection show 2>/dev/null | head -5
echo ""

echo "Activer/désactiver une connexion :"
echo "sudo nmcli connection up 'lab-static-devops'"
echo "sudo nmcli connection down 'lab-static-devops'"
echo ""

echo "Supprimer une connexion :"
echo "sudo nmcli connection delete 'lab-static-devops'"
echo ""

echo "EXEMPLE DE CONFIGURATION COMPLETE :"
echo "===================================="
echo ""
echo "Configuration step by step :"
echo "1. nmcli device status"
echo "2. sudo nmcli con add type ethernet con-name 'mon-config' ifname eth0 ip4 192.168.1.100/24 gw4 192.168.1.1"
echo "3. sudo nmcli con up 'mon-config'"
echo "4. ip addr show eth0"
echo "5. ping -c 2 192.168.1.1"
echo ""

echo "DEPANNAGE BASIQUE :"
echo "=================="
echo ""
echo "Problème : Interface pas active"
echo "- Diagnostic : nmcli device status"
echo "- Solution : sudo nmcli connection up 'nom-connexion'"
echo ""
echo "Problème : Pas d'IP configurée"
echo "- Diagnostic : ip addr show"
echo "- Solution : Vérifier la configuration nmcli"
echo ""
echo "Problème : Connexion ne démarre pas"
echo "- Diagnostic : nmcli connection show"
echo "- Solution : Recréer la connexion"
echo ""

echo "CRITERES DE VALIDATION - CONTROLE QUALITE :"
echo "==========================================="
echo ""
VALIDATION_SCORE=0
TOTAL_CRITERIA=5

echo "1. NetworkManager actif et fonctionnel :"
if systemctl is-active NetworkManager >/dev/null 2>&1; then
    echo "   [OK] NetworkManager en cours d'exécution"
    ((VALIDATION_SCORE++))
else
    echo "   [ERREUR] NetworkManager inactif"
fi

echo "2. Connexion NetworkManager créée :"
if nmcli connection show | grep -q "lab\|static"; then
    echo "   [OK] Connexion NetworkManager présente"
    ((VALIDATION_SCORE++))
else
    echo "   [INFO] Pas de connexion statique trouvée"
fi

echo "3. Adresse IP statique assignée :"
if ip addr show | grep -q "inet.*scope global"; then
    echo "   [OK] Adresse IP configurée"
    ((VALIDATION_SCORE++))
else
    echo "   [ERREUR] Pas d'adresse IP configurée"
fi

echo "4. Test de connectivité basique :"
if [ -n "$CURRENT_GW" ] && ping -c 1 -W 3 $CURRENT_GW >/dev/null 2>&1; then
    echo "   [OK] Connectivité locale OK"
    ((VALIDATION_SCORE++))
else
    echo "   [ERREUR] Problème connectivité locale"
fi

echo "7. Configuration persistante :"
if nmcli connection show | grep -q "static\|lab"; then
    echo "   [OK] Connexion statique enregistrée"
    ((VALIDATION_SCORE++))
else
    echo "   [INFO] Pas de connexion statique nommée trouvée"
fi

echo ""
echo "SCORE FINAL : $VALIDATION_SCORE/$TOTAL_CRITERIA"
if [ $VALIDATION_SCORE -ge 4 ]; then
    echo "RESULTAT : EXCELLENT - Configuration NetworkManager maîtrisée"
elif [ $VALIDATION_SCORE -ge 3 ]; then
    echo "RESULTAT : BIEN - Bases NetworkManager acquises"
elif [ $VALIDATION_SCORE -ge 2 ]; then
    echo "RESULTAT : SATISFAISANT - Révision recommandée"
else
    echo "RESULTAT : INSUFFISANT - Reprise du LAB nécessaire"
fi

echo ""
echo "=== FIN DE LA CORRECTION LAB 2 ==="
echo ""
echo "POINTS CLES A RETENIR :"
echo "- Device = interface physique (eth0, wlan0)"
echo "- Connection = profil de configuration"
echo "- nmcli = outil principal NetworkManager"
echo "- IP statique = configuration persistante"
echo ""
echo "COMMANDES ESSENTIELLES :"
echo "- nmcli device status : voir les interfaces"
echo "- nmcli connection show : voir les profils"
echo "- nmcli connection up/down : activer/désactiver"
echo ""
echo "RESSOURCES COMPLEMENTAIRES :"
echo "- man nmcli (manuel NetworkManager)"
echo "- /etc/NetworkManager/system-connections/ : Fichiers config"
