# LAB 1 - RBAC et sécurité cluster

## Objectifs

- Configurer RBAC pour différents rôles utilisateurs
- Créer des ServiceAccounts sécurisés
- Implémenter des politiques d'accès granulaires
- Tester les permissions et accès

## Prérequis

- Cluster Kubernetes fonctionnel
- Kubectl configuré avec droits admin
- Connaissance des concepts RBAC

## Contexte du LAB

Vous devez sécuriser un cluster Kubernetes pour une entreprise avec plusieurs équipes :

- **Équipe Development** : Accès complet au namespace `dev`
- **Équipe QA** : Accès lecture/écriture au namespace `staging`
- **Équipe Production** : Accès lecture seule au namespace `production`
- **Équipe DevOps** : Accès admin sur tous les namespaces

## Exercice 1 : Création des namespaces et structure

### Étape 1.1 : Créer les namespaces

Créez les namespaces suivants avec les labels de sécurité appropriés :

```bash
# Votre code ici
```

**Attendu :**

- Namespace `dev` avec Pod Security Standard `baseline`
- Namespace `staging` avec Pod Security Standard `restricted`
- Namespace `production` avec Pod Security Standard `restricted`

### Étape 1.2 : Créer les groupes d'utilisateurs

Créez un fichier `users-config.yaml` définissant les utilisateurs :

```yaml
# Compléter la configuration
```

## Exercice 2 : Configuration RBAC pour l'équipe Development

### Étape 2.1 : Créer un Role pour l'équipe dev

Créez un Role `dev-full-access` dans le namespace `dev` :

**Permissions requises :**

- Tous les verbes sur les pods, services, deployments
- Lecture seule sur les secrets et configmaps
- Pas d'accès aux resources de sécurité (rolebindings, roles)

```yaml
# Votre Role ici
```

### Étape 2.2 : Créer le RoleBinding

Liez le Role aux utilisateurs de l'équipe dev :

```yaml
# Votre RoleBinding ici
```

### Étape 2.3 : Créer un ServiceAccount pour les applications

Créez un ServiceAccount `dev-app-sa` avec des permissions limitées :

```yaml
# Votre ServiceAccount ici
```

## Exercice 3 : Configuration RBAC pour l'équipe QA

### Étape 3.1 : ClusterRole pour l'équipe QA

L'équipe QA a besoin d'accéder aux namespaces `dev` et `staging`. Créez un ClusterRole `qa-access` :

**Permissions :**

- Lecture/écriture sur pods, services, deployments dans dev et staging
- Lecture seule sur les logs de pods
- Accès aux metrics des pods

```yaml
# Votre ClusterRole ici
```

### Étape 3.2 : ClusterRoleBinding pour QA

```yaml
# Votre ClusterRoleBinding ici
```

## Exercice 4 : Configuration pour l'équipe Production

### Étape 4.1 : Role lecture seule production

Créez un Role `prod-readonly` :

```yaml
# Votre Role ici
```

### Étape 4.2 : Test des permissions

Créez un script de test `test-permissions.sh` qui vérifie :

- L'équipe dev peut créer des pods dans `dev`
- L'équipe QA peut lire dans `staging`
- L'équipe prod ne peut pas modifier `production`

```bash
#!/bin/bash
# Votre script de test ici
```

## Exercice 5 : ServiceAccount avancé pour applications

### Étape 5.1 : ServiceAccount avec token auto-monté

Créez un ServiceAccount `secure-app-sa` qui :

- N'auto-monte pas le token par défaut
- Utilise un token avec expiration limitée
- A accès uniquement aux configmaps de son namespace

```yaml
# Votre configuration ici
```

### Étape 5.2 : Pod utilisant ce ServiceAccount

Déployez un pod nginx qui utilise ce ServiceAccount :

```yaml
# Votre Pod ici
```

## Exercice 6 : Audit et monitoring des accès

### Étape 6.1 : Configuration d'audit

Créez une politique d'audit `audit-policy.yaml` qui log :

- Toutes les actions dans le namespace `production`
- Les échecs d'authentification
- Les modifications de RBAC

```yaml
# Votre politique d'audit ici
```

### Étape 6.2 : RBAC pour monitoring

Créez les permissions pour que Prometheus puisse collecter les métriques :

```yaml
# Votre configuration monitoring ici
```

## Exercice 7 : Sécurisation avancée

### Étape 7.1 : Admission Controller

Configurez un ValidatingAdmissionWebhook qui rejette :

- Les pods sans SecurityContext
- Les ServiceAccounts sans annotations de sécurité

```yaml
# Votre webhook ici
```

### Étape 7.2 : Network Policy pour isolation RBAC

Créez des Network Policies qui isolent les namespaces selon les équipes :

```yaml
# Vos Network Policies ici
```

## Exercice 8 : Cas pratique - Application multi-tiers

Déployez une application avec :

- Frontend (namespace `dev`)
- API (namespace `staging`)
- Database (namespace `production`)

Chaque composant doit avoir :

- Son propre ServiceAccount
- Des permissions minimales
- Communication sécurisée entre les tiers

```yaml
# Votre architecture complète ici
```

## Questions de validation

1. Comment vérifier les permissions effectives d'un utilisateur ?
2. Quelle est la différence entre Role et ClusterRole ?
3. Comment déboguer un problème d'autorisation RBAC ?
4. Quelles sont les bonnes pratiques pour les ServiceAccounts ?

## Livrables attendus

1. `namespaces.yaml` - Configuration des namespaces
2. `rbac-dev.yaml` - RBAC pour équipe dev
3. `rbac-qa.yaml` - RBAC pour équipe QA
4. `rbac-prod.yaml` - RBAC pour équipe production
5. `serviceaccounts.yaml` - ServiceAccounts sécurisés
6. `test-permissions.sh` - Script de test
7. `audit-policy.yaml` - Politique d'audit
8. `multi-tier-app.yaml` - Application complète
9. `README.md` - Documentation et explication des choix

## Critères d'évaluation

- **Sécurité** : Respect du principe de moindre privilège
- **Fonctionnalité** : Les permissions permettent le travail des équipes
- **Isolation** : Les équipes ne peuvent pas accéder aux resources des autres
- **Monitoring** : Audit et logging configurés correctement
- **Documentation** : Explication claire des choix architecturaux

## Ressources utiles

- [Documentation RBAC Kubernetes](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [ServiceAccount Security](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)

---

**Durée estimée : 3-4 heures**  
**Difficulté : ⭐⭐⭐⭐**
