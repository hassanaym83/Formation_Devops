#!/bin/bash

# =============================================================================
# LAB 2 - CORRECTION - Structures Conditionnelles - Diagnostic d'Environnement DevOps
# =============================================================================
# Objectif : Démonstration des structures conditionnelles pour validation système
# Contexte : Script de pré-validation d'environnement pour pipeline CI/CD
# 
# Cette correction illustre :
# - Tests de fichiers et répertoires (-d, -f, -x)
# - Tests de chaînes (==, !=, -z)
# - Tests numériques (-lt, -gt, -eq)
# - Conditions imbriquées (if dans if)
# - Gestion d'erreurs avec codes de sortie
# =============================================================================

echo "=== DIAGNOSTIC D'ENVIRONNEMENT DEVOPS ==="
echo "Vérification de la configuration système..."
echo ""

# SOLUTION 1: Variable pour tracker l'état global des validations
# Variable booléenne pour suivre si toutes les validations passent
validation_globale=true

# SOLUTION 2: Vérification des répertoires critiques DevOps
echo "1. Vérification des répertoires critiques :"

# Test du répertoire des logs système
if [[ -d "/var/log" ]]; then
    echo "  ✓ /var/log : Répertoire de logs présent"
else
    echo "  ✗ /var/log : ERREUR - Répertoire de logs manquant"
    validation_globale=false
fi

# Test du répertoire de configuration système  
if [[ -d "/etc" ]]; then
    echo "  ✓ /etc : Répertoire de configuration présent"
else
    echo "  ✗ /etc : ERREUR - Répertoire de configuration manquant"
    validation_globale=false
fi

# Test du répertoire temporaire
if [[ -d "/tmp" ]]; then
    echo "  ✓ /tmp : Répertoire temporaire présent"
else
    echo "  ✗ /tmp : ERREUR - Répertoire temporaire manquant"
    validation_globale=false
fi

echo ""

# SOLUTION 3: Vérification des outils DevOps essentiels
echo "2. Vérification des outils DevOps :"

# Test de l'outil Git (contrôle de version)
if [[ -x "/usr/bin/git" ]]; then
    echo "  ✓ Git : Disponible et exécutable"
else
    echo "  ✗ Git : MANQUANT - Installer avec : apt install git"
    validation_globale=false
fi

# Test de Docker (containerisation)
if [[ -x "/usr/bin/docker" ]]; then
    echo "  ✓ Docker : Disponible et exécutable"
else
    echo "  ⚠ Docker : Non trouvé dans /usr/bin/docker (peut être installé ailleurs)"
fi

# Test de curl (transfert de données)
if [[ -x "/usr/bin/curl" ]]; then
    echo "  ✓ curl : Disponible et exécutable"
else
    echo "  ✗ curl : MANQUANT - Installer avec : apt install curl"
    validation_globale=false
fi

echo ""

# SOLUTION 4: Vérification de l'espace disque disponible
echo "3. Vérification de l'espace disque :"

# Récupération du pourcentage d'utilisation du disque racine
utilisation_disque=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

# Calcul de l'espace disponible
espace_disponible=$((100 - utilisation_disque))

echo "  Espace utilisé : ${utilisation_disque}% (${espace_disponible}% disponible)"

# Tests numériques avec opérateurs de comparaison
if [[ $espace_disponible -lt 10 ]]; then
    echo "  ✗ ERREUR CRITIQUE : Espace disque < 10% disponible"
    validation_globale=false
elif [[ $espace_disponible -lt 20 ]]; then
    echo "  ⚠ AVERTISSEMENT : Espace disque < 20% disponible"
    # Note: ne pas mettre validation_globale=false pour un avertissement
else
    echo "  ✓ Espace disque suffisant (≥ 20% disponible)"
fi

echo ""

# SOLUTION 5: Conditions imbriquées - Validation des services système
echo "4. Validation des services système (conditions imbriquées) :"

# Première condition : vérifier si systemctl existe
if [[ -x "/bin/systemctl" ]]; then
    echo "  ✓ systemctl disponible"
    
    # Condition imbriquée : tester le service SSH
    if systemctl is-active ssh >/dev/null 2>&1; then
        echo "  ✓ Service SSH actif"
        
        # Condition imbriquée niveau 2 : vérifier le fichier de configuration
        if [[ -f "/etc/ssh/sshd_config" ]]; then
            echo "  ✓ Configuration SSH présente"
        else
            echo "  ✗ Fichier de configuration SSH manquant"
            validation_globale=false
        fi
    else
        echo "  ⚠ Service SSH inactif ou non installé"
    fi
elif [[ -x "/usr/bin/systemctl" ]]; then
    echo "  ✓ systemctl disponible dans /usr/bin"
    # Répéter les tests SSH...
    if systemctl is-active ssh >/dev/null 2>&1; then
        echo "  ✓ Service SSH actif"
        if [[ -f "/etc/ssh/sshd_config" ]]; then
            echo "  ✓ Configuration SSH présente"
        else
            echo "  ✗ Fichier de configuration SSH manquant"
            validation_globale=false
        fi
    else
        echo "  ⚠ Service SSH inactif ou non installé"
    fi
else
    echo "  ✗ systemctl NON DISPONIBLE - Système non compatible systemd"
    validation_globale=false
fi

echo ""

# SOLUTION 6: Test de chaînes - Validation de l'utilisateur
echo "5. Vérification de l'utilisateur :"

# Récupération du nom d'utilisateur actuel
utilisateur_actuel="$USER"

# Test de chaîne avec opérateur d'égalité
if [[ "$utilisateur_actuel" == "root" ]]; then
    echo "  ⚠ AVERTISSEMENT : Script exécuté en tant que root"
    echo "  Recommandation : Utiliser un utilisateur non privilégié"
elif [[ -z "$utilisateur_actuel" ]]; then
    echo "  ✗ ERREUR : Impossible de déterminer l'utilisateur"
    validation_globale=false
else
    echo "  ✓ Utilisateur actuel : $utilisateur_actuel (non root)"
fi

echo ""

# SOLUTION 7: Résultat final avec code de sortie
echo "=== RÉSULTAT DU DIAGNOSTIC ==="

# Condition finale basée sur l'état global
if [[ "$validation_globale" == true ]]; then
    echo "✅ SUCCÈS : Environnement DevOps validé"
    echo "Le système est prêt pour le déploiement"
    exit 0  # Code de sortie 0 = succès
else
    echo "❌ ÉCHEC : Problèmes détectés dans l'environnement"
    echo "Corriger les erreurs avant de continuer"
    exit 1  # Code de sortie 1 = erreur
fi

# =============================================================================
# Points pédagogiques couverts :
# 
# 1. TESTS DE FICHIERS ET RÉPERTOIRES :
#    -d : teste si c'est un répertoire
#    -f : teste si c'est un fichier régulier
#    -x : teste si le fichier est exécutable
#
# 2. TESTS DE CHAÎNES :
#    == : égalité entre chaînes
#    -z : teste si la chaîne est vide
#
# 3. TESTS NUMÉRIQUES :
#    -lt : less than (inférieur à)
#    -gt : greater than (supérieur à)
#    -eq : equal (égal à)
#
# 4. CONDITIONS IMBRIQUÉES :
#    if dans if pour logique complexe
#    elif pour conditions alternatives
#
# 5. GESTION D'ERREURS :
#    Variable de suivi d'état global
#    Codes de sortie appropriés (0=succès, 1=erreur)
#
# 6. BONNES PRATIQUES :
#    Messages informatifs clairs
#    Utilisation de [[ ]] au lieu de [ ]
#    Gestion de la redirection d'erreurs (>/dev/null 2>&1)
# =============================================================================
echo "Date: $(date)"
echo "Utilisateur: $USER"
echo ""

# Variable de suivi global de validation
validation_globale=true

echo "=== ÉTAPE 1: TESTS DE FICHIERS ET RÉPERTOIRES ==="

# Test 1: Vérification de l'existence du répertoire /etc (configuration système)
if [[ -d "/etc" ]]; then
    echo "✅ Répertoire /etc existe (configuration système)"
else
    echo "❌ ERREUR: Répertoire /etc manquant"
    validation_globale=false
fi

# Test 2: Vérification de l'existence du fichier /etc/hosts (réseau)
if [[ -f "/etc/hosts" ]]; then
    echo "✅ Fichier /etc/hosts existe (configuration réseau)"
    
    # Test imbriqué: vérifier si le fichier est lisible
    if [[ -r "/etc/hosts" ]]; then
        echo "  → Fichier /etc/hosts est lisible"
    else
        echo "  → ATTENTION: Fichier /etc/hosts non lisible"
        validation_globale=false
    fi
else
    echo "❌ ERREUR: Fichier /etc/hosts manquant"
    validation_globale=false
fi

echo ""
echo "=== ÉTAPE 2: TESTS DE CHAÎNES ==="

# Test 3: Vérification de la variable utilisateur
if [[ -n "$USER" ]]; then
    echo "✅ Variable USER définie: $USER"
    
    # Test imbriqué: vérifier si ce n'est pas l'utilisateur root
    if [[ "$USER" != "root" ]]; then
        echo "  → Utilisateur non-privilégié (recommandé pour développement)"
    else
        echo "  → ATTENTION: Utilisateur root détecté"
    fi
else
    echo "❌ ERREUR: Variable USER non définie"
    validation_globale=false
fi

echo ""
echo "=== ÉTAPE 3: TESTS NUMÉRIQUES ==="

# Test 4: Vérification de l'espace disque disponible
disk_usage=$(df / | tail -1 | awk '{print $(NF-1)}' | sed 's/%//')

if [[ $disk_usage -lt 80 ]]; then
    echo "✅ Espace disque suffisant (${disk_usage}% utilisé)"
elif [[ $disk_usage -ge 80 && $disk_usage -lt 90 ]]; then
    echo "⚠️  Espace disque modéré (${disk_usage}% utilisé)"
else
    echo "❌ ERREUR: Espace disque critique (${disk_usage}% utilisé)"
    validation_globale=false
fi

echo ""
echo "=== RÉSULTAT FINAL ==="

# Décision finale basée sur tous les tests
if [[ "$validation_globale" == true ]]; then
    echo "🎉 SUCCÈS: ENVIRONNEMENT VALIDÉ"
    echo "L'environnement DevOps est prêt pour le développement"
    exit 0  # Code de succès
else
    echo "💥 ÉCHEC: ENVIRONNEMENT NON CONFORME"
    echo "Corrigez les erreurs signalées avant de continuer"
    exit 1  # Code d'erreur
fi