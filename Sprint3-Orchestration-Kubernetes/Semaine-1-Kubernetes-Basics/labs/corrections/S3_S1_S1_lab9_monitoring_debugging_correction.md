# Correction - LAB 9 : Monitoring et debugging

## Objectif

- Installer des outils basiques de monitoring et dépannage

## Solution rapide

- Utiliser `kubectl top` pour vérifier l'utilisation des ressources (require metrics-server)
- Installer Prometheus Node Exporter et Grafana via manifests ou Helm

## Bonnes pratiques

- Centraliser logs et métriques
- Mettre des alertes basées sur SLO/SLI

## Tests

- kubectl top nodes
- kubectl logs -l app=prometheus
