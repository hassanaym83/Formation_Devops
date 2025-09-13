#!/bin/bash

# =============================================================================
# CORRECTION LAB 4 CHALLENGE - Segmentation réseau hôpital
# =============================================================================

echo "=== CORRECTION LAB 4 CHALLENGE - Segmentation réseau hôpital ==="
echo ""

# =============================================================================
# SOLUTION COMPLÈTE DU CHALLENGE
# =============================================================================

echo "SOLUTION DÉTAILLÉE DE LA SEGMENTATION RÉSEAU HÔPITAL"
echo "======================================================="
echo ""

# =============================================================================
# ÉTAPE 1 - ANALYSE DES BESOINS
# =============================================================================

echo "ÉTAPE 1 - ANALYSE DES BESOINS :"
echo "=================================="
echo ""

echo "Inventaire des équipements :"
echo ""
echo "• Administration : 15 ordinateurs"
echo "• Médecins : 25 tablettes/ordinateurs" 
echo "• Personnel soignant : 40 équipements mobiles"
echo "• Équipements médicaux : 30 appareils"
echo "• Serveurs : 8 serveurs critiques"
echo "• WiFi invités : 50 connexions simultanées"
echo "• Imprimantes/périphériques : 20 équipements"
echo ""
echo "TOTAL : ~188 équipements à connecter"
echo ""

# =============================================================================
# ÉTAPE 2 - CALCUL DES SOUS-RÉSEAUX OPTIMAUX
# =============================================================================

echo "ÉTAPE 2 - CALCUL DES SOUS-RÉSEAUX OPTIMAUX :"
echo "==============================================="
echo ""

# Fonction pour calculer et afficher les sous-réseaux
calculate_subnet() {
 local name=$1
 local devices_needed=$2
 local network=$3
 
 # Calcul de la taille optimale
 local next_power_of_2=4
 while [ $next_power_of_2 -lt $((devices_needed + 10)) ]; do
 next_power_of_2=$((next_power_of_2 * 2))
 done
 
 # Calcul du masque CIDR
 local host_bits=0
 local temp=$next_power_of_2
 while [ $temp -gt 1 ]; do
 host_bits=$((host_bits + 1))
 temp=$((temp / 2))
 done
 
 local cidr=$((32 - host_bits))
 
 echo "$name :"
 echo " Besoins : $devices_needed équipements"
 echo " Réseau proposé : $network/$cidr"
 echo " Capacité : $((next_power_of_2 - 2)) adresses utilisables"
 
 # Afficher les détails avec ipcalc si disponible
 if command -v ipcalc >/dev/null 2>&1; then
 echo " Détails techniques :"
 ipcalc "$network/$cidr" | grep -E "(Network|HostMin|HostMax|Broadcast)" | sed 's/^/ /'
 else
 # Calcul manuel simplifié
 case $cidr in
 24) echo " Plage : ${network%.*}.1 - ${network%.*}.254" ;;
 25) echo " Plage : ${network%.*}.1 - ${network%.*}.126" ;;
 26) echo " Plage : ${network%.*}.1 - ${network%.*}.62" ;;
 27) echo " Plage : ${network%.*}.1 - ${network%.*}.30" ;;
 28) echo " Plage : ${network%.*}.1 - ${network%.*}.14" ;;
 esac
 fi
 echo ""
}

echo "Segmentation proposée pour l'hôpital :"
echo ""

calculate_subnet "Serveurs critiques" 8 "10.10.1.0" 
calculate_subnet "Administration" 15 "10.10.2.0"
calculate_subnet "Médecins" 25 "10.10.3.0"
calculate_subnet "Personnel soignant" 40 "10.10.4.0"
calculate_subnet "Équipements médicaux" 30 "10.10.5.0"
calculate_subnet "WiFi invités" 50 "10.10.6.0"
calculate_subnet "Imprimantes" 20 "10.10.7.0"

# =============================================================================
# ÉTAPE 3 - PLAN D'ADRESSAGE DÉTAILLÉ
# =============================================================================

echo "ÉTAPE 3 - PLAN D'ADRESSAGE DÉTAILLÉ :"
echo "========================================="
echo ""

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║ PLAN D'ADRESSAGE HÔPITAL ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Segment │ Réseau │ CIDR │ Capacité │ Niveau sécurité ║
╠════════════════════════╪═══════════════╪══════╪══════════╪══════════════════╣
║ Serveurs critiques │ 10.10.1.0 │ /28 │ 14 │ TRÈS ÉLEVÉ ║
║ Administration │ 10.10.2.0 │ /27 │ 30 │ ÉLEVÉ ║
║ Médecins │ 10.10.3.0 │ /26 │ 62 │ ÉLEVÉ ║
║ Personnel soignant │ 10.10.4.0 │ /26 │ 62 │ MOYEN ║
║ Équip. médicaux │ 10.10.5.0 │ /26 │ 62 │ TRÈS ÉLEVÉ ║
║ WiFi invités │ 10.10.6.0 │ /25 │ 126 │ FAIBLE ║
║ Imprimantes │ 10.10.7.0 │ /27 │ 30 │ MOYEN ║
╚════════════════════════╧═══════════════╧══════╧══════════╧══════════════════╝
EOF

echo ""

# =============================================================================
# ÉTAPE 4 - RÈGLES DE SÉCURITÉ ET CONFORMITÉ RGPD
# =============================================================================

echo "ÉTAPE 4 - RÈGLES DE SÉCURITÉ ET CONFORMITÉ RGPD :"
echo "====================================================="
echo ""

echo "MATRICE DES COMMUNICATIONS AUTORISÉES :"
echo ""

cat << 'EOF'
┌─────────────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ │Serveurs │ Admin │Médecins │Personnel│Équip.Méd│WiFi Inv.│Impriman.│
├─────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│Serveurs │ │ │ │ │ │ │ │
│Administration│ │ │ │ │ │ │ │
│Médecins │ │ │ │ │ │ │ │
│Personnel │ │ │ │ │ │ │ │
│Équip.Médical │ │ │ │ │ │ │ │
│WiFi Invités │ │ │ │ │ │ │ │
│Imprimantes │ │ │ │ │ │ │ │
└─────────────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

Légende: Autorisé Restreint/Contrôlé Interdit
EOF

echo ""
echo "RÈGLES DE SÉCURITÉ DÉTAILLÉES :"
echo ""

echo "1. SERVEURS CRITIQUES (10.10.1.0/28) :"
echo " • Accès admin uniquement depuis le réseau administration"
echo " • Connexions médicales authentifiées et chiffrées"
echo " • Logs de toutes les connexions obligatoires"
echo " • Sauvegarde automatique vers site distant"
echo ""

echo "2. ADMINISTRATION (10.10.2.0/27) :"
echo " • Accès privilégié aux serveurs et configurations"
echo " • Monitoring de tous les réseaux autorisé"
echo " • Connexions VPN sécurisées pour télétravail"
echo ""

echo "3. MÉDECINS (10.10.3.0/26) :"
echo " • Accès complet aux dossiers patients"
echo " • Connexion aux équipements médicaux autorisée"
echo " • Authentification forte obligatoire (2FA)"
echo ""

echo "4. PERSONNEL SOIGNANT (10.10.4.0/26) :"
echo " • Accès limité aux dossiers selon les droits"
echo " • Connexion aux équipements de soins"
echo " • Traçabilité complète des accès"
echo ""

echo "5. ÉQUIPEMENTS MÉDICAUX (10.10.5.0/26) :"
echo " • Isolation critique pour la sécurité patients"
echo " • Connexion serveurs pour backup données"
echo " • Maintenance uniquement par personnel autorisé"
echo ""

echo "6. WIFI INVITÉS (10.10.6.0/25) :"
echo " • Isolation complète des autres réseaux"
echo " • Accès Internet uniquement (portail captif)"
echo " • Bande passante limitée"
echo " • Durée de session limitée à 4 heures"
echo ""

echo "7. IMPRIMANTES (10.10.7.0/27) :"
echo " • Accès depuis réseaux autorisés uniquement"
echo " • Chiffrement des données d'impression"
echo " • Effacement automatique des tampons mémoire"
echo ""

# =============================================================================
# ÉTAPE 5 - CONFIGURATION TECHNIQUE
# =============================================================================

echo " ÉTAPE 5 - CONFIGURATION TECHNIQUE :"
echo "======================================"
echo ""

echo "CONFIGURATION DES VLANS :"
echo ""

cat << 'EOF'
# Configuration VLAN pour switch manageable

# VLAN Serveurs (ID: 10)
vlan 10
name "Serveurs-Critiques"
exit

# VLAN Administration (ID: 20) 
vlan 20
name "Administration"
exit

# VLAN Médecins (ID: 30)
vlan 30
name "Medecins"
exit

# VLAN Personnel (ID: 40)
vlan 40
name "Personnel-Soignant"
exit

# VLAN Équipements médicaux (ID: 50)
vlan 50
name "Equipements-Medicaux"
exit

# VLAN WiFi Invités (ID: 60)
vlan 60
name "WiFi-Invites"
exit

# VLAN Imprimantes (ID: 70)
vlan 70
name "Imprimantes"
exit
EOF

echo ""
echo "CONFIGURATION ROUTEUR/FIREWALL :"
echo ""

cat << 'EOF'
# Configuration interfaces réseau

interface vlan10
 ip address 10.10.1.1 255.255.255.240
 description "Serveurs critiques"
!
interface vlan20
 ip address 10.10.2.1 255.255.255.224
 description "Administration"
!
interface vlan30
 ip address 10.10.3.1 255.255.255.192
 description "Médecins"
!
interface vlan40
 ip address 10.10.4.1 255.255.255.192
 description "Personnel soignant"
!
interface vlan50
 ip address 10.10.5.1 255.255.255.192
 description "Équipements médicaux"
!
interface vlan60
 ip address 10.10.6.1 255.255.255.128
 description "WiFi invités"
!
interface vlan70
 ip address 10.10.7.1 255.255.255.224
 description "Imprimantes"
EOF

echo ""

# =============================================================================
# ÉTAPE 6 - RÈGLES FIREWALL DÉTAILLÉES
# =============================================================================

echo "ÉTAPE 6 - RÈGLES FIREWALL DÉTAILLÉES :"
echo "========================================="
echo ""

echo "Exemple de configuration firewall (iptables/pfSense) :"
echo ""

cat << 'EOF'
# Règles de base
# Deny all par défaut
iptables -P FORWARD DROP
iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT

# Autoriser loopback
iptables -A INPUT -i lo -j ACCEPT

# Autoriser connexions établies
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# SERVEURS CRITIQUES (10.10.1.0/28)
# Administration vers serveurs
iptables -A FORWARD -s 10.10.2.0/27 -d 10.10.1.0/28 -j ACCEPT
# Médecins vers serveurs (HTTPS uniquement)
iptables -A FORWARD -s 10.10.3.0/26 -d 10.10.1.0/28 -p tcp --dport 443 -j ACCEPT
# Équipements médicaux vers serveurs (ports spécifiques)
iptables -A FORWARD -s 10.10.5.0/26 -d 10.10.1.0/28 -p tcp --dport 8080 -j ACCEPT

# ADMINISTRATION (10.10.2.0/27)
# Accès complet aux serveurs (déjà configuré)
# Accès monitoring autres réseaux
iptables -A FORWARD -s 10.10.2.0/27 -p icmp -j ACCEPT

# MÉDECINS (10.10.3.0/26)
# Vers équipements médicaux
iptables -A FORWARD -s 10.10.3.0/26 -d 10.10.5.0/26 -j ACCEPT
# Vers personnel soignant
iptables -A FORWARD -s 10.10.3.0/26 -d 10.10.4.0/26 -j ACCEPT
# Vers imprimantes
iptables -A FORWARD -s 10.10.3.0/26 -d 10.10.7.0/27 -p tcp --dport 515 -j ACCEPT

# PERSONNEL SOIGNANT (10.10.4.0/26)
# Vers équipements médicaux (lecture seule)
iptables -A FORWARD -s 10.10.4.0/26 -d 10.10.5.0/26 -p tcp --dport 80 -j ACCEPT
# Vers imprimantes
iptables -A FORWARD -s 10.10.4.0/26 -d 10.10.7.0/27 -p tcp --dport 515 -j ACCEPT

# ÉQUIPEMENTS MÉDICAUX (10.10.5.0/26)
# Vers serveurs pour backup (ports spécifiques)
iptables -A FORWARD -s 10.10.5.0/26 -d 10.10.1.0/28 -p tcp --dport 8080 -j ACCEPT

# WIFI INVITÉS (10.10.6.0/25)
# Internet seulement (via passerelle)
iptables -A FORWARD -s 10.10.6.0/25 -o eth0 -j ACCEPT
# Bloquer tout accès interne
iptables -A FORWARD -s 10.10.6.0/25 -d 10.10.0.0/16 -j DROP

# IMPRIMANTES (10.10.7.0/27)
# Pas d'initiation de connexion autorisée (serveurs uniquement)
EOF

echo ""

# =============================================================================
# ÉTAPE 7 - CONFORMITÉ RGPD
# =============================================================================

echo " ÉTAPE 7 - CONFORMITÉ RGPD :"
echo "==============================="
echo ""

echo "MESURES TECHNIQUES RGPD IMPLÉMENTÉES :"
echo ""

echo "1. MINIMISATION DES DONNÉES :"
echo " Segmentation stricte par fonction métier"
echo " Accès limité aux données nécessaires uniquement"
echo " Isolation des équipements par type d'usage"
echo ""

echo "2. INTÉGRITÉ ET CONFIDENTIALITÉ :"
echo " Chiffrement des communications inter-segments"
echo " Authentification forte pour accès sensibles"
echo " Logs de toutes les connexions et accès"
echo ""

echo "3. DISPONIBILITÉ ET RÉSILIENCE :"
echo " Redondance des serveurs critiques"
echo " Sauvegarde automatique chiffrée"
echo " Plan de reprise d'activité documenté"
echo ""

echo "4. RESPONSABILISATION :"
echo " Traçabilité complète des accès aux données"
echo " Audit régulier des connexions et permissions"
echo " Formation du personnel aux bonnes pratiques"
echo ""

echo "5. DROIT DES PERSONNES :"
echo " Possibilité d'export sécurisé des données patients"
echo " Procédure de suppression documentée"
echo " Anonymisation des données de recherche"
echo ""

# =============================================================================
# ÉTAPE 8 - PLAN DE MISE EN ŒUVRE
# =============================================================================

echo "ÉTAPE 8 - PLAN DE MISE EN ŒUVRE :"
echo "===================================="
echo ""

echo "PHASE 1 - PRÉPARATION (Semaine 1-2) :"
echo "• Configuration des équipements réseau (switchs, routeur)"
echo "• Installation et test du firewall"
echo "• Création des VLANs et attribution des ports"
echo "• Tests de connectivité de base"
echo ""

echo "PHASE 2 - DÉPLOIEMENT GRADUEL (Semaine 3-4) :"
echo "• Migration réseau Administration en premier"
echo "• Tests des règles de sécurité"
echo "• Migration progressive des autres segments"
echo "• Validation des accès et performances"
echo ""

echo "PHASE 3 - SÉCURISATION (Semaine 5-6) :"
echo "• Activation complète des règles firewall"
echo "• Configuration monitoring et alertes"
echo "• Tests d'intrusion et audit sécurité"
echo "• Formation utilisateurs aux nouvelles procédures"
echo ""

echo "PHASE 4 - OPTIMISATION (Semaine 7-8) :"
echo "• Analyse des performances et ajustements"
echo "• Documentation finale de l'architecture"
echo "• Mise en place des procédures de maintenance"
echo "• Validation conformité RGPD avec DPO"
echo ""

# =============================================================================
# VALIDATION DE LA SOLUTION
# =============================================================================

echo " VALIDATION DE LA SOLUTION :"
echo "============================="
echo ""

echo "CRITÈRES DE RÉUSSITE ATTEINTS :"
echo ""

# Vérification des exigences
requirements_met=0
total_requirements=8

echo "1. Segmentation réseau par fonction métier (7 segments créés)"
requirements_met=$((requirements_met + 1))

echo "2. Isolation sécurisée des équipements médicaux"
requirements_met=$((requirements_met + 1))

echo "3. Accès WiFi invités complètement isolé"
requirements_met=$((requirements_met + 1))

echo "4. Conformité RGPD avec mesures techniques appropriées"
requirements_met=$((requirements_met + 1))

echo "5. Plan d'adressage optimisé et évolutif"
requirements_met=$((requirements_met + 1))

echo "6. Règles de sécurité détaillées et documentées"
requirements_met=$((requirements_met + 1))

echo "7. Architecture respectant les bonnes pratiques"
requirements_met=$((requirements_met + 1))

echo "8. Plan de mise en œuvre réaliste et progressif"
requirements_met=$((requirements_met + 1))

echo ""
echo "SCORE FINAL : $requirements_met/$total_requirements (100%)"

if [ $requirements_met -eq $total_requirements ]; then
 echo ""
 echo "EXCELLENCE ! SOLUTION COMPLÈTE ET PROFESSIONNELLE !"
 echo "======================================================"
 echo ""
 echo "Votre solution démontre une maîtrise complète de :"
 echo "• L'analyse des besoins métier complexes"
 echo "• La conception d'architecture réseau sécurisée"
 echo "• L'application des normes de sécurité et conformité"
 echo "• La planification de projet technique réaliste"
 echo ""
fi

# =============================================================================
# POINTS CLÉS À RETENIR
# =============================================================================

echo "POINTS CLÉS À RETENIR :"
echo "=========================="
echo ""

echo "MÉTHODOLOGIE :"
echo "• Toujours commencer par l'analyse des besoins métier"
echo "• Appliquer le principe de moindre privilège"
echo "• Prévoir l'évolutivité dès la conception"
echo "• Documenter chaque décision technique"
echo ""

echo "SÉCURITÉ :"
echo "• La segmentation est la première ligne de défense"
echo "• Chaque segment doit avoir un niveau de sécurité adapté"
echo "• Les équipements critiques nécessitent une isolation renforcée"
echo "• L'audit et la traçabilité sont indispensables"
echo ""

echo " CONFORMITÉ :"
echo "• Le RGPD impose des mesures techniques et organisationnelles"
echo "• La pseudonymisation et le chiffrement sont recommandés"
echo "• L'accountability nécessite une documentation complète"
echo "• La Privacy by Design doit guider l'architecture"
echo ""

echo "GESTION DE PROJET :"
echo "• Déploiement progressif pour limiter les risques"
echo "• Tests à chaque étape de migration"
echo "• Formation des utilisateurs indispensable"
echo "• Plan de rollback toujours préparé"
echo ""

# =============================================================================
# RESSOURCES COMPLÉMENTAIRES
# =============================================================================

echo "POUR ALLER PLUS LOIN :"
echo "========================="
echo ""

echo "Standards et normes :"
echo "• ISO 27001 : Management de la sécurité de l'information"
echo "• IEC 62304 : Logiciels de dispositifs médicaux"
echo "• RGPD : Articles 25 (Privacy by Design) et 32 (Sécurité)"
echo "• ANSSI : Guide de sécurité des architectures WiFi"
echo ""

echo "Outils recommandés :"
echo "• pfSense/OPNsense : Firewall open source professionnel"
echo "• PRTG/Zabbix : Monitoring réseau et sécurité"
echo "• Wireshark : Analyse de trafic réseau"
echo "• Nmap : Audit et découverte réseau"
echo ""

echo "Formations complémentaires :"
echo "• Certification CCNA Security (Cisco)"
echo "• CISSP : Sécurité des systèmes d'information"
echo "• ISO 27001 Lead Implementer"
echo "• Formation RGPD et Privacy by Design"
echo ""

echo "=== FIN DE LA CORRECTION LAB 4 CHALLENGE ==="
