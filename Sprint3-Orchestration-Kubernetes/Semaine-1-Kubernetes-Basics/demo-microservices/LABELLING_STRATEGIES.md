## 🏷️ Stratégies de Labelling Kubernetes

### ❌ **PROBLÈME IDENTIFIÉ**

```bash
# Tous les objets ont le même label
kubectl get all -l app=frontend

# Résultat : TOUT est sélectionné !
NAME                                     READY   STATUS
deployment.apps/frontend-deployment      1/1     Ready
service/frontend-service                 1       Ready
pod/frontend-deployment-xxx              2/2     Running
```

### ✅ **SOLUTION 1 : Labels Hiérarchiques**

#### Deployment

```yaml
metadata:
  name: frontend-deployment
  labels:
    app: frontend # Application
    component: deployment # Type d'objet
    tier: frontend # Couche
```

#### Service

```yaml
metadata:
  name: frontend-service
  labels:
    app: frontend # Application
    component: service # Type d'objet
    tier: frontend # Couche
```

#### Pods (dans template)

```yaml
template:
  metadata:
    labels:
      app: frontend # Application
      component: pod # Type d'objet
      tier: frontend # Couche
```

### 📊 **Requêtes Sélectives**

```bash
# Sélectionner par application
kubectl get all -l app=frontend

# Sélectionner par type d'objet
kubectl get all -l component=deployment
kubectl get all -l component=service
kubectl get all -l component=pod

# Sélectionner par couche
kubectl get all -l tier=frontend

# Combinaisons
kubectl get deployments -l app=frontend,component=deployment
kubectl get services -l app=frontend,component=service
```

---

### ✅ **SOLUTION 2 : Labels Distincts**

#### Deployment

```yaml
metadata:
  name: frontend-deployment
  labels:
    app-deployment: frontend-deploy
    app: frontend
    tier: frontend
```

#### Service

```yaml
metadata:
  name: frontend-service
  labels:
    app-service: frontend-svc
    app: frontend
    tier: frontend
```

#### Pods

```yaml
template:
  metadata:
    labels:
      app-pod: frontend-pod
      app: frontend
      tier: frontend
```

### 📊 **Requêtes Distinctes**

```bash
# Sélectionner chaque type individuellement
kubectl get deployments -l app-deployment=frontend-deploy
kubectl get services -l app-service=frontend-svc
kubectl get pods -l app-pod=frontend-pod

# Sélectionner toute l'application
kubectl get all -l app=frontend
```

---

### ✅ **SOLUTION 3 : Labels Standards Kubernetes**

#### Deployment

```yaml
metadata:
  name: frontend-deployment
  labels:
    app.kubernetes.io/name: frontend
    app.kubernetes.io/component: deployment
    app.kubernetes.io/part-of: microservices-demo
    app.kubernetes.io/instance: prod-frontend
```

#### Service

```yaml
metadata:
  name: frontend-service
  labels:
    app.kubernetes.io/name: frontend
    app.kubernetes.io/component: service
    app.kubernetes.io/part-of: microservices-demo
    app.kubernetes.io/instance: prod-frontend
```

### 📊 **Requêtes Standards**

```bash
# Par nom d'application
kubectl get all -l app.kubernetes.io/name=frontend

# Par composant
kubectl get all -l app.kubernetes.io/component=deployment
kubectl get all -l app.kubernetes.io/component=service

# Par projet
kubectl get all -l app.kubernetes.io/part-of=microservices-demo
```

---

### 🎯 **RECOMMANDATION POUR VOS ÉTUDIANTS**

**Utilisez la Solution 1 (Labels Hiérarchiques)** - Plus simple à comprendre :

```yaml
# Pattern recommandé
labels:
  app: [nom-application] # Ex: frontend, backend, database
  component: [type-objet] # Ex: deployment, service, pod
  tier: [couche] # Ex: frontend, backend, database
  environment: [env] # Ex: dev, staging, prod
```

### 📋 **Exemples Pratiques**

```bash
# Voir tous les objets de l'app frontend
kubectl get all -l app=frontend

# Voir seulement les deployments
kubectl get deployments -l component=deployment

# Voir seulement les services
kubectl get services -l component=service

# Voir seulement les pods
kubectl get pods -l component=pod

# Combinaisons utiles
kubectl get all -l app=frontend,environment=prod
kubectl logs -l app=frontend,component=pod
kubectl delete all -l app=frontend,environment=dev
```

### 🔍 **Debugging avec Labels**

```bash
# Vérifier les labels d'un objet
kubectl describe deployment frontend-deployment

# Lister avec labels visibles
kubectl get pods --show-labels

# Filtrer par labels multiples
kubectl get pods -l app=frontend,tier=frontend
```
