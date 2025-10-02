#!/bin/sh
# =================================================================
# SCRIPT SHELL EXEMPLE - app.sh
# À utiliser avec le Dockerfile Alpine pour démonstration
# =================================================================

echo "==================================="
echo "   APPLICATION ALPINE DÉMARRÉE"
echo "==================================="
echo

# Afficher les informations système
echo "Informations système:"
echo "- Distribution: $(cat /etc/os-release | grep PRETTY_NAME | cut -d '"' -f 2)"
echo "- Hostname: $(hostname)"
echo "- Date: $(date)"
echo

# Tester curl (installé via le Dockerfile)
echo "Test de connectivité réseau avec curl:"
if curl -s --connect-timeout 5 https://httpbin.org/ip > /dev/null; then
    echo "✓ Connexion réseau OK"
    echo "  IP publique: $(curl -s https://httpbin.org/ip | grep origin | cut -d '"' -f 4)"
else
    echo "✗ Pas de connexion réseau"
fi
echo

# Boucle infinie pour maintenir le conteneur actif
echo "Application en cours d'exécution..."
echo "Appuyez sur Ctrl+C pour arrêter"
echo

while true; do
    echo "[$(date)] Conteneur Alpine actif - PID: $$"
    sleep 30
done