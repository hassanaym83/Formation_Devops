#!/bin/bash

# =============================================================================
# CORRECTION LAB 3 - Planification d'architecture réseau simple
# =============================================================================

echo "=== CORRECTION LAB 3 - Planification d'architecture réseau simple ==="
echo ""

# =============================================================================
# SOLUTION DU CALCUL DES BESOINS
# =============================================================================

echo "SOLUTION - CALCUL DES BESOINS D'ADRESSAGE :"
echo "==============================================="
echo ""

echo "MÉTHODE DE CALCUL :"
echo "-------------------"
echo "1. Identifier le besoin immédiat"
echo "2. Ajouter une marge de croissance (50-100%)"
echo "3. Choisir le masque CIDR qui offre assez d'adresses"
echo "4. Vérifier avec ipcalc"
echo ""

echo "EXEMPLE DÉTAILLÉ - Administration (10 machines) :"
echo "------------------------------------------------"
echo "• Besoin immédiat : 10 adresses"
echo "• Marge de croissance : +100% = 20 adresses total"
echo "• Masques possibles :"
echo " - /28 = 14 adresses (trop petit)"
echo " - /27 = 30 adresses (parfait)"
echo " - /26 = 62 adresses (trop grand, gaspillage)"
echo ""
echo "Vérification /27 :"
if command -v ipcalc >/dev/null 2>&1; then
 ipcalc 192.168.10.0/27 | grep -E "(Network|HostMin|HostMax|Hosts/Net)"
else
 echo "Network: 192.168.10.0/27"
 echo "HostMin: 192.168.10.1" 
 echo "HostMax: 192.168.10.30"
 echo "Hosts/Net: 30"
fi
echo ""

echo " RÉSULTAT : /27 offre 30 adresses pour 20 besoins → PARFAIT"
echo ""

# =============================================================================
# SOLUTION COMPLÈTE DU PLAN D'ADRESSAGE
# =============================================================================

echo "SOLUTION COMPLÈTE - PLAN D'ADRESSAGE ENTREPRISE :"
echo "====================================================="
echo ""

# Données du plan
departments=("Administration" "Employés" "Serveurs" "WiFi_Invités" "Imprimantes")
networks=("192.168.10.0/27" "192.168.20.0/26" "192.168.30.0/28" "192.168.40.0/25" "192.168.50.0/28")
needs=(10 25 5 50 5)
margins=(20 50 10 100 10)

echo "DÉTAIL DE CHAQUE SOUS-RÉSEAU :"
echo "------------------------------"

for i in "${!networks[@]}"; do
 echo ""
 echo "${departments[$i]} : ${networks[$i]}"
 echo " Besoin : ${needs[$i]} machines"
 echo " Avec marge : ${margins[$i]} adresses"
 
 if command -v ipcalc >/dev/null 2>&1; then
 hosts=$(ipcalc "${networks[$i]}" | grep "Hosts/Net" | awk '{print $2}')
 first_ip=$(ipcalc "${networks[$i]}" | grep "HostMin" | awk '{print $2}')
 last_ip=$(ipcalc "${networks[$i]}" | grep "HostMax" | awk '{print $2}')
 echo " Capacité : $hosts adresses"
 echo " Plage : $first_ip à $last_ip"
 
 if [ "$hosts" -ge "${margins[$i]}" ]; then
 echo " ADAPTÉ (Marge suffisante)"
 else
 echo " TROP PETIT"
 fi
 else
 echo " (Utilisez ipcalc pour voir les détails)"
 fi
done
echo ""

# =============================================================================
# EXPLICATION DES RÈGLES DE SÉCURITÉ
# =============================================================================

echo "EXPLICATION - RÈGLES DE SÉCURITÉ :"
echo "======================================"
echo ""

echo "PRINCIPE DE SÉCURITÉ : MOINDRE PRIVILÈGE"
echo "----------------------------------------"
echo "Chaque réseau n'a accès qu'à ce dont il a strictement besoin."
echo ""

echo "JUSTIFICATION DES RÈGLES :"
echo ""
echo "Administration → Partout :"
echo " ✓ Les administrateurs doivent pouvoir gérer tous les équipements"
echo " ✓ Maintenance, configuration, dépannage"
echo ""
echo "Employés → Serveurs + Imprimantes :"
echo " ✓ Besoin des données et de l'impression pour travailler"
echo " ✗ Pas besoin d'accéder à l'administration"
echo ""
echo "Serveurs → Internet uniquement :"
echo " ✓ Mises à jour et services web"
echo " ✗ Pas besoin d'accéder aux autres réseaux internes"
echo ""
echo "WiFi Invités → Internet + Imprimantes :"
echo " ✓ Service minimum pour les visiteurs"
echo " ✗ Aucun accès aux données de l'entreprise"
echo ""
echo "Imprimantes → Aucun Internet :"
echo " ✗ Risque de sécurité si piratage d'imprimante"
echo " ✗ Pas de besoin fonctionnel"
echo ""

# =============================================================================
# SOLUTION DE L'EXERCICE PRATIQUE - CAFÉ
# =============================================================================

echo "SOLUTION - EXERCICE DU CAFÉ :"
echo "================================="
echo ""

echo "ANALYSE DES BESOINS :"
echo "--------------------"
echo "• 5 machines de caisse → Sécurité critique (argent)"
echo "• 20 places WiFi clients → Accès Internet uniquement"
echo "• 3 ordinateurs personnel → Gestion + accès serveur"
echo "• 1 serveur de fichiers → Stockage central"
echo ""

echo "PLAN D'ADRESSAGE OPTIMISÉ :"
echo "----------------------------"
echo "Réseau de base : 192.168.100.0/24"
echo ""

# Solution café
cafe_networks=("192.168.100.0/28" "192.168.100.16/28" "192.168.100.32/27" "192.168.100.64/26")
cafe_services=("Caisses (Sécurisé)" "Personnel" "WiFi Clients" "Serveurs + Réserve")
cafe_capacity=(14 14 30 62)

for i in "${!cafe_networks[@]}"; do
 echo "${cafe_services[$i]} : ${cafe_networks[$i]}"
 if command -v ipcalc >/dev/null 2>&1; then
 echo " Capacité : ${cafe_capacity[$i]} adresses"
 range=$(ipcalc "${cafe_networks[$i]}" | grep -E "(HostMin|HostMax)" | tr '\n' ' ')
 echo " $range"
 fi
 echo ""
done

echo "VÉRIFICATION DE NON-CHEVAUCHEMENT :"
echo "----------------------------------"
echo " 192.168.100.0/28 : .1 à .14"
echo " 192.168.100.16/28 : .17 à .30" 
echo " 192.168.100.32/27 : .33 à .62"
echo " 192.168.100.64/26 : .65 à .126"
echo ""
echo "Tous les réseaux sont distincts, pas de conflit !"
echo ""

echo "RÈGLES DE SÉCURITÉ CAFÉ :"
echo "-------------------------"
echo "┌─────────────┬─────────┬─────────┬─────────┬─────────┬─────────┐"
echo "│ DEPUIS \\ VERS │ CAISSES │ PERSON. │ CLIENTS │ SERVEUR │ INTERNET│"
echo "├─────────────┼─────────┼─────────┼─────────┼─────────┼─────────┤"
echo "│ Caisses │ ✓ │ ✗ │ ✗ │ ✓ │ ✓ │"
echo "│ Personnel │ ✓ │ ✓ │ ✗ │ ✓ │ ✓ │"
echo "│ Clients │ ✗ │ ✗ │ ✓ │ ✗ │ ✓ │"
echo "│ Serveur │ ✗ │ ✗ │ ✗ │ ✓ │ ✓ │"
echo "└─────────────┴─────────┴─────────┴─────────┴─────────┴─────────┘"
echo ""

# =============================================================================
# MÉTHODE GÉNÉRALE DE PLANIFICATION
# =============================================================================

echo "MÉTHODE GÉNÉRALE DE PLANIFICATION RÉSEAU :"
echo "=============================================="
echo ""

echo "ÉTAPE 1 - INVENTAIRE :"
echo "----------------------"
echo "□ Lister tous les équipements/services"
echo "□ Estimer le nombre par catégorie"
echo "□ Prévoir la croissance (1-2 ans)"
echo ""

echo "ÉTAPE 2 - SEGMENTATION :"
echo "------------------------"
echo "□ Grouper par fonction similaire"
echo "□ Identifier les besoins de sécurité"
echo "□ Séparer les accès critiques"
echo ""

echo "ÉTAPE 3 - CALCUL D'ADRESSAGE :"
echo "------------------------------"
echo "□ Besoin immédiat × 2 (marge 100%)"
echo "□ Choisir le masque CIDR approprié"
echo "□ Vérifier avec ipcalc"
echo ""

echo "ÉTAPE 4 - ATTRIBUTION DES PLAGES :"
echo "----------------------------------"
echo "□ Commencer par les plus petits réseaux"
echo "□ Vérifier qu'il n'y a pas de chevauchement"
echo "□ Documenter clairement"
echo ""

echo "ÉTAPE 5 - RÈGLES DE SÉCURITÉ :"
echo "------------------------------"
echo "□ Principe du moindre privilège"
echo "□ Justifier chaque autorisation"
echo "□ Tester la logique des règles"
echo ""

# =============================================================================
# OUTILS ET COMMANDES UTILES
# =============================================================================

echo "BOÎTE À OUTILS POUR LA PLANIFICATION :"
echo "=========================================="
echo ""

echo "CALCULS RAPIDES :"
echo "-----------------"
echo "/30 = 2 adresses (liaison point-à-point)"
echo "/29 = 6 adresses (très petit réseau)" 
echo "/28 = 14 adresses (petit bureau)"
echo "/27 = 30 adresses (bureau moyen)"
echo "/26 = 62 adresses (grand bureau)"
echo "/25 = 126 adresses (département)"
echo "/24 = 254 adresses (site complet)"
echo ""

echo "COMMANDES DE VÉRIFICATION :"
echo "---------------------------"
echo "ipcalc 192.168.1.0/24 # Analyser un réseau"
echo "ip route show # Voir les routes actuelles"
echo "ip addr show # Voir les IPs configurées"
echo "ping -c 3 [IP] # Tester la connectivité"
echo ""

echo "OUTILS DE DOCUMENTATION :"
echo "-------------------------"
echo "• Tableur (Excel/LibreOffice) pour les plans d'adressage"
echo "• Outils de schéma réseau (draw.io, Visio)"
echo "• Documentation des règles de firewall"
echo "• Tests de validation et procédures"
echo ""

# =============================================================================
# VALIDATION FINALE ET ÉVALUATION
# =============================================================================

echo " GRILLE D'ÉVALUATION :"
echo "========================"
echo ""

# Simulation d'évaluation
score=0
total=6

echo "CRITÈRE 1 - Calcul des besoins en adresses :"
echo "□ Évaluation correcte du nombre de machines"
echo "□ Ajout de marge de croissance appropriée"
echo " Réussi (+1 point)"
score=$((score + 1))
echo ""

echo "CRITÈRE 2 - Choix des masques CIDR :"
echo "□ Masques adaptés aux besoins"
echo "□ Pas de gaspillage excessif d'adresses"
echo " Réussi (+1 point)"
score=$((score + 1))
echo ""

echo "CRITÈRE 3 - Plan d'adressage cohérent :"
echo "□ Pas de chevauchement entre réseaux"
echo "□ Attribution logique des plages"
echo " Réussi (+1 point)" 
score=$((score + 1))
echo ""

echo "CRITÈRE 4 - Règles de sécurité :"
echo "□ Application du principe de moindre privilège"
echo "□ Justification des autorisations"
echo " Réussi (+1 point)"
score=$((score + 1))
echo ""

echo "CRITÈRE 5 - Utilisation d'ipcalc :"
echo "□ Vérification des calculs avec l'outil"
echo "□ Interprétation correcte des résultats"
echo " Réussi (+1 point)"
score=$((score + 1))
echo ""

echo "CRITÈRE 6 - Compréhension globale :"
echo "□ Vision d'ensemble de l'architecture"
echo "□ Anticipation des besoins futurs"
echo " Réussi (+1 point)"
score=$((score + 1))
echo ""

echo "SCORE FINAL : $score/$total"

if [ $score -eq $total ]; then
 echo ""
 echo "EXCELLENT ! Vous maîtrisez la planification réseau de base"
 echo "Vous êtes prêt pour des concepts plus avancés (VLANs, routage dynamique)"
elif [ $score -ge 4 ]; then
 echo ""
 echo "BIEN ! Bonnes bases en planification réseau"
 echo "Continuez à pratiquer avec des scénarios variés"
else
 echo ""
 echo " ATTENTION ! Revoyez les concepts de base"
 echo "Reprenez les LABs 1 et 2 pour consolider"
fi

echo ""
echo "POINTS CLÉS À RETENIR :"
echo "=========================="
echo "• Planifiez toujours avec une marge de croissance"
echo "• La sécurité se conçoit dès la planification" 
echo "• Un bon plan d'adressage facilite la maintenance"
echo "• ipcalc est votre allié pour valider les calculs"
echo "• Documentez tout pour les équipes futures"
echo ""

echo "PROCHAINE ÉTAPE :"
echo "Vous pouvez maintenant aborder des sujets plus avancés :"
echo "• Configuration pratique des VLANs"
echo "• Mise en place de règles de firewall"
echo "• Routage inter-réseaux"
echo "• Haute disponibilité et redondance"
echo ""

echo "=== FIN DE LA CORRECTION LAB 3 ==="
