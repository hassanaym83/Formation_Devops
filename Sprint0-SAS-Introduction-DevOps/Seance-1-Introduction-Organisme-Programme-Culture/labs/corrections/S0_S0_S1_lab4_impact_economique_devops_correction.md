# LAB 4 - Impact Économique et Business Case DevOps - CORRECTION

## Contexte de correction

Cette correction présente une méthodologie d'évaluation économique d'une transformation DevOps. Elle s'appuie sur les études d'impact et les calculs de ROI vus en cours pour construire un business case solide.

---

## CORRECTION DÉTAILLÉE

### 1. CALCUL DU COÛT DE LA NON-QUALITÉ ACTUELLE (2 points)

**Question 1.1** : Coût des incidents

**Calcul du coût annuel des incidents** :

**Coût direct incidents** :

- Incidents/mois : 2.5 × 8h × 50 000€/h = 1 000 000€/mois
- **Coût annuel direct** : 1 000 000€ × 12 = **12 000 000€/an**

**Coût indirect** (+30%) :

- 12 000 000€ × 0.30 = **3 600 000€/an**

**Coût total incidents** : 12 000 000€ + 3 600 000€ = **15 600 000€/an**

**Question 1.2** : Coût d'opportunité time to market

**Calcul du manque à gagner** :

**Retard concurrentiel** :

- Retard : 18 mois - 6 mois = **12 mois**
- Part de marché perdue : 15% × 12 mois = **180% sur 12 mois** = 15% permanent

**Manque à gagner annuel** :

- Revenus par fonctionnalité : 2M€/an
- Fonctionnalités par an : 25 applications ÷ 4 (trimestriel) = 6.25 fonctionnalités
- **Revenus perdus** : 6.25 × 2M€ × 0.15 = **1 875 000€/an**

### 2. ESTIMATION DES GAINS DEVOPS (2 points)

**Question 2.1** : Gains de productivité

**Évaluation niveau de performance actuel vs cible** :

**Situation actuelle** :

- Deployment frequency : 1/trimestre = **Low performer**
- Lead time : 18 mois = **Low performer**
- MTTR : 8h = **Medium performer**
- Change failure rate : 25% = **Low performer**
- **Classification** : **Low performer global**

**Situation cible** :

- Deployment frequency : 1/semaine = **High performer**
- Lead time : 6 mois = **Medium performer**
- MTTR : 2h = **High performer**
- Change failure rate : 10% = **High performer**
- **Classification** : **High performer global**

**Gains de productivité DORA** :

- Low → High performers : **+46% productivité**
- Impact sur coût IT : 18M€ × 0.46 = **8 280 000€/an**

**Question 2.2** : Impact business quantifié

**Calcul impact business première année** :

**1. Amélioration Lead Time** :

- +20% satisfaction client → +5% rétention → +2% revenus
- Base revenus estimée bancaire : 500M€
- **Gain revenus** : 500M€ × 0.02 = **10 000 000€**

**2. Augmentation Deployment Frequency** :

- +30% innovation → +10% nouveaux produits
- Impact nouveaux produits : 25 applications × 2M€ × 0.10
- **Gain innovation** : **5 000 000€**

**3. Amélioration MTTR** :

- Réduction coût incidents : 15 600 000€ × 0.60 = **9 360 000€**
- Amélioration disponibilité : +15% × revenus digitaux (100M€)
- **Gain disponibilité** : 100M€ × 0.15 = **15 000 000€**

**Impact business total année 1** : 10M€ + 5M€ + 9.36M€ + 15M€ = **39 360 000€**

### 3. BUSINESS CASE ET ROI (1 point)

**Question 3.1** : Coût de transformation

**Calcul coût transformation DevOps** :

**Formation équipes** :

- Développeurs : 120 × 5 000€ = 600 000€
- Ops : 40 × 7 000€ = 280 000€
- **Sous-total formation** : **880 000€**

**Outils et plateforme** : **500 000€**

**Accompagnement** : 18 × 50 000€ = **900 000€**

**Infrastructure cloud** : **1 000 000€**

**Coût total transformation** : 880 000€ + 500 000€ + 900 000€ + 1 000 000€ = **3 280 000€**

**Question 3.2** : Calcul ROI sur 3 ans

**Projection gains sur 3 ans** :

- **Année 1** : 39 360 000€ (calculé ci-dessus)
- **Année 2** : 39 360 000€ × 1.5 = **59 040 000€** (montée en compétence)
- **Année 3** : 39 360 000€ × 2.0 = **78 720 000€** (maturité DevOps)

**Gains cumulés 3 ans** : 39.36M€ + 59.04M€ + 78.72M€ = **177 120 000€**

**Calcul ROI** :
ROI = (177 120 000€ - 3 280 000€) / 3 280 000€ × 100
ROI = 173 840 000€ / 3 280 000€ × 100 = **5 300%**

### 4. RECOMMANDATIONS STRATÉGIQUES (1 point)

**Question 4.1** : Argumentation pour le comité de direction

**Argument 1 - Impact financier massif** :
ROI de 5 300% sur 3 ans avec gains dès la première année de 39M€ vs investissement de 3.3M€. Retour sur investissement en moins de 3 mois.

**Argument 2 - Avantage concurrentiel critique** :
Time to market 3x plus rapide = capacité à devancer la concurrence FinTech et capturer 10M€ de revenus additionnels par an via l'innovation accélérée.

**Argument 3 - Réduction drastique des risques** :
Division par 4 du temps de résolution d'incidents et réduction de 60% des coûts d'incidents = économies de 9.36M€/an et protection de l'image de marque.

**Question 4.2** : Plan de déploiement économiquement optimal

**Phase 1 (6 mois) - Foundation & Quick Wins** :
Applications non-critiques + équipes volontaires. Investissement : 1M€. Gains attendus : 5M€ (ROI immédiat pour convaincre les sceptiques).

**Phase 2 (12 mois) - Core Systems** :
Applications critiques + généralisation. Investissement : 1.5M€. Gains : 15M€ (automatisation mature, réduction incidents majeure).

**Phase 3 (18 mois) - Excellence & Innovation** :
Optimisation avancée + nouveaux produits. Investissement : 0.78M€. Gains : 19M€ (innovation produit, leadership technologique).

---

## GRILLE D'ÉVALUATION DÉTAILLÉE

### Barème précis (5 points total)

**Calculs économiques (2 points)** :

- 2 pts : Calculs corrects avec méthodologie DORA et prise en compte coûts directs/indirects
- 1.5 pts : Calculs majoritairement corrects mais méthodologie partielle
- 1 pt : Calculs approximatifs mais logique économique présente
- 0 pt : Calculs erronés ou absence de méthodologie

**Analyse impact (2 points)** :

- 2 pts : Évaluation complète des bénéfices avec corrélations performance/business
- 1.5 pts : Analyse impact correcte mais liens DORA partiels
- 1 pt : Impact identifié mais quantification approximative
- 0 pt : Analyse superficielle ou incorrecte

**Business case (1 point)** :

- 1 pt : ROI cohérent avec arguments convaincants et plan réaliste
- 0.5 pt : Business case correct mais arguments ou plan perfectibles
- 0 pt : Business case incohérent ou irréaliste

### Éléments différenciateurs

**Excellence** :

- Référence aux études DORA et corrélations précises
- Prise en compte coûts cachés et bénéfices indirects
- Arguments business adaptés au contexte bancaire
- Plan de déploiement avec ROI progressif

**Erreurs fréquentes** :

- Confusion entre corrélation et causalité dans les gains
- Sous-estimation des coûts de transformation
- Surestimation des gains sans base méthodologique
- Plan de déploiement irréaliste (tout en même temps)

### Bonifications possibles

**Excellence économique** (+0.5 pt) : Prise en compte coûts d'opportunité et valeur temps de l'argent
**Innovation business** (+0.5 pt) : Identification bénéfices non quantifiés (image, recrutement, moral)

---

_Correction validée par Hassan ESSADIK | Sprint 0 - Séance 1 DevOps_
