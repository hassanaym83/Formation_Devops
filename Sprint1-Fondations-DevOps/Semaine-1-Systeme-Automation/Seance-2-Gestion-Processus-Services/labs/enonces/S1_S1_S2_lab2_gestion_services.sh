#!/bin/bash

"""
LAB 2 - Gestion des services systemd

Objectifs :
- Maîtriser les commandes systemctl pour la gestion des services
- Configurer les services pour un environnement de production
- Analyser les états et dépendances des services système

Points : 5/30

Durée estimée : 20 minutes
"""

echo "=== LAB 2 - GESTION SERVICES SYSTEMD ==="
echo "Mission: Configuration services infrastructure web"
echo "Contexte: Gestion production serveur nginx + base de données"
echo

# EXERCICE 1 : État des services (3 minutes)
echo "EXERCICE 1 : Vérification état des services"
echo "systemctl status nginx"
echo "systemctl status ssh" 
echo "systemctl is-active nginx"
echo "systemctl is-enabled ssh"
echo "Mission : Analyser l'état de chaque service (active/inactive/enabled)"
echo

# EXERCICE 2 : Gestion cycle de vie (5 minutes)
echo "EXERCICE 2 : Contrôle des services"
echo "sudo systemctl start nginx"
echo "sudo systemctl stop nginx"
echo "sudo systemctl restart nginx"
echo "sudo systemctl reload nginx"
echo "Mission : Maîtriser le démarrage/arrêt des services"
echo

# EXERCICE 3 : Configuration auto-démarrage (4 minutes)
echo "EXERCICE 3 : Activation au boot"
echo "sudo systemctl enable nginx"
echo "sudo systemctl disable nginx"
echo "sudo systemctl enable --now nginx"
echo "systemctl list-unit-files --type=service --state=enabled"
echo "Mission : Configurer le démarrage automatique"
echo

# EXERCICE 4 : Analyse des logs (4 minutes)
echo "EXERCICE 4 : Consultation logs service"
echo "journalctl -u nginx"
echo "journalctl -u nginx --since '1 hour ago'"
echo "journalctl -u nginx -f"
echo "Mission : Analyser les logs pour diagnostic"
echo

# EXERCICE 5 : Services système critiques (2 minutes)
echo "EXERCICE 5 : Inventaire services actifs"
echo "systemctl list-units --type=service --state=active"
echo "systemctl list-units --type=service --state=failed"
echo "Mission : Identifier services en échec"
echo

# EXERCICE 6 : Test de résilience (2 minutes)
echo "EXERCICE 6 : Simulation panne et récupération"
echo "sudo systemctl kill nginx"
echo "systemctl status nginx"
echo "sudo systemctl start nginx"
echo "Mission : Tester la robustesse des services"
echo

echo "=== POINTS DE CONTRÔLE ==="
echo "1. Le service nginx est-il actif ?"
echo "2. Le service ssh démarre-t-il au boot ?"
echo "3. Comment redémarrer un service sans coupure ?"
echo "4. Où consulter les logs d'un service ?"
echo "5. Comment identifier un service en échec ?"

echo
echo "=== FIN LAB 2 ==="

