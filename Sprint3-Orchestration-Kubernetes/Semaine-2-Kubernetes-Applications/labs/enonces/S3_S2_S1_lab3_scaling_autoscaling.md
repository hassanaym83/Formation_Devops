# LAB 3 - Scaling et Autoscaling

## Objectif

Configurer l'autoscaling horizontal et vertical pour gérer automatiquement la charge applicative.

## Contexte

Mettre en place l'autoscaling sur l'application e-commerce pour :

- Gérer les pics de trafic automatiquement
- Optimiser l'utilisation des ressources
- Assurer une performance constante sous charge variable

## Prérequis

- Application e-commerce déployée
- Metrics-server installé sur le cluster
- Prometheus pour métriques custom (optionnel)

## Instructions détaillées

### Étape 1 : Installer et configurer metrics-server

1. Vérifier ou installer metrics-server :

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Vérifier l'installation
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
kubectl top pods -n ecommerce
```

### Étape 2 : Configurer HPA pour l'API backend

2. Créer HorizontalPodAutoscaler pour l'API :

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
```

### Étape 3 : Configurer HPA pour le frontend

3. Créer HPA pour le frontend avec métriques custom :

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 2
  maxReplicas: 8
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Object
      object:
        metric:
          name: nginx_ingress_controller_requests_rate
        target:
          type: Value
          value: '100'
        describedObject:
          apiVersion: v1
          kind: Service
          name: frontend-service
```

### Étape 4 : Générer de la charge pour tester l'autoscaling

4. Créer un job de test de charge :

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: load-test
  namespace: ecommerce
spec:
  template:
    spec:
      containers:
        - name: load-test
          image: busybox
          command:
            - /bin/sh
            - -c
            - |
              apk add --no-cache curl
              while true; do
                for i in $(seq 1 10); do
                  curl -s http://frontend-service/ > /dev/null &
                  curl -s http://api-service/health > /dev/null &
                done
                wait
                sleep 1
              done
      restartPolicy: Never
```

### Étape 5 : Configurer VPA (Vertical Pod Autoscaler)

5. Installer VPA (si disponible) :

```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler/
./hack/vpa-install.sh
```

6. Créer VPA pour optimisation des ressources :

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
  namespace: ecommerce
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-backend
  updatePolicy:
    updateMode: 'Auto'
  resourcePolicy:
    containerPolicies:
      - containerName: api
        maxAllowed:
          cpu: 1
          memory: 2Gi
        minAllowed:
          cpu: 100m
          memory: 128Mi
```

### Étape 6 : Monitoring et observabilité

7. Surveiller le comportement de l'autoscaling :

```bash
# Surveiller les événements HPA
kubectl get hpa -n ecommerce --watch

# Voir les événements de scaling
kubectl describe hpa api-hpa -n ecommerce

# Surveiller les pods
kubectl get pods -n ecommerce --watch

# Vérifier les métriques
kubectl top pods -n ecommerce
```

## Tests pratiques

### Test de montée en charge

```bash
# Lancer un test de charge intense
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Dans le pod :
while true; do wget -q -O- http://frontend-service.ecommerce.svc.cluster.local/; done
```

### Surveillance des métriques

```bash
# Observer le scaling en temps réel
watch kubectl get hpa,pods -n ecommerce

# Vérifier les recommandations VPA
kubectl describe vpa api-vpa -n ecommerce
```

## Critères de validation

- [ ] Metrics-server installé et fonctionnel
- [ ] HPA configuré avec seuils appropriés
- [ ] Autoscaling déclenché sous charge
- [ ] Pods ajoutés automatiquement lors des pics
- [ ] Scale-down automatique après réduction de charge
- [ ] VPA fournit des recommandations pertinentes
- [ ] Métriques de performance suivies

## Métriques à surveiller

- Utilisation CPU/mémoire des pods
- Nombre de replicas par deployment
- Temps de réponse des applications
- Taux de requêtes par seconde
- Événements de scaling

## Durée estimée

35 minutes
