# LAB 4 - Impact Économique et Business Case DevOps

## Contexte de l'exercice

**InnovBank** est une banque traditionnelle de 1500 employés qui évalue l'opportunité d'une transformation DevOps. Le comité de direction demande une analyse économique complète pour justifier l'investissement dans cette transformation.

Vous êtes consultant DevOps et devez présenter un business case convaincant basé sur les données d'impact économique vues en cours et les métriques de performance DevOps.

---

## Données de contexte - InnovBank

### Situation actuelle

- **Équipes IT** : 120 développeurs, 40 administrateurs systèmes, 20 testeurs
- **Coût annuel IT** : 18M€ (salaires + infrastructure + outils)
- **Applications critiques** : 25 applications bancaires en production
- **Fréquence déploiement** : 1 déploiement/trimestre par application
- **Incidents production** : 2-3 incidents majeurs/mois, 8h MTTR moyen
- **Time to market** : 18 mois pour nouvelle fonctionnalité

### Objectifs business

- **Réduction time to market** : Passer de 18 mois à 6 mois
- **Amélioration stabilité** : Réduire incidents de 50%
- **Augmentation vélocité** : 3x plus de livraisons par an
- **Optimisation coûts** : ROI positif sur 3 ans

---

## Questions d'analyse

### 1. CALCUL DU COÛT DE LA NON-QUALITÉ ACTUELLE (2 points)

**Question 1.1** : Coût des incidents

Calculez le coût annuel des incidents en production pour InnovBank. Utilisez les données d'impact vues en cours :

**Données de référence** :

- **Coût horaire incident majeur** : 50 000€/heure (perte business + ressources mobilisées)
- **Incidents actuels** : 2.5 incidents/mois × 8h MTTR
- **Coût indirect** : +30% du coût direct (image, clients, réglementaire)

**Votre calcul** :

---

**Question 1.2** : Coût d'opportunité time to market

Calculez le manque à gagner lié au time to market lent. Utilisez l'exemple vu en cours :

**Données** :

- **Revenus moyens nouvelle fonctionnalité** : 2M€/an
- **Retard vs concurrence** : 12 mois (18 mois InnovBank vs 6 mois FinTech)
- **Part de marché perdue** : 15% par année de retard

**Votre calcul** :

---

### 2. ESTIMATION DES GAINS DEVOPS (2 points)

**Question 2.1** : Gains de productivité

Calculez les gains de productivité attendus avec DevOps. Basez-vous sur les études DORA vues en cours :

**Améliorations cibles** :

- **Deployment frequency** : 1/trimestre → 1/semaine (12x amélioration)
- **Lead time** : 18 mois → 6 mois (3x amélioration)
- **MTTR** : 8h → 2h (4x amélioration)
- **Change failure rate** : 25% → 10% (2.5x amélioration)

**Gains de référence DORA** :

- Elite performers : +46% productivité vs Low performers
- High performers : +25% productivité vs Medium performers

**Votre estimation de gains** :

---

**Question 2.2** : Impact business quantifié

Calculez l'impact business total sur la première année. Utilisez les corrélations vues en cours :

**Métriques de performance** → **Impact business** :

- Lead time réduit : +20% satisfaction client → +5% rétention → +2% revenus
- Deployment frequency : +30% innovation → +10% nouveaux produits
- MTTR amélioré : -60% coût incidents + +15% disponibilité

**Votre calcul d'impact** :

---

### 3. BUSINESS CASE ET ROI (1 point)

**Question 3.1** : Coût de transformation

Estimez le coût de la transformation DevOps pour InnovBank :

**Postes d'investissement** :

- **Formation équipes** : 120 développeurs × 5 000€ + 40 ops × 7 000€
- **Outils et plateforme** : CI/CD, monitoring, sécurité = 500 000€
- **Accompagnement** : 18 mois × 50 000€/mois consultant
- **Infrastructure cloud** : Migration + nouveaux services = 1M€

**Votre estimation** :

---

**Question 3.2** : Calcul ROI sur 3 ans

Calculez le ROI de la transformation DevOps sur 3 ans :

**Formule ROI** : (Gains cumulés - Investissement) / Investissement × 100

**Hypothèses** :

- Gains année 1 : Calculés en question 2.2
- Gains année 2 : +150% des gains année 1 (montée en compétence)
- Gains année 3 : +200% des gains année 1 (maturité DevOps)

**Votre calcul ROI** :

---

### 4. RECOMMANDATIONS STRATÉGIQUES (1 point)

**Question 4.1** : Argumentation pour le comité de direction

Rédigez les 3 arguments économiques les plus convaincants pour justifier la transformation DevOps :

**Argument 1** : ****\_\_\_****

**Argument 2** : ****\_\_\_****

**Argument 3** : ****\_\_\_****

**Question 4.2** : Plan de déploiement économiquement optimal

Proposez un plan de déploiement qui maximise le ROI :

**Phase 1 (6 mois)** : ****\_\_\_****

**Phase 2 (12 mois)** : ****\_\_\_****

**Phase 3 (18 mois)** : ****\_\_\_****

---

## Modalités de réalisation

**Durée** : 20 minutes
**Format** : Travail individuel  
**Support** : Cours section 7 (Impact Économique et Business Case)
**Ressources autorisées** : Notes de cours, calculatrice

## Critères d'évaluation

- **Calculs économiques** (2 pts) : Justesse des calculs de coûts et gains
- **Analyse impact** (2 pts) : Pertinence de l'évaluation des bénéfices DevOps
- **Business case** (1 pt) : Cohérence du ROI et qualité des recommandations

**Note** : /5 points

---

_LAB 4 conçu par Hassan ESSADIK | Sprint 0 - Séance 1 DevOps_
