#!/bin/bash

# =============================================================================
# LAB 2 - Configuration de base du réseau
# =============================================================================
#
# Énoncé : Apprendre à voir et comprendre la configuration réseau d'une machine Linux
#
# Objectif : Utiliser les commandes de base pour examiner et comprendre le réseau
#
# Durée estimée : 20 minutes
# Niveau de difficulté : Intermédiaire
# Prérequis : Aucune connaissance de scripting - commandes simples uniquement
# =============================================================================

# =============================================================================
# PARTIE 1 - Qu'est-ce que le routage ?
# =============================================================================

echo "=== LAB 2 - Configuration de base du réseau ==="
echo ""
echo " QU'EST-CE QUE LE ROUTAGE ?"
echo "=============================="
echo ""
echo "Le routage permet aux machines de communiquer entre différents réseaux."
echo "Votre machine sait automatiquement :"
echo "• Comment accéder aux machines du même réseau"
echo "• Par où passer pour accéder à Internet" 
echo "• Quels réseaux elle peut atteindre"
echo ""
echo " TABLES DE ROUTAGE :"
echo "======================"
echo ""
echo "Linux garde une 'table de routage' qui liste :"
echo "• Les réseaux connus"
echo "• Par quelle interface (carte réseau) les atteindre"
echo "• L'adresse IP de la passerelle (routeur/box)"
echo ""

# =============================================================================
# PARTIE 2 - Examiner la configuration actuelle
# =============================================================================

echo " EXERCICE 1 - Voir toutes les interfaces réseau :"
echo "==================================================="
echo ""
echo "Une interface réseau = une 'carte réseau' (physique ou virtuelle)"
echo ""
echo "1. Listez toutes les interfaces de votre machine :"
echo " ip link show"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip link show
echo ""
echo " RECHERCHEZ dans les résultats :"
echo "• lo → Interface de boucle locale (localhost)"
echo "• eth0/enp → Interface Ethernet (câble réseau)"
echo "• wlan0 → Interface WiFi (si présente)"
echo "• UP → Interface active"
echo "• DOWN → Interface inactive"
echo ""

echo "2. Voyez les adresses IP assignées :"
echo " ip addr show"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip addr show
echo ""
echo " RECHERCHEZ :"
echo "• inet 127.0.0.1/8 → Adresse localhost"
echo "• inet 192.168.X.X/24 → Votre adresse IP locale"
echo "• state UP → Interface fonctionnelle"
echo ""

# =============================================================================
# PARTIE 3 - Comprendre la table de routage
# =============================================================================

echo "EXERCICE 2 - Examiner la table de routage :"
echo "==============================================="
echo ""
echo "La table de routage indique où envoyer les paquets réseau."
echo ""
echo "1. Affichez la table de routage principale :"
echo " ip route show"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip route show
echo ""
echo " INTERPRÉTATION DES RÉSULTATS :"
echo ""
echo "• default via X.X.X.X → Route par défaut (vers Internet)"
echo " └─ Tous les paquets inconnus vont vers cette adresse"
echo ""
echo "• 192.168.X.X/24 dev ethY → Réseau local direct"
echo " └─ Les machines de ce réseau sont accessibles directement"
echo ""
echo "• 127.0.0.0/8 dev lo → Réseau local (localhost)"
echo " └─ Communication interne à la machine"
echo ""

echo "2. Voyez plus de détails avec :"
echo " ip route show table main"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip route show table main
echo ""

# =============================================================================
# PARTIE 4 - Identifier la passerelle
# =============================================================================

echo "EXERCICE 3 - Identifier votre passerelle (routeur/box) :"
echo "==========================================================="
echo ""
echo "La passerelle est l'appareil qui vous connecte à Internet."
echo "C'est généralement votre box Internet ou routeur."
echo ""
echo "1. Trouvez votre passerelle par défaut :"
echo " ip route show | grep default"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip route show | grep default
echo ""
echo " ANALYSE :"
echo "La ligne 'default via X.X.X.X' montre l'adresse de votre passerelle."
echo "Exemple : default via 192.168.1.1 dev eth0"
echo " ↳ Votre box/routeur est probablement 192.168.1.1"
echo ""

echo "2. Testez la connectivité vers votre passerelle :"
echo " ping -c 3 [ADRESSE_PASSERELLE]"
echo ""
GATEWAY=$(ip route show | grep default | awk '{print $3}' | head -1)
if [ -n "$GATEWAY" ]; then
 echo "Votre passerelle semble être : $GATEWAY"
 echo ""
 echo "Test de connectivité :"
 ping -c 3 $GATEWAY || echo " Pas de réponse de la passerelle"
else
 echo " Impossible de détecter la passerelle automatiquement"
 echo "Regardez la sortie de 'ip route show' ci-dessus."
fi
echo ""

# =============================================================================
# PARTIE 5 - Tester la connectivité réseau
# =============================================================================

echo "EXERCICE 4 - Tester différents types de connectivité :"
echo "========================================================="
echo ""
echo "Testons la connectivité à différents niveaux :"
echo ""

echo "1. Test local (votre propre machine) :"
echo " ping -c 3 127.0.0.1"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ping -c 3 127.0.0.1
echo ""
echo " Si ça fonctionne : La pile réseau de votre machine fonctionne"
echo ""

echo "2. Test réseau local (votre passerelle) :"
if [ -n "$GATEWAY" ]; then
 echo " ping -c 3 $GATEWAY"
 echo ""
 echo "EXERCICE : Copiez et exécutez :"
 echo ""
 ping -c 3 $GATEWAY || echo " Problème de connectivité locale"
else
 echo " ping -c 3 [ADRESSE_DE_VOTRE_PASSERELLE]"
 echo ""
 echo "Remplacez [ADRESSE_DE_VOTRE_PASSERELLE] par l'adresse trouvée plus haut."
fi
echo ""
echo " Si ça fonctionne : Votre connexion réseau locale fonctionne"
echo ""

echo "3. Test Internet (DNS public) :"
echo " ping -c 3 8.8.8.8"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ping -c 3 8.8.8.8 || echo " Pas d'accès Internet ou DNS"
echo ""
echo " Si ça fonctionne : Votre connexion Internet fonctionne"
echo ""

# =============================================================================
# PARTIE 6 - Informations système réseau
# =============================================================================

echo " EXERCICE 5 - Informations complémentaires sur le réseau :"
echo "============================================================="
echo ""
echo "Découvrons d'autres informations utiles :"
echo ""

echo "1. Voir le nom de votre machine sur le réseau :"
echo " hostname"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
hostname
echo ""

echo "2. Voir la configuration DNS (serveurs de noms) :"
echo " cat /etc/resolv.conf"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
cat /etc/resolv.conf
echo ""
echo " EXPLICATION :"
echo "Les serveurs DNS traduisent les noms (google.com) en adresses IP."
echo ""

echo "3. Voir les connexions réseau actives :"
echo " ss -tuln"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ss -tuln | head -10
echo ""
echo " EXPLICATION :"
echo "Cette commande montre les services réseau qui écoutent sur votre machine."
echo "• LISTEN → Service en attente de connexions"
echo "• :22 → Service SSH (connexion à distance)"
echo "• :80 → Serveur web HTTP"
echo "• :443 → Serveur web HTTPS"
echo ""

# =============================================================================
# PARTIE 7 - Quiz de compréhension
# =============================================================================

echo " QUIZ - Testez votre compréhension :"
echo "======================================"
echo ""
echo "Basé sur ce que vous avez observé :"
echo ""
echo "Question 1 : Quelle est l'adresse IP de votre machine ?"
echo " (Regardez la sortie de 'ip addr show')"
echo ""
echo "Question 2 : Quelle est l'adresse de votre passerelle ?"
echo " (Regardez la sortie de 'ip route show | grep default')"
echo ""
echo "Question 3 : Combien d'interfaces réseau votre machine a-t-elle ?"
echo " (Comptez dans 'ip link show', excluez 'lo')"
echo ""
echo "Question 4 : Votre machine peut-elle accéder à Internet ?"
echo " (Regardez le résultat de 'ping 8.8.8.8')"
echo ""
echo "Question 5 : Quel est le nom de votre machine sur le réseau ?"
echo " (Regardez la sortie de 'hostname')"
echo ""

# =============================================================================
# VALIDATION ET RÉCAPITULATIF
# =============================================================================

echo " CRITÈRES DE RÉUSSITE :"
echo "========================"
echo ""
echo "Vous avez réussi si vous pouvez :"
echo "□ Lister les interfaces réseau avec 'ip link show'"
echo "□ Voir les adresses IP avec 'ip addr show'"
echo "□ Afficher la table de routage avec 'ip route show'"
echo "□ Identifier votre passerelle dans la table de routage"
echo "□ Tester la connectivité avec 'ping'"
echo "□ Comprendre les informations affichées par ces commandes"
echo ""

echo " CE QUE VOUS AVEZ APPRIS :"
echo "============================"
echo ""
echo "• Les interfaces réseau (lo, eth0, wlan0, etc.)"
echo "• Les adresses IP et leur notation CIDR"
echo "• La table de routage et la passerelle par défaut"
echo "• Comment tester la connectivité avec ping"
echo "• Les commandes de base du diagnostic réseau"
echo "• La configuration DNS de votre système"
echo ""

echo " POUR ALLER PLUS LOIN :"
echo "========================="
echo ""
echo "Dans les prochains LABs, vous apprendrez :"
echo "• À diagnostiquer les problèmes de connectivité"
echo "• À comprendre les ports et services réseau"
echo "• À analyser le trafic réseau"
echo ""

echo "=== FIN DU LAB 2 - Configuration de base du réseau ==="
