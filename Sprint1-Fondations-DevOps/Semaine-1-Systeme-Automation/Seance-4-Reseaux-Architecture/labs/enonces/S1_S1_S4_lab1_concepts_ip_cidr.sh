#!/bin/bash

# =============================================================================
# LAB 1 - Concepts de base IP et CIDR
# =============================================================================
#
# Énoncé : Découvrir les concepts de base des adresses IP et des masques CIDR 
# en utilisant des commandes Linux simples.
#
# Objectif : Comprendre l'adressage IP et CIDR avec des commandes de base
#
# Durée estimée : 15 minutes
# Niveau de difficulté : Débutant
# Prérequis : Aucune connaissance de scripting requise - commandes simples uniquement
# =============================================================================

# =============================================================================
# PARTIE 1 - Théorie de base
# =============================================================================

echo "=== LAB 1 - Concepts de base IP et CIDR ==="
echo ""
echo "QU'EST-CE QU'UNE ADRESSE IP ?"
echo "================================"
echo ""
echo "Une adresse IP est un identifiant unique pour chaque machine sur un réseau."
echo "Format : 4 nombres de 0 à 255, séparés par des points"
echo "Exemple : 192.168.1.10"
echo ""
echo "QU'EST-CE QU'UN MASQUE CIDR ?"
echo "================================"
echo ""
echo "Le CIDR (/XX) indique combien de bits sont utilisés pour le réseau."
echo "Plus le nombre est grand, plus le réseau est petit."
echo ""
echo "Exemples courants :"
echo "/24 = 255.255.255.0 → 254 adresses utilisables"
echo "/16 = 255.255.0.0 → 65,534 adresses utilisables" 
echo ""

# =============================================================================
# PARTIE 2 - Vérification des outils
# =============================================================================

echo "OUTILS NECESSAIRES :"
echo "======================="
echo ""
echo "Nous allons utiliser la commande 'ipcalc' pour faire nos calculs."
echo ""
echo "1. Vérifiez si ipcalc est installé :"
echo " which ipcalc"
echo ""
echo "2. Si pas installé, installez-le :"
echo " sudo apt install ipcalc"
echo ""
echo "EXERCICE : Tapez la commande suivante pour vérifier :"

which ipcalc
echo ""
echo "Résultat attendu : /usr/bin/ipcalc (ou chemin similaire)"
echo "Si rien ne s'affiche, l'outil n'est pas installé."
echo ""

# =============================================================================
# PARTIE 3 - Premier calcul CIDR
# =============================================================================

echo "EXERCICE 1 - Découvrir un réseau avec ipcalc :"
echo "=================================================="
echo ""
echo "Nous allons analyser un réseau simple : 192.168.1.0/24"
echo ""
echo "1. Tapez cette commande pour analyser le réseau :"
echo " ipcalc 192.168.1.0/24"
echo ""
echo "EXERCICE : Copiez et exécutez cette commande :"
echo ""
ipcalc 192.168.1.0/24 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""
echo "EXPLICATION DES RÉSULTATS :"
echo "• Network : L'adresse du réseau (première adresse)"
echo "• Netmask : Le masque de sous-réseau" 
echo "• HostMin : Première adresse utilisable pour une machine"
echo "• HostMax : Dernière adresse utilisable pour une machine"
echo "• Broadcast : Adresse de diffusion (dernière adresse)"
echo "• Hosts/Net : Nombre de machines possibles sur ce réseau"
echo ""

# =============================================================================
# PARTIE 4 - Comparer différents réseaux
# =============================================================================

echo "EXERCICE 2 - Comparer différents masques CIDR :"
echo "==================================================="
echo ""
echo "Voyons la différence entre /24 et /16 :"
echo ""
echo "1. D'abord analysons un réseau /16 (plus grand) :"
echo " ipcalc 192.168.0.0/16"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ipcalc 192.168.0.0/16 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""
echo "2. Maintenant analysons un réseau /24 (plus petit) :"
echo " ipcalc 192.168.1.0/24"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ipcalc 192.168.1.0/24 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""
echo "OBSERVATION :"
echo "• /16 → Beaucoup d'adresses (65,534 machines possibles)"
echo "• /24 → Peu d'adresses (254 machines possibles)"
echo "• Plus le nombre après / est grand, plus le réseau est petit"
echo ""

# =============================================================================
# PARTIE 5 - Découvrir votre réseau actuel
# =============================================================================

echo "EXERCICE 3 - Voir la configuration réseau de votre machine :"
echo "================================================================"
echo ""
echo "Découvrons l'adresse IP de votre machine :"
echo ""
echo "1. Affichez toutes les interfaces réseau :"
echo " ip addr show"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip addr show
echo ""
echo "RECHERCHEZ dans les résultats :"
echo "• inet 192.168.X.X/24 → Votre adresse IP locale"
echo "• inet 127.0.0.1/8 → Interface de boucle locale (localhost)"
echo ""
echo "2. Voyez vers où vont vos connexions :"
echo " ip route show"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ip route show
echo ""
echo "RECHERCHEZ :"
echo "• default via X.X.X.X → Votre passerelle (routeur/box)"
echo "• 192.168.X.X/24 → Votre réseau local"
echo ""

# =============================================================================
# PARTIE 6 - Exercices pratiques de calculs
# =============================================================================

echo "EXERCICE 4 - Pratiquer avec différents masques :"
echo "==================================================="
echo ""
echo "Essayons différents masques CIDR pour comprendre :"
echo ""
echo "1. Un très grand réseau /8 :"
echo " ipcalc 10.0.0.0/8"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ipcalc 10.0.0.0/8 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""
echo "2. Un réseau moyen /16 :"
echo " ipcalc 172.16.0.0/16"
echo ""
echo "EXERCICE : Copiez et exécutez :" 
echo ""
ipcalc 172.16.0.0/16 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""
echo "3. Un petit réseau /28 (seulement 14 machines) :"
echo " ipcalc 192.168.1.0/28"
echo ""
echo "EXERCICE : Copiez et exécutez :"
echo ""
ipcalc 192.168.1.0/28 2>/dev/null || echo " Installez ipcalc avec : sudo apt install ipcalc"
echo ""

# =============================================================================
# PARTIE 7 - Quiz de validation
# =============================================================================

echo " QUIZ - Testez votre compréhension :"
echo "======================================"
echo ""
echo "Répondez à ces questions après avoir fait les exercices :"
echo ""
echo "Question 1 : Dans le réseau 192.168.1.0/24 :"
echo " a) Combien de machines peut-on connecter au maximum ?"
echo " b) Quelle est la première adresse utilisable ?"
echo " c) Quelle est l'adresse de broadcast ?"
echo ""
echo "Question 2 : Quel réseau est le plus grand ?"
echo " a) 10.0.0.0/8"
echo " b) 192.168.1.0/24" 
echo " c) 172.16.0.0/16"
echo ""
echo "Question 3 : Si vous voulez connecter seulement 10 machines,"
echo " quel masque CIDR convient le mieux ?"
echo " a) /24 (254 machines possibles)"
echo " b) /28 (14 machines possibles)"
echo " c) /16 (65,534 machines possibles)"
echo ""
echo "POUR VÉRIFIER VOS RÉPONSES :"
echo "Utilisez ipcalc avec les adresses des questions !"
echo ""

# =============================================================================
# VALIDATION ET RÉCAPITULATIF 
# =============================================================================

echo " CRITÈRES DE RÉUSSITE :"
echo "========================"
echo ""
echo "Vous avez réussi si vous pouvez :"
echo "□ Expliquer ce qu'est une adresse IP"
echo "□ Comprendre ce que signifie /24, /16, /8"
echo "□ Utiliser la commande ipcalc pour analyser un réseau"
echo "□ Lire les informations d'un réseau (Network, HostMin, HostMax, etc.)"
echo "□ Voir la configuration réseau de votre machine avec 'ip addr show'"
echo "□ Répondre correctement aux questions du quiz"
echo ""

echo "CE QUE VOUS AVEZ APPRIS :"
echo "============================"
echo ""
echo "• Une adresse IP identifie une machine sur le réseau"
echo "• Le masque CIDR (/XX) définit la taille du réseau" 
echo "• Plus le nombre est grand, plus le réseau est petit"
echo "• La commande 'ipcalc' calcule automatiquement les informations d'un réseau"
echo "• La commande 'ip addr show' montre la configuration de votre machine"
echo "• La commande 'ip route show' montre les chemins réseau"
echo ""

echo "POUR ALLER PLUS LOIN :"
echo "========================="
echo ""
echo "Dans les prochains LABs, vous apprendrez :"
echo "• À configurer des adresses IP"
echo "• À créer des routes réseau"
echo "• À diagnostiquer les problèmes de connectivité"
echo ""

echo "=== FIN DU LAB 1 - Concepts de base IP et CIDR ==="
