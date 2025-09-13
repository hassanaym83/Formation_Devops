#!/bin/bash

# =============================================================================
# CORRECTION LAB 2 - Configuration de base du réseau
# =============================================================================

echo "=== CORRECTION LAB 2 - Configuration de base du réseau ==="
echo ""

# =============================================================================
# ANALYSE AUTOMATIQUE DU SYSTÈME
# =============================================================================

echo " ANALYSE AUTOMATIQUE DE VOTRE CONFIGURATION :"
echo "==============================================="
echo ""

echo "1. INTERFACES RÉSEAU DÉTECTÉES :"
echo "--------------------------------"
interfaces=$(ip link show | grep -E "^[0-9]+" | awk -F: '{print $2}' | sed 's/^ *//')
interface_count=0
for interface in $interfaces; do
 if [ "$interface" != "lo" ]; then
 interface_count=$((interface_count + 1))
 state=$(ip link show $interface | grep -o "state [A-Z]*" | cut -d' ' -f2)
 echo "✓ Interface $interface_count : $interface (État: $state)"
 
 # Vérifier si elle a une IP
 ip_info=$(ip addr show $interface | grep "inet " | head -1)
 if [ -n "$ip_info" ]; then
 ip_addr=$(echo $ip_info | awk '{print $2}')
 echo " └─ Adresse IP : $ip_addr"
 else
 echo " └─ Pas d'adresse IP assignée"
 fi
 fi
done
echo " └─ Interface de boucle : lo (localhost - 127.0.0.1)"
echo ""
echo " RÉSUMÉ : $interface_count interface(s) réseau physique(s) détectée(s)"
echo ""

echo "2. CONFIGURATION IP PRINCIPALE :"
echo "--------------------------------"
# Trouver l'IP principale (pas 127.x.x.x)
main_ip=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K[\d.]+' | head -1)
main_interface=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'dev \K\w+' | head -1)

if [ -n "$main_ip" ] && [ -n "$main_interface" ]; then
 echo "✓ IP principale : $main_ip"
 echo "✓ Interface principale : $main_interface"
 
 # Déterminer le réseau
 network=$(ip route show | grep "$main_interface" | grep -E "/[0-9]+" | head -1 | awk '{print $1}')
 echo "✓ Réseau local : $network"
else
 echo " Impossible de détecter l'IP principale automatiquement"
fi
echo ""

echo "3. PASSERELLE ET ROUTAGE :"
echo "-------------------------"
gateway=$(ip route show default | awk '{print $3}' | head -1)
gateway_interface=$(ip route show default | awk '{print $5}' | head -1)

if [ -n "$gateway" ]; then
 echo "✓ Passerelle par défaut : $gateway"
 echo "✓ Interface de sortie : $gateway_interface"
 
 # Test de connectivité passerelle
 echo ""
 echo "Test de connectivité vers la passerelle :"
 if ping -c 1 -W 2 $gateway >/dev/null 2>&1; then
 echo " Passerelle accessible (ping réussi)"
 else
 echo " Passerelle non accessible (ping échoué)"
 fi
else
 echo " Aucune passerelle par défaut configurée"
fi
echo ""

# =============================================================================
# TESTS DE CONNECTIVITÉ AUTOMATISÉS
# =============================================================================

echo "TESTS DE CONNECTIVITÉ AUTOMATISÉS :"
echo "======================================"
echo ""

echo "Test 1 - Interface de boucle locale :"
echo "-------------------------------------"
if ping -c 1 -W 1 127.0.0.1 >/dev/null 2>&1; then
 echo " Interface lo fonctionnelle (127.0.0.1 accessible)"
else
 echo " Problème avec l'interface de boucle"
fi
echo ""

echo "Test 2 - Réseau local :"
echo "-----------------------"
if [ -n "$gateway" ]; then
 if ping -c 1 -W 3 $gateway >/dev/null 2>&1; then
 echo " Réseau local fonctionnel (passerelle $gateway accessible)"
 else
 echo " Problème de connectivité réseau local"
 fi
else
 echo " Impossible de tester sans passerelle configurée"
fi
echo ""

echo "Test 3 - Connectivité Internet :"
echo "--------------------------------"
if ping -c 1 -W 5 8.8.8.8 >/dev/null 2>&1; then
 echo " Accès Internet fonctionnel (8.8.8.8 accessible)"
else
 echo " Pas d'accès Internet ou problème DNS"
fi
echo ""

echo "Test 4 - Résolution DNS :"
echo "-------------------------"
if nslookup google.com >/dev/null 2>&1 || host google.com >/dev/null 2>&1; then
 echo " Résolution DNS fonctionnelle"
else
 echo " Problème de résolution DNS"
fi
echo ""

# =============================================================================
# ANALYSE DE LA CONFIGURATION DNS
# =============================================================================

echo " CONFIGURATION DNS :"
echo "======================"
echo ""
if [ -f /etc/resolv.conf ]; then
 dns_servers=$(grep "^nameserver" /etc/resolv.conf | awk '{print $2}')
 if [ -n "$dns_servers" ]; then
 echo "Serveurs DNS configurés :"
 echo "$dns_servers" | while read server; do
 echo " • $server"
 done
 else
 echo " Aucun serveur DNS configuré dans /etc/resolv.conf"
 fi
 
 # Vérifier le domaine de recherche
 search_domain=$(grep "^search\|^domain" /etc/resolv.conf | head -1 | cut -d' ' -f2-)
 if [ -n "$search_domain" ]; then
 echo "Domaine de recherche : $search_domain"
 fi
else
 echo " Fichier /etc/resolv.conf non trouvé"
fi
echo ""

# =============================================================================
# ANALYSE DES SERVICES RÉSEAU
# =============================================================================

echo " SERVICES RÉSEAU ACTIFS :"
echo "==========================="
echo ""
echo "Services en écoute sur votre machine :"

# Vérifier les services courants
services_found=0

# SSH
if ss -tuln | grep -q ":22 "; then
 echo "✓ SSH (port 22) - Connexion à distance activée"
 services_found=$((services_found + 1))
fi

# Web servers
if ss -tuln | grep -q ":80 "; then
 echo "✓ HTTP (port 80) - Serveur web détecté"
 services_found=$((services_found + 1))
fi

if ss -tuln | grep -q ":443 "; then
 echo "✓ HTTPS (port 443) - Serveur web sécurisé détecté"
 services_found=$((services_found + 1))
fi

# DNS
if ss -tuln | grep -q ":53 "; then
 echo "✓ DNS (port 53) - Serveur DNS local détecté"
 services_found=$((services_found + 1))
fi

# DHCP client
if ss -tuln | grep -q ":68 "; then
 echo "✓ DHCP Client (port 68) - Configuration automatique IP"
 services_found=$((services_found + 1))
fi

if [ $services_found -eq 0 ]; then
 echo " Aucun service réseau standard détecté en écoute"
else
 echo ""
 echo " Total : $services_found service(s) réseau actif(s)"
fi
echo ""

# =============================================================================
# RÉPONSES AU QUIZ
# =============================================================================

echo " RÉPONSES AU QUIZ :"
echo "===================="
echo ""

echo "Question 1 : Quelle est l'adresse IP de votre machine ?"
if [ -n "$main_ip" ]; then
 echo " Réponse : $main_ip"
else
 echo "À déterminer avec 'ip addr show' (cherchez 'inet' hors 127.x.x.x)"
fi
echo ""

echo "Question 2 : Quelle est l'adresse de votre passerelle ?"
if [ -n "$gateway" ]; then
 echo " Réponse : $gateway"
else
 echo "À déterminer avec 'ip route show | grep default'"
fi
echo ""

echo "Question 3 : Combien d'interfaces réseau votre machine a-t-elle ?"
echo " Réponse : $interface_count interface(s) réseau physique(s)"
echo ""

echo "Question 4 : Votre machine peut-elle accéder à Internet ?"
if ping -c 1 -W 5 8.8.8.8 >/dev/null 2>&1; then
 echo " Réponse : Oui, accès Internet fonctionnel"
else
 echo " Réponse : Non, pas d'accès Internet détecté"
fi
echo ""

echo "Question 5 : Quel est le nom de votre machine sur le réseau ?"
hostname_result=$(hostname)
echo " Réponse : $hostname_result"
echo ""

# =============================================================================
# COMMANDES DE DIAGNOSTIC UTILES
# =============================================================================

echo " COMMANDES DE DIAGNOSTIC RÉCAPITULATIVES :"
echo "============================================"
echo ""
echo "Pour reproduire cette analyse, utilisez :"
echo ""
echo "1. Voir toutes les interfaces :"
echo " ip link show"
echo ""
echo "2. Voir les adresses IP :"
echo " ip addr show"
echo ""
echo "3. Voir la table de routage :"
echo " ip route show"
echo ""
echo "4. Identifier la passerelle :"
echo " ip route show | grep default"
echo ""
echo "5. Tester la connectivité :"
echo " ping -c 3 127.0.0.1 # Test local"
echo " ping -c 3 [PASSERELLE] # Test réseau local"
echo " ping -c 3 8.8.8.8 # Test Internet"
echo ""
echo "6. Voir la configuration DNS :"
echo " cat /etc/resolv.conf"
echo ""
echo "7. Voir les services en écoute :"
echo " ss -tuln | head -10"
echo ""
echo "8. Voir le nom de la machine :"
echo " hostname"
echo ""

# =============================================================================
# DIAGNOSTIC ET DÉPANNAGE
# =============================================================================

echo "GUIDE DE DIAGNOSTIC RÉSEAU :"
echo "==============================="
echo ""
echo "PROBLÈME : Pas d'IP assignée"
echo "DIAGNOSTIC : ip addr show → aucune ligne 'inet' sur l'interface"
echo "SOLUTION : Vérifier la connexion physique et DHCP"
echo ""
echo "PROBLÈME : Pas de passerelle"
echo "DIAGNOSTIC : ip route show → pas de ligne 'default'" 
echo "SOLUTION : Configuration manuelle ou redémarrage du service réseau"
echo ""
echo "PROBLÈME : Pas d'Internet"
echo "DIAGNOSTIC : ping 8.8.8.8 échoue mais ping passerelle fonctionne"
echo "SOLUTION : Problème de routage au niveau de l'opérateur/FAI"
echo ""
echo "PROBLÈME : Résolution DNS"
echo "DIAGNOSTIC : ping 8.8.8.8 fonctionne mais pas 'ping google.com'"
echo "SOLUTION : Vérifier /etc/resolv.conf et les serveurs DNS"
echo ""

# =============================================================================
# VALIDATION FINALE
# =============================================================================

echo " VALIDATION FINALE :"
echo "====================="
echo ""

# Calcul du score
score=0
total=5

# Test 1 : Interface détectée
if [ $interface_count -gt 0 ]; then
 echo " Test 1 : Interfaces réseau détectées"
 score=$((score + 1))
else
 echo " Test 1 : Aucune interface réseau détectée"
fi

# Test 2 : IP assignée
if [ -n "$main_ip" ]; then
 echo " Test 2 : Adresse IP assignée"
 score=$((score + 1))
else
 echo " Test 2 : Aucune adresse IP détectée"
fi

# Test 3 : Passerelle configurée
if [ -n "$gateway" ]; then
 echo " Test 3 : Passerelle configurée"
 score=$((score + 1))
else
 echo " Test 3 : Aucune passerelle configurée"
fi

# Test 4 : Connectivité locale
if [ -n "$gateway" ] && ping -c 1 -W 2 $gateway >/dev/null 2>&1; then
 echo " Test 4 : Connectivité réseau local"
 score=$((score + 1))
else
 echo " Test 4 : Pas de connectivité réseau local"
fi

# Test 5 : Connectivité Internet
if ping -c 1 -W 5 8.8.8.8 >/dev/null 2>&1; then
 echo " Test 5 : Connectivité Internet"
 score=$((score + 1))
else
 echo " Test 5 : Pas de connectivité Internet"
fi

echo ""
echo " SCORE FINAL : $score/$total"

if [ $score -eq $total ]; then
 echo " PARFAIT ! Configuration réseau complète et fonctionnelle"
elif [ $score -ge 3 ]; then
 echo "BIEN ! Configuration de base fonctionnelle"
else
 echo " ATTENTION ! Configuration réseau incomplète ou dysfonctionnelle"
fi

echo ""
echo " PROCHAINE ÉTAPE :"
echo "Vous êtes prêt pour le LAB 3 - Diagnostic avancé de la connectivité"
echo ""

echo "=== FIN DE LA CORRECTION LAB 2 ==="
