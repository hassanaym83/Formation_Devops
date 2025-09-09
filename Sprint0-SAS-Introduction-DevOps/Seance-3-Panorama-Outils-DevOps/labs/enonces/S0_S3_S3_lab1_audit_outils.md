# LAB 1 - Audit et Analyse d'Écosystème d'Outils DevOps

**Séance 3 - Panorama des Outils DevOps**  
**Durée estimée :** 15 minutes  
**Prérequis :** Compréhension de la segmentation de l'écosystème DevOps et des acteurs majeurs vus en cours

---

## Objectif

Analyser l'écosystème d'outils actuel d'une organisation selon la segmentation par phases DevOps, identifier les gaps, et proposer une stratégie d'amélioration basée sur les acteurs majeurs du marché.

---

## Contexte

**InnovateTech** est une PME de développement logiciel de 150 employés spécialisée dans les solutions B2B. L'entreprise a grandi rapidement et utilise aujourd'hui un ensemble d'outils disparates sans stratégie d'intégration globale.

**Situation actuelle :**

L'entreprise utilise actuellement :

- **Gestion de projet :** Trello (équipe marketing), Jira (équipe dev), Excel (management)
- **Code source :** GitHub (projets récents), Subversion SVN (legacy)
- **Communication :** Slack, email, réunions physiques
- **Build/CI :** Scripts manuels, quelques projets sur Jenkins
- **Tests :** Tests manuels principalement, JUnit sur certains projets
- **Déploiement :** FTP manuel, scripts bash custom
- **Monitoring :** Logs serveur, alertes email basiques

**Enjeux business :**

- Processus de livraison lents (2-3 semaines)
- Erreurs fréquentes en production
- Difficulté à tracer les changements
- Outils non intégrés, ressaisie manuelle
- Pas de visibilité globale sur les projets

---

## Instructions

### Étape 1 : Cartographie selon la segmentation DevOps (5 minutes)

**1.1 Positionnement des outils actuels**

Complétez le tableau selon la segmentation par phases DevOps vue en cours :

| Phase DevOps | Outils actuels InnovateTech | Niveau couverture (1-5) | Acteurs majeurs disponibles         |
| ------------ | --------------------------- | ----------------------- | ----------------------------------- |
| **PLAN**     | ********\_\_********        | \_\_\_/5                | Jira, Trello, Azure Boards          |
| **CODE**     | ********\_\_********        | \_\_\_/5                | GitHub, GitLab, Bitbucket           |
| **BUILD**    | ********\_\_********        | \_\_\_/5                | Jenkins, GitLab CI, Azure DevOps    |
| **TEST**     | ********\_\_********        | \_\_\_/5                | Selenium, Jest, SonarQube           |
| **RELEASE**  | ********\_\_********        | \_\_\_/5                | Nexus, Artifactory, Docker Registry |
| **DEPLOY**   | ********\_\_********        | \_\_\_/5                | Ansible, Terraform, Kubernetes      |
| **OPERATE**  | ********\_\_********        | \_\_\_/5                | Prometheus, AWS CloudWatch          |
| **MONITOR**  | ********\_\_********        | \_\_\_/5                | ELK Stack, DataDog, New Relic       |

**1.2 Analyse de maturité globale**

Score de maturité global InnovateTech : **_/40 (_**%)

**Phases critiques (score ≤ 2) :**

- ***
- ***
- ***

### Étape 2 : Analyse des gaps et opportunités (5 minutes)

**2.1 Classification des problèmes**

**Redondances fonctionnelles :**
Liste des outils qui font double emploi :

1. ***
2. ***
3. ***

**Ruptures de chaîne :**
Points où l'information ne passe pas automatiquement :

1. ********\_******** → ********\_********
2. ********\_******** → ********\_********
3. ********\_******** → ********\_********

**Phases manquantes :**
Phases sans outil dédié :

1. ***
2. ***

**2.2 Impact organisationnel**

**Estimation des coûts cachés :**

- Temps perdu/développeur/jour : **\_** heures
- Incidents production/mois liés aux outils : **\_**
- Délai moyen livraison client : **\_** semaines

### Étape 3 : Stratégie d'amélioration par acteurs (3 minutes)

**3.1 Choix de stratégie d'écosystème**

Sélectionnez et justifiez la stratégie optimale pour InnovateTech :

**Option A - Plateforme intégrée unique :**
□ Microsoft (Azure DevOps + GitHub)
□ Atlassian (Jira + Bitbucket + Bamboo)
□ GitLab (Platform DevOps complète)

**Option B - Best-of-breed avec intégrations :**
□ Jenkins + GitHub + outils spécialisés
□ Outils open source intégrés
□ Solutions cloud natives

**Choix recommandé :** ********\_********

**Justification :**

---

**3.2 Phases prioritaires à traiter**

Classez les 3 phases les plus urgentes à améliorer :

**Priorité 1 :** ********\_********
**Justification :** ********\_********

**Priorité 2 :** ********\_********
**Justification :** ********\_********

**Priorité 3 :** ********\_********
**Justification :** ********\_********

### Étape 4 : Plan d'action immédiat (2 minutes)

**4.1 Actions quick wins (< 1 mois)**

Actions rapides pour améliorer immédiatement la situation :

1. ***
2. ***
3. ***

**4.2 Métriques de succès**

Indicateurs pour mesurer l'amélioration :

- **Productivité :** ********\_********
- **Qualité :** ********\_********
- **Délais :** ********\_********

---

## Critères d'évaluation

| Critère                          | Points    | Description                                                    |
| -------------------------------- | --------- | -------------------------------------------------------------- |
| **Cartographie et segmentation** | 2 pts     | Positionnement correct selon phases DevOps et analyse maturité |
| **Analyse des gaps**             | 2 pts     | Identification pertinente des problèmes et impact business     |
| **Stratégie d'amélioration**     | 1 pt      | Recommandations cohérentes avec acteurs majeurs                |
| **TOTAL**                        | **5 pts** |                                                                |

---

## Aide-mémoire

**Segmentation écosystème DevOps :**

- **8 phases principales** : Plan → Code → Build → Test → Release → Deploy → Operate → Monitor
- **500+ outils spécialisés** dans l'écosystème global
- **Évolution constante** avec nouvelles technologies

**Acteurs majeurs :**

- **Plateformes intégrées :** Microsoft, Atlassian, GitLab, Google
- **Solutions open source :** Jenkins, Docker, Kubernetes, Prometheus
- **Approches hybrides :** Combinaison platform + best-of-breed

**Critères d'évaluation :**

- **Couverture fonctionnelle** par phase
- **Niveau d'intégration** entre outils
- **Maturité organisationnelle** pour adoption

---

_InnovateTech compte sur votre expertise pour optimiser son écosystème d'outils DevOps !_
