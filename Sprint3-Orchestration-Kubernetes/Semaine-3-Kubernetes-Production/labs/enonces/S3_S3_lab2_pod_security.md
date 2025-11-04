# LAB 2 - Pod Security et Network Policies

## Objectifs

- Implémenter Pod Security Standards
- Configurer des Network Policies avancées
- Sécuriser la communication inter-pods
- Mettre en place la micro-segmentation réseau

## Prérequis

- Cluster Kubernetes avec CNI supportant Network Policies (Calico, Cilium, etc.)
- Kubectl configuré
- Connaissance des concepts réseau Kubernetes

## Contexte du LAB

Vous devez sécuriser une application e-commerce avec plusieurs microservices :

- **Frontend** (React SPA)
- **API Gateway**
- **Service de paiement** (sensible)
- **Base de données** (très sensible)
- **Service de logs** (accès lecture pour tous)

## Exercice 1 : Configuration Pod Security Standards

### Étape 1.1 : Namespaces avec niveaux de sécurité

Créez des namespaces avec différents niveaux Pod Security :

```yaml
# frontend-ns.yaml
# Niveau : baseline (interface utilisateur)

# payment-ns.yaml
# Niveau : restricted (données sensibles)

# database-ns.yaml
# Niveau : restricted (très sensible)
```

### Étape 1.2 : Pod sécurisé niveau baseline

Créez un deployment frontend avec Pod Security baseline :

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: frontend-ns
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: web
    spec:
      # Compléter avec les contraintes de sécurité baseline
      containers:
        - name: frontend
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
          # Ajouter les configurations de sécurité
```

### Étape 1.3 : Pod sécurisé niveau restricted

Créez un deployment pour le service de paiement avec niveau restricted :

```yaml
# payment-deployment.yaml
# Compléter avec toutes les contraintes restricted
```

## Exercice 2 : Security Context avancé

### Étape 2.1 : Pod avec utilisateur non-root

Créez un pod qui :

- Execute avec un utilisateur non-root spécifique (UID 1001)
- A un système de fichiers en lecture seule
- N'autorise pas l'escalade de privilèges
- Utilise un profil seccomp restrictif

```yaml
# secure-pod.yaml
```

### Étape 2.2 : Configuration avec capabilities

Créez un pod qui drop toutes les capabilities Linux :

```yaml
# no-caps-pod.yaml
```

### Étape 2.3 : Pod avec volumes sécurisés

Déployez un pod avec :

- Volume tmpfs pour les fichiers temporaires
- Volume configmap monté en lecture seule
- Pas de volume hostPath

```yaml
# secure-volumes-pod.yaml
```

## Exercice 3 : Network Policies - Isolation de base

### Étape 3.1 : Deny-all par défaut

Créez une Network Policy qui bloque tout le trafic par défaut :

```yaml
# default-deny-all.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: # À compléter
spec:
  # Compléter la policy
```

### Étape 3.2 : Autoriser DNS

Créez une policy qui autorise uniquement les requêtes DNS :

```yaml
# allow-dns.yaml
```

### Étape 3.3 : Isolation entre namespaces

Créez des policies qui interdisent la communication entre namespaces :

```yaml
# namespace-isolation.yaml
```

## Exercice 4 : Network Policies - Micro-segmentation

### Étape 4.1 : Frontend vers API Gateway

Autorisez uniquement le frontend à communiquer avec l'API Gateway :

```yaml
# frontend-to-api.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-api
  namespace: api-ns
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
    - Ingress
  ingress:
    - from:
      # Compléter les règles
      ports:
      # Compléter les ports
```

### Étape 4.2 : API Gateway vers services métier

L'API Gateway doit pouvoir accéder aux services :

- Service utilisateur (port 8080)
- Service produit (port 8081)
- Mais PAS au service de paiement directement

```yaml
# api-to-services.yaml
```

### Étape 4.3 : Service de paiement isolation

Le service de paiement ne doit être accessible que par :

- L'API Gateway (pour les transactions)
- Le service de monitoring (pour les métriques)

```yaml
# payment-access.yaml
```

## Exercice 5 : Database Security avancée

### Étape 5.1 : Database Network Policy

La base de données doit être accessible uniquement par :

- Services autorisés avec label `db-access: allowed`
- Sur le port 5432 uniquement
- Depuis des namespaces spécifiques

```yaml
# database-policy.yaml
```

### Étape 5.2 : Database Pod Security

Créez un déploiement PostgreSQL avec sécurité maximale :

```yaml
# secure-database.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-postgres
  namespace: database-ns
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
      db-access: allowed
  template:
    metadata:
      labels:
        app: postgres
        db-access: allowed
    spec:
      # Configuration sécurité maximale
      securityContext:
        # Compléter
      containers:
        - name: postgres
          image: postgres:14-alpine
          # Compléter la configuration sécurisée
```

## Exercice 6 : Egress Policies

### Étape 6.1 : Restriction accès externe

Créez des policies qui limitent l'accès externe :

- Frontend : peut accéder aux CDN (ports 80/443)
- API : peut accéder aux services externes d'API (liste blanche)
- Database : aucun accès externe

```yaml
# egress-policies.yaml
```

### Étape 6.2 : Proxy pour accès externe

Configurez un proxy pour contrôler l'accès externe :

```yaml
# egress-proxy.yaml
```

## Exercice 7 : Monitoring et observabilité

### Étape 7.1 : Network Policy pour monitoring

Autorisez Prometheus à collecter les métriques de tous les services :

```yaml
# monitoring-access.yaml
```

### Étape 7.2 : Logging centralisé

Permettez à Fluent Bit de collecter les logs :

```yaml
# logging-access.yaml
```

## Exercice 8 : Test et validation

### Étape 8.1 : Script de test réseau

Créez un script qui teste toutes les connexions :

```bash
#!/bin/bash
# test-network-policies.sh

echo "Testing network policies..."

# Test 1: Frontend peut accéder à l'API
kubectl run test-frontend --rm -i --tty --restart=Never \
  --image=busybox --namespace=frontend-ns \
  -- wget -qO- http://api-gateway.api-ns:8080/health

# Test 2: Frontend ne peut PAS accéder directement à la DB
kubectl run test-frontend-db --rm -i --tty --restart=Never \
  --image=busybox --namespace=frontend-ns \
  -- nc -zv postgres.database-ns 5432

# Ajouter d'autres tests...
```

### Étape 8.2 : Validation Pod Security

Script pour valider la conformité Pod Security :

```bash
#!/bin/bash
# validate-pod-security.sh
```

## Exercice 9 : Cas d'urgence et maintenance

### Étape 9.1 : Break-glass access

Créez une procédure d'accès d'urgence qui :

- Permet un accès temporaire en cas d'incident
- Log tous les accès d'urgence
- Se révoque automatiquement après 1h

```yaml
# emergency-access.yaml
```

### Étape 9.2 : Maintenance windows

Policy pour les fenêtres de maintenance :

```yaml
# maintenance-policy.yaml
```

## Exercice 10 : Architecture complète

Déployez l'architecture e-commerce complète avec :

```yaml
# ecommerce-architecture.yaml
# - Frontend (3 replicas)
# - API Gateway (2 replicas)
# - User Service (2 replicas)
# - Product Service (2 replicas)
# - Payment Service (2 replicas)
# - Database (1 replica)
# - Redis Cache (1 replica)
# - Monitoring stack

# Toutes les Network Policies
# Tous les Pod Security Standards
# Toute la configuration de sécurité
```

## Tests d'intrusion et validation

### Test 1 : Tentative d'accès non autorisé

```bash
# Tenter d'accéder à la DB depuis le frontend
```

### Test 2 : Escalade de privilèges

```bash
# Tenter d'exécuter en tant que root
```

### Test 3 : Accès réseau non autorisé

```bash
# Tenter communication entre namespaces interdits
```

## Questions de validation

1. Quelle est la différence entre les niveaux Pod Security privileged, baseline et restricted ?
2. Comment déboguer une Network Policy qui bloque le trafic ?
3. Quels sont les risques de ne pas utiliser de Security Context ?
4. Comment implémenter une stratégie zero-trust avec Network Policies ?

## Livrables attendus

1. `pod-security-namespaces.yaml` - Namespaces avec Pod Security
2. `secure-deployments.yaml` - Deployments sécurisés
3. `network-policies.yaml` - Toutes les Network Policies
4. `test-scripts/` - Scripts de test et validation
5. `ecommerce-secure-architecture.yaml` - Architecture complète
6. `emergency-procedures.md` - Procédures d'urgence
7. `security-documentation.md` - Documentation sécurité

## Critères d'évaluation

- **Isolation** : Communication autorisée uniquement où nécessaire
- **Sécurité** : Pods conformes aux standards de sécurité
- **Fonctionnalité** : L'application fonctionne correctement
- **Observabilité** : Monitoring et logging configurés
- **Résilience** : Procédures d'urgence définies
- **Documentation** : Architecture et choix bien documentés

## Ressources utiles

- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [Calico Network Policies](https://docs.projectcalico.org/security/calico-network-policy)

---

**Durée estimée : 4-5 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
