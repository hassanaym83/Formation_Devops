# LAB 3 - Métriques DORA et Performance DevOps

## Contexte de l'exercice

**TechCorp** est une entreprise de services numériques de 200 personnes qui développe des applications SaaS pour des clients européens. L'entreprise a commencé sa transformation DevOps il y a 18 mois et souhaite évaluer sa progression à l'aide des métriques DORA.

Le DSI de TechCorp vous demande d'analyser les données collectées sur leurs équipes de développement pour identifier les points d'amélioration prioritaires et mesurer l'impact potentiel des optimisations.

---

## Données collectées - Métriques DORA TechCorp

### Équipe Alpha (Application CRM)

- **Deployment Frequency** : 2 déploiements par semaine
- **Lead Time for Changes** : 3 jours (du commit à la production)
- **Change Failure Rate** : 12%
- **Time to Restore Service** : 2 heures

### Équipe Beta (Plateforme E-commerce)

- **Deployment Frequency** : 1 déploiement par mois
- **Lead Time for Changes** : 2 semaines
- **Change Failure Rate** : 8%
- **Time to Restore Service** : 6 heures

### Équipe Gamma (API Gateway)

- **Deployment Frequency** : 3 déploiements par jour
- **Lead Time for Changes** : 4 heures
- **Change Failure Rate** : 5%
- **Time to Restore Service** : 30 minutes

---

## Questions d'analyse

### 1. CLASSIFICATION PERFORMANCE DORA (2 points)

**Question 1.1** : Niveau de performance par équipe

Pour chaque équipe (Alpha, Beta, Gamma), déterminez le niveau de performance DORA global en vous basant sur les 4 métriques. Utilisez les seuils vus en cours :

**Niveaux de référence DORA** :

- **Elite** : Plusieurs déploiements/jour + Lead time < 1 heure + Change failure rate < 15% + Time to restore < 1 heure
- **High** : 1 déploiement/jour à 1/semaine + Lead time < 1 jour + Change failure rate < 15% + Time to restore < 1 jour
- **Medium** : 1 déploiement/semaine à 1/mois + Lead time 1 jour à 1 semaine + Change failure rate 16-30% + Time to restore 1 jour à 1 semaine
- **Low** : < 1 déploiement/mois + Lead time > 1 semaine + Change failure rate > 30% + Time to restore > 1 semaine

**Votre analyse** :

**Équipe Alpha** :

- Niveau DORA : ****\_\_\_****
- Justification : ****\_\_\_****

**Équipe Beta** :

- Niveau DORA : ****\_\_\_****
- Justification : ****\_\_\_****

**Équipe Gamma** :

- Niveau DORA : ****\_\_\_****
- Justification : ****\_\_\_****

**Question 1.2** : Métrique la plus critique

Identifiez quelle métrique DORA est la plus critique pour TechCorp dans l'ensemble et expliquez pourquoi en vous basant sur l'impact business vu en cours.

**Votre réponse** :

---

### 2. DIAGNOSTIC DES GOULOTS D'ÉTRANGLEMENT (2 points)

**Question 2.1** : Analyse des problèmes par équipe

Pour chaque équipe, identifiez le principal goulot d'étranglement qui limite sa performance DevOps en vous basant sur les métriques :

**Équipe Alpha** :

- Goulot principal : ****\_\_\_****
- Explication : ****\_\_\_****

**Équipe Beta** :

- Goulot principal : ****\_\_\_****
- Explication : ****\_\_\_****

**Équipe Gamma** :

- Goulot principal : ****\_\_\_****
- Explication : ****\_\_\_****

**Question 2.2** : Impact économique

Calculez l'impact économique potentiel d'une amélioration de l'équipe Beta au niveau "High". Utilisez les données d'impact vues en cours :

**Données de référence** :

- Coût développeur TechCorp : 60 000€/an
- Équipe Beta : 8 développeurs
- Amélioration Lead Time Medium→High : +25% productivité
- Réduction Change Failure Rate : -50% coût incidents

**Votre calcul** :

---

### 3. PLAN D'AMÉLIORATION PRIORITAIRE (1 point)

**Question 3.1** : Recommandations par équipe

Proposez 2 améliorations concrètes prioritaires pour chaque équipe, basées sur les bonnes pratiques DevOps vues en cours :

**Équipe Alpha** :

1. ***
2. ***

**Équipe Beta** :

1. ***
2. ***

**Équipe Gamma** :

1. ***
2. ***

**Question 3.2** : ROI des améliorations

Estimez le retour sur investissement (ROI) sur 12 mois pour l'amélioration prioritaire de l'équipe Beta en vous basant sur les gains de productivité calculés en question 2.2.

**Votre estimation** :

---

---

## Modalités de réalisation

**Durée** : 20 minutes
**Format** : Travail individuel
**Support** : Cours sections 6.1 et 6.2 (Métriques DORA)
**Ressources autorisées** : Notes de cours, calculatrice

## Critères d'évaluation

- **Classification performance** (2 pts) : Justesse des niveaux DORA et pertinence des justifications
- **Diagnostic goulots** (2 pts) : Précision de l'analyse et cohérence avec les métriques
- **Recommandations** (1 pt) : Pertinence des améliorations et réalisme du plan

**Note** : /5 points

---

_LAB 3 conçu par Hassan ESSADIK | Sprint 0 - Séance 1 DevOps_
