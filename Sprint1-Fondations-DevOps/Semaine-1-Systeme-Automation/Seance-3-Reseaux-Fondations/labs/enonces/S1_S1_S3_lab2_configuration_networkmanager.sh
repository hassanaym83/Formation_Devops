#!/bin/bash

# =============================================================================
# LAB 2 - Configuration NetworkManager
# =============================================================================
#
# Énoncé : Votre équipe DevOps doit configurer un nouveau serveur avec une 
# adresse IP statique pour assurer la stabilité des connexions.
#
# Objectif : Maîtriser NetworkManager pour créer une configuration réseau 
# statique simple et fiable
#
# Contexte : Serveur de développement nécessitant une IP fixe pour les 
# connexions depuis d'autres machines du réseau local
#
# Durée estimée : 20 minutes
# Niveau de difficulté : Intermédiaire (2/3)
# =============================================================================

echo "=== LAB 2 - Configuration NetworkManager ==="
echo "Date: $(date)"
echo "Utilisateur: $USER"
echo ""

# Rappels théoriques NetworkManager
echo "RAPPEL NETWORKMANAGER (Section 5 du cours) :"
echo "============================================="
echo "NetworkManager = Gestionnaire réseau moderne Linux"
echo "Outil principal : nmcli (NetworkManager CLI)"
echo ""
echo "Concepts clés :"
echo "- DEVICE (interface physique) : eth0, enp0s8, etc."
echo "- CONNECTION (profil de configuration) : nom donné à une config"
echo "- Un device peut avoir plusieurs connections"
echo "- Une seule connection active à la fois par device"
echo ""
echo "Avantages IP statique vs DHCP :"
echo "- STATIQUE : Adresse fixe, prévisible, stable pour serveurs"
echo "- DHCP : Attribution automatique, simple, mais peut changer"
echo ""

# Vérifications préalables
echo "VERIFICATIONS PREALABLES :"
echo "=========================="
echo "1. NetworkManager doit être installé et actif"
echo "2. Droits sudo requis pour les modifications"
echo "3. Interface réseau disponible (eth0, enp0s*)"
echo ""

echo "ETAPE 1 - Découverte de votre configuration actuelle :"
echo "====================================================="
echo "État de NetworkManager :"
systemctl is-active NetworkManager
echo ""

echo "Devices (interfaces physiques) disponibles :"
nmcli device status
echo ""

echo "Connections (profils) existantes :"
nmcli connection show
echo ""

echo "ETAPE 2 - Identifier votre réseau actuel :"
echo "=========================================="
echo "Regardez votre configuration actuelle :"
echo ""
ip addr show
echo ""
echo "Votre route par défaut (passerelle) :"
ip route show default
echo ""

echo "ETAPE 3 - Création d'une connexion statique :"
echo "============================================="
echo "Nous allons créer une nouvelle connection avec IP fixe"
echo ""
echo "Syntaxe générale :"
echo "sudo nmcli connection add type ethernet \\"
echo "     con-name 'NOM-CONNEXION' \\"
echo "     ifname INTERFACE \\"
echo "     ip4 ADRESSE-IP/MASQUE \\"
echo "     gw4 PASSERELLE"
echo ""
echo "EXEMPLE PRATIQUE (adaptez à votre réseau) :"
echo "Si votre réseau actuel est 192.168.1.x :"
echo ""
echo "sudo nmcli connection add type ethernet \\"
echo "     con-name 'lab-static' \\"
echo "     ifname eth0 \\"
echo "     ip4 192.168.1.150/24 \\"
echo "     gw4 192.168.1.1"
echo ""

echo "ETAPE 4 - Activation de la connexion :"
echo "======================================"
echo "Activez votre nouvelle connexion :"
echo "sudo nmcli connection up 'lab-static'"
echo ""
echo "Vérifiez que la connexion est active :"
echo "nmcli connection show --active"
echo ""

echo "INSTRUCTIONS DETAILLEES A SUIVRE :"
echo "=================================="
echo ""
echo "1. IDENTIFIEZ votre interface principale :"
echo "   ip link show"
echo "   (Notez le nom : eth0, enp0s3, etc.)"
echo ""
echo "2. REGARDEZ votre réseau actuel :"
echo "   ip route show default"
echo "   (Notez l'IP de passerelle après 'via')"
echo ""
echo "3. CHOISISSEZ une IP libre dans le même réseau :"
echo "   Si passerelle = 192.168.1.1, choisissez 192.168.1.XXX"
echo "   Si passerelle = 10.0.2.1, choisissez 10.0.2.XXX"
echo ""
echo "4. CREEZ la connexion (remplacez les valeurs) :"
echo "   sudo nmcli connection add type ethernet \\"
echo "        con-name 'lab-static' \\"
echo "        ifname VOTRE_INTERFACE \\"
echo "        ip4 VOTRE_IP_CHOISIE/24 \\"
echo "        gw4 VOTRE_PASSERELLE"
echo ""
echo "5. ACTIVEZ la connexion :"
echo "   sudo nmcli connection up 'lab-static'"
echo ""

echo "ETAPE 5 - Tests de validation :"
echo "==============================="
echo ""
echo "1. VERIFIEZ que votre IP statique est assignée :"
echo "   ip addr show"
echo "   (Cherchez votre nouvelle IP dans la sortie)"
echo ""
echo "2. TESTEZ la connectivité vers la passerelle :"
echo "   ping -c 3 VOTRE_PASSERELLE"
echo "   (Remplacez VOTRE_PASSERELLE par l'IP de l'étape 2)"
echo ""
echo "3. VERIFIEZ que la connexion est persistante :"
echo "   nmcli connection show"
echo "   (Votre connexion 'lab-static' doit apparaître)"
echo ""

echo "GESTION AVANCEE DES CONNEXIONS :"
echo "================================"
echo ""
echo "Lister toutes les connexions :"
echo "nmcli connection show"
echo ""
echo "Basculer entre connexions (concept device vs connection) :"
echo "sudo nmcli connection down 'ancienne-connexion'"
echo "sudo nmcli connection up 'nouvelle-connexion'"
echo ""
echo "Supprimer une connexion :"
echo "sudo nmcli connection delete 'nom-connexion'"
echo ""
echo "Modifier une connexion existante :"
echo "sudo nmcli connection modify 'lab-static' ipv4.addresses 192.168.1.200/24"
echo ""

echo "EXEMPLES SELON VOTRE ENVIRONNEMENT :"
echo "===================================="
echo ""
echo "Si votre réseau est 192.168.1.x :"
echo "sudo nmcli con add type ethernet con-name 'static-home' \\"
echo "     ifname eth0 ip4 192.168.1.100/24 gw4 192.168.1.1"
echo ""
echo "Si votre réseau est 10.0.2.x :"  
echo "sudo nmcli con add type ethernet con-name 'static-vm' \\"
echo "     ifname eth0 ip4 10.0.2.100/24 gw4 10.0.2.1"
echo ""
echo "Si votre réseau est 172.16.x.x :"
echo "sudo nmcli con add type ethernet con-name 'static-lab' \\"
echo "     ifname eth0 ip4 172.16.1.100/24 gw4 172.16.1.1"
echo ""

echo "DEPANNAGE SIMPLE :"
echo "=================="
echo ""
echo "Problème : 'Connection activation failed'"
echo "Solution : Vérifier que l'interface existe avec 'ip link show'"
echo ""
echo "Problème : IP n'apparaît pas"
echo "Solution : Vérifier que la connexion est UP avec 'nmcli con show --active'"
echo ""
echo "Problème : Pas d'accès réseau"
echo "Solution : Tester la passerelle avec 'ping PASSERELLE'"
echo ""

echo "CRITERES DE VALIDATION :"
echo "[] NetworkManager actif et fonctionnel"
echo "[] Device (interface) identifié correctement"
echo "[] Connexion statique créée avec nmcli"
echo "[] Adresse IP statique assignée et visible dans 'ip addr show'"
echo "[] Passerelle accessible avec ping"
echo "[] Configuration persistante (connexion visible dans 'nmcli con show')"
echo "[] Compréhension de la différence device vs connection"
echo ""

echo "COMPETENCES ACQUISES :"
echo "[] Utilisation de base de nmcli"
echo "[] Configuration IP statique sans GUI"
echo "[] Tests de connectivité réseau de base"
echo "[] Gestion des profils de connexion NetworkManager"
echo ""

echo "=== FIN DU LAB 2 ==="
