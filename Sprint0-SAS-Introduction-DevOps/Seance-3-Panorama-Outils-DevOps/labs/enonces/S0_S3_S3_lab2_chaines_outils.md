# LAB 2 - Conception de Chaînes d'Outils DevOps

**Séance 3 - Panorama des Outils DevOps**  
**Durée estimée :** 20 minutes  
**Prérequis :** Compréhension des mécanismes d'intégration et patterns d'architecture vus en cours

---

## Objectif

Concevoir et analyser différentes chaînes d'outils DevOps en appliquant les mécanismes d'intégration (APIs, webhooks, message queues) et patterns d'architecture (Pipeline, Hub, Microservices) selon des contextes spécifiques.

---

## Contexte

**TechFlow Enterprises** doit moderniser son infrastructure DevOps pour 3 équipes produit distinctes ayant des besoins différents. L'objectif est de concevoir des chaînes d'outils adaptées à chaque contexte en appliquant les bonnes pratiques d'intégration.

**Équipes à équiper :**

1. **Équipe Web** - Application e-commerce critique, déploiements fréquents
2. **Équipe Mobile** - Applications iOS/Android, cycles de release coordonnés
3. **Équipe Data** - Pipelines ML, traitement batch, analytique temps réel

---

## Instructions

### Étape 1 : Analyse des mécanismes d'intégration (8 minutes)

**1.1 Équipe Web - Flux e-commerce**

**Contexte :** Application critique avec 100+ déploiements/jour, monitoring intensif requis.

**Complétez le tableau des intégrations :**

| Intégration Source → Cible | Mécanisme  | Justification  |
| -------------------------- | ---------- | -------------- |
| Git → Jenkins              | **\_\_\_** | ******\_****** |
| Jenkins → SonarQube        | **\_\_\_** | ******\_****** |
| Jenkins → Nexus            | **\_\_\_** | ******\_****** |
| Docker Hub → Kubernetes    | **\_\_\_** | ******\_****** |
| Prometheus → Slack         | **\_\_\_** | ******\_****** |
| Application → Logs ELK     | **\_\_\_** | ******\_****** |

**Questions d'analyse :**

a) Quel mécanisme utiliseriez-vous pour déclencher un rollback automatique si les métriques de performance dégradent après déploiement ?

**Mécanisme choisi :** ********\_********

**Justification :** ****************\_****************

b) Comment assurer la communication fiable entre le système de monitoring et les équipes de garde ?

**Solution proposée :** ****************\_****************

**1.2 Équipe Mobile - Coordination multi-plateforme**

**Contexte :** Releases coordonnées iOS/Android, validation stores, déploiements synchronisés.

**Schéma de communication à compléter :**

```
Git (iOS) ────→ [?] ────→ TestFlight
     │                        │
     ↓                        ↓
[Orchestrateur] ←──── [?] ←── App Store Review
     │
     ↓
Git (Android) ──→ [?] ────→ Play Console
```

**Mécanismes à identifier :**

- **[?] 1 :** Type de communication pour synchroniser les builds
- **[?] 2 :** Type de communication pour les feedbacks de validation
- **[?] 3 :** Type de communication pour l'orchestration

**Réponses :**

- **[?] 1 :** ******\_\_\_******
- **[?] 2 :** ******\_\_\_******
- **[?] 3 :** ******\_\_\_******

### Étape 2 : Application des patterns d'architecture (8 minutes)

**2.1 Choix du pattern par équipe**

Pour chaque équipe, choisissez et justifiez le pattern d'architecture optimal :

| Équipe                   | Pattern choisi | Justification principale     |
| ------------------------ | -------------- | ---------------------------- |
| **Web** (e-commerce)     | ******\_****** | **********\_\_\_\_********** |
| **Mobile** (iOS/Android) | ******\_****** | **********\_\_\_\_********** |
| **Data** (ML/Analytics)  | ******\_****** | **********\_\_\_\_********** |

**2.2 Équipe Web - Implémentation Pipeline Pattern**

**Si vous avez choisi Pipeline Pattern pour l'équipe Web, dessinez le flux linéaire :**

```
[Étape 1] → [Étape 2] → [Étape 3] → [Étape 4] → [Étape 5] → [Étape 6]
```

**Remplissez les étapes :**

- **Étape 1 :** ******\_\_\_******
- **Étape 2 :** ******\_\_\_******
- **Étape 3 :** ******\_\_\_******
- **Étape 4 :** ******\_\_\_******
- **Étape 5 :** ******\_\_\_******
- **Étape 6 :** ******\_\_\_******

**Points de contrôle qualité :**

- **Entre étapes 2-3 :** ******\_\_\_******
- **Entre étapes 4-5 :** ******\_\_\_******

**2.3 Équipe Mobile - Hub Pattern avec GitLab**

**Si vous avez choisi Hub Pattern, complétez l'architecture GitLab :**

```
           GitLab Hub Central
                  │
        ┌─────────┼─────────┐
        │         │         │
   [Service 1] [Service 2] [Service 3]
        │         │         │
   [Mobile iOS] [Mobile Android] [Backend API]
```

**Services GitLab à identifier :**

- **Service 1 :** ******\_\_\_******
- **Service 2 :** ******\_\_\_******
- **Service 3 :** ******\_\_\_******

**Avantages pour l'équipe Mobile :**

- ***
- ***
- ***

**2.4 Équipe Data - Microservices Pattern**

**Si vous avez choisi Microservices Pattern, complétez l'architecture distribuée :**

```
[Airflow] ←→ [?] ←→ [Spark Cluster]
    ↕              ↕
   [?] ←→ [Message Queue] ←→ [?]
    ↕              ↕
[Jupyter] ←→ [?] ←→ [MLflow]
```

**Outils spécialisés à identifier :**

- **[?] 1 :** ******\_\_\_******
- **[?] 2 :** ******\_\_\_******
- **[?] 3 :** ******\_\_\_******
- **[?] 4 :** ******\_\_\_******

### Étape 3 : Analyse des formats d'échange (2 minutes)

**3.1 Identification des formats**

Pour chaque échange, identifiez le format optimal :

| Échange                    | Format     | Justification  |
| -------------------------- | ---------- | -------------- |
| Configuration Kubernetes   | **\_\_\_** | ******\_****** |
| Données metrics Prometheus | **\_\_\_** | ******\_****** |
| Métadonnées build Jenkins  | **\_\_\_** | ******\_****** |
| Images applicatives        | **\_\_\_** | ******\_****** |
| Code source et historique  | **\_\_\_** | ******\_****** |

### Étape 4 : Recommandations d'implémentation (2 minutes)

**4.1 Priorisation par équipe**

**Équipe Web (priorité haute) :**

- **Implémentation immédiate :** ******\_\_\_******
- **Phase 2 (3 mois) :** ******\_\_\_******

**Équipe Mobile (priorité moyenne) :**

- **Implémentation immédiate :** ******\_\_\_******
- **Phase 2 (6 mois) :** ******\_\_\_******

**Équipe Data (priorité basse) :**

- **Implémentation immédiate :** ******\_\_\_******
- **Phase 2 (12 mois) :** ******\_\_\_******

**4.2 Points d'attention transverses**

**Sécurité :**

- Mécanisme d'authentification APIs : ******\_\_\_******
- Chiffrement des communications : ******\_\_\_******

**Monitoring :**

- Observabilité des intégrations : ******\_\_\_******
- Alerting sur les échecs de communication : ******\_\_\_******

---

## Critères d'évaluation

| Critère                      | Points    | Description                                         |
| ---------------------------- | --------- | --------------------------------------------------- |
| **Mécanismes d'intégration** | 2 pts     | Choix appropriés des APIs, webhooks, message queues |
| **Patterns d'architecture**  | 2 pts     | Application correcte des patterns selon contexte    |
| **Cohérence technique**      | 1 pt      | Solutions réalistes et bien justifiées              |
| **TOTAL**                    | **5 pts** |                                                     |

---

## Aide-mémoire

**Mécanismes d'intégration :**

- **REST APIs :** Communication synchrone, récupération données
- **Webhooks :** Notifications événements, déclenchements automatiques
- **Message Queues :** Communication asynchrone, traitement différé

**Patterns d'architecture :**

- **Pipeline :** Flux linéaire, simple, traçable
- **Hub :** Centralisé, intégré, gestion unifiée
- **Microservices :** Distribué, flexible, best-of-breed

**Formats d'échange courants :**

- **YAML/JSON :** Configuration, métadonnées
- **Docker images :** Artefacts containerisés
- **Git repositories :** Code source, versioning

---

_TechFlow Enterprises compte sur votre expertise pour moderniser efficacement leurs chaînes DevOps !_
