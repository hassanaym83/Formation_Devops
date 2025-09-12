#!/bin/bash

# =============================================================================
# LAB 4 - Configuration et résolution DNS
# =============================================================================
#
# Énoncé : Apprendre à configurer et tester la résolution DNS sur Linux
# pour comprendre comment les noms de domaine sont traduits en adresses IP
#
# Objectif : Maîtriser la configuration DNS et les outils de résolution de noms
# - Configuration des serveurs DNS
# - Tests de résolution avec nslookup et dig
# - Dépannage des problèmes DNS
#
# Contexte : Le DNS est essentiel pour l'accès aux services par nom
#
# Durée estimée : 20 minutes
# Niveau de difficulté : Intermédiaire (2/3)
# =============================================================================

echo "=== LAB 4 - Configuration et résolution DNS ==="
echo "Date: $(date)"
echo "Utilisateur: $USER"
echo ""

echo "OBJECTIF DU LAB :"
echo "================="
echo "Comprendre et configurer le DNS (Domain Name System) :"
echo "- Comprendre le rôle du DNS dans les réseaux"
echo "- Configurer les serveurs DNS"
echo "- Tester la résolution de noms"
echo "- Diagnostiquer les problèmes DNS"
echo ""

echo "RAPPEL THEORIQUE - DNS :"
echo "========================"
echo "Le DNS (Domain Name System) traduit les noms en adresses IP"
echo "Exemple : google.com → 172.217.16.110"
echo ""
echo "Composants principaux :"
echo "- Serveurs DNS : Machines qui résolvent les noms"
echo "- Fichier /etc/resolv.conf : Configuration des serveurs DNS"
echo "- Cache DNS : Mémorisation temporaire des résolutions"
echo ""
echo "Outils de test :"
echo "- nslookup : Test simple de résolution"
echo "- dig : Test avancé avec détails"
echo "- ping : Test avec résolution automatique"
echo ""

echo "ETAPE 1 - ANALYSE DE LA CONFIGURATION DNS ACTUELLE :"
echo "===================================================="
echo ""
echo "1.1. Configuration des serveurs DNS :"
echo "Fichier : /etc/resolv.conf"
echo "Commande : cat /etc/resolv.conf"
echo ""
if [ -f /etc/resolv.conf ]; then
    cat /etc/resolv.conf
else
    echo "Fichier /etc/resolv.conf non trouvé"
fi
echo ""
echo "Explication :"
echo "- nameserver : Adresse IP du serveur DNS"
echo "- domain : Domaine local par défaut"
echo "- search : Domaines de recherche automatique"
echo ""

echo "1.2. Test de résolution DNS actuelle :"
echo "Test avec nslookup :"
echo "Commande : nslookup google.com"
echo ""
if command -v nslookup >/dev/null 2>&1; then
    nslookup google.com
else
    echo "nslookup n'est pas installé"
    echo "Installation : sudo apt install dnsutils (Ubuntu/Debian)"
fi
echo ""

echo "ETAPE 2 - TESTS AVEC DIFFERENTS SERVEURS DNS :"
echo "=============================================="
echo ""
echo "2.1. Test avec le serveur DNS de Google (8.8.8.8) :"
echo "Commande : nslookup google.com 8.8.8.8"
echo ""
if command -v nslookup >/dev/null 2>&1; then
    nslookup google.com 8.8.8.8
else
    echo "Test non disponible - nslookup requis"
fi
echo ""

echo "2.2. Test avec le serveur DNS de Cloudflare (1.1.1.1) :"
echo "Commande : nslookup google.com 1.1.1.1"
echo ""
if command -v nslookup >/dev/null 2>&1; then
    nslookup google.com 1.1.1.1
else
    echo "Test non disponible - nslookup requis"
fi
echo ""

echo "2.3. Comparaison des temps de réponse :"
echo "Serveurs DNS populaires :"
echo "- 8.8.8.8 : Google DNS (rapide, global)"
echo "- 1.1.1.1 : Cloudflare DNS (privé, sécurisé)"
echo "- 208.67.222.222 : OpenDNS (filtrage parental)"
echo ""

echo "ETAPE 3 - UTILISATION DE L'OUTIL DIG :"
echo "======================================"
echo ""
echo "3.1. Test de base avec dig :"
echo "Commande : dig google.com"
echo ""
if command -v dig >/dev/null 2>&1; then
    dig google.com +short
    echo ""
    echo "Version détaillée :"
    dig google.com | head -20
else
    echo "dig n'est pas installé"
    echo "Installation : sudo apt install dnsutils (Ubuntu/Debian)"
fi
echo ""

echo "3.2. Test de différents types d'enregistrements :"
echo ""
echo "Enregistrement A (adresse IPv4) :"
echo "Commande : dig google.com A +short"
if command -v dig >/dev/null 2>&1; then
    dig google.com A +short
fi
echo ""

echo "Enregistrement AAAA (adresse IPv6) :"
echo "Commande : dig google.com AAAA +short"
if command -v dig >/dev/null 2>&1; then
    dig google.com AAAA +short
fi
echo ""

echo "Enregistrement MX (serveur de mail) :"
echo "Commande : dig google.com MX +short"
if command -v dig >/dev/null 2>&1; then
    dig google.com MX +short
fi
echo ""

echo "ETAPE 4 - CONFIGURATION DES SERVEURS DNS :"
echo "=========================================="
echo ""
echo "4.1. Sauvegarde de la configuration actuelle :"
echo "Commande : sudo cp /etc/resolv.conf /etc/resolv.conf.backup"
echo ""
echo "IMPORTANT : Toujours sauvegarder avant modification !"
echo ""

echo "4.2. Méthode 1 - Modification temporaire :"
echo "Cette méthode est temporaire (perdue au redémarrage)"
echo ""
echo "Voir le contenu actuel :"
echo "cat /etc/resolv.conf"
echo ""
echo "Exemple de modification (NE PAS EXECUTER sans supervision) :"
echo "echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf"
echo "echo 'nameserver 1.1.1.1' | sudo tee -a /etc/resolv.conf"
echo ""

echo "4.3. Méthode 2 - Configuration avec NetworkManager :"
echo "Méthode recommandée (persistante) :"
echo ""
echo "Lister les connexions :"
echo "nmcli connection show"
echo ""
CONNECTION_NAME=$(nmcli connection show | grep -v "NAME" | head -1 | awk '{print $1}')
if [ -n "$CONNECTION_NAME" ]; then
    echo "Exemple avec la connexion '$CONNECTION_NAME' :"
    echo "sudo nmcli connection modify '$CONNECTION_NAME' ipv4.dns '8.8.8.8,1.1.1.1'"
    echo "sudo nmcli connection up '$CONNECTION_NAME'"
else
    echo "sudo nmcli connection modify [nom-connexion] ipv4.dns '8.8.8.8,1.1.1.1'"
    echo "sudo nmcli connection up [nom-connexion]"
fi
echo ""

echo "ETAPE 5 - TESTS DE VALIDATION DNS :"
echo "==================================="
echo ""
echo "5.1. Test de résolution de base :"
echo "Commandes à tester après configuration :"
echo ""
echo "nslookup google.com"
echo "nslookup facebook.com"
echo "nslookup github.com"
echo ""

echo "5.2. Test de résolution inverse :"
echo "Résolution IP → nom de domaine :"
echo "Commande : nslookup 8.8.8.8"
if command -v nslookup >/dev/null 2>&1; then
    nslookup 8.8.8.8
fi
echo ""

echo "5.3. Test avec ping (résolution automatique) :"
echo "Le ping fait automatiquement la résolution DNS :"
echo "Commande : ping -c 2 google.com"
ping -c 2 google.com 2>/dev/null || echo "Test ping échoué"
echo ""

echo "ETAPE 6 - DIAGNOSTIC DES PROBLEMES DNS :"
echo "========================================"
echo ""
echo "6.1. Problèmes courants et solutions :"
echo ""
echo "Problème : 'Name or service not known'"
echo "Cause : Serveur DNS inaccessible ou mal configuré"
echo "Solution : Vérifier /etc/resolv.conf et connectivité"
echo ""
echo "Problème : Résolution très lente"
echo "Cause : Serveur DNS lent ou surchargé"
echo "Solution : Changer de serveur DNS (8.8.8.8, 1.1.1.1)"
echo ""
echo "Problème : Certains sites ne résolvent pas"
echo "Cause : DNS avec filtrage ou censure"
echo "Solution : Utiliser DNS neutres (1.1.1.1)"
echo ""

echo "6.2. Tests de diagnostic :"
echo ""
echo "Test connectivité vers serveur DNS :"
DNS_SERVER=$(cat /etc/resolv.conf 2>/dev/null | grep nameserver | head -1 | awk '{print $2}')
if [ -n "$DNS_SERVER" ]; then
    echo "ping -c 2 $DNS_SERVER"
    ping -c 2 "$DNS_SERVER" 2>/dev/null || echo "Serveur DNS $DNS_SERVER inaccessible"
else
    echo "ping -c 2 8.8.8.8"
    ping -c 2 8.8.8.8 2>/dev/null || echo "Test avec 8.8.8.8"
fi
echo ""

echo "ETAPE 7 - SCRIPT DE DIAGNOSTIC DNS :"
echo "===================================="
echo ""

# Script de diagnostic DNS automatisé
diagnostic_dns() {
    echo "=== DIAGNOSTIC DNS AUTOMATISE ==="
    SCORE=0
    TOTAL=5
    
    echo "Test 1 - Configuration DNS présente :"
    if [ -f /etc/resolv.conf ] && grep -q "nameserver" /etc/resolv.conf; then
        echo "   [OK] Serveurs DNS configurés"
        ((SCORE++))
    else
        echo "   [ERREUR] Pas de serveurs DNS configurés"
    fi
    
    echo "Test 2 - Résolution de nom simple :"
    if nslookup google.com >/dev/null 2>&1; then
        echo "   [OK] Résolution google.com réussie"
        ((SCORE++))
    else
        echo "   [ERREUR] Échec résolution google.com"
    fi
    
    echo "Test 3 - Connectivité vers serveur DNS :"
    DNS_IP=$(cat /etc/resolv.conf 2>/dev/null | grep nameserver | head -1 | awk '{print $2}')
    if [ -n "$DNS_IP" ] && ping -c 1 -W 2 "$DNS_IP" >/dev/null 2>&1; then
        echo "   [OK] Serveur DNS $DNS_IP accessible"
        ((SCORE++))
    else
        echo "   [ERREUR] Serveur DNS inaccessible"
    fi
    
    echo "Test 4 - Résolution avec ping :"
    if ping -c 1 -W 3 google.com >/dev/null 2>&1; then
        echo "   [OK] Résolution DNS via ping fonctionnelle"
        ((SCORE++))
    else
        echo "   [ERREUR] Ping avec résolution DNS échoué"
    fi
    
    echo "Test 5 - Test serveur DNS externe :"
    if nslookup google.com 8.8.8.8 >/dev/null 2>&1; then
        echo "   [OK] Serveur DNS externe (8.8.8.8) fonctionne"
        ((SCORE++))
    else
        echo "   [ERREUR] Problème avec serveurs DNS externes"
    fi
    
    echo ""
    echo "SCORE DNS : $SCORE/$TOTAL"
    if [ $SCORE -eq $TOTAL ]; then
        echo "RESULTAT : EXCELLENT - DNS parfaitement configuré"
    elif [ $SCORE -ge 3 ]; then
        echo "RESULTAT : ACCEPTABLE - DNS fonctionne avec quelques améliorations"
    else
        echo "RESULTAT : PROBLEMATIQUE - Configuration DNS à revoir"
    fi
    
    echo ""
    echo "Configuration DNS actuelle :"
    cat /etc/resolv.conf 2>/dev/null | grep nameserver || echo "Aucun serveur DNS configuré"
}

diagnostic_dns

echo ""
echo "EXERCICES PRATIQUES :"
echo "===================="
echo ""
echo "1. Analysez la configuration DNS actuelle de votre système"
echo "2. Testez la résolution de différents domaines (google.com, github.com)"
echo "3. Comparez les temps de réponse entre différents serveurs DNS"
echo "4. Configurez des serveurs DNS alternatifs avec NetworkManager"
echo "5. Testez la résolution après changement de configuration"
echo "6. Diagnostiquez un problème de résolution DNS simulé"
echo ""

echo "COMMANDES ESSENTIELLES A RETENIR :"
echo "=================================="
echo ""
echo "cat /etc/resolv.conf           → Voir serveurs DNS configurés"
echo "nslookup [domaine]             → Test résolution simple"
echo "nslookup [domaine] [dns-ip]    → Test avec serveur spécifique"
echo "dig [domaine]                  → Test résolution détaillé"
echo "dig [domaine] +short           → Résolution rapide"
echo "ping [domaine]                 → Test avec résolution automatique"
echo ""
echo "Configuration NetworkManager :"
echo "nmcli con modify [nom] ipv4.dns '[dns1,dns2]'"
echo "nmcli con up [nom]"
echo ""

echo "CRITERES DE VALIDATION :"
echo "[] Configuration DNS actuelle analysée"
echo "[] Tests de résolution avec nslookup réussis"
echo "[] Tests avec différents serveurs DNS effectués"
echo "[] Utilisation de dig pour tests avancés"
echo "[] Configuration DNS modifiée avec NetworkManager"
echo "[] Diagnostic des problèmes DNS maîtrisé"
echo "[] Scripts de test DNS automatisés compris"
echo ""

echo "SERVEURS DNS RECOMMANDES :"
echo "========================="
echo ""
echo "DNS publics rapides :"
echo "- 8.8.8.8, 8.8.4.4 : Google DNS"
echo "- 1.1.1.1, 1.0.0.1 : Cloudflare DNS"
echo "- 208.67.222.222 : OpenDNS"
echo ""
echo "DNS sécurisés :"
echo "- 9.9.9.9 : Quad9 (bloque malware)"
echo "- 76.76.19.19 : Alternate DNS"
echo ""

echo "POINTS CLES A RETENIR :"
echo "======================"
echo ""
echo "- DNS traduit noms → adresses IP"
echo "- /etc/resolv.conf contient les serveurs DNS"
echo "- nslookup et dig sont les outils de test principaux"
echo "- NetworkManager gère la configuration DNS persistante"
echo "- Toujours tester après changement de configuration"
echo "- Avoir des serveurs DNS de secours (8.8.8.8, 1.1.1.1)"
echo ""

echo "=== FIN DU LAB 4 - DNS ==="
