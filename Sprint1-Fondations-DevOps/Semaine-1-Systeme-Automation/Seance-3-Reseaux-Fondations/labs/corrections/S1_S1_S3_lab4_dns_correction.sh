#!/bin/bash

# =============================================================================
# CORRECTION LAB 4 - Configuration et résolution DNS
# =============================================================================
#
# Cette correction présente la solution complète pour la configuration DNS
# selon le Framework Hassan Section A - Adaptabilité Pédagogique
#
# =============================================================================

echo "=== CORRECTION LAB 4 - Configuration et résolution DNS ==="
echo "Date: $(date)"
echo "Formateur: Correction officielle"
echo ""

# Rappel des objectifs pédagogiques
echo "OBJECTIFS PEDAGOGIQUES RAPPEL :"
echo "==============================="
echo "1. Comprendre le rôle et fonctionnement du DNS"
echo "2. Maîtriser la configuration des serveurs DNS"
echo "3. Utiliser les outils de test DNS (nslookup, dig)"
echo "4. Diagnostiquer et résoudre les problèmes DNS"
echo ""

echo "SOLUTION DETAILLEE ETAPE PAR ETAPE :"
echo "===================================="
echo ""

echo "ETAPE 1 - ANALYSE DE LA CONFIGURATION DNS (SOLUTION) :"
echo "======================================================"
echo ""
echo "1.1. Examen du fichier de configuration DNS :"
echo "Fichier clé : /etc/resolv.conf"
echo "Commande : cat /etc/resolv.conf"
echo ""
echo "Configuration actuelle sur ce système :"
if [ -f /etc/resolv.conf ]; then
    cat /etc/resolv.conf
    echo ""
    echo "Analyse des paramètres :"
    
    # Analyse des serveurs DNS
    DNS_COUNT=$(grep -c "nameserver" /etc/resolv.conf 2>/dev/null)
    echo "Nombre de serveurs DNS configurés : ${DNS_COUNT:-0}"
    
    if [ $DNS_COUNT -gt 0 ]; then
        echo "Serveurs DNS configurés :"
        grep "nameserver" /etc/resolv.conf | while read line; do
            DNS_IP=$(echo $line | awk '{print $2}')
            echo "  - $DNS_IP"
            
            # Classification des serveurs DNS
            case $DNS_IP in
                "8.8.8.8"|"8.8.4.4")
                    echo "    → Google DNS (performant, global)"
                    ;;
                "1.1.1.1"|"1.0.0.1")
                    echo "    → Cloudflare DNS (rapide, privé)"
                    ;;
                "208.67.222.222"|"208.67.220.220")
                    echo "    → OpenDNS (avec filtrage)"
                    ;;
                "9.9.9.9")
                    echo "    → Quad9 (sécurisé, bloque malware)"
                    ;;
                192.168.*|10.*|172.*)
                    echo "    → DNS local/entreprise"
                    ;;
                *)
                    echo "    → DNS personnalisé"
                    ;;
            esac
        done
    else
        echo "ATTENTION : Aucun serveur DNS configuré explicitement"
    fi
else
    echo "PROBLEME : Fichier /etc/resolv.conf non trouvé"
fi
echo ""

echo "1.2. Test de la configuration actuelle :"
echo "Commande : nslookup google.com"
echo ""
if command -v nslookup >/dev/null 2>&1; then
    echo "Résultat du test :"
    nslookup google.com 2>/dev/null || echo "Échec de résolution - problème DNS détecté"
else
    echo "ATTENTION : nslookup non installé"
    echo "Installation requise : sudo apt install dnsutils (Ubuntu/Debian)"
    echo "                      sudo yum install bind-utils (CentOS/RHEL)"
fi
echo ""

echo "ETAPE 2 - TESTS AVEC DIFFERENTS SERVEURS DNS (SOLUTION) :"
echo "========================================================="
echo ""
echo "2.1. Comparaison des serveurs DNS publics :"
echo ""

# Fonction de test de performance DNS
test_dns_performance() {
    local dns_server=$1
    local dns_name=$2
    local domain="google.com"
    
    echo "Test $dns_name ($dns_server) :"
    if command -v nslookup >/dev/null 2>&1; then
        start_time=$(date +%s%N)
        result=$(nslookup $domain $dns_server 2>/dev/null)
        end_time=$(date +%s%N)
        
        if [ $? -eq 0 ]; then
            duration=$(( (end_time - start_time) / 1000000 ))
            echo "  [OK] Résolution réussie en ${duration}ms"
            echo "  Résultat : $(echo "$result" | grep "Address:" | tail -1 | awk '{print $2}')"
        else
            echo "  [ERREUR] Échec de résolution"
        fi
    else
        echo "  [INFO] Test non disponible (nslookup requis)"
    fi
}

# Tests avec différents serveurs DNS
test_dns_performance "8.8.8.8" "Google DNS"
test_dns_performance "1.1.1.1" "Cloudflare DNS"
test_dns_performance "208.67.222.222" "OpenDNS"
echo ""

echo "2.2. Recommandations basées sur les tests :"
echo "Serveurs DNS recommandés par ordre de préférence :"
echo "1. 1.1.1.1 (Cloudflare) - Rapide et respecte la vie privée"
echo "2. 8.8.8.8 (Google) - Très fiable et performant"
echo "3. 9.9.9.9 (Quad9) - Sécurisé avec protection malware"
echo ""

echo "ETAPE 3 - UTILISATION AVANCEE AVEC DIG (SOLUTION) :"
echo "==================================================="
echo ""
if command -v dig >/dev/null 2>&1; then
    echo "3.1. Test simple avec dig :"
    echo "Commande : dig google.com +short"
    dig google.com +short
    echo ""
    
    echo "3.2. Test détaillé :"
    echo "Commande : dig google.com"
    echo "Informations principales :"
    dig google.com | grep -E "(QUESTION|ANSWER|Query time|SERVER)"
    echo ""
    
    echo "3.3. Tests de différents types d'enregistrements :"
    
    echo "Enregistrement A (IPv4) :"
    echo "dig google.com A +short"
    dig google.com A +short
    echo ""
    
    echo "Enregistrement AAAA (IPv6) :"
    echo "dig google.com AAAA +short"
    dig google.com AAAA +short
    echo ""
    
    echo "Enregistrement MX (serveur mail) :"
    echo "dig google.com MX +short"
    dig google.com MX +short
    echo ""
    
    echo "Enregistrement NS (serveurs de noms) :"
    echo "dig google.com NS +short"
    dig google.com NS +short | head -3
    echo ""
else
    echo "dig non installé - installation requise pour tests avancés"
fi

echo "ETAPE 4 - CONFIGURATION DES SERVEURS DNS (SOLUTION) :"
echo "====================================================="
echo ""
echo "4.1. Méthode recommandée - NetworkManager :"
echo ""

# Détection de la connexion active
ACTIVE_CONNECTION=$(nmcli connection show --active | grep -v "NAME" | head -1 | awk '{print $1}')
if [ -n "$ACTIVE_CONNECTION" ]; then
    echo "Connexion active détectée : $ACTIVE_CONNECTION"
    echo ""
    echo "Configuration DNS actuelle de cette connexion :"
    nmcli connection show "$ACTIVE_CONNECTION" | grep ipv4.dns
    echo ""
    
    echo "Commandes pour configurer les DNS (EXEMPLE - NE PAS EXECUTER) :"
    echo "# Configuration de serveurs DNS Cloudflare et Google :"
    echo "sudo nmcli connection modify '$ACTIVE_CONNECTION' ipv4.dns '1.1.1.1,8.8.8.8'"
    echo ""
    echo "# Ignorer les DNS automatiques (DHCP) :"
    echo "sudo nmcli connection modify '$ACTIVE_CONNECTION' ipv4.ignore-auto-dns yes"
    echo ""
    echo "# Appliquer la configuration :"
    echo "sudo nmcli connection up '$ACTIVE_CONNECTION'"
    echo ""
else
    echo "Aucune connexion active détectée"
    echo "Utilisez : nmcli connection show"
    echo "Puis : sudo nmcli connection modify [nom] ipv4.dns '[dns1,dns2]'"
fi

echo "4.2. Méthode alternative - Modification directe (temporaire) :"
echo ""
echo "ATTENTION : Cette méthode est temporaire !"
echo ""
echo "# Sauvegarde :"
echo "sudo cp /etc/resolv.conf /etc/resolv.conf.backup"
echo ""
echo "# Configuration temporaire :"
echo "echo 'nameserver 1.1.1.1' | sudo tee /etc/resolv.conf"
echo "echo 'nameserver 8.8.8.8' | sudo tee -a /etc/resolv.conf"
echo ""
echo "# Restauration :"
echo "sudo cp /etc/resolv.conf.backup /etc/resolv.conf"
echo ""

echo "ETAPE 5 - VALIDATION DE LA CONFIGURATION (SOLUTION) :"
echo "====================================================="
echo ""
echo "5.1. Tests de résolution après configuration :"

# Tests de validation
validate_dns() {
    echo ""
    echo "=== TESTS DE VALIDATION DNS ==="
    
    # Test 1 : Domaines populaires
    echo "Test 1 - Résolution de domaines populaires :"
    for domain in google.com facebook.com github.com wikipedia.org; do
        if nslookup $domain >/dev/null 2>&1; then
            echo "  [OK] $domain résolu"
        else
            echo "  [ERREUR] $domain non résolu"
        fi
    done
    echo ""
    
    # Test 2 : Résolution inverse
    echo "Test 2 - Résolution inverse (IP → nom) :"
    if nslookup 8.8.8.8 >/dev/null 2>&1; then
        reverse_result=$(nslookup 8.8.8.8 2>/dev/null | grep "name =" | awk '{print $4}')
        echo "  [OK] 8.8.8.8 → ${reverse_result:-nom non trouvé}"
    else
        echo "  [ERREUR] Résolution inverse échoué"
    fi
    echo ""
    
    # Test 3 : Performance
    echo "Test 3 - Test de performance :"
    if command -v dig >/dev/null 2>&1; then
        query_time=$(dig google.com | grep "Query time" | awk '{print $4}')
        if [ -n "$query_time" ]; then
            echo "  [INFO] Temps de requête : ${query_time}ms"
            if [ "$query_time" -lt 50 ]; then
                echo "  [OK] Performance excellente (< 50ms)"
            elif [ "$query_time" -lt 200 ]; then
                echo "  [OK] Performance acceptable (< 200ms)"
            else
                echo "  [ATTENTION] Performance lente (> 200ms)"
            fi
        fi
    fi
    echo ""
}

validate_dns

echo "5.2. Test avec ping (résolution automatique) :"
echo "Le ping utilise automatiquement le DNS configuré :"
echo ""
for domain in google.com github.com; do
    echo "ping -c 1 $domain"
    if ping -c 1 -W 2 $domain >/dev/null 2>&1; then
        ip_resolved=$(ping -c 1 $domain 2>/dev/null | head -1 | grep -oE '\([0-9.]+\)' | tr -d '()')
        echo "  [OK] $domain résolu vers $ip_resolved"
    else
        echo "  [ERREUR] $domain non accessible"
    fi
done
echo ""

echo "ETAPE 6 - DIAGNOSTIC DES PROBLEMES DNS (SOLUTION) :"
echo "=================================================="
echo ""

# Fonction de diagnostic complet
diagnostic_dns_complet() {
    echo "=== DIAGNOSTIC DNS AUTOMATISE COMPLET ==="
    ISSUES=0
    
    echo ""
    echo "1. Configuration DNS :"
    if [ -f /etc/resolv.conf ] && grep -q "nameserver" /etc/resolv.conf; then
        dns_count=$(grep -c "nameserver" /etc/resolv.conf)
        echo "   [OK] $dns_count serveur(s) DNS configuré(s)"
    else
        echo "   [ERREUR] Aucun serveur DNS configuré"
        ((ISSUES++))
    fi
    
    echo ""
    echo "2. Connectivité vers serveurs DNS :"
    if [ -f /etc/resolv.conf ]; then
        while read line; do
            if [[ $line == nameserver* ]]; then
                dns_ip=$(echo $line | awk '{print $2}')
                if ping -c 1 -W 2 $dns_ip >/dev/null 2>&1; then
                    echo "   [OK] Serveur $dns_ip accessible"
                else
                    echo "   [ERREUR] Serveur $dns_ip inaccessible"
                    ((ISSUES++))
                fi
            fi
        done < /etc/resolv.conf
    fi
    
    echo ""
    echo "3. Résolution de noms :"
    if nslookup google.com >/dev/null 2>&1; then
        echo "   [OK] Résolution DNS fonctionnelle"
    else
        echo "   [ERREUR] Résolution DNS défaillante"
        ((ISSUES++))
    fi
    
    echo ""
    echo "4. Test avec serveur DNS externe :"
    if nslookup google.com 8.8.8.8 >/dev/null 2>&1; then
        echo "   [OK] DNS externe (8.8.8.8) accessible"
    else
        echo "   [ERREUR] Problème connectivité Internet ou DNS"
        ((ISSUES++))
    fi
    
    echo ""
    echo "5. Performance DNS :"
    if command -v dig >/dev/null 2>&1; then
        query_time=$(dig google.com | grep "Query time" | awk '{print $4}')
        if [ -n "$query_time" ]; then
            echo "   [INFO] Temps de requête : ${query_time}ms"
            if [ "$query_time" -gt 1000 ]; then
                echo "   [ATTENTION] DNS très lent (> 1000ms)"
                ((ISSUES++))
            fi
        fi
    fi
    
    echo ""
    echo "=== RESULTAT DU DIAGNOSTIC ==="
    if [ $ISSUES -eq 0 ]; then
        echo "EXCELLENT : DNS parfaitement configuré et fonctionnel"
    elif [ $ISSUES -le 2 ]; then
        echo "ACCEPTABLE : DNS fonctionne avec $ISSUES problème(s) mineur(s)"
    else
        echo "PROBLEMATIQUE : $ISSUES problèmes détectés - intervention requise"
    fi
    
    echo ""
    echo "=== SOLUTIONS AUX PROBLEMES DETECTES ==="
    if [ $ISSUES -gt 0 ]; then
        echo ""
        echo "Problème : Serveur DNS inaccessible"
        echo "Solution : Changer de serveurs DNS"
        echo "Commande : sudo nmcli connection modify [connexion] ipv4.dns '1.1.1.1,8.8.8.8'"
        echo ""
        echo "Problème : Résolution lente"
        echo "Solution : Utiliser des DNS plus rapides (Cloudflare 1.1.1.1)"
        echo ""
        echo "Problème : Configuration DNS vide"
        echo "Solution : Configurer manuellement les DNS ou vérifier DHCP"
        echo ""
    fi
}

diagnostic_dns_complet

echo ""
echo "SCENARIOS DE DEPANNAGE COURANTS :"
echo "================================"
echo ""
echo "Scénario 1 : 'Name or service not known'"
echo "Cause : Serveurs DNS mal configurés ou inaccessibles"
echo "Solution :"
echo "  1. Vérifier /etc/resolv.conf"
echo "  2. Tester connectivité : ping 8.8.8.8"
echo "  3. Reconfigurer DNS : nmcli connection modify [nom] ipv4.dns '8.8.8.8'"
echo ""

echo "Scénario 2 : DNS très lent"
echo "Cause : Serveur DNS surchargé ou éloigné"
echo "Solution :"
echo "  1. Tester performance : dig google.com"
echo "  2. Changer pour DNS rapides : 1.1.1.1, 8.8.8.8"
echo "  3. Vider le cache DNS : sudo systemctl restart systemd-resolved"
echo ""

echo "Scénario 3 : Certains sites inaccessibles"
echo "Cause : DNS avec filtrage ou censure"
echo "Solution :"
echo "  1. Tester avec DNS neutre : nslookup site.com 1.1.1.1"
echo "  2. Configurer DNS libre : 1.1.1.1 (Cloudflare)"
echo "  3. Vérifier configuration entreprise/FAI"
echo ""

echo "COMPETENCES VALIDEES PAR CE LAB :"
echo "================================="
echo ""
echo "✓ Compréhension du rôle du DNS dans les réseaux"
echo "✓ Analyse de la configuration DNS existante"
echo "✓ Utilisation des outils nslookup et dig"
echo "✓ Configuration persistante avec NetworkManager"
echo "✓ Tests de validation et performance"
echo "✓ Diagnostic systématique des problèmes DNS"
echo "✓ Résolution des incidents DNS courants"
echo ""

echo "CONFIGURATION DNS RECOMMANDEE POUR PRODUCTION :"
echo "=============================================="
echo ""
echo "Serveurs DNS primaires :"
echo "- 1.1.1.1 (Cloudflare - rapide, privé)"
echo "- 8.8.8.8 (Google - fiable, global)"
echo ""
echo "Serveurs DNS sécurisés :"
echo "- 9.9.9.9 (Quad9 - bloque malware)"
echo "- 208.67.222.222 (OpenDNS - filtrage)"
echo ""
echo "Configuration NetworkManager type :"
echo "sudo nmcli con modify [connexion] ipv4.dns '1.1.1.1,8.8.8.8'"
echo "sudo nmcli con modify [connexion] ipv4.ignore-auto-dns yes"
echo "sudo nmcli con up [connexion]"
echo ""

echo "OUTILS ET COMMANDES ESSENTIELS :"
echo "==============================="
echo ""
echo "Configuration :"
echo "cat /etc/resolv.conf                     → Voir DNS configurés"
echo "nmcli con show [nom] | grep dns          → Voir DNS de la connexion"
echo ""
echo "Tests :"
echo "nslookup [domaine]                       → Test résolution simple"
echo "nslookup [domaine] [dns-ip]              → Test avec DNS spécifique"
echo "dig [domaine]                            → Test résolution détaillé"
echo "dig [domaine] +short                     → Résolution rapide"
echo "dig [domaine] A/AAAA/MX/NS               → Tests par type"
echo ""
echo "Configuration :"
echo "sudo nmcli con modify [nom] ipv4.dns '[dns1,dns2]'  → Configurer DNS"
echo "sudo nmcli con modify [nom] ipv4.ignore-auto-dns yes → Ignorer DHCP DNS"
echo "sudo nmcli con up [nom]                             → Appliquer config"
echo ""

echo "POINTS CLES DE LA CORRECTION :"
echo "============================="
echo ""
echo "1. COMPREHENSION DNS :"
echo "   - DNS = traduction nom ↔ IP"
echo "   - /etc/resolv.conf = configuration système"
echo "   - NetworkManager = gestion persistante"
echo ""
echo "2. OUTILS DIAGNOSTIC :"
echo "   - nslookup = test simple et rapide"
echo "   - dig = test détaillé et professionnel"
echo "   - ping = test avec résolution automatique"
echo ""
echo "3. BONNES PRATIQUES :"
echo "   - Configurer plusieurs serveurs DNS"
echo "   - Utiliser des DNS rapides et fiables"
echo "   - Tester après chaque modification"
echo "   - Avoir une procédure de rollback"
echo ""
echo "4. DEPANNAGE SYSTEMATIQUE :"
echo "   - Vérifier configuration locale"
echo "   - Tester connectivité serveurs DNS"
echo "   - Comparer avec DNS externes"
echo "   - Analyser les performances"
echo ""

echo "=== FIN DE LA CORRECTION LAB 4 - DNS ==="
