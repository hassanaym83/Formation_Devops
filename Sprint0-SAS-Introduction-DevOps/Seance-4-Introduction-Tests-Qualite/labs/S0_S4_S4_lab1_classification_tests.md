# LAB 1 - Classification et Stratégie de Tests

**Séance 4 - Introduction aux Tests et Qualité**  
**Durée estimée :** 15 minutes  
**Prérequis :** Compréhension de la typologie des tests et niveaux vus en cours

---

## 🎯 Objectif

Analyser une application web e-commerce et définir une stratégie de tests complète avec classification appropriée des différents types de tests selon les risques business.

---

## 📋 Contexte

**ShopOnline** est une plateforme e-commerce B2C de vêtements en ligne qui traite 10 000 commandes par mois avec un panier moyen de 85€. L'entreprise vient de lever des fonds et veut professionnaliser sa stratégie qualité.

**Architecture technique :**

- **Frontend** : React.js, responsive design
- **Backend** : Node.js API REST
- **Base de données** : MongoDB pour catalogue, PostgreSQL pour commandes
- **Paiement** : Intégration Stripe et PayPal
- **Livraison** : APIs Colissimo, Chronopost, UPS

**Fonctionnalités principales :**

1. **Catalogue produits** : Navigation, recherche, filtres
2. **Compte utilisateur** : Inscription, login, profil, historique
3. **Panier et commande** : Ajout produits, calcul prix, validation
4. **Paiement** : Choix méthodes, saisie coordonnées, confirmation
5. **Gestion commande** : Suivi, modification, annulation
6. **Administration** : Gestion produits, commandes, utilisateurs

**Contraintes business :**

- **Pic de trafic** : Black Friday (×10 charge normale)
- **Conversion critique** : Taux d'abandon panier élevé (65%)
- **Mobile-first** : 70% du trafic sur mobile
- **Réglementation** : RGPD, PCI-DSS pour paiements

---

## 📝 Instructions

### Étape 1 : Identification des fonctionnalités critiques (4 minutes)

**1.1 Analyse des risques business :**

Classez les fonctionnalités par impact business (1=faible, 5=critique) :

| Fonctionnalité           | Impact Business | Justification |
| ------------------------ | --------------- | ------------- |
| Navigation catalogue     | /5              |               |
| Recherche produits       | /5              |               |
| Inscription/Login        | /5              |               |
| Ajout au panier          | /5              |               |
| Processus paiement       | /5              |               |
| Confirmation commande    | /5              |               |
| Suivi commande           | /5              |               |
| Gestion stock temps réel | /5              |               |
| Calcul frais de port     | /5              |               |
| Interface admin          | /5              |               |

**1.2 Identification des parcours critiques :**

Listez les 3 parcours utilisateur les plus critiques pour le business :

**Parcours critique 1 :**
_Description :_

_Impact si défaillant :_

**Parcours critique 2 :**
_Description :_

_Impact si défaillant :_

**Parcours critique 3 :**
_Description :_

_Impact si défaillant :_

### Étape 2 : Classification des tests par niveau (5 minutes)

**2.1 Tests unitaires :**

Identifiez les composants nécessitant des tests unitaires prioritaires :

| Composant                  | Type de test | Justification |
| -------------------------- | ------------ | ------------- |
| Calcul prix total          |              |               |
| Validation formulaires     |              |               |
| Gestion stock              |              |               |
| Algorithme recommandations |              |               |
| Utilitaires de formatage   |              |               |

**2.2 Tests d'intégration :**

Définissez les intégrations critiques à tester :

| Intégration              | Risque | Tests nécessaires |
| ------------------------ | ------ | ----------------- |
| Frontend ↔ API Backend   |        |                   |
| API ↔ Base de données    |        |                   |
| Paiement ↔ Stripe/PayPal |        |                   |
| Commande ↔ API Livraison |        |                   |
| Stock ↔ Système ERP      |        |                   |

**2.3 Tests système et E2E :**

Listez les scénarios E2E indispensables :

1. **Achat complet invité :**

   - Étapes : **********\_**********
   - Critères succès : **********\_**********

2. **Achat complet utilisateur connecté :**

   - Étapes : **********\_**********
   - Critères succès : **********\_**********

3. **Gestion panier multi-sessions :**
   - Étapes : **********\_**********
   - Critères succès : **********\_**********

### Étape 3 : Classification par type de test (4 minutes)

**3.1 Tests fonctionnels prioritaires :**

| Type de test         | Scénarios | Fréquence d'exécution |
| -------------------- | --------- | --------------------- |
| **Smoke tests**      |           |                       |
| **Sanity tests**     |           |                       |
| **Regression tests** |           |                       |
| **User acceptance**  |           |                       |

**3.2 Tests non-fonctionnels critiques :**

| Type              | Critères cibles | Justification business |
| ----------------- | --------------- | ---------------------- |
| **Performance**   |                 |                        |
| **Charge**        |                 |                        |
| **Sécurité**      |                 |                        |
| **Compatibilité** |                 |                        |
| **Usabilité**     |                 |                        |

### Étape 4 : Priorisation et critères d'acceptation (2 minutes)

**4.1 Matrice de priorisation :**

Classez vos tests selon effort vs impact :

```
    Impact Business
         ↑
    HIGH │ [Test 2] │ [Test 1] │ HIGH
         │          │          │
         │ [Test 4] │ [Test 3] │
    LOW  └──────────┼──────────┘ LOW
              Effort → HIGH
```

**Tests identifiés :**

- Test 1 (High Impact, High Effort) : **********\_**********
- Test 2 (High Impact, Low Effort) : **********\_**********
- Test 3 (Low Impact, High Effort) : **********\_**********
- Test 4 (Low Impact, Low Effort) : **********\_**********

**4.2 Critères d'acceptation qualité :**

**Critères de release :**

- [ ] Smoke tests : **\_** % de succès
- [ ] Tests critiques : **\_** % de succès
- [ ] Performance : **\_** secondes max
- [ ] Sécurité : **\_** vulnérabilités max
- [ ] Régression : **\_** % de succès

**Critères d'escalade :**

- **Bloquant** : **********\_**********
- **Critique** : **********\_**********
- **Majeur** : **********\_**********

---

## 🎯 Critères d'évaluation

| Critère                       | Points    | Description                                       |
| ----------------------------- | --------- | ------------------------------------------------- |
| **Classification pertinente** | 2 pts     | Répartition correcte des tests par niveau et type |
| **Priorisation justifiée**    | 2 pts     | Priorisation basée sur les risques business       |
| **Critères d'acceptation**    | 1 pt      | Définition claire des seuils qualité              |
| **TOTAL**                     | **5 pts** |                                                   |

---

## 💡 Indices et aide

**Pour l'identification des risques :**

- Pensez impact chiffre d'affaires (conversion, panier moyen)
- Considérez l'expérience utilisateur (abandon, satisfaction)
- Évaluez les risques réglementaires et sécurité

**Pour la classification :**

- Tests unitaires : Logique métier complexe, calculs
- Tests intégration : Points de communication entre systèmes
- Tests E2E : Parcours utilisateur complets de bout en bout

**Pour la priorisation :**

- Quick wins : Impact élevé, effort faible (priorité 1)
- Tests critiques : Impact élevé même si effort élevé (priorité 2)
- Évitez : Impact faible, effort élevé (déprioritiser)

---

## 📚 Données ShopOnline pour votre analyse

**Métriques actuelles :**

- **Trafic mensuel :** 150 000 visiteurs uniques
- **Taux de conversion :** 4.2%
- **Taux d'abandon panier :** 65%
- **Temps de chargement moyen :** 3.2 secondes
- **Incidents production :** 2-3 par mois
- **Support client :** 15% tickets liés à bugs techniques

**Pic d'activité (Black Friday) :**

- **Trafic ×10** : 1.5M visiteurs en 24h
- **Objectif conversion :** Maintenir 4%+
- **Performance cible :** < 5 secondes même en pic
- **Zéro défaillance** sur parcours achat

---

_ShopOnline compte sur votre expertise pour optimiser sa stratégie de tests !_
