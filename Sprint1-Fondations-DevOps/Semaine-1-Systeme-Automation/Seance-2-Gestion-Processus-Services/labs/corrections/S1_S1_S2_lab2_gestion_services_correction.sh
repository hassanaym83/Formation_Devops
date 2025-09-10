#!/bin/bash

"""
LAB 2 - Gestion des services systemd - CORRECTION

Cette correction présente une solution complète et optimisée.

Concepts démontrés :
- Gestion complète du cycle de vie des services avec systemctl
- Configuration du démarrage automatique des services
- Analyse des logs avec journalctl
- Diagnostic et résolution des problèmes de services

Bonnes pratiques appliquées :
- Vérification systématique de l'état avant modification
- Utilisation des commandes systemctl appropriées
- Analyse des logs pour diagnostic
- Tests de résilience des services
"""

echo "=== LAB 2 - GESTION SERVICES SYSTEMD - CORRECTION ==="
echo "Mission: Configuration services infrastructure web"
echo "Contexte: Gestion production serveur nginx + base de données"
echo

# EXERCICE 1 : État des services (3 minutes)
echo "EXERCICE 1 : Vérification état des services"
echo "État du service nginx :"
systemctl is-active nginx 2>/dev/null || echo "nginx non installé/inactif"
systemctl is-enabled nginx 2>/dev/null || echo "nginx non activé au boot"

echo
echo "État du service SSH :"
systemctl is-active ssh 2>/dev/null || systemctl is-active sshd 2>/dev/null || echo "SSH inactif"
systemctl is-enabled ssh 2>/dev/null || systemctl is-enabled sshd 2>/dev/null || echo "SSH non activé"

echo
echo "Status détaillé nginx :"
systemctl status nginx --no-pager -l 2>/dev/null || echo "nginx non disponible"

echo "Mission : Analyser l'état de chaque service (active/inactive/enabled)"
echo "Analyse : Les services critiques doivent être active + enabled"
echo

# EXERCICE 2 : Gestion cycle de vie (5 minutes)
echo "EXERCICE 2 : Contrôle des services"
echo "Simulation gestion nginx (si disponible) :"

# Vérifier si nginx est installé
if systemctl list-unit-files | grep -q nginx; then
    echo "nginx détecté - démonstration des commandes :"
    echo "sudo systemctl start nginx   # Démarrer"
    echo "sudo systemctl stop nginx    # Arrêter"
    echo "sudo systemctl restart nginx # Redémarrer"
    echo "sudo systemctl reload nginx  # Recharger config"
    
    echo "Test d'état après commandes :"
    systemctl is-active nginx 2>/dev/null || echo "nginx inactif"
else
    echo "nginx non installé - simulation des commandes :"
    echo "Les commandes seraient :"
    echo "- sudo systemctl start nginx"
    echo "- sudo systemctl stop nginx"  
    echo "- sudo systemctl restart nginx"
    echo "- sudo systemctl reload nginx"
fi

echo "Mission : Maîtriser le démarrage/arrêt des services"
echo "Analyse : restart = stop + start, reload = recharge config sans arrêt"
echo

# EXERCICE 3 : Configuration auto-démarrage (4 minutes)
echo "EXERCICE 3 : Activation au boot"
echo "Services activés au démarrage :"
systemctl list-unit-files --type=service --state=enabled | head -10

echo
echo "Commandes de gestion du démarrage automatique :"
echo "sudo systemctl enable service    # Activer au boot"
echo "sudo systemctl disable service   # Désactiver au boot"
echo "sudo systemctl enable --now service # Activer + démarrer"

echo
echo "Vérification d'un service critique (SSH) :"
systemctl is-enabled ssh 2>/dev/null || systemctl is-enabled sshd 2>/dev/null || echo "SSH non configuré"

echo "Mission : Configurer le démarrage automatique"
echo "Analyse : Les services critiques doivent être enabled pour démarrer au boot"
echo

# EXERCICE 4 : Analyse des logs (4 minutes)
echo "EXERCICE 4 : Consultation logs service"
echo "Logs SSH récents :"
journalctl -u ssh --since "1 hour ago" --no-pager | tail -5 2>/dev/null || \
journalctl -u sshd --since "1 hour ago" --no-pager | tail -5 2>/dev/null || \
echo "Logs SSH non disponibles"

echo
echo "Logs système critiques :"
journalctl -p err --since "1 hour ago" --no-pager | head -5

echo
echo "Commandes journalctl essentielles :"
echo "journalctl -u service                # Logs d'un service"
echo "journalctl -u service --since '1h'   # Logs récents"
echo "journalctl -u service -f             # Suivi temps réel"
echo "journalctl -p err                    # Erreurs uniquement"

echo "Mission : Analyser les logs pour diagnostic"
echo "Analyse : journalctl centralise tous les logs systemd"
echo

# EXERCICE 5 : Services système critiques (2 minutes)
echo "EXERCICE 5 : Inventaire services actifs"
echo "Services actifs (top 10) :"
systemctl list-units --type=service --state=active --no-pager | head -10

echo
echo "Services en échec :"
FAILED_SERVICES=$(systemctl list-units --type=service --state=failed --no-pager)
if [ -z "$FAILED_SERVICES" ] || echo "$FAILED_SERVICES" | grep -q "0 loaded units"; then
    echo "Aucun service en échec détecté"
else
    echo "$FAILED_SERVICES"
fi

echo "Mission : Identifier services en échec"
echo "Analyse : Les services failed nécessitent une intervention immédiate"
echo

# EXERCICE 6 : Test de résilience (2 minutes)
echo "EXERCICE 6 : Simulation panne et récupération"
echo "Test avec un service de démonstration :"

# Créer un service temporaire pour test
cat << 'EOF' > /tmp/test-service.service
[Unit]
Description=Service de test pour démonstration
After=network.target

[Service]
Type=simple
ExecStart=/bin/sleep 3600
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "Service de test créé : /tmp/test-service.service"
echo "En production, vous utiliseriez :"
echo "sudo systemctl kill service      # Tuer brutalement"
echo "systemctl status service         # Vérifier état"
echo "sudo systemctl start service     # Redémarrer"

echo "Mission : Tester la robustesse des services"
echo "Analyse : Un bon service doit pouvoir redémarrer automatiquement"
echo

echo "=== RÉPONSES AUX POINTS DE CONTRÔLE ==="
echo "1. Service nginx actif :"
systemctl is-active nginx 2>/dev/null || echo "Dépend de l'installation"

echo "2. Service SSH au boot :"
systemctl is-enabled ssh 2>/dev/null || systemctl is-enabled sshd 2>/dev/null || echo "Généralement activé"

echo "3. Redémarrage sans coupure :"
echo "   sudo systemctl reload service (si supporté)"
echo "   Sinon : sudo systemctl restart service"

echo "4. Consultation logs :"
echo "   journalctl -u service_name"

echo "5. Services en échec :"
echo "   systemctl list-units --state=failed"

echo
echo "=== SCRIPT DE MONITORING SERVICES ==="
cat << 'EOF' > service_monitor.sh
#!/bin/bash
echo "=== MONITORING SERVICES SYSTÈME ==="
echo "Date : $(date)"
echo
echo "Services actifs : $(systemctl list-units --type=service --state=active --no-legend | wc -l)"
echo "Services en échec : $(systemctl list-units --type=service --state=failed --no-legend | wc -l)"
echo
echo "Top 5 services critiques :"
systemctl list-units --type=service --state=active --no-pager | grep -E "(ssh|nginx|apache|mysql|postgresql)" | head -5
echo
echo "Dernières erreurs système :"
journalctl -p err --since "1 hour ago" --no-pager | tail -3
EOF

chmod +x service_monitor.sh
echo "Script créé : service_monitor.sh"
./service_monitor.sh

echo
echo "=== FIN CORRECTION LAB 2 ==="
echo "Concepts maîtrisés : systemctl, journalctl, gestion services, monitoring"

