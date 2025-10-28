# Application Node.js pour démonstration Kubernetes

Cette application simple est conçue pour démontrer les concepts de base de Kubernetes avec des Pods et Deployments.

## 🎯 Objectif pédagogique

- Créer un premier Pod Kubernetes
- Comprendre le comportement des conteneurs qui crashent
- Tester les mécanismes de redémarrage automatique

## 📋 Endpoints disponibles

- **GET /** : Page d'accueil avec informations sur l'application
- **GET /404** : Endpoint qui provoque un crash intentionnel avec `exit(1)`
- **GET /health** : Endpoint de santé pour les health checks Kubernetes

## 🚀 Installation locale

```bash
# Installer les dépendances
npm install

# Démarrer l'application
npm start
```

L'application sera accessible sur http://localhost:3000

## 🐳 Containerisation

### Dockerfile

Un Dockerfile est inclus pour créer une image Docker de l'application.

### Construction de l'image

```bash
docker build -t demo-pod-app:v1.0 .
```

### Test local avec Docker

```bash
docker run -p 3000:3000 demo-pod-app:v1.0
```

## ☸️ Déploiement Kubernetes

### Exemples de manifests inclus :

1. **pod.yaml** : Pod simple
2. **deployment.yaml** : Deployment avec réplication
3. **service.yaml** : Service pour exposer l'application

### Commandes Kubernetes

```bash
# Créer un Pod
kubectl apply -f k8s/pod.yaml

# Créer un Deployment
kubectl apply -f k8s/deployment.yaml

# Créer un Service
kubectl apply -f k8s/service.yaml

# Tester l'endpoint qui crash
kubectl port-forward pod/demo-pod 3000:3000
curl http://localhost:3000/404
```

## 🧪 Tests de crash

L'endpoint `/404` est conçu pour simuler un crash d'application :

- Retourne un message d'erreur
- Termine l'application avec `exit(1)`
- Permet de tester la résilience Kubernetes

Kubernetes redémarrera automatiquement le Pod en cas de crash !
