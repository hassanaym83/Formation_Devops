# Quiz - Séance 4 : Introduction aux Tests et Qualité

**Sprint 0 - Introduction DevOps**  
**Durée :** 15 minutes  
**Total :** 20 questions

---

## Instructions

- Cochez la ou les bonnes réponses pour chaque question
- Certaines questions peuvent avoir plusieurs réponses correctes
- Pas de points négatifs, tentez toutes les questions

---

## 1. Fondations des Tests Logiciels

**Question 1 (1 pt) :** Quels sont les objectifs principaux du test logiciel ? _(Plusieurs réponses possibles)_

☐ a) Vérification que le logiciel répond aux spécifications  
☐ b) Validation que le logiciel répond aux besoins utilisateur  
☐ c) Garantir un logiciel 100% sans bug  
☐ d) Détection de défauts avant la production  
☐ e) Prévention de l'introduction de nouveaux défauts

**Question 2 (1 pt) :** Selon le principe ISTQB "Le test montre la présence de défauts", que signifie cette affirmation ?

☐ a) Les tests prouvent qu'un logiciel est parfait  
☐ b) Les tests peuvent révéler des bugs mais ne prouvent pas leur absence  
☐ c) Seuls les tests exhaustifs sont valables  
☐ d) Les tests ne servent qu'à documenter les problèmes

**Question 3 (1 pt) :** Quel est l'ordre de grandeur du coût de correction d'un défaut selon la phase où il est détecté ?

☐ a) Même coût quelle que soit la phase  
☐ b) Analyse: 1€ → Développement: 10€ → Production: 100€  
☐ c) Analyse: 1€ → Développement: 10€ → Production: 10000€  
☐ d) Le coût diminue avec le temps

---

## 2. Typologie des Tests

**Question 4 (2 pts) :** Associez chaque niveau de test à sa caractéristique principale :

**Niveaux :** Tests unitaires, Tests d'intégration, Tests système, Tests d'acceptation  
**Caractéristiques :** Validation métier, Interaction composants, Module isolé, Application complète

- Tests unitaires → ********\_********
- Tests d'intégration → ********\_********
- Tests système → ********\_********
- Tests d'acceptation → ********\_********

**Question 5 (1 pt) :** Quels tests appartiennent à la catégorie "tests non-fonctionnels" ? _(Plusieurs réponses possibles)_

☐ a) Tests de performance  
☐ b) Tests de régression  
☐ c) Tests de sécurité  
☐ d) Tests de charge  
☐ e) Tests d'acceptation utilisateur  
☐ f) Tests d'usabilité

**Question 6 (1 pt) :** Quelle est la différence entre tests statiques et tests dynamiques ?

☐ a) Statique = sans exécution, Dynamique = avec exécution  
☐ b) Statique = automatisé, Dynamique = manuel  
☐ c) Statique = unitaire, Dynamique = intégration  
☐ d) Aucune différence significative

---

## 3. Stratégies de Test

**Question 7 (2 pts) :** Dans la pyramide des tests, quelle est la répartition recommandée ?

☐ a) 70% unitaires, 20% intégration, 10% E2E  
☐ b) 33% unitaires, 33% intégration, 33% E2E  
☐ c) 10% unitaires, 20% intégration, 70% E2E  
☐ d) 50% unitaires, 30% intégration, 20% E2E

**Question 8 (1 pt) :** Quel est l'ordre correct du cycle TDD (Test-Driven Development) ?

☐ a) Green → Red → Refactor  
☐ b) Red → Green → Refactor  
☐ c) Refactor → Red → Green  
☐ d) Test → Code → Debug

**Question 9 (1 pt) :** Dans les Agile Testing Quadrants, quel quadrant correspond aux tests unitaires ?

☐ a) Q1 - Technology-facing & Supporting  
☐ b) Q2 - Business-facing & Supporting  
☐ c) Q3 - Business-facing & Critiquing  
☐ d) Q4 - Technology-facing & Critiquing

---

## 4. Qualité Logicielle et Métriques

**Question 10 (1 pt) :** Selon ISO 25010, quelles sont des caractéristiques principales de la qualité ? _(Plusieurs réponses possibles)_

☐ a) Functional Suitability  
☐ b) Performance Efficiency  
☐ c) Code Complexity  
☐ d) Reliability  
☐ e) Security  
☐ f) Budget Compliance

**Question 11 (2 pts) :** Calculez la Defect Removal Efficiency si 45 défauts ont été trouvés en test et 5 défauts ont été trouvés en production :

☐ a) 90%  
☐ b) 80%  
☐ c) 45%  
☐ d) 11%

**Question 12 (1 pt) :** Que mesure la métrique "Escape Rate" ?

☐ a) Temps de résolution des défauts  
☐ b) Défauts trouvés en production / Total défauts  
☐ c) Couverture de code par les tests  
☐ d) Vitesse d'exécution des tests

---

## 5. Automatisation des Tests

**Question 13 (1 pt) :** Quand NE faut-il PAS automatiser des tests ? _(Plusieurs réponses possibles)_

☐ a) Tests exploratoires  
☐ b) Tests de régression  
☐ c) Tests qui changent fréquemment  
☐ d) Tests de performance  
☐ e) Tests d'usabilité

**Question 14 (1 pt) :** Que signifie l'acronyme FIRST dans les bonnes pratiques de tests ?

☐ a) Fast, Independent, Repeatable, Self-validating, Timely  
☐ b) Functional, Integrated, Robust, Secure, Tested  
☐ c) Full, Isolated, Reliable, Simple, Traceable  
☐ d) Formal, Incremental, Recursive, Structured, Timed

**Question 15 (1 pt) :** Le Pattern Page Object est utilisé pour :

☐ a) Organiser le code de tests unitaires  
☐ b) Structurer les tests d'API  
☐ c) Encapsuler les éléments d'interface dans les tests UI  
☐ d) Gérer les données de test

---

## 6. Tests dans le Cycle DevOps

**Question 16 (1 pt) :** Que signifie "Shift-Left Testing" ?

☐ a) Exécuter les tests à gauche de l'écran  
☐ b) Déplacer les tests plus tôt dans le cycle de développement  
☐ c) Utiliser des outils open-source  
☐ d) Tester en production uniquement

**Question 17 (2 pts) :** Quelles sont les techniques de "Testing in Production" ? _(Plusieurs réponses possibles)_

☐ a) Canary Testing  
☐ b) A/B Testing  
☐ c) Feature Flags  
☐ d) Chaos Engineering  
☐ e) Waterfall Testing

**Question 18 (1 pt) :** Dans l'observabilité, quels sont les "Three Pillars" ?

☐ a) Tests, Code, Deploy  
☐ b) Metrics, Logs, Traces  
☐ c) Build, Test, Release  
☐ d) Plan, Do, Check

---

## 7. Gestion des Défauts et Culture Qualité

**Question 19 (1 pt) :** Dans une matrice Severity vs Priority, comment traiter un bug "Critical Severity, Low Priority" ?

☐ a) Fix immédiat  
☐ b) Fix dans la journée  
☐ c) Planifié selon roadmap  
☐ d) Won't fix

**Question 20 (2 pts) :** Quels sont les éléments essentiels d'un bon rapport de bug ? _(Plusieurs réponses possibles)_

☐ a) Title descriptif et concis  
☐ b) Steps to reproduce précis  
☐ c) Expected vs Actual behavior  
☐ d) Environment (OS, browser, version)  
☐ e) Code source de la fonctionnalité  
☐ f) Severity et Priority

---

## Correction et Barème

**Barème total :** 25 points

- **20-25 points :** Excellent - Maîtrise complète des tests et qualité
- **16-19 points :** Bien - Bonne compréhension avec quelques lacunes
- **12-15 points :** Satisfaisant - Bases acquises, révision recommandée
- **Moins de 12 points :** Insuffisant - Révision complète nécessaire

---

## Correction

1. **a, b, d, e** Vérification, validation, détection, prévention (pas garantie sans bug)
2. **b** Les tests révèlent des bugs mais ne prouvent pas leur absence
3. **c** Coût exponentiel : 1€ → 10€ → 10000€
4. Tests unitaires → Module isolé, Tests d'intégration → Interaction composants, Tests système → Application complète, Tests d'acceptation → Validation métier
5. **a, c, d, f** Performance, sécurité, charge, usabilité (non-fonctionnels)
6. **a** Statique sans exécution, dynamique avec exécution
7. **a** 70% unitaires, 20% intégration, 10% E2E
8. **b** Red → Green → Refactor
9. **a** Q1 - Technology-facing & Supporting
10. **a, b, d, e** Functional Suitability, Performance, Reliability, Security
11. **a** 90% (45/(45+5) = 45/50 = 0.9)
12. **b** Défauts production / Total défauts
13. **a, c, e** Exploratoires, changeants, usabilité
14. **a** Fast, Independent, Repeatable, Self-validating, Timely
15. **c** Encapsuler éléments UI
16. **b** Tests plus tôt dans le cycle
17. **a, b, c, d** Canary, A/B, Feature Flags, Chaos Engineering
18. **b** Metrics, Logs, Traces
19. **c** Critical mais low priority = planifié selon roadmap
20. **a, b, c, d, f** Title, steps, expected/actual, environment, severity/priority

---

_Quiz Séance 4 - Introduction aux Tests et Qualité | Hassan ESSADIK_
