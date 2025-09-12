# Séance 3 : Réseaux - Fondamentaux IP

## Description de la séance

Cette séance introduit les concepts fondamentaux des réseaux IP indispensables en DevOps. Elle couvre l'architecture TCP/IP, les adresses IP, la notation CIDR, et la subdivision de réseaux pour concevoir des architectures réseau DevOps sécurisées et évolutives.

## Objectifs pédagogiques

- Comprendre l'architecture réseau TCP/IP et les couches de communication
- Maîtriser les concepts d'adresses IP, masques de sous-réseau et notation CIDR
- Calculer et subdiviser des plages d'adresses IP pour l'infrastructure DevOps
- Appliquer les concepts de routage et résolution DNS dans des environnements professionnels

## Prérequis

- Connaissances de base en informatique
- Compréhension des concepts réseau élémentaires
- Bases mathématiques (puissances de 2, calculs binaires)

## Durée

**2 heures** (120 minutes)

- Cours théorique : 45 minutes
- LABs pratiques : 75 minutes (LAB 1: 15min, LAB 2: 20min, LAB 3: 20min)
- LAB 4 Challenge : Hors séance (30-45 minutes)
- Quiz de validation : Post-séance (15 minutes)

## Structure de la séance

### Contenu théorique (45 minutes)

1. **Modèle TCP/IP et architecture réseau**

   - 4 couches du modèle TCP/IP
   - Protocoles par couche et exemples DevOps
   - Analogies et schémas conceptuels

2. **Adresses IP et classes d'adresses**

   - Format IPv4 et représentation binaire
   - Adresses publiques vs privées (RFC 1918)
   - Classes traditionnelles A, B, C

3. **Masques de sous-réseau et notation CIDR**

   - Concept de masque binaire
   - Notation CIDR et équivalences
   - Calculs d'hôtes et de plages

4. **Subdivision de réseaux et calculs IP**

   - Méthodes de subdivision (subnetting)
   - VLSM (Variable Length Subnet Mask)
   - Optimisation de l'espace d'adressage

5. **Routage de base et tables de routage**

   - Concepts de routage IP
   - Types de routes (directe, statique, par défaut)
   - Analyse des tables de routage Linux

6. **Système DNS et résolution de noms**
   - Architecture hiérarchique DNS
   - Types d'enregistrements (A, CNAME, MX, PTR)
   - Processus de résolution et configuration

### Activités pratiques (75 minutes)

**LAB 1 - Exploration du modèle TCP/IP** (15 minutes)

- Analyse de scénarios réseau DevOps
- Identification des couches et protocoles
- Propositions d'optimisations infrastructure

**LAB 2 - Analyse d'adresses IP et classification** (20 minutes)

- Audit d'infrastructure DevOps multi-environnements
- Classification d'adresses (publique/privée/spéciale)
- Calculs de plages et propositions d'architecture

**LAB 3 - Calculs de masques et notation CIDR** (20 minutes)

- Conversions masques décimaux vers CIDR
- Calculs précis d'hôtes et de plages
- Conception d'architecture multi-environnements

**LAB 4 Challenge - Architecture réseau DevOps complète** (Hors séance)

- Conception VLSM optimale avec croissance anticipée
- Architecture de sécurité réseau multi-niveaux
- Stratégies d'évolutivité et de performance

## Évaluation

### Système de points

- **LAB 1 :** 5 points (concepts TCP/IP)
- **LAB 2 :** 5 points (classification IP)
- **LAB 3 :** 5 points (calculs CIDR)
- **LAB 4 Challenge :** 15 points (architecture avancée, hors séance)
- **Quiz :** 15 points (15 questions, seuil 72%)

### Critères de validation

- **Séance validée :** 11/15 points sur LABs 1-3 (72%)
- **Excellence :** 25+ points avec LAB 4 Challenge
- **Quiz requis :** Post-séance pour validation des acquis

## Ressources pédagogiques

### Documentation de référence

- RFC 791 : Internet Protocol (IPv4)
- RFC 1918 : Address Allocation for Private Internets
- RFC 4632 : Classless Inter-domain Routing (CIDR)
- RFC 1035 : Domain Names Implementation

### Outils recommandés

- Calculateurs IP : ipcalc, subnetmask.info
- Simulateurs réseau : GNS3, Packet Tracer
- Documentation Linux : man ip, man resolv.conf
- Standards DevOps : Network automation best practices

## Compétences développées

### Techniques

- Calculs d'adressage IP et CIDR
- Conception d'architectures réseau segmentées
- Analyse de tables de routage
- Configuration DNS de base
- Subdivision optimisée avec VLSM

### DevOps

- Segmentation réseau par environnements
- Sécurisation des communications inter-services
- Planification de l'évolutivité réseau
- Optimisation des performances réseau
- Best practices d'architecture infrastructure

## Continuité pédagogique

### Liens avec séances précédentes

- **Séance 1 :** Commandes réseau Linux de base
- **Séance 2 :** Services système et networking

### Préparation séance suivante

- **Séance 4 :** Configuration pratique des interfaces
- NetworkManager et outils de gestion réseau
- Diagnostic et troubleshooting avancé

Cette séance établit les fondements théoriques indispensables pour la configuration pratique des réseaux en environnement DevOps.
