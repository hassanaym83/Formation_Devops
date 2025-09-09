# LAB 2 - Définition de Métriques Qualité

**Séance 4 - Introduction aux Tests et Qualité**  
**Durée estimée :** 20 minutes  
**Prérequis :** Compréhension des métriques qualité et modèles de qualité vus en cours

---

## 🎯 Objectif

Concevoir un système de métriques qualité adapté à un projet bancaire et définir les seuils, tableaux de bord et processus de suivi appropriés aux contraintes réglementaires.

---

## 📋 Contexte

**BankApp** est l'application mobile de **DigitalBank**, une banque 100% digitale qui vise 500 000 clients d'ici 2 ans. L'application gère les comptes, virements, crédits et investissements avec des exigences de sécurité et fiabilité maximales.

**Contexte réglementaire :**

- **PCI-DSS** : Sécurité des données de paiement
- **GDPR** : Protection données personnelles
- **Bâle III** : Gestion des risques opérationnels
- **ACPR** : Réglementation bancaire française
- **Zero tolerance** : Aucun bug critique en production autorisé

**Architecture technique :**

- **Frontend** : React Native (iOS/Android)
- **Backend** : Java Spring Boot microservices
- **Databases** : PostgreSQL (transactionnel), Redis (cache)
- **APIs** : REST + GraphQL, architecture event-driven
- **Security** : OAuth2, 2FA, chiffrement end-to-end
- **Infrastructure** : Kubernetes on AWS, multi-AZ

**Fonctionnalités critiques :**

1. **Authentification** : Biométrie, 2FA, gestion sessions
2. **Consultation comptes** : Soldes, historique, PDF relevés
3. **Virements** : SEPA, instantanés, virements programmés
4. **Paiements** : Contactless, QR codes, prélèvements
5. **Crédits** : Simulation, demande, gestion remboursements
6. **Investissements** : Portefeuille, ordres bourse, analyses

**SLA exigés :**

- **Disponibilité** : 99.95% (4h downtime/an max)
- **Performance** : 95% requêtes < 1s, 99% < 3s
- **Sécurité** : 0 incident critique, scan continu
- **Compliance** : Audit mensuel automatisé

---

## 📝 Instructions

### Étape 1 : Sélection des métriques par dimension qualité (6 minutes)

**1.1 Métriques de fonctionnalité :**

Identifiez les métriques pertinentes pour chaque caractéristique :

| Caractéristique                | Métriques sélectionnées | Justification contexte bancaire |
| ------------------------------ | ----------------------- | ------------------------------- |
| **Functional Correctness**     |                         |                                 |
| **Functional Completeness**    |                         |                                 |
| **Functional Appropriateness** |                         |                                 |

**1.2 Métriques de fiabilité :**

| Métrique                              | Définition | Calcul | Cible BankApp |
| ------------------------------------- | ---------- | ------ | ------------- |
| **MTBF (Mean Time Between Failures)** |            |        |               |
| **MTTR (Mean Time To Repair)**        |            |        |               |
| **Availability**                      |            |        |               |
| **Error Rate**                        |            |        |               |

**1.3 Métriques de performance :**

| Métrique                 | Cible | Justification | Mesure |
| ------------------------ | ----- | ------------- | ------ |
| **Response Time (P95)**  |       |               |        |
| **Throughput**           |       |               |        |
| **Resource Utilization** |       |               |        |
| **Scalability**          |       |               |        |

**1.4 Métriques de sécurité :**

| Métrique                       | Cible | Fréquence mesure | Alerting |
| ------------------------------ | ----- | ---------------- | -------- |
| **Critical Vulnerabilities**   |       |                  |          |
| **Failed Authentication Rate** |       |                  |          |
| **Data Encryption Coverage**   |       |                  |          |
| **Security Incidents**         |       |                  |          |

### Étape 2 : Métriques de test et processus (5 minutes)

**2.1 Couverture de tests :**

Définissez les cibles de couverture par niveau :

| Type de test                     | Cible de couverture | Justification | Outil de mesure |
| -------------------------------- | ------------------- | ------------- | --------------- |
| **Unit Tests - Line Coverage**   | \_\_\_%             |               |                 |
| **Unit Tests - Branch Coverage** | \_\_\_%             |               |                 |
| **Integration Tests Coverage**   | \_\_\_%             |               |                 |
| **E2E Critical Paths Coverage**  | \_\_\_%             |               |                 |
| **Security Tests Coverage**      | \_\_\_%             |               |                 |

**2.2 Métriques de défauts :**

Calculez et définissez les seuils :

| Métrique                      | Formule                            | Seuil acceptable | Seuil critique |
| ----------------------------- | ---------------------------------- | ---------------- | -------------- |
| **Defect Density**            | Défauts/KLOC                       |                  |                |
| **Defect Removal Efficiency** | Défauts trouvés test/Total défauts |                  |                |
| **Escape Rate**               | Défauts prod/Total défauts         |                  |                |
| **Defect Age**                | Temps moyen ouverture→fermeture    |                  |                |

**2.3 Métriques de processus :**

| Métrique DevOps             | Cible BankApp | Mesure | Impact business |
| --------------------------- | ------------- | ------ | --------------- |
| **Deployment Frequency**    |               |        |                 |
| **Lead Time for Changes**   |               |        |                 |
| **Change Failure Rate**     |               |        |                 |
| **Time to Restore Service** |               |        |                 |

### Étape 3 : Conception du tableau de bord qualité (5 minutes)

**3.1 Dashboard exécutif (Management) :**

Concevez un dashboard pour le management :

```
┌─────────────────────────────────────────────────────────┐
│ BANKAPP QUALITY DASHBOARD - EXECUTIVE VIEW             │
├─────────────────────────────────────────────────────────┤
│ Business KPIs:                                          │
│ • App Store Rating: ___/5 ⭐ (Target: >4.5)           │
│ • Customer Satisfaction: ___% (Target: >90%)           │
│ • Critical Incidents: ___ (Target: 0)                  │
│ • Compliance Score: ___% (Target: 100%)                │
├─────────────────────────────────────────────────────────┤
│ Technical Health:                                       │
│ • System Availability: ___% (Target: 99.95%)           │
│ • Performance (P95): ___s (Target: <1s)                │
│ • Security Posture: ___/10 (Target: 10/10)             │
│ • Test Coverage: ___% (Target: >85%)                    │
├─────────────────────────────────────────────────────────┤
│ Trends & Alerts:                                        │
│ • [___] Critical alerts requiring attention             │
│ • [___] Improvement trends last 30 days                 │
└─────────────────────────────────────────────────────────┘
```

**3.2 Dashboard technique (Équipes Dev/QA) :**

```
┌─────────────────────────────────────────────────────────┐
│ BANKAPP QUALITY DASHBOARD - TECHNICAL VIEW             │
├─────────────────────────────────────────────────────────┤
│ Test Metrics:                                           │
│ • Unit Tests: ___% coverage, ___ tests passing         │
│ • Integration Tests: ___% coverage, ___ tests passing  │
│ • E2E Tests: ___% critical paths, ___ tests passing    │
│ • Performance Tests: ___ scenarios, ___ms average      │
├─────────────────────────────────────────────────────────┤
│ Quality Gates Status:                                   │
│ • Build Quality: [PASS/FAIL] - ___% success rate       │
│ • Security Scan: [PASS/FAIL] - ___ vulnerabilities     │
│ • Performance Test: [PASS/FAIL] - ___s response time   │
│ • Compliance Check: [PASS/FAIL] - ___% coverage        │
├─────────────────────────────────────────────────────────┤
│ Defect Tracking:                                        │
│ • Open Bugs: P1: ___, P2: ___, P3: ___, P4: ___       │
│ • Bug Trend: ↗↘ ___% vs last sprint                   │
│ • Defect Age: ___% > 5 days (Target: <10%)             │
└─────────────────────────────────────────────────────────┘
```

### Étape 4 : Processus de suivi et amélioration (4 minutes)

**4.1 Fréquence de reporting :**

Définissez la cadence de suivi :

| Audience            | Fréquence | Format | Métriques clés |
| ------------------- | --------- | ------ | -------------- |
| **Équipe Dev/QA**   |           |        |                |
| **Product Owner**   |           |        |                |
| **Management**      |           |        |                |
| **Compliance Team** |           |        |                |
| **Executive Board** |           |        |                |

**4.2 Triggers d'alerte et escalade :**

| Seuil        | Métrique | Action immédiate | Escalade |
| ------------ | -------- | ---------------- | -------- |
| **Critique** |          |                  |          |
| **Majeur**   |          |                  |          |
| **Mineur**   |          |                  |          |
| **Tendance** |          |                  |          |

**4.3 Processus d'amélioration continue :**

**Réunions qualité :**

**Weekly Quality Sync (Équipe technique) :**

- Participants : **\_**
- Durée : **\_** minutes
- Agenda : **\_**

**Monthly Quality Review (Management) :**

- Participants : **\_**
- Durée : **\_** minutes
- Deliverables : **\_**

**Quarterly Quality Retrospective :**

- Participants : **\_**
- Objectif : **\_**
- Actions : **\_**

**Actions d'amélioration :**

| Métrique dégradée     | Root Cause probable | Action corrective | Owner | Délai |
| --------------------- | ------------------- | ----------------- | ----- | ----- |
| Test coverage < 80%   |                     |                   |       |       |
| Defect density élevée |                     |                   |       |       |
| Performance dégradée  |                     |                   |       |       |
| Incident sécurité     |                     |                   |       |       |

---

## 🎯 Critères d'évaluation

| Critère                       | Points    | Description                                                |
| ----------------------------- | --------- | ---------------------------------------------------------- |
| **Pertinence des métriques**  | 2 pts     | Sélection adaptée au contexte bancaire réglementé          |
| **Seuils justifiés**          | 2 pts     | Cibles réalistes et alignées avec les contraintes business |
| **Tableau de bord pertinent** | 1 pt      | Dashboards adaptés aux audiences et actionnable            |
| **TOTAL**                     | **5 pts** |                                                            |

---

## 💡 Indices et aide

**Pour la sélection des métriques :**

- Contexte bancaire = sécurité et fiabilité prioritaires
- Réglementation = traçabilité et audit obligatoires
- Mobile banking = performance et disponibilité critiques

**Pour les seuils :**

- Benchmark industrie bancaire vs contraintes internes
- Coût de non-qualité très élevé en banque
- SLA clients vs SLA techniques internes

**Pour les dashboards :**

- Management = vision business et risques
- Technique = métriques actionnables et détaillées
- Real-time vs périodique selon l'usage

**Pour l'amélioration continue :**

- Boucles de feedback courtes (hebdomadaires)
- Actions correctives traçables
- Prévention > correction

---

## 📚 Données DigitalBank pour votre analyse

**Contraintes réglementaires spécifiques :**

- **Audit PCI-DSS** : Trimestriel, score > 95%
- **Stress tests ACPR** : Disponibilité lors pics 10× charge normale
- **GDPR compliance** : 0 fuite de données personnelles
- **Cyber resilience** : Recovery < 4h en cas d'attaque

**Métriques business actuelles :**

- **Customer satisfaction** : 4.2/5 (cible 4.5/5)
- **App crashes** : 0.1% sessions (cible < 0.05%)
- **Support tickets** : 15% liés à bugs (cible < 5%)
- **Churn rate** : 8% annuel (cible < 5%)

**Budget qualité annuel :** 1.2M€ (Testing: 600k€, Tools: 300k€, Training: 300k€)

---

_DigitalBank compte sur votre expertise pour définir sa stratégie de métriques qualité !_
