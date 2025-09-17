#!/bin/bash
# Script d'audit de connectivité infrastructure avec boucle for

# Vérification de connectivité sur plusieurs serveurs - automatisation avec boucle for
echo "=== AUDIT DE CONNECTIVITÉ INFRASTRUCTURE ==="

# DÉCLARATION DE TABLEAU : liste des serveurs à tester
# Syntaxe : nom_tableau=(élément1 élément2 élément3 ...)
serveurs=("web-prod-01" "web-prod-02" "api-prod-01" "db-prod-01")

# BOUCLE FOR : itère sur chaque élément du tableau
# "${serveurs[@]}" : expansion de tous les éléments du tableau
# for ... in ... do ... done : structure de boucle for
for serveur in "${serveurs[@]}"; do
    # echo -n : affiche sans saut de ligne final (pour le formatage)
    echo -n "Test connectivité $serveur : "

    # TEST DE CONNECTIVITÉ :
    # ping -c 1 : envoie 1 seul paquet ICMP
    # -W 2 : timeout de 2 secondes maximum
    # >/dev/null 2>&1 : redirige sortie standard et erreurs vers /dev/null (silencieux)
    if ping -c 1 -W 2 "$serveur" >/dev/null 2>&1; then
        echo "ACCESSIBLE"     # Code de retour 0 : serveur répond
    else
        echo "INACCESSIBLE"   # Code de retour ≠ 0 : serveur ne répond pas
    fi
done  # Fin de la boucle for

echo "Audit terminé"