# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 1 - Séance 4 : Réseaux Architecture

## Objectifs pédagogiques

À la fin de cette séance, les participants seront capables de :

### Objectifs principaux

- **Comprendre** les concepts d'adressage IP et de masques CIDR
- **Calculer** et **planifier** des sous-réseaux optimisés
- **Concevoir** des architectures réseau multi-environnements
- **Appliquer** les bonnes pratiques de segmentation réseau
- **Réaliser** des projets complexes d'architecture réseau

## Objectifs techniques

### Compétences DevOps visées

- **Network Design** : Conception d'architectures réseau évolutives
- **Planning** : Planification d'adressage et de croissance
- **Segmentation** : Isolation et sécurisation par segments
- **Documentation** : Plans d'adressage et architectures techniques

## Table des matières

1. [Concepts de base IP et CIDR](#1-concepts-de-base-ip-et-cidr)
2. [Configuration et routage réseau](#2-configuration-et-routage-réseau)
3. [Architecture multi-environnements](#3-architecture-multi-environnements)
4. [Challenge : Segmentation réseau complexe](#4-challenge-segmentation-réseau-complexe)
5. [Quiz de validation](#5-quiz-de-validation)
6. [Récapitulatif et prochaines étapes](#6-récapitulatif-et-prochaines-étapes)
7. [Ressources complémentaires](#7-ressources-complémentaires)

## 1. Concepts de base IP et CIDR

### 1.1 Vue d'ensemble

Introduction aux adresses IP, masques de sous-réseau et notation CIDR pour comprendre l'adressage réseau moderne.

**Durée :** 15 minutes  
**Niveau :** Débutant  
**Outils :** `ipcalc`, `ip addr show`

### 1.2 Application pratique

**LAB 1** - Concepts de base IP et CIDR : `S1_S1_S4_lab1_concepts_ip_cidr.sh`

**Objectif :** Découvrir les concepts de base des adresses IP et des masques CIDR en utilisant des commandes Linux simples.

**Contexte :** Apprentissage des fondamentaux de l'adressage IP nécessaires pour tout administrateur réseau.

**Instructions :**

- Comprendre la structure des adresses IP
- Utiliser l'outil ipcalc pour les calculs réseau
- Réaliser des exercices pratiques de calcul CIDR
- Valider sa compréhension avec un quiz intégré

**Critères d'évaluation :**

- Compréhension correcte des concepts IP/CIDR (40%)
- Utilisation appropriée des outils de calcul (30%)
- Réponses correctes aux exercices pratiques (30%)

**Durée estimée :** 15 minutes

## 2. Configuration et routage réseau

### 2.1 Vue d'ensemble

Exploration de la configuration réseau locale et compréhension des tables de routage pour diagnostiquer et configurer les connexions réseau.

**Durée :** 20 minutes  
**Niveau :** Intermédiaire  
**Outils :** `ip route show`, `ss`, `ping`, `traceroute`

### 2.2 Application pratique

**LAB 2** - Configuration routage : `S1_S1_S4_lab2_configuration_routage.sh`

**Objectif :** Comprendre et analyser la configuration réseau d'une machine Linux avec les outils modernes.

**Contexte :** Diagnostic réseau essentiel pour identifier et résoudre les problèmes de connectivité dans un environnement professionnel.

**Instructions :**

- Analyser la configuration IP actuelle
- Examiner les tables de routage
- Tester la connectivité réseau
- Identifier les interfaces et services réseau actifs

**Critères d'évaluation :**

- Analyse correcte de la configuration réseau (35%)
- Utilisation appropriée des commandes de diagnostic (35%)
- Interprétation des résultats de connectivité (30%)

**Durée estimée :** 20 minutes

## 3. Architecture multi-environnements

### 3.1 Vue d'ensemble

Conception de plans d'adressage pour des environnements d'entreprise avec segmentation par fonction métier et planification de la croissance.

**Durée :** 25 minutes  
**Niveau :** Intermédiaire  
**Outils :** `ipcalc`, calculateurs de sous-réseaux

### 3.2 Application pratique

**LAB 3** - Architecture multi-environnements : `S1_S1_S4_lab3_architecture_multi_environnements.sh`

**Objectif :** Concevoir un plan d'adressage complet pour une entreprise avec plusieurs environnements et services.

**Contexte :** Planification réseau réaliste pour une startup tech en croissance nécessitant une architecture évolutive.

**Instructions :**

- Analyser les besoins par environnement (dev/test/prod)
- Calculer les sous-réseaux optimaux
- Planifier la croissance future
- Documenter l'architecture proposée

**Critères d'évaluation :**

- Pertinence de la segmentation proposée (40%)
- Optimisation des calculs de sous-réseaux (30%)
- Anticipation de l'évolution future (30%)

**Durée estimée :** 25 minutes

## 4. Challenge : Segmentation réseau complexe

### 4.1 Vue d'ensemble

Projet avancé de conception d'une architecture réseau complète pour un environnement critique avec contraintes de sécurité et conformité.

**Durée :** 30 minutes  
**Niveau :** Avancé  
**Outils :** `ipcalc`, outils de planification réseau

### 4.2 Application pratique

**LAB 4 CHALLENGE** - Segmentation réseau hôpital : `S1_S1_S4_lab4_challenge_segmentation.sh`

**Objectif :** Concevoir une architecture réseau complète pour un hôpital avec contraintes de sécurité, évolutivité et conformité RGPD.

**Contexte :** Mission complexe de segmentation réseau pour un environnement critique nécessitant isolation des équipements médicaux, protection des données patients et conformité réglementaire.

**Instructions :**

- Analyser les besoins complexes par segment métier
- Concevoir une segmentation sécurisée (7 segments)
- Appliquer les contraintes de conformité RGPD
- Planifier l'évolution sur 5 ans
- Documenter l'architecture complète

**Critères d'évaluation :**

- Pertinence de l'analyse des besoins (25%)
- Qualité de la segmentation sécurisée (25%)
- Conformité aux exigences réglementaires (25%)
- Documentation technique complète (25%)

**Durée estimée :** 30 minutes

## 5. Quiz de validation

**Quiz Séance 4** : `S1_S1_S4_quiz_reseaux_architecture.py`

**Validation des acquis** : 15 questions - Seuil de validation : 11/15 (72%)  
**Durée maximale :** 15 minutes

Couvre tous les concepts de la séance :

- Adressage IP et notation CIDR
- Calculs de sous-réseaux
- Commandes de diagnostic réseau
- Planification d'architecture réseau
- Bonnes pratiques de segmentation

## 6. Récapitulatif et prochaines étapes

### Compétences acquises

- Maîtrise des concepts d'adressage IP et CIDR
- Capacité à planifier des architectures réseau évolutives
- Compétences en diagnostic et configuration réseau
- Compréhension des enjeux de segmentation sécurisée

### Préparation séance suivante

La **Séance 5 - Réseaux Sécurité** s'appuiera sur ces fondements pour :

- Configurer des firewalls et règles de sécurité
- Sécuriser les accès SSH
- Implémenter du monitoring réseau
- Automatiser la surveillance sécurisée

## 7. Ressources complémentaires

### Documentation technique

- [RFC 1918 - Address Allocation for Private Internets](https://tools.ietf.org/html/rfc1918)
- [Guide CIDR et sous-réseaux](https://www.subnet-calculator.com/)
- [Linux Network Administration Guide](https://tldp.org/LDP/nag2/index.html)

### Outils recommandés

- **ipcalc** : Calculateur de sous-réseaux en ligne de commande
- **Subnet Calculator** : Outils web pour planification réseau
- **Draw.io** : Création de diagrammes d'architecture réseau

### Standards et bonnes pratiques

- **RFC 1918** : Adresses IP privées
- **IEEE 802.1Q** : VLANs et segmentation
- **NIST Cybersecurity Framework** : Sécurisation réseau

---

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 4_
