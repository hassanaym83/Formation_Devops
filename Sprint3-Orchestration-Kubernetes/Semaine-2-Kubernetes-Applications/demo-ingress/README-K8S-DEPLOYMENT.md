# Déploiement Kubernetes - Application de Gestion des Dons de Sang

## Vue d'ensemble

Cette documentation décrit le déploiement complet de l'application de gestion des campagnes de don de sang sur Kubernetes. L'application est composée de 7 services conteneurisés déployés via des manifestes Kubernetes.

## Architecture de l'application

```
┌─────────────────┐    ┌─────────────────┐
│  Donor Frontend │    │ Admin Dashboard │
│    (Port 3100)  │    │    (Port 3200)  │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
              ┌──────▼──────┐
              │   Ingress   │
              │ Controller  │
              └──────┬──────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐  ┌────▼────┐  ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
│ User  │  │Campaign │  │Appoint. │  │Analytics│  │ Admin   │
│Service│  │Service  │  │Service  │  │Service  │  │Service  │
│:3001  │  │:3002    │  │:3003    │  │:3004    │  │:3005    │
└───┬───┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
    └────────────┼────────────┼────────────┼────────────┘
                 │            │            │
              ┌──▼────────────▼────────────▼──┐
              │         MySQL Database        │
              │           (Port 3306)         │
              └───────────────────────────────┘
```

## Structure des artefacts Kubernetes

```
demo-ingress/
├── k8s/                              # Dossier principal Kubernetes
│   ├── namespace/                    # Isolation des ressources
│   │   └── namespace.yaml
│   ├── configmaps/                   # Configuration non-sensible
│   │   ├── mysql-config.yaml
│   │   ├── user-service-config.yaml
│   │   ├── campaign-service-config.yaml
│   │   ├── appointment-service-config.yaml
│   │   ├── analytics-service-config.yaml
│   │   └── admin-service-config.yaml
│   ├── secrets/                      # Données sensibles
│   │   ├── mysql-secret.yaml
│   │   └── jwt-secret.yaml
│   ├── storage/                      # Stockage persistant
│   │   ├── mysql-pv.yaml
│   │   └── mysql-pvc.yaml
│   ├── database/                     # Base de données
│   │   ├── mysql-deployment.yaml
│   │   └── mysql-service.yaml
│   ├── backend-services/             # Services API
│   │   ├── user-service-deployment.yaml
│   │   ├── user-service-service.yaml
│   │   ├── campaign-service-deployment.yaml
│   │   ├── campaign-service-service.yaml
│   │   ├── appointment-service-deployment.yaml
│   │   ├── appointment-service-service.yaml
│   │   ├── analytics-service-deployment.yaml
│   │   ├── analytics-service-service.yaml
│   │   ├── admin-service-deployment.yaml
│   │   └── admin-service-service.yaml
│   ├── frontend-services/            # Interfaces utilisateur
│   │   ├── donor-frontend-deployment.yaml
│   │   ├── donor-frontend-service.yaml
│   │   ├── admin-dashboard-deployment.yaml
│   │   └── admin-dashboard-service.yaml
│   ├── ingress/                      # Exposition externe
│   │   └── app-ingress.yaml
│   └── kustomization/                # Gestion des environnements
│       ├── base/
│       │   └── kustomization.yaml
│       └── overlays/
│           ├── dev/
│           └── prod/
```

## Plan de déploiement - 8 étapes

### **Étape 1 : Namespace et ConfigMaps**

**Objectif** : Créer le namespace et centraliser la configuration

**Ressources à créer** :

- `namespace.yaml` - Namespace `blood-donation`
- `mysql-config.yaml` - Configuration MySQL
- `user-service-config.yaml` - Config service utilisateurs
- `campaign-service-config.yaml` - Config service campagnes
- `appointment-service-config.yaml` - Config service RDV
- `analytics-service-config.yaml` - Config service analytics
- `admin-service-config.yaml` - Config service admin

**Concepts Kubernetes** : `Namespace`, `ConfigMap`

---

### **Étape 2 : Secrets**

**Objectif** : Gérer les données sensibles de manière sécurisée

**Ressources à créer** :

- `mysql-secret.yaml` - Mots de passe MySQL
- `jwt-secret.yaml` - Clés JWT pour l'authentification

**Concepts Kubernetes** : `Secret`, encodage base64, sécurité

---

### **Étape 3 : Stockage persistant**

**Objectif** : Configurer le stockage pour la persistance des données

**Ressources à créer** :

- `mysql-pv.yaml` - PersistentVolume pour MySQL
- `mysql-pvc.yaml` - PersistentVolumeClaim pour MySQL

**Concepts Kubernetes** : `PersistentVolume`, `PersistentVolumeClaim`, `StorageClass`

---

### **Étape 4 : Base de données MySQL**

**Objectif** : Déployer MySQL avec persistance

**Ressources à créer** :

- `mysql-deployment.yaml` - Déploiement MySQL avec volumes
- `mysql-service.yaml` - Service ClusterIP pour MySQL

**Concepts Kubernetes** : `Deployment`, `ReplicaSet`, `Pod`, `Service ClusterIP`, `Volume`

---

### **Étape 5 : Services Backend (APIs)**

**Objectif** : Déployer les 5 microservices API

**Ressources à créer** :

- `user-service-deployment.yaml` + `user-service-service.yaml`
- `campaign-service-deployment.yaml` + `campaign-service-service.yaml`
- `appointment-service-deployment.yaml` + `appointment-service-service.yaml`
- `analytics-service-deployment.yaml` + `analytics-service-service.yaml`
- `admin-service-deployment.yaml` + `admin-service-service.yaml`

**Concepts Kubernetes** : `Deployment`, `Service ClusterIP`, `Environment Variables`, `Health Checks`

---

### **Étape 6 : Services Frontend**

**Objectif** : Déployer les interfaces utilisateur

**Ressources à créer** :

- `donor-frontend-deployment.yaml` + `donor-frontend-service.yaml`
- `admin-dashboard-deployment.yaml` + `admin-dashboard-service.yaml`

**Concepts Kubernetes** : `Deployment`, `Service NodePort/LoadBalancer`

---

### **Étape 7 : Ingress Controller et Ingress**

**Objectif** : Exposer l'application via Ingress (OBJECTIF PRINCIPAL !)

**Ressources à créer** :

- `app-ingress.yaml` - Règles de routage HTTP

**Prérequis** :

- Installation Ingress Controller (NGINX)

**Concepts Kubernetes** : `Ingress Controller`, `Ingress`, routage HTTP, exposition externe

---

### **Étape 8 : Test et validation complète**

**Objectif** : Validation du déploiement complet

**Actions** :

- Déploiement de tous les manifestes
- Tests de connectivité inter-services
- Validation des règles Ingress
- Tests fonctionnels de l'application

---

## Services et Ports

| Service             | Type        | Port Interne | Port Exposé | Description        |
| ------------------- | ----------- | ------------ | ----------- | ------------------ |
| mysql               | ClusterIP   | 3306         | -           | Base de données    |
| user-service        | ClusterIP   | 3001         | -           | API Utilisateurs   |
| campaign-service    | ClusterIP   | 3002         | -           | API Campagnes      |
| appointment-service | ClusterIP   | 3003         | -           | API Rendez-vous    |
| analytics-service   | ClusterIP   | 3004         | -           | API Analytics      |
| admin-service       | ClusterIP   | 3005         | -           | API Administration |
| donor-frontend      | NodePort/LB | 3100         | 30100       | Interface Donneurs |
| admin-dashboard     | NodePort/LB | 3200         | 30200       | Interface Admin    |

## Variables d'environnement

### Configuration commune (ConfigMaps)

```yaml
DB_HOST: mysql-service
DB_PORT: '3306'
DB_NAME: dondesang
DB_USER: blooduser
NODE_ENV: production
CORS_ORIGIN: '*'
```

### Données sensibles (Secrets)

```yaml
DB_PASSWORD: <base64-encoded>
MYSQL_ROOT_PASSWORD: <base64-encoded>
JWT_SECRET: <base64-encoded>
ADMIN_JWT_SECRET: <base64-encoded>
```

## Commandes de déploiement

### Déploiement par étapes

```bash
# Étape 1 : Namespace et ConfigMaps
kubectl apply -f k8s/namespace/
kubectl apply -f k8s/configmaps/

# Étape 2 : Secrets
kubectl apply -f k8s/secrets/

# Étape 3 : Stockage
kubectl apply -f k8s/storage/

# Étape 4 : Base de données
kubectl apply -f k8s/database/

# Étape 5 : Services Backend
kubectl apply -f k8s/backend-services/

# Étape 6 : Services Frontend
kubectl apply -f k8s/frontend-services/

# Étape 7 : Ingress
kubectl apply -f k8s/ingress/
```

### Déploiement complet

```bash
# Déploiement de toute l'application
kubectl apply -f k8s/ --recursive

# Vérification du déploiement
kubectl get all -n blood-donation
```

## Commandes de monitoring

```bash
# Vérifier les pods
kubectl get pods -n blood-donation

# Vérifier les services
kubectl get services -n blood-donation

# Vérifier les ingress
kubectl get ingress -n blood-donation

# Voir les logs d'un service
kubectl logs -f deployment/user-service -n blood-donation

# Accéder à un pod pour debug
kubectl exec -it <pod-name> -n blood-donation -- /bin/sh
```

## Accès à l'application

Une fois déployé avec Ingress :

- **Interface Donneurs** : `http://<ingress-ip>/donor` ou `http://blood-donation.local/donor`
- **Dashboard Admin** : `http://<ingress-ip>/admin` ou `http://blood-donation.local/admin`
- **APIs** : `http://<ingress-ip>/api/...`

## Notes importantes

1. **Ordre de déploiement** : Respecter l'ordre des étapes (dépendances)
2. **Secrets** : Changer les mots de passe par défaut en production
3. **Storage** : Configurer un StorageClass approprié pour la production
4. **Ingress Controller** : Installer un Ingress Controller avant l'étape 7
5. **DNS** : Configurer le DNS ou /etc/hosts pour les noms de domaines

## Processus de validation

À chaque étape :

1. Créer les manifestes YAML
2. Valider la syntaxe avec `kubectl apply --dry-run=client`
3. Appliquer les manifestes
4. Vérifier le statut des ressources
5. Passer à l'étape suivante

---

**Objectif principal** : Maîtriser les **Ingress** pour l'exposition et le routage HTTP de l'application microservices.
