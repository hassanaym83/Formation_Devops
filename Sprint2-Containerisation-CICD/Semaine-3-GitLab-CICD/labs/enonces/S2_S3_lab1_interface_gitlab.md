# LAB 1 - Découverte interface GitLab CI/CD

## Contexte

Vous êtes nouvellement arrivé dans une équipe DevOps qui utilise GitLab pour tous ses projets. Votre première mission est de vous familiariser avec l'interface GitLab CI/CD pour comprendre l'écosystème et identifier tous les composants essentiels.

## Objectif

Naviguer dans GitLab.com et identifier tous les éléments CI/CD disponibles pour comprendre l'architecture globale et les possibilités offertes.

## Prérequis

- Accès internet
- Navigateur web moderne
- Compte GitLab.com (gratuit)

## Instructions détaillées

### Étape 1 : Création compte GitLab.com (5 minutes)

1. Aller sur https://gitlab.com
2. Cliquer sur "Register"
3. Créer un compte avec email professionnel
4. Vérifier l'email et activer le compte
5. Compléter le profil avec informations DevOps

### Étape 2 : Exploration projet GitLab (8 minutes)

1. Rechercher le projet public : `gitlab-org/gitlab`
2. Explorer la structure du projet :
   - Code source et branches
   - Issues et merge requests
   - Wiki et documentation
3. Identifier la section "CI/CD" dans le menu latéral
4. Noter l'organisation générale de l'interface

### Étape 3 : Analyse interface CI/CD (7 minutes)

Dans la section CI/CD du projet, explorer et documenter :

1. **Pipelines** :

   - Voir les pipelines récents
   - Analyser le statut (success, failed, running)
   - Identifier la durée d'exécution

2. **Jobs** :

   - Cliquer sur un pipeline pour voir les jobs
   - Observer les stages et leur organisation
   - Noter les artifacts et logs disponibles

3. **Schedules** :

   - Voir les pipelines planifiés
   - Comprendre la configuration cron

4. **Runner** :
   - Identifier les runners disponibles
   - Noter les différents types (shared, group, project)

## Livrables attendus

Créer un document Markdown `gitlab_interface_analysis.md` contenant :

### Section 1 : Vue d'ensemble GitLab

- Capture d'écran de la page principale du projet
- Description en 3 phrases de l'organisation GitLab

### Section 2 : Composants CI/CD identifiés

Pour chaque composant, fournir :

- Nom du composant
- Fonction principale
- Exemple concret observé

**Composants à identifier (8 minimum requis)** :

1. Pipelines
2. Jobs
3. Stages
4. Runners
5. Artifacts
6. Variables
7. Environments
8. Schedules

### Section 3 : Observations personnelles

- 3 avantages de GitLab CI/CD observés
- 2 questions ou points à approfondir
- Comparaison rapide avec un autre outil CI/CD connu

## Critères d'évaluation

**Total : 15 points**

- **Identification complète (8 points)** : 8 composants CI/CD correctement identifiés et décrits
- **Captures d'écran (3 points)** : Screenshots pertinents et annotés
- **Analyse qualité (2 points)** : Observations personnelles pertinentes
- **Format documentation (2 points)** : Markdown structuré et professionnel

## Durée estimée

**20 minutes** réparties :

- Création compte : 5 minutes
- Exploration : 8 minutes
- Analyse : 7 minutes

## Conseils

- Ne pas hésiter à cliquer et explorer
- Prendre des notes pendant l'exploration
- Utiliser les tooltips et aide contextuelle
- Observer les patterns d'organisation des jobs

## Ressources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Projet exemple GitLab](https://gitlab.com/gitlab-org/gitlab)
- [Interface GitLab Guide](https://docs.gitlab.com/ee/user/project/)
