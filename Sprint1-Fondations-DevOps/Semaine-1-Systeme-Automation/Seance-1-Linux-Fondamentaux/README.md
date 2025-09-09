# Séance 1 - Linux Fondamentaux pour DevOps

## Vue d'ensemble

**Sprint:** 1 - Fondations DevOps 
**Semaine:** 2 - Système et Automation 
**Séance:** 1 - Linux Fondamentaux 
**Durée:** 7 heures 
**Niveau:** Débutant

## Objectifs pédagogiques

À l'issue de cette séance, l'apprenant sera capable de :

- **Naviguer efficacement** dans l'arborescence Linux selon la hiérarchie FHS
- **Gérer les fichiers et dossiers** avec les commandes essentielles
- **Configurer les permissions** selon les bonnes pratiques de sécurité
- **Manipuler les variables d'environnement** pour la configuration système
- **Appliquer les fondamentaux Linux** dans un contexte DevOps

## Contenu de la séance

### Cours magistral

- **Fichier:** `S1_S1_Seance1_Linux_Fondamentaux.md`
- **Durée:** 3 heures
- **Format:** Théorie avec exemples pratiques intégrés

#### Chapitres couverts :

1. **Introduction Linux et DevOps** (45 min)

 - Histoire et philosophie Linux
 - Importance pour l'écosystème DevOps
 - Distributions et cas d'usage

2. **Hiérarchie système de fichiers FHS** (45 min)

 - Structure standard Linux
 - Rôles des répertoires principaux
 - Navigation et localisation

3. **Commandes fondamentales** (45 min)

 - Navigation (`pwd`, `cd`, `ls`)
 - Gestion fichiers (`cp`, `mv`, `rm`, `mkdir`)
 - Consultation (`cat`, `less`, `head`, `tail`)

4. **Permissions et sécurité** (45 min)
 - Système de permissions rwx
 - Commandes `chmod`, `chown`, `chgrp`
 - Bonnes pratiques sécurité

### Travaux pratiques

#### LAB 1 - Navigation système

- **Fichier énoncé:** `S1_S1_S1_lab1_navigation_systeme.sh`
- **Fichier correction:** `S1_S1_S1_lab1_navigation_systeme_correction.sh`
- **Objectif:** Maîtriser la navigation FHS et l'analyse système
- **Durée:** 45 minutes

#### LAB 2 - Gestion fichiers

- **Fichier énoncé:** `S1_S1_S1_lab2_gestion_fichiers.sh`
- **Fichier correction:** `S1_S1_S1_lab2_gestion_fichiers_correction.sh`
- **Objectif:** Automatiser la création et gestion de projets web
- **Durée:** 60 minutes

#### LAB 3 - Permissions sécurité

- **Fichier énoncé:** `S1_S1_S1_lab3_permissions_securite.sh`
- **Fichier correction:** `S1_S1_S1_lab3_permissions_securite_correction.sh`
- **Objectif:** Sécuriser un serveur selon les bonnes pratiques
- **Durée:** 45 minutes

#### LAB 4 - Configuration environnement

- **Fichier énoncé:** `S1_S1_S1_lab4_env_config.sh`
- **Fichier correction:** `S1_S1_S1_lab4_env_config_correction.sh`
- **Objectif:** Configurer des environnements multi-plateformes
- **Durée:** 60 minutes

### 📝 Évaluation

- **Quiz interactif:** `S1_S1_S1_quiz_linux_fondamentaux.py`
- **Format:** 15 questions QCM avec explications
- **Durée:** 30 minutes
- **Seuil de validation:** 70% de bonnes réponses

## Prérequis techniques

### Système

- Accès à un environnement Linux (Ubuntu 20.04+ recommandé)
- Terminal avec droits utilisateur standard
- Connexion Internet pour téléchargements

### Connaissances

- Notions de base en informatique
- Familiarité avec l'interface de ligne de commande
- Concepts généraux de programmation (variables, fichiers)

## Compétences développées

### Techniques

- **Navigation système** : FHS, chemins, localisation
- **Gestion fichiers** : CRUD, arborescences, organisation
- **Sécurité** : Permissions, propriétés, audit
- **Configuration** : Variables, environnements, automation

### DevOps

- **Infrastructure as Code** : Scripts de configuration
- **Bonnes pratiques** : Sécurité, documentation, tests
- **Automation** : Processus répétables et fiables
- **Monitoring** : Surveillance et validation système

## Ressources pédagogiques

### Documentations

- [Linux FHS Standard](https://refspecs.linuxfoundation.org/fhs.shtml)
- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)

### Guides pratiques

- Linux Command Line Basics
- File Permissions Best Practices
- Environment Configuration Guide

## Déroulement type

| Horaire | Activité | Durée | Format |
| ----------- | ------------------------- | ------ | ---------- |
| 09:00-09:15 | Accueil et présentation | 15 min | Magistral |
| 09:15-10:00 | Introduction Linux/DevOps | 45 min | Magistral |
| 10:00-10:15 | Pause | 15 min | - |
| 10:15-11:00 | Hiérarchie FHS | 45 min | Magistral |
| 11:00-11:45 | LAB 1 - Navigation | 45 min | Pratique |
| 11:45-12:00 | Débriefing LAB 1 | 15 min | Échanges |
| 12:00-13:00 | Pause déjeuner | 60 min | - |
| 13:00-13:45 | Commandes fondamentales | 45 min | Magistral |
| 13:45-14:45 | LAB 2 - Gestion fichiers | 60 min | Pratique |
| 14:45-15:00 | Pause | 15 min | - |
| 15:00-15:45 | Permissions et sécurité | 45 min | Magistral |
| 15:45-16:30 | LAB 3 - Permissions | 45 min | Pratique |
| 16:30-16:45 | Pause | 15 min | - |
| 16:45-17:45 | LAB 4 - Configuration env | 60 min | Pratique |
| 17:45-18:15 | Quiz final | 30 min | Évaluation |
| 18:15-18:30 | Bilan et perspectives | 15 min | Magistral |

## Critères de validation

### Savoirs théoriques (30%)

- Compréhension de la hiérarchie FHS
- Maîtrise des commandes essentielles
- Principes de permissions Linux
- Configuration des variables d'environnement

### Savoir-faire pratiques (50%)

- Navigation efficace dans le système
- Gestion autonome des fichiers et dossiers
- Application correcte des permissions
- Configuration d'environnements multi-contextes

### Savoir-être professionnels (20%)

- Respect des bonnes pratiques sécuritaires
- Documentation des actions réalisées
- Approche méthodique et rigoureuse
- Adaptation aux contextes DevOps

## Continuité pédagogique

### Prérequis pour la séance suivante

- Maîtrise des commandes Linux de base
- Compréhension des permissions système
- Capacité à naviguer et configurer le système
- Automatisation simple par scripts

### Préparation Séance 2

- **Sujet :** Gestion des processus et services
- **Prérequis :** Tous les LABs de cette séance validés
- **Lecture :** Documentation systemd et gestion des processus

## Support et assistance

### Pendant la séance

- Formateur disponible pour questions techniques
- Entraide encouragée entre apprenants
- Documentation en ligne accessible

### Après la séance

- Corrections détaillées disponibles
- Ressources complémentaires fournies
- Session de rattrapage planifiable si nécessaire

---

**Formateur :** Support technique et pédagogique 
**Version :** 1.0 - Framework HASSAN 
**Dernière mise à jour :** Décembre 2024


