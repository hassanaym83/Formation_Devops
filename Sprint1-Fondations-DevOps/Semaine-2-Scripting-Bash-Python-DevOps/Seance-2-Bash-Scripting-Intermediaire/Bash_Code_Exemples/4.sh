# Sortie normale (stdout)
echo "Traitement réussi"

# Sortie d'erreur (stderr)
echo "Erreur: Paramètres manquants" >&2

# Démonstration de la différence
echo "Message normal"                    # Vers stdout (1)
echo "Message d'erreur" >&2            # Vers stderr (2