#!/bin/bash

# =============================================================================
# LAB 2 - Structures Conditionnelles - Diagnostic d'Environnement DevOps
# =============================================================================
# Objectif : Maîtriser les structures conditionnelles pour validation système
# Contexte : Script de pré-validation d'environnement pour pipeline CI/CD
# 
# Instructions :
# 1. Implémenter 4 types de tests différents (fichiers, chaînes, numériques, services)
# 2. Utiliser conditions imbriquées pour logique complexe
# 3. Gérer les erreurs avec codes de sortie appropriés
# 4. Fournir des messages informatifs pour chaque test
#
# Durée estimée : 25 minutes
# =============================================================================

echo "=== DIAGNOSTIC D'ENVIRONNEMENT DEVOPS ==="
echo "Vérification de la configuration système..."
echo ""

# TODO 1: Déclarer une variable pour tracker l'état global des validations
# Utiliser une variable booléenne qui sera mise à false si un test échoue

# TODO 2: Vérification des répertoires critiques DevOps
# Tester l'existence des répertoires suivants et afficher le statut :
# - /var/log (logs système)
# - /etc (configuration système)  
# - /tmp (fichiers temporaires)
# Utiliser l'opérateur -d pour tester les répertoires

echo "1. Vérification des répertoires critiques :"
# Votre code ici

echo ""

# TODO 3: Vérification des outils DevOps essentiels
# Tester l'existence et l'exécutabilité des outils suivants :
# - /usr/bin/git (contrôle de version)
# - /usr/bin/docker (containerisation) 
# - /usr/bin/curl (transfert de données)
# Utiliser l'opérateur -x pour tester l'exécutabilité

echo "2. Vérification des outils DevOps :"
# Votre code ici

echo ""

# TODO 4: Vérification de l'espace disque disponible
# Récupérer l'espace disque disponible en % et implémenter la logique suivante :
# - Si < 10% : Erreur critique
# - Si < 20% : Avertissement  
# - Sinon : OK
# Utiliser les opérateurs numériques -lt (less than)
# Commande suggérée : df / | tail -1 | awk '{print $5}' | sed 's/%//'

echo "3. Vérification de l'espace disque :"
# Votre code ici

echo ""

# TODO 5: Conditions imbriquées - Validation des services système
# Implémenter une validation complexe avec conditions imbriquées :
# 1. D'abord vérifier si systemctl existe (-x /bin/systemctl)
# 2. Si oui, tester si le service ssh est actif (systemctl is-active ssh)
# 3. Si ssh actif, vérifier le fichier de config (/etc/ssh/sshd_config)
# 4. Utiliser elif pour les différents cas de figure

echo "4. Validation des services système (conditions imbriquées) :"
# Votre code ici

echo ""

# TODO 6: Test de chaînes - Validation de l'utilisateur
# Vérifier que le script n'est pas exécuté en tant que root
# Utiliser la variable $USER et l'opérateur == pour comparer les chaînes
# Afficher un avertissement si l'utilisateur est root

echo "5. Vérification de l'utilisateur :"
# Votre code ici

echo ""

# TODO 7: Résultat final avec code de sortie
# Analyser la variable d'état global et :
# - Si toutes les validations OK : afficher "SUCCÈS" et exit 0
# - Sinon : afficher "ÉCHEC" et exit 1
# Utiliser une condition if/else pour le résultat final

echo "=== RÉSULTAT DU DIAGNOSTIC ==="
# Votre code ici

# =============================================================================
# Points d'évaluation :
# - 4 types de tests implémentés (fichiers/répertoires, exécutables, numériques, chaînes)
# - 2 conditions imbriquées minimum (validation services)
# - Gestion appropriée des codes de sortie
# - Messages informatifs et clairs
# - Logique de validation globale cohérente
# =============================================================================