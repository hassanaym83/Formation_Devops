#!/bin/bash
# Script démontrant l'utilisation des paramètres positionnels

# Récupération des paramètres passés au script
# $1, $2, $3... correspondent aux arguments dans l'ordre

environnement=$1                    # Premier argument : environnement de déploiement
application=$2                      # Deuxième argument : nom de l'application

# ${3:-"latest"} : valeur par défaut si $3 est vide ou non fourni
version=${3:-"latest"}              # Troisième argument avec valeur par défaut

# Affichage des paramètres récupérés
echo "Déploiement de $application"
echo "Environnement: $environnement"
echo "Version: $version"