# Brief Projet - Virtualisation et Automatisation DevOps

**Sprint 0 - Semaine 1 - Introduction à VirtualBox et Vagrant**

## Contexte du Projet

Vous êtes consultant DevOps dans une startup technologique qui développe une application web moderne. L'équipe de développement est composée de 8 développeurs travaillant sur différents systèmes d'exploitation (Windows, macOS, Linux) et rencontre des problèmes récurrents de compatibilité environnementale.

Les problématiques identifiées :

- Configurations différentes entre les postes de développement
- Difficultés à reproduire les bugs en local
- Temps de setup d'environnement trop long pour nouveaux développeurs
- Déploiements qui échouent à cause de différences environnementales

Votre mission est de standardiser l'environnement de développement en utilisant les technologies VirtualBox et Vagrant pour créer un environnement reproductible et distribué.

## Objectifs Pédagogiques

À l'issue de ce projet, vous devrez être capables de :

- Maîtriser les concepts fondamentaux de la virtualisation
- Créer et configurer des machines virtuelles avec VirtualBox
- Automatiser la création d'environnements avec Vagrant
- Gérer le cycle de vie complet des machines virtuelles
- Créer des configurations reproductibles et partageables
- Publier et distribuer des environnements standardisés via Vagrant Cloud
- Documenter et présenter une solution technique

## Livrables Attendus

### Livrable 1 : Infrastructure Multi-Machines avec Site Web et Base de Données

**Objectif** : Déployer deux machines virtuelles avec des rôles distincts et des systèmes d'exploitation différents

**Architecture de la solution** :

```
┌─────────────────┐    Réseau Public     ┌─────────────────┐
│   UTILISATEUR   │─────────────────────▶│   WEB SERVER    │
│                 │   (192.168.1.0/24)   │   (Ubuntu)      │
└─────────────────┘                      └─────────┬───────┘
                                                   │
                                         Réseau Privé
                                         (192.168.56.0/24)
                                                   │
                  Machine Physique                │
                  Port 3307                       │
                        ▲                         │
                        └─────────────────────────┼───────┐
                                         ┌─────────▼───────┐
                                         │  DATABASE       │
                                         │  (CentOS)       │
                                         └─────────────────┘
```

**Machine 1 : Web Server (Ubuntu 22.04)**

- **Nom** : `web-server`
- **OS** : Ubuntu 22.04 LTS
- **Services** :
  - Nginx (serveur web statique)
  - Site web depuis repository GitHub public au choix
- **Réseau** :
  - Public network (accès internet)
  - Private network IP : 192.168.56.10
- **Sync Folder** :
  - Dossier local `./website/` synchronisé avec `/var/www/html/`
  - Clone automatique d'un repository GitHub public
- **Accès** :
  - Site web accessible via l'IP publique de la machine
  - SSH disponible pour administration

**Machine 2 : Database Server (CentOS 9)**

- **Nom** : `db-server`
- **OS** : CentOS 9 Stream
- **Services** :
  - MySQL 8.0 (base de données)
  - Une seule table `users` avec données de démonstration
- **Réseau** :
  - Private network IP : 192.168.56.20
  - Port forwarding 3306 → 3307 pour accès depuis machine physique
- **Base de données** :
  - Database : `demo_db`
  - Table : `users` (id, nom, email, date_creation)
  - 5-10 utilisateurs de test pré-chargés
- **Accès** :
  - Consultation directe depuis machine physique via `localhost:3307`
  - Interface MySQL accessible en ligne de commande

**Structure de projet attendue** :

```
projet-infra-simple/
├── Vagrantfile
├── scripts/
│   ├── provision-web-ubuntu.sh
│   └── provision-db-centos.sh
├── website/
│   └── (contenu du repository GitHub cloné)
├── database/
│   ├── create-table.sql
│   └── insert-demo-data.sql
└── README.md
```

**Fonctionnalités requises dans le Vagrantfile** :

- Configuration multi-machines (web Ubuntu + db CentOS)
- Réseaux public et privé configurés
- Provisioning automatisé par machine et OS
- Synchronisation du dossier website
- Port forwarding pour accès base de données
- Variables paramétrables pour IP et ports

**Scripts de provisioning** :

- `provision-web-ubuntu.sh` : Installation Nginx, clone repo GitHub
- `provision-db-centos.sh` : Installation MySQL, création table users
- Configuration automatique des services
- Chargement des données de démonstration

**Critères de validation** :

- Les deux machines démarrent automatiquement avec `vagrant up`
- Site web accessible depuis navigateur via IP publique
- Base de données consultable depuis machine physique via `mysql -h localhost -P 3307`
- Communication réseau fonctionnelle entre les machines
- Provisioning automatique sans intervention manuelle
- Fichiers synchronisés entre hôte et machine web

### Livrable 2 : Distribution via Vagrant Cloud

**Objectif** : Packager et distribuer l'infrastructure complète sur Vagrant Cloud

**Étapes de réalisation** :

1. **Préparation des machines** :

   - Nettoyer et optimiser les deux machines virtuelles
   - Supprimer les fichiers temporaires et logs
   - Réduire la taille des disques virtuels
   - Valider le fonctionnement complet

2. **Packaging des boxes** :

   - Créer une box pour le serveur web Ubuntu : `vagrant package web-server --output ubuntu-web.box`
   - Créer une box pour le serveur base CentOS : `vagrant package db-server --output centos-db.box`
   - Tester les boxes localement avant publication

3. **Publication sur Vagrant Cloud** :

   - Créer un compte sur https://app.vagrantup.com/
   - Publier la box web : `username/ubuntu-web-server`
   - Publier la box database : `username/centos-mysql-db`
   - Configurer les métadonnées et descriptions

4. **Documentation complète** :
   - Instructions d'installation et d'utilisation
   - Exemples de Vagrantfile pour utiliser les boxes
   - Guide de configuration réseau
   - Procédures de troubleshooting

**Critères de validation** :

- Boxes téléchargeables publiquement depuis Vagrant Cloud
- Documentation claire et complète
- Test de déploiement depuis un autre poste
- Fonctionnalité complète après déploiement des boxes
- Versions correctement taguées et décrites

**Contenu de la documentation** :

- Architecture de l'infrastructure
- Prérequis système nécessaires
- Instructions de déploiement step-by-step
- Configuration des réseaux
- Accès aux services (web et database)
- Exemples d'utilisation et cas d'usage
- FAQ et résolution des problèmes courants

## Contraintes Techniques

### Spécifications des Machines Virtuelles

**Machine Web (Ubuntu)** :

- RAM : 1024 MB minimum
- CPU : 1 vCPU
- Disque dur : 20 GB allocation dynamique
- Réseau : Public network + Private network (192.168.56.10)

**Machine Database (CentOS)** :

- RAM : 1024 MB minimum
- CPU : 1 vCPU
- Disque dur : 20 GB allocation dynamique
- Réseau : Private network (192.168.56.20) + Port forwarding (3306→3307)

### Configuration Réseau

**Réseau Public** :

- Interface réseau en mode bridged ou NAT
- Accès internet pour la machine web
- IP automatique via DHCP

**Réseau Privé** :

- Sous-réseau : 192.168.56.0/24
- Machine web : 192.168.56.10
- Machine database : 192.168.56.20
- Communication inter-machines sécurisée

### Services et Sécurité

**Services requis** :

- Nginx configuré et démarré automatiquement sur Ubuntu
- MySQL configuré et démarré automatiquement sur CentOS
- SSH activé sur les deux machines
- Synchronisation de dossiers fonctionnelle

**Configuration sécurité** :

- Firewall configuré pour autoriser les ports nécessaires
- Utilisateurs non-root avec privilèges sudo
- Accès base de données sécurisé avec utilisateur dédié
- Logs système configurés

## Évaluation par Compétences

### Compétences du Référentiel DevOps Visées

Ce projet permet de valider les compétences suivantes du référentiel officiel DevOps :

**C1 - Définir un environnement de développement commun (Niveau 1)**

- Produire les sources nécessaires (Vagrantfile, scripts de provisioning)
- Choisir les outils de virtualisation (VirtualBox/Vagrant)
- Appliquer les principes d'Infrastructure as Code
- Automatiser l'installation de l'environnement

**C3 - Concevoir les éléments de configuration de l'infrastructure (Niveau 1)**

- Utiliser un gestionnaire de configuration (Vagrant)
- Automatiser les actions de gestion et provisionnement
- Configurer l'infrastructure de manière reproductible

### Critères de Validation par Compétence

#### **C1 - Définir un environnement de développement commun** VALIDE/NON VALIDE

**Niveau 1 - Fondamentaux**

**Critères de validation** :

- [ ] Le Vagrantfile définit un environnement reproductible multi-machines
- [ ] Les sources de configuration sont versionnées et documentées
- [ ] L'infrastructure as code est appliquée (déclaratif vs impératif)
- [ ] L'installation est entièrement automatisée avec `vagrant up`

**Livrables attendus** :

- Vagrantfile multi-machines fonctionnel
- Scripts de provisioning pour Ubuntu et CentOS
- Documentation de l'architecture et des choix techniques
- Démonstration de la reproductibilité

**Modalités de validation** :

- Démonstration en direct du déploiement automatique
- Test de reproductibilité sur un autre poste
- Vérification du respect des principes Infrastructure as Code
- Validation de la documentation des choix techniques

#### **C3 - Concevoir les éléments de configuration de l'infrastructure** VALIDE/NON VALIDE

**Niveau 1 - Fondamentaux**

**Critères de validation** :

- [ ] La configuration utilise Vagrant comme gestionnaire
- [ ] Les actions de provisionnement sont automatisées
- [ ] La configuration réseau et services est déclarative
- [ ] L'infrastructure est gérée de manière collaborative
- [ ] L'infrastructure est gérée de manière collaborative

**Livrables attendus** :

- Configuration Vagrant déclarative et versionnée
- Scripts de provisioning automatisés
- Architecture réseau et services documentée
- Procédures de gestion d'infrastructure

**Modalités de validation** :

- Revue de la configuration et architecture
- Test des procédures de provisionnement
- Validation de l'approche déclarative
- Vérification de la gestion collaborative (Git)

### Validation Globale du Projet

**Statut de validation** : VALIDE / NON VALIDE

**Conditions de validation** :

- **Les 2 compétences (C1 et C3) doivent être validées** pour obtenir la validation globale
- En cas de compétence non validée, des actions correctives seront définies
- Une nouvelle évaluation sera programmée après correction

**Actions en cas de non-validation** :

1. **Analyse des lacunes** avec le formateur référent
2. **Plan d'amélioration** personnalisé par compétence
3. **Accompagnement technique** ciblé sur les points faibles
4. **Nouvelle tentative** avec délai adapté selon les besoins

## Ressources et Documentation

### Exemples de Repositories GitHub

**Sites web statiques recommandés** :

- Bootstrap templates : https://github.com/startbootstrap
- Portfolio sites : https://github.com/topics/portfolio-website
- Landing pages : https://github.com/topics/landing-page
- Documentation sites : https://github.com/topics/documentation

### Commandes Essentielles

**Gestion multi-machines** :

```bash
# Démarrage de toutes les machines
vagrant up

# Démarrage d'une machine spécifique
vagrant up web-server
vagrant up db-server

# Connexion SSH à une machine
vagrant ssh web-server
vagrant ssh db-server

# Statut des machines
vagrant status

# Arrêt des machines
vagrant halt
```

**Test de la base de données** :

```bash
# Depuis la machine physique
mysql -h localhost -P 3307 -u root -p

# Consulter la table users
USE demo_db;
SELECT * FROM users;
```

**Packaging et distribution** :

```bash
# Création des boxes
vagrant package web-server --output ubuntu-web.box
vagrant package db-server --output centos-db.box

# Test local des boxes
vagrant box add test/ubuntu-web ubuntu-web.box
vagrant box add test/centos-db centos-db.box

# Publication sur Vagrant Cloud
vagrant cloud auth login
vagrant cloud publish username/ubuntu-web-server 1.0.0 virtualbox ubuntu-web.box
```

**Scripts de provisioning Web Server** :

- Installation et configuration Nginx
- Installation Python 3.9+ et pip
- Déploiement de l'API Flask
- Configuration du reverse proxy
- Setup des logs et monitoring

**Scripts de provisioning Database Server** :

- Installation et sécurisation MySQL
- Création des bases et utilisateurs
- Chargement des données de démonstration
- Configuration des sauvegardes automatiques
- Optimisation des performances

**API REST fonctionnelle** :

- Endpoints CRUD complets
- Authentification basique
- Gestion des erreurs HTTP
- Documentation automatique
- Tests unitaires intégrés

**Dashboard web interactif** :

- Interface utilisateur moderne
- Graphiques en temps réel
- Gestion des utilisateurs
- Monitoring système
- Design responsive

### Livrable 3 : Distribution via Vagrant Cloud

**Objectif** : Packager et distribuer l'infrastructure complète

**Packaging de l'infrastructure** :

- Création de deux boxes séparées (web et db)
- Ou création d'une box multi-machines
- Optimisation des tailles de boxes
- Tests de déploiement automatisé

**Publication sur Vagrant Cloud** :

- Box `username/devops-api-web` pour le serveur web
- Box `username/devops-api-db` pour la base de données
- Documentation détaillée de l'architecture
- Instructions de déploiement et configuration

**Validation complète** :

- Test de déploiement sur machine vierge
- Vérification de la communication inter-machines
- Test des fonctionnalités API et dashboard
- Validation de la sécurité réseau

**Documentation avancée** :

- Guide d'architecture et choix techniques
- Documentation API avec exemples
- Procédures de maintenance et backup
- Guide de troubleshooting

## Critères de Validation

### Tests Fonctionnels

**Communication réseau** :

- Machine web accessible depuis l'hôte via réseau public
- Communication web ↔ db via réseau privé uniquement
- Isolation de la base de données (pas d'accès externe)

**API REST fonctionnelle** :

- `GET http://192.168.1.X/api/users` retourne la liste des utilisateurs
- `POST http://192.168.1.X/api/users` permet de créer un utilisateur
- `GET http://192.168.1.X/api/stats` affiche les métriques système
- Dashboard accessible via `http://192.168.1.X/dashboard`

**Base de données opérationnelle** :

- MySQL accessible uniquement depuis la machine web
- Données de démonstration chargées automatiquement
- Sauvegardes automatiques configurées
- Logs de performance activés

**Déploiement automatisé** :

- `vagrant up` déploie les deux machines automatiquement
- Provisioning complet sans intervention manuelle
- Services démarrés et configurés automatiquement
- Communication inter-machines fonctionnelle

### Architecture et Sécurité

**Réseau sécurisé** :

- Base de données isolée sur réseau privé
- Firewall configuré sur les deux machines
- Accès SSH sécurisé avec clés
- Ports non nécessaires fermés

**Performance optimisée** :

- Ressources appropriées pour chaque machine
- Configuration MySQL optimisée
- Nginx configuré en reverse proxy
- Logs rotatifs configurés

## Ressources et Documentation

- Code et configuration exemplaires
- Innovation dans l'approche
- Optimisation des performances
- Sécurité renforcée

## Ressources et Documentation

### Documentation Officielle

**VirtualBox** :

- Manuel utilisateur : https://www.virtualbox.org/manual/
- Guide d'installation : https://www.virtualbox.org/wiki/Downloads
- FAQ et troubleshooting : https://www.virtualbox.org/wiki/User_FAQ

**Vagrant** :

- Documentation complète : https://www.vagrantup.com/docs
- Getting Started : https://learn.hashicorp.com/vagrant
- Providers et provisioning : https://www.vagrantup.com/docs/providers

**Vagrant Cloud** :

- Interface web : https://app.vagrantup.com/
- Documentation API : https://www.vagrantup.com/docs/vagrant-cloud
- Guide de publication : https://www.vagrantup.com/docs/vagrant-cloud/boxes

### Commandes Essentielles

**Gestion des machines virtuelles** :

```bash
# Initialisation du projet
vagrant init ubuntu/jammy64

# Démarrage de la VM
vagrant up

# Connexion SSH
vagrant ssh

# Arrêt de la VM
vagrant halt

# Destruction complète
vagrant destroy

# Rechargement avec nouveau Vagrantfile
vagrant reload

# Reprovisioning
vagrant provision
```

**Packaging et distribution** :

```bash
# Création du package
vagrant package --output nom-de-la-box.box

# Ajout local pour test
vagrant box add ma-box nom-de-la-box.box

# Authentification Vagrant Cloud
vagrant cloud auth login

# Publication sur Vagrant Cloud
vagrant cloud publish username/boxname version provider box-file.box
```

**Commandes de diagnostic** :

```bash
# Statut des VMs
vagrant global-status

# Informations détaillées
vagrant status

# Logs de démarrage
vagrant up --debug

# Validation Vagrantfile
vagrant validate
```

## Modalités de Rendu

### Format de Livraison

**Repository Git** :

- Code source complet et organisé
- Historique de commits significatifs
- Branches feature si applicable
- README principal avec instructions

**Archive ZIP** :

- Projet complet avec tous les fichiers
- Structure de dossiers respectée
- Fichiers de configuration inclus
- Documentation au format Markdown

**Lien Vagrant Cloud** :

- Box publiée et accessible publiquement
- Description et documentation complètes
- Version correctement taguée
- Métadonnées renseignées

**Vidéo de Démonstration** :

- Durée maximum : 5 minutes
- Démonstration du déploiement complet
- Explication des choix techniques
- Test de fonctionnalité en direct

### Planning et Échéances

**Échéances** :

- Date limite de rendu : Vendredi 17h00
- Présentation orale : Lundi suivant
- Durée présentation : 10 minutes par apprenant
- Questions/réponses : 5 minutes

**Jalons recommandés** :

- Lundi : Livrable 1 terminé
- Mercredi : Livrable 2 terminé
- Jeudi : Livrable 3 et documentation
- Vendredi : Tests finaux et rendu

### Présentation Orale

**Structure de présentation** :

1. Contexte et problématique (2 min)
2. Solution technique développée (4 min)
3. Démonstration en direct (3 min)
4. Retour d'expérience et difficultés (1 min)

**Questions de soutenance** :

- Expliquez la différence entre VirtualBox et Vagrant dans votre solution
- Quels sont les avantages du provisioning automatique pour une équipe ?
- Comment gérez-vous les versions de vos environnements ?
- Quel est l'intérêt de Vagrant Cloud pour une équipe DevOps ?
- Quelles améliorations pourriez-vous apporter à votre solution ?

## Support et Aide

### Ressources d'Aide

**Documentation de cours** :

- Section 3 : Concepts et workflow Vagrant
- Section 2 : Installation et configuration VirtualBox
- Exemples pratiques et cas d'usage

**Entraide collaborative** :

- Forum de classe pour questions techniques
- Sessions de pair programming encouragées
- Partage de ressources et bonnes pratiques

### Créneaux de Support

**Permanences formateur** :

- Mardi : 17h30 - 18h30
- Jeudi : 17h30 - 18h30
- Sur rendez-vous si nécessaire

**Types de support** :

- Aide au debugging technique
- Clarification des exigences
- Conseils méthodologiques
- Validation des approches

### Troubleshooting Commun

**Problèmes fréquents** :

- Conflits de ports réseau
- Problèmes de permissions SSH
- Erreurs de provisioning
- Configuration VirtualBox

**Solutions documentées** :

- Base de connaissances commune
- FAQ mise à jour régulièrement
- Procédures de résolution step-by-step

## Conclusion

Ce projet constitue votre première expérience pratique complète avec les outils de virtualisation et d'automatisation essentiels en DevOps. Il vous permettra de comprendre concrètement les enjeux de standardisation des environnements et l'importance de l'Infrastructure as Code.

Les compétences acquises durant ce projet seront directement réutilisables dans les sprints suivants, notamment pour la containerisation avec Docker et l'orchestration avec Kubernetes.

Prenez le temps de bien documenter votre travail et n'hésitez pas à expérimenter au-delà des exigences minimales. L'objectif est autant d'apprendre les outils que de développer une méthodologie de travail rigoureuse.

**Bon courage pour ce premier projet DevOps !**
