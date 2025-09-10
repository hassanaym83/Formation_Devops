# Séance 2 - Gestion des Processus et Services

## Vue d'ensemble

Cette séance couvre la gestion complète des processus Linux et des services systemd, compétences essentielles pour tout professionnel DevOps gérant des infrastructures de production.

## Objectifs pédagogiques

À l'issue de cette séance, les apprenants seront capables de :

### Compétences techniques

- Analyser et gérer les processus système Linux
- Configurer et déployer des services systemd en production
- Surveiller les ressources système (CPU, mémoire, disque, réseau)
- Analyser les logs système avec journalctl et outils forensiques
- Automatiser la maintenance avec les timers systemd

### Compétences DevOps

- Déployer des applications comme services système
- Implémenter une surveillance proactive des infrastructures
- Diagnostiquer et résoudre les incidents de production
- Appliquer les bonnes pratiques de sécurité systemd

## Structure du contenu

### Cours principal

- **Fichier :** `cours/S1_S1_Seance2_Gestion_Processus_Services.md`
- **Durée :** 2h30 de formation théorique et pratique
- **Approche :** Concepts intégrés avec démonstrations pratiques

### Travaux pratiques

#### LAB 1 - Analyse des processus système

- **Énoncé :** Intégré dans le cours (section 2.4)
- **Correction :** `labs/corrections/S1_S1_S1_lab1_analyse_processus_correction.sh`
- **Objectif :** Maîtriser l'analyse et la surveillance des processus Linux
- **Outils :** ps, top, htop, kill, jobs, nohup

#### LAB 2 - Déploiement de services systemd

- **Énoncé :** Intégré dans le cours (section 4.5)
- **Correction :** `labs/corrections/S1_S1_S1_lab2_gestion_services_correction.sh`
- **Objectif :** Créer et gérer des services systemd complets
- **Livrables :** Service web avec monitoring et maintenance automatisée

#### LAB 3 - Monitoring des ressources système

- **Énoncé :** Intégré dans le cours (section 5.4)
- **Correction :** `labs/corrections/S1_S1_S1_lab3_monitoring_ressources_correction.sh`
- **Objectif :** Implémenter une surveillance complète des ressources
- **Fonctionnalités :** Alertes automatiques, rapports, surveillance continue

#### LAB 4 - Analyse des logs système

- **Énoncé :** Intégré dans le cours (section 6.4)
- **Correction :** `labs/corrections/S1_S1_S1_lab4_analyse_logs_correction.sh`
- **Objectif :** Maîtriser l'analyse forensique des logs
- **Cas d'usage :** Détection d'incidents, analyse de sécurité, troubleshooting

### 📝 Évaluation

- **Quiz :** `quiz/S1_S1_S1_quiz_gestion_processus_services.md`
- **Format :** QCM + questions pratiques + études de cas
- **Durée :** 45 minutes
- **Seuil de réussite :** 70%

## Prérequis techniques

### Connaissances requises

- Bases Linux (navigation, fichiers, permissions)
- Notions de programmation (variables, scripts bash)
- Concepts réseau de base

### Environnement technique

- Distribution Linux (Ubuntu/CentOS/Debian)
- Accès root ou sudo
- Terminal avec bash
- Connexion internet pour téléchargements

### Outils utilisés

- **Gestion processus :** ps, top, htop, kill, pgrep, pkill
- **Services :** systemctl, journalctl, systemd
- **Monitoring :** vmstat, iostat, free, df, netstat
- **Logs :** journalctl, grep, awk, sed, tail

## Approche pédagogique

### Méthode d'enseignement

- **70% pratique / 30% théorie** pour maximiser l'apprentissage
- Démonstrations en direct avec explications
- Exercices progressifs du simple au complexe
- Cas d'usage réels tirés de la production

### Différenciation pédagogique

- **Débutants :** Focus sur les concepts de base avec exemples guidés
- **Intermédiaires :** Exercices autonomes avec validation
- **Avancés :** Défis additionnels et optimisations

### Validation des acquis

- Checkpoints réguliers pendant les LABs
- Peer-review entre apprenants
- Démonstration des réalisations en fin de séance

## Calendrier détaillé

| Temps     | Activité                     | Type       | Contenu                                       |
| --------- | ---------------------------- | ---------- | --------------------------------------------- |
| 0h00-0h30 | Introduction processus       | Cours      | Concepts de base, états des processus         |
| 0h30-1h00 | LAB 1 - Analyse processus    | Pratique   | Commandes ps, top, gestion signaux            |
| 1h00-1h15 | **PAUSE**                    |            |                                               |
| 1h15-1h45 | Services systemd             | Cours      | Architecture, configuration, bonnes pratiques |
| 1h45-2h30 | LAB 2 - Déploiement service  | Pratique   | Création service complet avec monitoring      |
| 2h30-2h45 | **PAUSE**                    |            |                                               |
| 2h45-3h15 | Monitoring ressources        | Cours      | Outils, métriques, alertes                    |
| 3h15-4h00 | LAB 3 - Surveillance système | Pratique   | Implémentation monitoring automatisé          |
| 4h00-4h15 | **PAUSE**                    |            |                                               |
| 4h15-4h45 | Analyse des logs             | Cours      | journalctl, techniques forensiques            |
| 4h45-5h30 | LAB 4 - Forensique logs      | Pratique   | Détection incidents, rapports                 |
| 5h30-6h15 | Quiz et synthèse             | Évaluation | Validation des acquis                         |

## Livrables attendus

### Pour chaque apprenant

1. **Scripts d'analyse de processus** fonctionnels et documentés
2. **Service systemd complet** avec fichier de configuration et scripts de maintenance
3. **Système de monitoring** avec alertes et rapports automatisés
4. **Outils d'analyse de logs** avec détection d'incidents

### Critères de qualité

- **Fonctionnalité :** Scripts exécutables sans erreur
- **Documentation :** Code commenté et README explicatif
- **Bonnes pratiques :** Respect des standards Linux et systemd
- **Sécurité :** Application des directives de sécurisation

## Dépannage et support

### Problèmes fréquents

- **Permissions :** Utiliser sudo pour les opérations système
- **Services :** Vérifier les logs avec journalctl en cas d'échec
- **Monitoring :** S'assurer que les outils de surveillance sont installés
- **Logs :** Adapter les chemins selon la distribution Linux

### Ressources d'aide

- Documentation intégrée dans chaque LAB
- Scripts de diagnostic fournis dans les corrections
- Support formateur pendant les exercices pratiques

## Évaluation et progression

### Critères d'évaluation

- **Compréhension technique (40%)** : Maîtrise des concepts et outils
- **Mise en pratique (40%)** : Qualité des réalisations LAB
- **Analyse et résolution (20%)** : Capacité de troubleshooting

### Validation des compétences

- **Acquis** : Quiz ≥ 70% + LABs fonctionnels
- **En cours** : Quiz 50-69% + LABs partiels
- **Non acquis** : Quiz < 50% ou LABs non fonctionnels

### Remédiation

- Sessions de rattrapage individualisées
- Exercices complémentaires ciblés
- Accompagnement renforcé sur les points de difficulté

## Perspectives et suite

### Compétences développées

Cette séance prépare aux formations avancées :

- **Orchestration** (Kubernetes, Docker Swarm)
- **Monitoring avancé** (Prometheus, Grafana)
- **Automatisation** (Ansible, CI/CD)
- **Sécurité** (Hardening, audit)

### Applications professionnelles

- Administration système en production
- Déploiement d'applications microservices
- Surveillance d'infrastructures critiques
- Incident response et forensique

---

## Contact et support

**Formateur :** Équipe DevOps Simplon
**Email :** support@formation-devops.fr
**Documentation :** Framework HASSAN - Standards de formation DevOps
