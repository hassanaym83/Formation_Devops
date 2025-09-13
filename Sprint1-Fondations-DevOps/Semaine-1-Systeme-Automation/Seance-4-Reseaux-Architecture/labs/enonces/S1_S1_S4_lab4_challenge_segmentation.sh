#!/bin/bash

# =============================================================================
# LAB 4 CHALLENGE - Segmentation réseau pratique (BONUS)
# =============================================================================
#
# Énoncé : Projet avancé de planification réseau pour une infrastructure complète
#
# Objectif : Concevoir et documenter une architecture réseau complexe avec segmentation
#
# Durée estimée : 30 minutes
# Niveau de difficulté : Avancé - Challenge optionnel
# Prérequis : Maîtrise des LABs 1, 2 et 3
# =============================================================================

# =============================================================================
# PARTIE 1 - Contexte du challenge
# =============================================================================

echo "=== LAB 4 CHALLENGE - Segmentation réseau pratique (BONUS) ==="
echo ""
echo "MISSION COMPLEXE :"
echo "===================="
echo ""
echo "Vous êtes consultant réseau pour une entreprise technologique"
echo "qui déménage dans de nouveaux locaux. Ils ont besoin d'une"
echo "architecture réseau complète et sécurisée."
echo ""
echo "CONTRAINTES DE L'ENTREPRISE :"
echo "================================="
echo ""
echo "• 150 employés répartis sur 3 étages"
echo "• 25 serveurs dans le datacenter"
echo "• 50 invités simultanés maximum (WiFi)"
echo "• 10 machines d'administration/sécurité"
echo "• 15 imprimantes et équipements réseau"
echo "• Besoins de croissance : +50% dans 2 ans"
echo ""
echo "EXIGENCES DE SÉCURITÉ :"
echo "=========================="
echo ""
echo "• Isoler complètement les invités du réseau interne"
echo "• Séparer les serveurs de production du reste"
echo "• Permettre l'administration depuis un réseau dédié"
echo "• Prévoir l'accès aux imprimantes depuis tous les réseaux"
echo "• Pas d'accès Internet direct pour les serveurs sensibles"
echo ""

# =============================================================================
# PARTIE 2 - Calculs de capacité
# =============================================================================

echo " ÉTAPE 1 - Calculs de capacité avec marge :"
echo "============================================="
echo ""
echo "Calculons les besoins en adresses IP avec une marge de croissance."
echo ""

# Fonction de calcul avec marge
calculate_network_size() {
local description="$1"
local current_need="$2"
local growth_factor="$3"

echo "$description :"
echo " Besoin actuel : $current_need machines"

local future_need=$((current_need * growth_factor / 100))
echo " Croissance prévue : +$((growth_factor - 100))% = $future_need machines"

# Trouver la taille de réseau appropriée
local network_sizes=(14 30 62 126 254 510 1022)
local network_masks=(28 27 26 25 24 23 22)

for i in "${!network_sizes[@]}"; do
if [ "${network_sizes[$i]}" -ge "$future_need" ]; then
echo " Réseau recommandé : /${network_masks[$i]} (${network_sizes[$i]} adresses)"
echo " Marge disponible : $((network_sizes[$i] - future_need)) adresses"
break
fi
done
echo ""
}

# Calculs pour chaque département
calculate_network_size "EMPLOYÉS (3 étages)" 150 150
calculate_network_size "SERVEURS (datacenter)" 25 150 
calculate_network_size "INVITÉS (WiFi public)" 50 120
calculate_network_size "ADMINISTRATION" 10 140
calculate_network_size "ÉQUIPEMENTS (imprimantes, etc.)" 15 130

echo "RECOMMANDATION GÉNÉRALE :"
echo "============================="
echo "Utilisez la plage privée 10.0.0.0/16 qui offre 65,534 adresses"
echo "disponibles, largement suffisant pour cette infrastructure."
echo ""

# =============================================================================
# PARTIE 3 - Plan d'adressage proposé 
# =============================================================================

echo " ÉTAPE 2 - Plan d'adressage détaillé :"
echo "========================================="
echo ""
echo "Basé sur l'analyse précédente, voici un plan d'adressage optimisé :"
echo ""

networks=("10.0.10.0/24" "10.0.20.0/25" "10.0.30.0/26" "10.0.40.0/27" "10.0.50.0/27")
departments=("EMPLOYÉS" "SERVEURS" "INVITÉS" "ADMINISTRATION" "ÉQUIPEMENTS")
capacities=(254 126 62 30 30)
usages=("150 postes + marge" "25 serveurs + expansion" "50 invités max" "10 machines admin" "15 équipements réseau")

echo "┌─────────────────┬─────────────────┬─────────────┬──────────────────────┐"
echo "│ DÉPARTEMENT │ RÉSEAU CIDR │ CAPACITÉ │ USAGE PRÉVU │"
echo "├─────────────────┼─────────────────┼─────────────┼──────────────────────┤"

for i in "${!networks[@]}"; do
printf "│ %-15s │ %-15s │ %-11s │ %-20s │\n" \
"${departments[$i]}" \
"${networks[$i]}" \
"${capacities[$i]}" \
"${usages[$i]}"
done

echo "└─────────────────┴─────────────────┴─────────────┴──────────────────────┘"
echo ""

echo "VÉRIFICATION AVEC IPCALC :"
echo "============================="
echo ""
echo "Vérifions la cohérence de notre plan :"
echo ""

for i in "${!networks[@]}"; do
echo "${departments[$i]} (${networks[$i]}) :"
if command -v ipcalc >/dev/null 2>&1; then
ipcalc "${networks[$i]}" | grep -E "(Network|HostMin|HostMax|Hosts/Net)" | sed 's/^/ /'
else
echo " (Utilisez 'sudo apt install ipcalc' pour voir les détails)"
fi
echo ""
done

# =============================================================================
# PARTIE 4 - Matrice de sécurité
# =============================================================================

echo "ÉTAPE 3 - Matrice de communication et sécurité :"
echo "=================================================="
echo ""
echo "Définissons les règles de communication entre réseaux :"
echo ""

echo "┌─────────────┬─────┬─────┬─────┬─────┬─────┬─────────┐"
echo "│ DEPUIS \\ VERS │ EMP │ SRV │ INV │ ADM │ EQP │ INTERNET│"
echo "├─────────────┼─────┼─────┼─────┼─────┼─────┼─────────┤"
echo "│ Employés │ │ │ │ │ │ │"
echo "│ Serveurs │ │ │ │ │ │ │"
echo "│ Invités │ │ │ │ │ │ │"
echo "│ Admin │ │ │ │ │ │ │"
echo "│ Équipements │ │ │ │ │ │ │"
echo "└─────────────┴─────┴─────┴─────┴─────┴─────┴─────────┘"
echo ""

echo "JUSTIFICATION DES RÈGLES :"
echo "============================="
echo ""
echo " AUTORISATIONS logiques :"
echo "• Employés → Serveurs : Accès aux applications métier"
echo "• Employés → Équipements : Utilisation imprimantes/scanners"
echo "• Invités → Équipements : Service minimal pour visiteurs"
echo "• Admin → Tous : Gestion et maintenance complète"
echo "• Serveurs → Admin : Rapports de monitoring"
echo ""
echo " INTERDICTIONS sécurisées :"
echo "• Invités ↔ Employés : Isolation sécurité"
echo "• Invités ↔ Serveurs : Protection données sensibles"
echo "• Serveurs → Employés : Principe de moindre privilège"
echo "• Équipements → Internet : Risque de compromission"
echo ""

# =============================================================================
# PARTIE 5 - Implémentation technique
# =============================================================================

echo " ÉTAPE 4 - Simulation technique :"
echo "===================================="
echo ""
echo "Simulons la configuration de quelques éléments clés :"
echo ""

echo "1. CONFIGURATION D'UN SERVEUR MULTI-INTERFACES :"
echo "------------------------------------------------"
echo ""
echo "Supposons un serveur Linux avec plusieurs interfaces réseau :"
echo ""
echo "# Voir les interfaces disponibles :"
echo "ip link show"
echo ""
ip link show
echo ""

echo "# Configuration simulée (NE PAS EXÉCUTER en production) :"
echo "# Interface vers réseau employés"
echo "sudo ip addr add 10.0.10.1/24 dev eth0"
echo "# Interface vers réseau serveurs" 
echo "sudo ip addr add 10.0.20.1/25 dev eth1"
echo "# Interface vers réseau admin"
echo "sudo ip addr add 10.0.40.1/27 dev eth2"
echo ""

echo "2. ROUTES ENTRE RÉSEAUX :"
echo "-------------------------"
echo ""
echo "# Routes pour permettre la communication selon la matrice :"
echo "# (Commandes d'exemple - à adapter selon la topologie réelle)"
echo ""
echo "# Route employés vers serveurs"
echo "sudo ip route add 10.0.20.0/25 via 10.0.10.1 dev eth0"
echo ""
echo "# Route admin vers tous les réseaux" 
echo "sudo ip route add 10.0.10.0/24 via 10.0.40.1 dev eth2"
echo "sudo ip route add 10.0.20.0/25 via 10.0.40.1 dev eth2"
echo ""

echo "3. VÉRIFICATION DE LA CONNECTIVITÉ :"
echo "------------------------------------"
echo ""
echo "Testez la connectivité de votre réseau actuel :"
echo ""
echo "Votre réseau actuel :"
current_network=$(ip route show | grep -E "192.168\.[0-9]+\.[0-9]+/[0-9]+" | head -1 | awk '{print $1}')
if [ -n "$current_network" ]; then
echo "Réseau détecté : $current_network"
echo ""
echo "Analyse avec ipcalc :"
ipcalc "$current_network" 2>/dev/null || echo "Utilisez ipcalc pour analyser ce réseau"
else
echo " Réseau local non détecté automatiquement"
fi
echo ""

# =============================================================================
# PARTIE 6 - Exercice pratique du challenge
# =============================================================================

echo " EXERCICE PRATIQUE DU CHALLENGE :"
echo "==================================="
echo ""
echo "MISSION : Concevez votre propre architecture !"
echo ""
echo "Scénario : Vous devez planifier le réseau d'un hôpital avec :"
echo ""
echo "• 200 postes médecins/infirmières (accès patients)"
echo "• 50 postes administration (facturation, RH)" 
echo "• 30 serveurs médicaux (données patients CRITIQUES)"
echo "• 10 serveurs administration (comptabilité)"
echo "• 100 tablettes/mobiles médecins (WiFi sécurisé)"
echo "• 80 invités/familles (WiFi public)"
echo "• 20 équipements médicaux connectés"
echo "• 15 imprimantes/scanners"
echo ""
echo "CONTRAINTES STRICTES :"
echo "• AUCUNE communication invités ↔ données médicales"
echo "• Serveurs médicaux isolés (administration autorisée)"
echo "• Équipements médicaux accès serveurs médicaux SEULEMENT"
echo "• Tablettes médecins accès serveurs médicaux + admin"
echo "• Conformité RGPD et secret médical OBLIGATOIRES"
echo ""

echo "QUESTIONS À RÉSOUDRE :"
echo "========================="
echo ""
echo "1. Combien de réseaux créer ? (au minimum 6-8 réseaux)"
echo "2. Quelle plage d'adresses utiliser ? (10.0.0.0/16 ou 172.16.0.0/12)"
echo "3. Quelles tailles de sous-réseaux (/XX) pour chaque usage ?"
echo "4. Quelles sont les 3 règles de sécurité les plus critiques ?"
echo "5. Comment isoler totalement les données patients ?"
echo "6. Où placer les serveurs de sauvegarde ?"
echo ""

echo "MÉTHODOLOGIE RECOMMANDÉE :"
echo "============================="
echo ""
echo "1. Calculer les besoins (actuel + croissance 3 ans)"
echo "2. Dessiner l'architecture sur papier" 
echo "3. Attribuer les plages CIDR avec ipcalc"
echo "4. Définir la matrice de communication"
echo "5. Vérifier la cohérence et non-chevauchement"
echo "6. Documenter les choix et justifications"
echo ""

echo "LIVRABLES ATTENDUS :"
echo "======================="
echo ""
echo "□ Plan d'adressage complet avec justifications"
echo "□ Matrice de communication détaillée"
echo "□ Règles de sécurité spécifiques au médical"
echo "□ Calculs de capacité avec outil ipcalc"
echo "□ Procédure d'implémentation étape par étape"
echo "□ Plan de tests de connectivité"
echo ""

# =============================================================================
# VALIDATION ET RÉCAPITULATIF
# =============================================================================

echo " CRITÈRES DE RÉUSSITE DU CHALLENGE :"
echo "======================================="
echo ""
echo "NIVEAU BRONZE (5 points) :"
echo "□ Plan d'adressage cohérent et sans chevauchement"
echo "□ Capacités appropriées pour tous les besoins"
echo "□ Utilisation correcte d'ipcalc pour validation"
echo ""
echo "NIVEAU ARGENT (8 points) :"
echo "□ Tous les critères Bronze"
echo "□ Matrice de sécurité logique et justifiée"
echo "□ Prise en compte des contraintes métier"
echo "□ Documentation claire et professionnelle"
echo ""
echo "NIVEAU OR (12 points) :"
echo "□ Tous les critères Argent"
echo "□ Innovation dans l'approche sécuritaire"
echo "□ Procédures d'implémentation détaillées"
echo "□ Plan de tests et validation complet"
echo "□ Anticipation des évolutions futures"
echo ""

echo "COMPÉTENCES DÉVELOPPÉES :"
echo "==========================="
echo ""
echo "À l'issue de ce challenge, vous maîtriserez :"
echo "• La conception d'architectures réseau complexes"
echo "• L'analyse des besoins métier et contraintes techniques"
echo "• L'application des principes de sécurité réseau"
echo "• L'utilisation professionnelle des outils de calcul réseau"
echo "• La documentation technique et la justification des choix"
echo "• La planification de projets d'infrastructure réseau"
echo ""

echo "APRÈS CE CHALLENGE :"
echo "======================="
echo ""
echo "Vous serez préparé pour :"
echo "• Les certifications réseau (CCNA, CompTIA Network+)"
echo "• Les projets d'infrastructure d'entreprise"
echo "• Les architectures cloud (AWS VPC, Azure VNet)"
echo "• Les réseaux de conteneurs (Docker, Kubernetes)"
echo "• Les solutions de sécurité réseau avancées"
echo ""

echo "TEMPS CONSEILLÉ : 30-45 minutes"
echo "NIVEAU : Intermédiaire à Avancé"
echo "STATUT : Challenge optionnel pour l'excellence"
echo ""

echo "=== FIN DU LAB 4 CHALLENGE - Segmentation réseau pratique ==="
