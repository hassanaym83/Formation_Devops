#!/bin/bash

# =============================================================================
# LAB 3 - Outils de diagnostic réseau : ping, traceroute, ss, netstat
# =============================================================================
#
# Énoncé : Maîtriser les 4 outils essentiels de diagnostic réseau Linux
#
# Objectifs pédagogiques :
# - Comprendre et utiliser ping pour tester la connectivité
# - Utiliser traceroute pour tracer les chemins réseau
# - Maîtriser ss pour analyser les connexions
# - Connaître netstat comme alternative à ss
#
# Durée estimée : 15 minutes
# Niveau : Débutant (1/3)
# =============================================================================

echo "=== LAB 3 - Outils de diagnostic réseau ==="
echo "Date: $(date)"
echo "Utilisateur: $USER"
echo ""

echo "OUTILS DE DIAGNOSTIC A MAITRISER :"
echo "=================================="
echo "1. ping      : Test de connectivité"
echo "2. traceroute: Tracer le chemin réseau"  
echo "3. ss        : Analyser les connexions (moderne)"
echo "4. netstat   : Analyser les connexions (classique)"
echo ""

# =============================================================================
# PARTIE 1 : COMMANDE PING
# =============================================================================

echo "PARTIE 1 - COMMANDE PING :"
echo "=========================="
echo ""
echo "Utilité : Tester si une adresse réseau répond"
echo ""

echo "Test 1 - Ping local (loopback) :"
echo "Commande : ping -c 3 127.0.0.1"
ping -c 3 127.0.0.1
echo ""

echo "Test 2 - Ping vers serveur externe :"
echo "Commande : ping -c 3 8.8.8.8"
ping -c 3 8.8.8.8
echo ""

echo "Exercice PING :"
echo "□ Testez ping vers 1.1.1.1 avec 2 paquets seulement"
echo "□ Observez les temps de réponse (time=)"
echo "□ Notez le pourcentage de perte de paquets"
echo ""

# =============================================================================
# PARTIE 2 : COMMANDE TRACEROUTE
# =============================================================================

echo "PARTIE 2 - COMMANDE TRACEROUTE :"
echo "================================"
echo ""
echo "Utilité : Voir le chemin que prennent les paquets"
echo ""

# Vérifier si traceroute est installé
if command -v traceroute >/dev/null 2>&1; then
    echo "Traceroute vers 8.8.8.8 (limité à 5 sauts) :"
    echo "Commande : traceroute -m 5 8.8.8.8"
    traceroute -m 5 8.8.8.8
else
    echo "Note : traceroute n'est pas installé sur ce système"
    echo "Installation : sudo apt install traceroute (Debian/Ubuntu)"
    echo "             : sudo yum install traceroute (CentOS/RHEL)"
fi
echo ""

echo "Exercice TRACEROUTE :"
echo "□ Installez traceroute si nécessaire"
echo "□ Tracez le chemin vers google.com"
echo "□ Comptez le nombre de sauts (hops)"
echo ""

# =============================================================================
# PARTIE 3 : COMMANDE SS (MODERNE)
# =============================================================================

echo "PARTIE 3 - COMMANDE SS :"
echo "========================"
echo ""
echo "Utilité : Voir les connexions et ports réseau"
echo ""

echo "Services en écoute (ports ouverts) :"
echo "Commande : ss -tuln"
ss -tuln
echo ""

echo "Connexions établies :"
echo "Commande : ss -tu"
ss -tu | grep ESTAB
echo ""

echo "Services avec processus (nécessite sudo) :"
echo "Commande : sudo ss -tulpn"
echo "Note : Exécutez cette commande manuellement avec sudo"
echo ""

echo "Exercice SS :"
echo "□ Identifiez si le port 22 (SSH) est ouvert"
echo "□ Comptez combien de services sont en écoute (LISTEN)"
echo "□ Trouvez les connexions TCP établies"
echo ""

# =============================================================================
# PARTIE 4 : COMMANDE NETSTAT (CLASSIQUE)
# =============================================================================

echo "PARTIE 4 - COMMANDE NETSTAT :"
echo "============================="
echo ""
echo "Utilité : Alternative classique à ss"
echo ""

if command -v netstat >/dev/null 2>&1; then
    echo "Services en écoute avec netstat :"
    echo "Commande : netstat -tuln"
    netstat -tuln | head -10
    echo ""
    
    echo "Statistiques réseau :"
    echo "Commande : netstat -s"
    netstat -s | head -15
else
    echo "Note : netstat n'est pas installé par défaut sur ce système"
    echo "Installation : sudo apt install net-tools"
fi
echo ""

echo "Exercice NETSTAT :"
echo "□ Comparez les résultats de netstat -tuln avec ss -tuln"
echo "□ Utilisez netstat -r pour voir les routes"
echo "□ Testez netstat -i pour voir les statistiques d'interfaces"
echo ""

# =============================================================================
# PARTIE 5 : COMPARAISON ET RESUME
# =============================================================================

echo "PARTIE 5 - COMPARAISON DES OUTILS :"
echo "===================================="
echo ""
echo "PING vs TRACEROUTE :"
echo "- ping    : Est-ce que ça répond ? (OUI/NON)"
echo "- traceroute : Par où ça passe ? (CHEMIN)"
echo ""
echo "SS vs NETSTAT :"
echo "- ss      : Moderne, rapide, plus d'infos"
echo "- netstat : Classique, compatible partout"
echo ""

echo "GUIDE DES OPTIONS IMPORTANTES :"
echo "==============================="
echo ""
echo "PING :"
echo "  -c N     : Envoyer N paquets puis s'arrêter"
echo "  -W N     : Timeout de N secondes"
echo ""
echo "SS :"
echo "  -t       : TCP seulement"
echo "  -u       : UDP seulement"  
echo "  -l       : Services en écoute (LISTEN)"
echo "  -n       : Format numérique (pas de résolution DNS)"
echo "  -p       : Afficher les processus"
echo ""
echo "NETSTAT :"
echo "  -t       : TCP"
echo "  -u       : UDP"
echo "  -l       : En écoute"
echo "  -n       : Numérique"
echo "  -p       : Processus"
echo "  -r       : Routes"
echo "  -s       : Statistiques"
echo ""

echo "EXERCICE FINAL - DIAGNOSTIC COMPLET :"
echo "====================================="
echo ""
echo "Réalisez ce diagnostic étape par étape :"
echo ""
echo "1. Testez la connectivité locale :"
echo "   □ ping -c 2 127.0.0.1"
echo ""
echo "2. Testez la connectivité Internet :"
echo "   □ ping -c 3 1.1.1.1"
echo ""
echo "3. Tracez un chemin réseau :"
echo "   □ traceroute google.com (si installé)"
echo ""
echo "4. Analysez les services locaux :"
echo "   □ ss -tuln | grep :22  (chercher SSH)"
echo "   □ ss -tu | grep ESTAB   (connexions actives)"
echo ""
echo "5. Comparez avec netstat :"
echo "   □ netstat -tuln | head -5 (si installé)"
echo ""

echo "CRITERES DE VALIDATION :"
echo "[] ping fonctionne vers 127.0.0.1 et Internet"
echo "[] traceroute installé et testé (optionnel)"
echo "[] ss -tuln exécuté et interprété"
echo "[] Services en écoute identifiés"
echo "[] Différence ss/netstat comprise"
echo ""

echo "=== FIN DU LAB 3 ==="
