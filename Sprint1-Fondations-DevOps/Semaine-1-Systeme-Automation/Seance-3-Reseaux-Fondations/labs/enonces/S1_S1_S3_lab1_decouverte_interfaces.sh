#!/bin/bash

# =============================================================================
#
# Énoncé : Vous venez d'hériter d'un serveur Linux et devez faire un audit
# de base de sa configuration réseau pour comprendre l'architecture existante.
#
# Objectif : Maîtriser les commandes de base pour découvrir et documenter 
# la configuration réseau d'un système Linux
#
# Contexte : Nouveau serveur, nécessitant documentation de base de la 
# configuration réseau pour la maintenance
#
# Durée estimée : 15 minutes
# Niveau de difficulté : Débutant (1/3)
# =============================================================================

echo "=== LAB 1 - Découverte des interfaces réseau Linux ==="
echo "Date: $(date)"
echo "Utilisateur: $USER"
echo ""

# Rappels théoriques
echo "RAPPELS THEORIQUES :"
echo "==================="
echo "Couches OSI concernées :"
echo "- Couche 1 (Physique) : Câbles, connecteurs, signaux électriques"
echo "- Couche 2 (Liaison) : Adresses MAC, trames Ethernet"
echo "- Couche 3 (Réseau) : Adresses IP, routage"
echo ""
echo "Types d'interfaces réseau :"
echo "- PHYSIQUES (eth0, enp0s*) : Interfaces matérielles réelles"
echo "- VIRTUELLES (lo, docker0, br-*) : Interfaces logicielles"
echo "- États UP/DOWN : Activation au niveau couche 2 (liaison)"
echo ""
echo "Adressage réseau :"
echo "- Adresse MAC : Identifiant unique couche 2 (ex: 00:1B:63:84:45:E6)"
echo "- Adresse IP : Identifiant logique couche 3 (ex: 192.168.1.50/24)"
echo "- Loopback (127.0.0.1) : Interface virtuelle locale système"
echo ""

# Instructions simplifiées pour débutants
echo "INSTRUCTIONS DU LAB :"
echo "===================="
echo "Vous allez exécuter 3 commandes et analyser les résultats"
echo ""
echo "1. Listez toutes les interfaces réseau disponibles"
echo "2. Affichez les adresses IP configurées"  
echo "3. Identifiez l'interface principale connectée au réseau"
echo ""

# Commandes de base à utiliser
echo "COMMANDES A EXECUTER :"
echo "====================="
echo ""
echo "ETAPE 1 : ip link show"
echo "Cette commande montre toutes les interfaces et leur état UP/DOWN"
echo ""
echo "ETAPE 2 : ip addr show"
echo "Cette commande ajoute les adresses IP et MAC"
echo ""
echo "ETAPE 3 : ip route show default"
echo "Cette commande montre l'interface principale (route par défaut)"
echo ""

# Phase d'exécution simplifiée
echo "PHASE D'EXECUTION :"
echo "=================="
echo ""
echo "EXECUTEZ CES COMMANDES UNE PAR UNE :"
echo ""
echo ">>> ip link show"
echo ""
echo ">>> ip addr show"
echo ""
echo ">>> ip route show default"
echo ""

# Exercices d'analyse simplifiés
echo "EXERCICES D'ANALYSE (après exécution des commandes) :"
echo "====================================================="
echo ""
echo "1. ANALYSE DES RESULTATS selon Section 4.2 du cours :"
echo ""
echo "Dans la sortie de 'ip addr show', cherchez :"
echo "- Mots 'UP' ou 'DOWN' pour l'état de chaque interface"
echo "- Adresses IP au format X.X.X.X/24"
echo "- Valeurs MTU (généralement 1500 pour Ethernet)"
echo "- Adresses MAC au format XX:XX:XX:XX:XX:XX"
echo ""
echo "2. COMPLETEZ CE TABLEAU SIMPLE :"
echo ""
echo "| Interface | État UP/DOWN | A une IP | Type (physique/virtuelle) |"
echo "|-----------|--------------|----------|---------------------------|"
echo "| lo        |              |          |                           |"
echo "| eth0      |              |          |                           |"
echo "| (autre)   |              |          |                           |"
echo ""
echo "3. QUESTIONS SIMPLES D'ANALYSE :"
echo "   - Combien d'interfaces sont en état UP ?"
echo "   - Quelle interface a une adresse IP qui commence par 192.168 ?"
echo "   - L'interface 'lo' a-t-elle l'adresse 127.0.0.1 ?"
echo "   - Selon 'ip route show default', quelle interface est principale ?"
echo ""

# Vérifications simplifiées
echo "CRITERES DE VALIDATION :"
echo "[] J'ai exécuté les 3 commandes demandées"
echo "[] J'ai identifié les interfaces en état UP"
echo "[] J'ai noté les adresses IP de chaque interface active"
echo "[] J'ai trouvé l'interface principale avec la route par défaut"
echo "[] J'ai complété le tableau simple"
echo "[] J'ai répondu aux 4 questions d'analyse"
echo ""

echo "AIDE-MEMOIRE POUR DEBUTANTS :"
echo "lo = Interface loopback (127.0.0.1) - toujours présente"
echo "eth0/enp0s* = Interface Ethernet physique principale"
echo "UP = Interface activée et fonctionnelle"
echo "DOWN = Interface désactivée ou déconnectée"
echo "/24 = Masque réseau 255.255.255.0"
echo "192.168.x.x = Plage d'adresses réseau local typique"
echo ""

echo "=== FIN DU LAB 1 ==="
