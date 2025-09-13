# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 1 - Séance 4 : Réseaux - Architecture et Routage

## Objectifs pédagogiques

- Comprendre les concepts d'adressage IP et de masques de sous-réseaux pour la segmentation DevOps
- Maîtriser la configuration du routage Linux pour des architectures multi-réseaux
- Concevoir des architectures réseau adaptées aux environnements de développement et production
- Implémenter la segmentation réseau basique pour isoler les services DevOps

## Objectifs techniques

Adressage IP, CIDR, masques sous-réseaux, ip route, tables de routage, passerelles, segmentation réseau, architecture DevOps

## Table des matières

1. [Adressage IP et masques de sous-réseaux](#1-adressage-ip-et-masques-de-sous-réseaux)
2. [Configuration du routage Linux](#2-configuration-du-routage-linux)
3. [Architecture réseau pour DevOps](#3-architecture-réseau-pour-devops)
4. [Segmentation réseau pratique](#4-segmentation-réseau-pratique)
5. [Récapitulatif et prochaines étapes](#5-récapitulatif-et-prochaines-étapes)

---

## 1. Adressage IP et masques de sous-réseaux

### 1.1 Comprendre les adresses IP

**Définition** : Une adresse IP (Internet Protocol) est un identifiant numérique unique qui permet à un équipement de communiquer sur un réseau informatique.

**Analogie** : Une adresse IP est comme l'adresse postale de votre maison - elle indique précisément où vous vous trouvez sur le "réseau" des rues de votre ville.

**Format d'une adresse IPv4** :

- **Structure** : 4 nombres séparés par des points
- **Exemple** : 192.168.1.100
- **Plage** : Chaque nombre va de 0 à 255

**Composition** :

- **Partie réseau** : Identifie le réseau (comme le nom de la ville)
- **Partie hôte** : Identifie l'équipement spécifique (comme le numéro de maison)

### 1.2 Masques de sous-réseau et notation CIDR

**Définition du masque** : Le masque de sous-réseau détermine quelle partie de l'adresse IP identifie le réseau et quelle partie identifie l'équipement.

**Notation CIDR** : Notation compacte qui utilise /XX pour indiquer le nombre de bits du réseau.

**Exemples pratiques** :

```bash
# Notation complète vs CIDR
192.168.1.100 avec masque 255.255.255.0  =  192.168.1.100/24
192.168.0.50  avec masque 255.255.0.0    =  192.168.0.50/16
10.0.1.200    avec masque 255.0.0.0      =  10.0.1.200/8
```

**Calculs pratiques pour DevOps** :

- **/24** = 256 adresses (254 utilisables) → Petit bureau, équipe DevOps
- **/16** = 65536 adresses → Grande entreprise, datacenter
- **/8** = 16 millions d'adresses → Cloud provider, ISP

### 1.3 Plages d'adresses privées

**RFC 1918 - Adresses privées** pour réseaux internes :

```bash
# Classe A privée
10.0.0.0/8         # 10.0.0.0 à 10.255.255.255

# Classe B privée
172.16.0.0/12      # 172.16.0.0 à 172.31.255.255

# Classe C privée
192.168.0.0/16     # 192.168.0.0 à 192.168.255.255
```

**Usage DevOps typique** :

- **192.168.x.0/24** : Réseaux de développement, petites équipes
- **10.x.0.0/16** : Réseaux de production, cloud privé
- **172.16.x.0/24** : Réseaux de staging, intégration

### 1.4 Application pratique

📝 **LAB 1** - Calculs d'adressage IP : `S1_S1_S4_lab1_calculs_adressage.py`

**Énoncé du LAB 1** :

Votre équipe DevOps doit planifier l'architecture réseau d'une nouvelle infrastructure avec plusieurs environnements.

**Objectif** : Calculer et planifier l'adressage IP pour une infrastructure DevOps multi-environnements

**Contexte** : Nouvelle startup tech nécessitant des réseaux séparés pour dev, staging, et production

**Instructions** :

1. Calculez combien d'adresses sont disponibles dans 192.168.1.0/24
2. Déterminez combien d'équipements peuvent être connectés (adresses utilisables)
3. Planifiez la répartition pour 3 environnements :
   - Développement : 192.168.1.0/26 (64 adresses)
   - Staging : 192.168.1.64/26 (64 adresses)
   - Production : 192.168.1.128/26 (64 adresses)
4. Calculez les adresses de réseau, broadcast et plage utilisable pour chaque environnement
5. Proposez une adresse IP pour les serveurs suivants :
   - Serveur web de production
   - Base de données de staging
   - Serveur CI/CD de développement

**Critères d'évaluation** :

- Calculs d'adresses corrects (2 points)
- Planification environnements logique (2 points)
- Attribution IP serveurs appropriée (1 point)

**Durée estimée** : 15 minutes  
**Fichier de travail** : `S1_S1_S4_lab1_calculs_adressage.py`

---

## 2. Configuration du routage Linux

### 2.1 Comprendre le routage

**Définition** : Le routage est le processus qui détermine le chemin que doivent prendre les paquets réseau pour atteindre leur destination.

**Analogie** : Le routage est comme un GPS pour les données - il calcule le meilleur chemin pour que vos informations arrivent à destination sur le réseau.

**Types de routes** :

- **Route locale** : Communication dans le même réseau
- **Route par défaut** : Chemin vers Internet ou réseau externe
- **Route statique** : Chemin configuré manuellement par l'administrateur

### 2.2 Table de routage Linux

**Consulter la table de routage** :

```bash
# Voir toutes les routes
ip route show

# Voir la route par défaut
ip route show default

# Voir les routes vers un réseau spécifique
ip route show 192.168.1.0/24
```

**Exemple de table de routage** :

```bash
$ ip route show
default via 192.168.1.1 dev eth0 proto dhcp metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
```

**Explication** :

- **default via 192.168.1.1** : Passerelle par défaut (route vers Internet)
- **192.168.1.0/24 dev eth0** : Route locale directe via interface eth0
- **src 192.168.1.100** : Adresse source utilisée pour ce réseau

### 2.3 Ajouter et supprimer des routes

**Ajouter des routes statiques** :

```bash
# Ajouter une route vers un réseau spécifique
sudo ip route add 10.0.1.0/24 via 192.168.1.10 dev eth0

# Ajouter une route par défaut
sudo ip route add default via 192.168.1.1 dev eth0

# Route vers un serveur spécifique
sudo ip route add 172.16.10.5 via 192.168.1.20
```

**Supprimer des routes** :

```bash
# Supprimer une route spécifique
sudo ip route del 10.0.1.0/24 via 192.168.1.10

# Supprimer la route par défaut
sudo ip route del default via 192.168.1.1
```

### 2.4 Configuration persistante avec NetworkManager

**Méthode recommandée** - Routes via NetworkManager :

```bash
# Ajouter une route statique à une connexion existante
nmcli connection modify "prod-server" +ipv4.routes "10.0.1.0/24 192.168.1.10"

# Redémarrer la connexion pour appliquer
nmcli connection down "prod-server"
nmcli connection up "prod-server"

# Vérifier la configuration
nmcli connection show "prod-server" | grep routes
```

### 2.5 Application pratique

📝 **LAB 2** - Configuration de routage : `S1_S1_S4_lab2_configuration_routage.py`

**Énoncé du LAB 2** :

Votre infrastructure DevOps s'étend avec un nouveau datacenter. Vous devez configurer le routage pour permettre la communication entre les sites.

**Objectif** : Configurer des routes statiques pour connecter plusieurs réseaux DevOps

**Contexte** : Entreprise avec site principal (192.168.1.0/24) et nouveau datacenter (10.0.1.0/24)

**Instructions** :

1. Vérifiez votre table de routage actuelle avec `ip route show`
2. Identifiez votre passerelle par défaut actuelle
3. Ajoutez une route temporaire vers le réseau 10.0.1.0/24 via 192.168.1.254
4. Testez la nouvelle route avec `ping` (même si destination fictive)
5. Affichez la nouvelle table de routage pour confirmer l'ajout
6. Supprimez la route temporaire créée
7. Configurez la même route de manière persistante via NetworkManager
8. Documentez les commandes utilisées et les résultats obtenus

**Critères d'évaluation** :

- Consultation table de routage (1 point)
- Ajout/suppression de route temporaire (2 points)
- Configuration persistante NetworkManager (2 points)

**Durée estimée** : 20 minutes  
**Fichier de travail** : `S1_S1_S4_lab2_configuration_routage.py`

---

## 3. Architecture réseau pour DevOps

### 3.1 Principes d'architecture réseau DevOps

**Définition** : L'architecture réseau DevOps organise les ressources informatiques en zones logiques pour optimiser la sécurité, les performances et la gestion.

**Analogie** : Une architecture réseau DevOps est comme l'organisation d'un hôpital - différentes zones (urgences, chirurgie, consultation) sont séparées mais connectées selon leurs besoins de communication.

**Zones typiques DevOps** :

- **Zone développement** : Serveurs de dev, outils de test
- **Zone staging** : Environnement de pré-production
- **Zone production** : Applications et services en production
- **Zone management** : Outils d'administration et monitoring

### 3.2 Exemple d'architecture simple

**Infrastructure DevOps typique** :

```
Internet
   |
[192.168.1.1] -- Routeur/Firewall
   |
   +-- Réseau Management    : 192.168.10.0/24
   |   └── Monitoring       : 192.168.10.10
   |   └── CI/CD Server     : 192.168.10.20
   |
   +-- Réseau Development   : 192.168.20.0/24
   |   └── Dev Web Server   : 192.168.20.10
   |   └── Dev Database     : 192.168.20.20
   |
   +-- Réseau Production    : 192.168.30.0/24
       └── Prod Web Server  : 192.168.30.10
       └── Prod Database    : 192.168.30.20
```

**Avantages de cette séparation** :

- **Sécurité** : Isolation des environnements
- **Performance** : Trafic optimisé par usage
- **Gestion** : Administration simplifiée
- **Debugging** : Isolation des problèmes

### 3.3 Communication inter-réseaux

**Règles de communication typiques** :

```bash
# Management peut accéder à tout (monitoring)
# Development isolé de Production (sécurité)
# Production accessible depuis Management et Internet seulement
```

**Configuration réseau pour permettre ces règles** :

```bash
# Route depuis Management vers tous les réseaux
ip route add 192.168.20.0/24 via 192.168.1.1  # Vers Development
ip route add 192.168.30.0/24 via 192.168.1.1  # Vers Production

# Routes spécifiques selon besoins business
```

### 3.4 Application pratique

📝 **LAB 3** - Architecture réseau DevOps : `S1_S1_S4_lab3_architecture_devops.py`

**Énoncé du LAB 3** :

Vous devez concevoir l'architecture réseau complète pour une startup qui lance sa première application web avec des pratiques DevOps.

**Objectif** : Concevoir et documenter une architecture réseau DevOps complète avec segmentation

**Contexte** : Startup SaaS avec besoin de séparer développement, staging, production, et management

**Instructions** :

1. Concevez un plan d'adressage basé sur 192.168.0.0/16 avec 4 sous-réseaux /24
2. Attribuez les plages suivantes :
   - Management : 192.168.10.0/24
   - Development : 192.168.20.0/24
   - Staging : 192.168.30.0/24
   - Production : 192.168.40.0/24
3. Planifiez les adresses IP pour les serveurs :
   - Serveur web (dans chaque environnement)
   - Base de données (dans chaque environnement)
   - Serveur CI/CD (management)
   - Serveur monitoring (management)
4. Définissez les routes nécessaires pour que Management puisse accéder à tous les environnements
5. Créez un schéma textuel de votre architecture
6. Justifiez vos choix de segmentation pour cette startup

**Critères d'évaluation** :

- Plan d'adressage logique et cohérent (2 points)
- Attribution IP serveurs appropriée (2 points)
- Justification architecture DevOps (1 point)

**Durée estimée** : 20 minutes  
**Fichier de travail** : `S1_S1_S4_lab3_architecture_devops.py`

---

## 4. Segmentation réseau pratique

### 4.1 Concept de segmentation réseau

**Définition** : La segmentation réseau consiste à diviser un réseau en sous-réseaux plus petits pour améliorer la sécurité, les performances et la gestion.

**Analogie** : La segmentation réseau est comme diviser un grand bureau open-space en différents départements - chaque équipe a son espace dédié tout en pouvant communiquer avec les autres selon les besoins.

**Bénéfices pour DevOps** :

- **Isolation des pannes** : Un problème dans dev n'affecte pas prod
- **Sécurité renforcée** : Limitation des accès par zone
- **Performance optimisée** : Trafic local dans chaque segment
- **Gestion simplifiée** : Administration par environnement

### 4.2 Segmentation avec des interfaces multiples

**Configuration avec plusieurs interfaces** :

```bash
# Interface pour le réseau management
nmcli connection add type ethernet con-name "mgmt-net" ifname eth0 \
    ip4 192.168.10.100/24 gw4 192.168.10.1

# Interface pour le réseau production
nmcli connection add type ethernet con-name "prod-net" ifname eth1 \
    ip4 192.168.30.100/24

# Activation des connexions
nmcli connection up "mgmt-net"
nmcli connection up "prod-net"
```

### 4.3 Routage entre segments

**Routes pour communication inter-segments** :

```bash
# Permettre au serveur management d'accéder aux autres réseaux
sudo ip route add 192.168.20.0/24 via 192.168.10.1  # Vers development
sudo ip route add 192.168.30.0/24 via 192.168.10.1  # Vers production

# Route spécifique pour serveur critique
sudo ip route add 192.168.30.10/32 via 192.168.10.254
```

### 4.4 Vérification de la segmentation

**Tests de connectivité entre segments** :

```bash
# Test depuis management vers production
ping -c 3 192.168.30.10

# Test depuis management vers development
ping -c 3 192.168.20.10

# Vérifier que development ne peut pas atteindre production
# (nécessiterait configuration firewall - séance suivante)
```

### 4.5 Application pratique

📝 **LAB 4 - Challenge** - Segmentation réseau avancée : `S1_S1_S4_lab4_challenge_segmentation.py`

**Énoncé du LAB 4 Challenge (Hors séance - Bonus)** :

Ce challenge avancé simule la configuration complète d'une infrastructure réseau DevOps avec plusieurs segments et règles de routage complexes.

**Objectif** : Implémenter une segmentation réseau complète avec routage conditionnel pour une infrastructure DevOps

**Contexte** : Grande entreprise DevOps avec besoins de sécurité élevés et architecture multi-sites

**Instructions** :

1. Planifiez une architecture avec 5 segments réseau :
   - DMZ (servers publics) : 172.16.1.0/24
   - Management : 172.16.10.0/24
   - Development : 172.16.20.0/24
   - Staging : 172.16.30.0/24
   - Production : 172.16.40.0/24
2. Configurez plusieurs connexions NetworkManager simulant ces réseaux
3. Créez des routes statiques pour les communications autorisées :
   - Management → Tous les autres segments
   - DMZ → Internet uniquement
   - Development ↔ Staging (bidirectionnel)
   - Production isolée (Management uniquement)
4. Testez votre configuration avec des pings simulés
5. Créez un script de configuration automatique
6. Documentez les règles de communication et leur justification sécurité
7. Préparez une procédure de rollback en cas de problème
8. Simulez un troubleshooting avec routes cassées et leur réparation

**Critères d'évaluation** :

- Architecture réseau complexe et cohérente (4 points)
- Configuration NetworkManager multiple (3 points)
- Routes statiques appropriées (3 points)
- Script d'automatisation fonctionnel (2 points)
- Documentation sécurité complète (2 points)
- Procédure troubleshooting (1 point)

**Statut** : Activité bonus, hors des 2 heures de séance  
**Durée estimée** : 30-45 minutes  
**Fichier de travail** : `S1_S1_S4_lab4_challenge_segmentation.py`

---

## 5. Récapitulatif et prochaines étapes

### Concepts maîtrisés

- **Adressage IP et CIDR** : Calculs de sous-réseaux et planification d'infrastructure
- **Routage Linux** : Configuration et gestion des routes statiques
- **Architecture DevOps** : Segmentation logique des environnements
- **Communication inter-réseaux** : Routage entre segments pour besoins business

### Compétences DevOps acquises

- **Planification réseau** pour infrastructures multi-environnements
- **Configuration routage** pour connectivité inter-sites et cloud
- **Segmentation sécurisée** pour isolation des environnements critiques
- **Troubleshooting réseau** avec outils de diagnostic avancés

### Préparation séance suivante

La **Séance 5 : Sécurité réseau et monitoring** abordera :

- Configuration de pare-feu Linux (iptables/ufw)
- Sécurisation SSH pour administration distante
- Monitoring réseau et détection d'incidents
- Automatisation de la surveillance DevOps

### Architecture réseau et conteneurs

Ces concepts de routage et segmentation sont essentiels pour :

- **Docker networking** : Communication entre conteneurs
- **Kubernetes clusters** : Réseau de pods et services
- **Cloud networking** : VPC, subnets, security groups
- **Microservices** : Communication sécurisée entre services

### Bonnes pratiques retenues

- **Segmentation par environnement** : dev/staging/prod séparés
- **Routage minimal** : Ouvertures strictes selon besoins business
- **Documentation systématique** : Plans réseau à jour pour l'équipe
- **Tests réguliers** : Validation connectivité après chaque changement

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 4_
