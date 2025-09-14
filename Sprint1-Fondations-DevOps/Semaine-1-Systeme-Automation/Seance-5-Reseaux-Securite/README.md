# Séance 5 : Réseaux - Configuration et Diagnostic

## Description de la séance

Cette séance se concentre sur la configuration pratique des interfaces réseau, la gestion avancée du routage, et les outils de diagnostic réseau en environnement DevOps. Elle complète la séance précédente sur les fondamentaux IP en abordant l'aspect opérationnel.

## Objectifs pédagogiques

- Configurer et gérer les interfaces réseau avec NetworkManager et outils système
- Implémenter des configurations réseau avancées (VLAN, bonding, bridging)
- Maîtriser les outils de diagnostic et troubleshooting réseau
- Automatiser la configuration réseau pour l'infrastructure DevOps

## Prérequis

- Séance 3 : Fondamentaux IP et architecture TCP/IP validée
- Connaissances des concepts d'adressage IP et CIDR
- Bases de l'administration système Linux

## Durée

**2 heures** (120 minutes)

- Cours théorique : 45 minutes
- LABs pratiques : 75 minutes (LAB 1: 20min, LAB 2: 25min, LAB 3: 30min)
- Quiz de validation : Post-séance (15 minutes)

## Structure de la séance

### Contenu théorique (45 minutes)

1. **Configuration des interfaces réseau**

   - NetworkManager vs configuration manuelle
   - Fichiers de configuration réseau (/etc/netplan, /etc/network/interfaces)
   - Configuration statique et DHCP

2. **Gestion avancée du routage**

   - Tables de routage multiples
   - Routage par politiques (Policy-based routing)
   - Métriques et priorités des routes

3. **Technologies réseau avancées**

   - VLAN (Virtual LAN) et configuration
   - Network bonding et agrégation de liens
   - Bridges et interfaces virtuelles

4. **Outils de diagnostic réseau**
   - Analyse du trafic (tcpdump, Wireshark)
   - Tests de connectivité avancés
   - Monitoring de la performance réseau

### Activités pratiques (75 minutes)

**LAB 1 - Configuration d'interfaces et routage** (20 minutes)

- Configuration d'interfaces multiples
- Mise en place de routes statiques
- Tests de connectivité inter-réseaux

**LAB 2 - VLAN et technologies avancées** (25 minutes)

- Configuration de VLAN tagged/untagged
- Mise en place d'un bridge réseau
- Tests de segmentation réseau

**LAB 3 - Diagnostic et troubleshooting** (30 minutes)

- Utilisation d'outils d'analyse réseau
- Résolution de problèmes de connectivité
- Monitoring de performance en temps réel

## Évaluation

### Système de points

- **LAB 1 :** 6 points (configuration interfaces/routage)
- **LAB 2 :** 8 points (VLAN et technologies avancées)
- **LAB 3 :** 16 points (diagnostic approfondi)
- **Quiz :** 15 points (15 questions, seuil 72%)

### Critères de validation

- **Séance validée :** 22/30 points sur les LABs (72%)
- **Quiz requis :** Post-séance pour validation des acquis

## Ressources pédagogiques

### Documentation de référence

- NetworkManager Documentation
- Linux Advanced Routing & Traffic Control HOWTO
- IEEE 802.1Q VLAN Standard
- Linux Bridge Documentation

### Outils utilisés

- NetworkManager (nmcli, nmtui)
- iproute2 (ip, ss, tc)
- tcpdump, Wireshark
- iftop, nethogs, nload
- bridge-utils, vlan

## Compétences développées

### Techniques

- Configuration réseau avancée Linux
- Diagnostic et troubleshooting réseau
- Implémentation VLAN et segmentation
- Automatisation des configurations réseau

### DevOps

- Configuration d'infrastructure réseau évolutive
- Monitoring et alerting réseau
- Sécurisation par segmentation réseau
- Automatisation des déploiements réseau

## Continuité pédagogique

### Liens avec séances précédentes

- **Séance 3 :** Fondamentaux IP et calculs réseau
- **Séance 4 :** Sécurité réseau et pare-feu

### Préparation séance suivante

- **Séance 6 :** Services avancés et automatisation
- Intégration réseau dans l'automatisation système

Cette séance établit les compétences opérationnelles nécessaires pour gérer efficacement les réseaux en environnement DevOps de production.
