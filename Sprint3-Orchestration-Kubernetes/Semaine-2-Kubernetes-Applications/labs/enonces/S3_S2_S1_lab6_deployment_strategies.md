# LAB 6 - Stratégies de déploiement avancées

## Objectif

Implémenter les stratégies de déploiement Blue/Green et Canary avec Kubernetes.

## Contexte

Mettre en place des stratégies de déploiement sans interruption de service pour :

- Blue/Green deployment avec basculement instantané
- Canary deployment avec montée en charge progressive
- Rollback automatique en cas de problème
- Tests automatisés entre les versions

## Prérequis

- Application e-commerce fonctionnelle
- Ingress Controller NGINX installé
- Monitoring configuré (LAB 4)
- Scripts de test de charge

## Instructions détaillées

### Étape 1 : Préparer l'environnement Blue/Green

1. Créer les déploiements Blue et Green :

```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-blue
  namespace: ecommerce
  labels:
    app: api-backend
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-backend
      version: blue
  template:
    metadata:
      labels:
        app: api-backend
        version: blue
    spec:
      containers:
        - name: api
          image: ecommerce/api:v1.0.0 # Version actuelle
          ports:
            - containerPort: 3000
          env:
            - name: VERSION
              value: 'v1.0.0'
            - name: COLOR
              value: 'blue'
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5

---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-green
  namespace: ecommerce
  labels:
    app: api-backend
    version: green
spec:
  replicas: 0 # Initialement arrêté
  selector:
    matchLabels:
      app: api-backend
      version: green
  template:
    metadata:
      labels:
        app: api-backend
        version: green
    spec:
      containers:
        - name: api
          image: ecommerce/api:v2.0.0 # Nouvelle version
          ports:
            - containerPort: 3000
          env:
            - name: VERSION
              value: 'v2.0.0'
            - name: COLOR
              value: 'green'
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Étape 2 : Configurer les Services pour Blue/Green

2. Créer services pour chaque version :

```yaml
# blue-green-services.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: ecommerce
spec:
  selector:
    app: api-backend
    version: blue # Pointe initialement vers blue
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000

---
apiVersion: v1
kind: Service
metadata:
  name: api-blue-service
  namespace: ecommerce
spec:
  selector:
    app: api-backend
    version: blue
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000

---
apiVersion: v1
kind: Service
metadata:
  name: api-green-service
  namespace: ecommerce
spec:
  selector:
    app: api-backend
    version: green
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
```

### Étape 3 : Script de déploiement Blue/Green

3. Créer script automatisé pour Blue/Green :

```bash
#!/bin/bash
# blue-green-deploy.sh

NEW_VERSION=$1
NAMESPACE=${2:-ecommerce}

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new_version> [namespace]"
    exit 1
fi

echo "🔄 Démarrage du déploiement Blue/Green vers $NEW_VERSION"

# 1. Déterminer la version active
CURRENT_VERSION=$(kubectl get service api-service -n $NAMESPACE -o jsonpath='{.spec.selector.version}')
echo "📍 Version actuelle: $CURRENT_VERSION"

# 2. Déterminer la version cible
if [ "$CURRENT_VERSION" = "blue" ]; then
    TARGET_VERSION="green"
    SOURCE_VERSION="blue"
else
    TARGET_VERSION="blue"
    SOURCE_VERSION="green"
fi

echo "🎯 Déploiement vers: $TARGET_VERSION"

# 3. Mettre à jour l'image de la version cible
kubectl set image deployment/api-$TARGET_VERSION api=ecommerce/api:$NEW_VERSION -n $NAMESPACE

# 4. Scaler la version cible
kubectl scale deployment api-$TARGET_VERSION --replicas=3 -n $NAMESPACE

# 5. Attendre que la nouvelle version soit prête
echo "⏳ Attente de la disponibilité de la nouvelle version..."
kubectl rollout status deployment/api-$TARGET_VERSION -n $NAMESPACE --timeout=300s

if [ $? -ne 0 ]; then
    echo "❌ Échec du déploiement de la nouvelle version"
    kubectl scale deployment api-$TARGET_VERSION --replicas=0 -n $NAMESPACE
    exit 1
fi

# 6. Tests de santé sur la nouvelle version
echo "🔍 Tests de santé sur la nouvelle version..."
TARGET_POD=$(kubectl get pods -n $NAMESPACE -l app=api-backend,version=$TARGET_VERSION -o jsonpath='{.items[0].metadata.name}')

# Test health check
kubectl exec $TARGET_POD -n $NAMESPACE -- curl -f http://localhost:3000/health
if [ $? -ne 0 ]; then
    echo "❌ Health check échoué sur la nouvelle version"
    kubectl scale deployment api-$TARGET_VERSION --replicas=0 -n $NAMESPACE
    exit 1
fi

# 7. Tests fonctionnels (simulation)
echo "🧪 Tests fonctionnels..."
sleep 5  # Simulation de tests

# 8. Basculer le trafic
echo "🔄 Basculement du trafic vers $TARGET_VERSION"
kubectl patch service api-service -n $NAMESPACE -p '{"spec":{"selector":{"version":"'$TARGET_VERSION'"}}}'

# 9. Vérifier le basculement
sleep 10
NEW_ACTIVE=$(kubectl get service api-service -n $NAMESPACE -o jsonpath='{.spec.selector.version}')
if [ "$NEW_ACTIVE" != "$TARGET_VERSION" ]; then
    echo "❌ Échec du basculement"
    exit 1
fi

# 10. Scaler l'ancienne version à 0 (après délai de grâce)
echo "⏳ Délai de grâce de 30 secondes avant arrêt de l'ancienne version..."
sleep 30
kubectl scale deployment api-$SOURCE_VERSION --replicas=0 -n $NAMESPACE

echo "✅ Déploiement Blue/Green terminé avec succès!"
echo "📊 Version active: $TARGET_VERSION ($NEW_VERSION)"
```

### Étape 4 : Configuration Canary avec Ingress

4. Configurer Ingress pour déploiement Canary :

```yaml
# canary-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-main-ingress
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
spec:
  rules:
    - host: api.ecommerce.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 3000

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-canary-ingress
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/canary: 'true'
    nginx.ingress.kubernetes.io/canary-weight: '0' # Commencer à 0%
    nginx.ingress.kubernetes.io/canary-by-header: 'X-Canary-Version'
    nginx.ingress.kubernetes.io/canary-by-header-value: 'v2.0.0'
spec:
  rules:
    - host: api.ecommerce.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-canary-service
                port:
                  number: 3000
```

### Étape 5 : Script de déploiement Canary

5. Créer script pour déploiement Canary progressif :

```bash
#!/bin/bash
# canary-deploy.sh

NEW_VERSION=$1
NAMESPACE=${2:-ecommerce}
MAX_WEIGHT=${3:-100}

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new_version> [namespace] [max_weight]"
    exit 1
fi

echo "🐤 Démarrage du déploiement Canary vers $NEW_VERSION"

# 1. Déployer la version Canary
kubectl set image deployment/api-canary api=ecommerce/api:$NEW_VERSION -n $NAMESPACE
kubectl scale deployment api-canary --replicas=1 -n $NAMESPACE

# 2. Attendre la disponibilité
kubectl rollout status deployment/api-canary -n $NAMESPACE --timeout=300s

# 3. Déploiement progressif du trafic
WEIGHTS=(5 10 25 50 75 100)
for WEIGHT in "${WEIGHTS[@]}"; do
    if [ $WEIGHT -gt $MAX_WEIGHT ]; then
        break
    fi

    echo "📈 Redirection de ${WEIGHT}% du trafic vers Canary"

    # Mettre à jour le poids Canary
    kubectl annotate ingress api-canary-ingress \
        nginx.ingress.kubernetes.io/canary-weight=$WEIGHT \
        -n $NAMESPACE --overwrite

    # Attendre la stabilisation
    sleep 60

    # Vérifier les métriques
    echo "📊 Vérification des métriques..."

    # Simulation de vérification d'erreurs
    ERROR_RATE=$(kubectl exec -n monitoring deployment/prometheus -- \
        promtool query instant 'rate(http_requests_total{status_code=~"5.."}[5m])' | grep -o '[0-9.]*' | head -1)

    if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
        echo "⚠️  Taux d'erreur trop élevé: $ERROR_RATE"
        echo "🔄 Rollback automatique..."
        kubectl annotate ingress api-canary-ingress \
            nginx.ingress.kubernetes.io/canary-weight=0 \
            -n $NAMESPACE --overwrite
        kubectl scale deployment api-canary --replicas=0 -n $NAMESPACE
        exit 1
    fi

    echo "✅ Métriques OK pour ${WEIGHT}%"
done

# 4. Finaliser le déploiement si MAX_WEIGHT = 100
if [ $MAX_WEIGHT -eq 100 ]; then
    echo "🔄 Finalisation du déploiement Canary"

    # Basculer complètement vers Canary
    kubectl patch service api-service -n $NAMESPACE \
        -p '{"spec":{"selector":{"version":"canary"}}}'

    # Arrêter l'ancien déploiement
    kubectl scale deployment api-main --replicas=0 -n $NAMESPACE

    # Renommer Canary en main pour le prochain déploiement
    kubectl patch deployment api-canary -n $NAMESPACE \
        -p '{"metadata":{"name":"api-main"}}'
fi

echo "✅ Déploiement Canary terminé avec succès!"
```

### Étape 6 : Tests automatisés

6. Créer suite de tests pour validation des déploiements :

```bash
#!/bin/bash
# test-deployment.sh

SERVICE_URL=$1
VERSION_EXPECTED=$2

if [ -z "$SERVICE_URL" ] || [ -z "$VERSION_EXPECTED" ]; then
    echo "Usage: $0 <service_url> <expected_version>"
    exit 1
fi

echo "🧪 Tests de validation du déploiement"
echo "🎯 URL: $SERVICE_URL"
echo "📌 Version attendue: $VERSION_EXPECTED"

# Test 1: Health Check
echo "🔍 Test Health Check..."
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/health)
if [ "$HEALTH_STATUS" != "200" ]; then
    echo "❌ Health check échoué (HTTP $HEALTH_STATUS)"
    exit 1
fi
echo "✅ Health check OK"

# Test 2: Vérification de la version
echo "🔍 Test Version..."
VERSION_ACTUAL=$(curl -s $SERVICE_URL/version | jq -r .version)
if [ "$VERSION_ACTUAL" != "$VERSION_EXPECTED" ]; then
    echo "❌ Version incorrecte (attendue: $VERSION_EXPECTED, actuelle: $VERSION_ACTUAL)"
    exit 1
fi
echo "✅ Version correcte"

# Test 3: Test de charge
echo "🔍 Test de charge..."
ab -n 1000 -c 10 $SERVICE_URL/ > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Test de charge échoué"
    exit 1
fi
echo "✅ Test de charge OK"

# Test 4: Vérification des métriques
echo "🔍 Test métriques..."
METRICS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/metrics)
if [ "$METRICS_STATUS" != "200" ]; then
    echo "❌ Métriques inaccessibles"
    exit 1
fi
echo "✅ Métriques OK"

echo "🎉 Tous les tests sont passés avec succès!"
```

## Critères de validation

- [ ] Déploiements Blue et Green fonctionnels
- [ ] Script de basculement Blue/Green automatisé
- [ ] Canary deployment avec montée progressive
- [ ] Tests automatisés intégrés au processus
- [ ] Rollback automatique en cas d'erreur
- [ ] Métriques surveillées pendant les déploiements
- [ ] Zero-downtime pendant les basculements
- [ ] Documentation des procédures

## Tests pratiques

```bash
# Test Blue/Green
./blue-green-deploy.sh v2.0.0
./test-deployment.sh http://api.ecommerce.local v2.0.0

# Test Canary
./canary-deploy.sh v2.1.0 ecommerce 50  # Canary à 50% max
./test-deployment.sh http://api.ecommerce.local v2.1.0

# Test Rollback
kubectl rollout undo deployment/api-green -n ecommerce
```

## Durée estimée

45 minutes
