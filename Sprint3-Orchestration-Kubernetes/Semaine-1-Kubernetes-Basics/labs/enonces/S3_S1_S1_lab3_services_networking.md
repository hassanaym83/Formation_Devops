# LAB 3 - Services et networking

## Objectifs

- Comprendre les concepts de Services Kubernetes
- Implémenter différents types de Services (ClusterIP, NodePort, LoadBalancer)
- Maîtriser la découverte de services et DNS interne
- Tester la communication inter-pods

## Contexte

Configuration du networking et exposition des applications dans un environnement Kubernetes.

## Prérequis

- Cluster Kubernetes fonctionnel
- Connaissance des pods (LAB 2)

## Instructions

### 1. Déploiement de l'application de test

```yaml
# Créer le fichier app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  labels:
    app: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          ports:
            - containerPort: 80
          env:
            - name: NODE_NAME
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
```

```bash
# Déployer l'application
kubectl apply -f app-deployment.yaml

# Vérifier le déploiement
kubectl get deployments
kubectl get pods -l app=webapp
```

### 2. Service ClusterIP (par défaut)

```yaml
# Créer le fichier service-clusterip.yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-clusterip
spec:
  selector:
    app: webapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

```bash
# Créer le service ClusterIP
kubectl apply -f service-clusterip.yaml

# Vérifier le service
kubectl get services
kubectl describe service webapp-clusterip

# Tester la connectivité interne
kubectl run test-pod --image=busybox -it --rm -- /bin/sh
# Dans le pod de test :
wget -qO- webapp-clusterip
nslookup webapp-clusterip
exit
```

### 3. Service NodePort

```yaml
# Créer le fichier service-nodeport.yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-nodeport
spec:
  selector:
    app: webapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30080
  type: NodePort
```

```bash
# Créer le service NodePort
kubectl apply -f service-nodeport.yaml

# Vérifier le service
kubectl get services webapp-nodeport

# Obtenir l'IP du node minikube
minikube ip

# Tester l'accès externe
curl http://$(minikube ip):30080
```

### 4. Service LoadBalancer (simulation)

```yaml
# Créer le fichier service-loadbalancer.yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-loadbalancer
spec:
  selector:
    app: webapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

```bash
# Créer le service LoadBalancer
kubectl apply -f service-loadbalancer.yaml

# Dans minikube, simuler le LoadBalancer
minikube tunnel &

# Vérifier l'IP externe assignée
kubectl get services webapp-loadbalancer

# Tester l'accès via l'IP externe
curl http://<EXTERNAL-IP>
```

### 5. Test de découverte de services DNS

```yaml
# Créer un pod de test DNS
apiVersion: v1
kind: Pod
metadata:
  name: dns-test
spec:
  containers:
    - name: dns-test
      image: busybox
      command: ['sleep', '3600']
```

```bash
# Déployer le pod de test
kubectl apply -f dns-test-pod.yaml

# Tester la résolution DNS
kubectl exec -it dns-test -- nslookup webapp-clusterip
kubectl exec -it dns-test -- nslookup webapp-clusterip.default.svc.cluster.local

# Tester la connectivité par nom de service
kubectl exec -it dns-test -- wget -qO- webapp-clusterip
kubectl exec -it dns-test -- wget -qO- webapp-nodeport
```

### 6. Service sans sélecteur (endpoints manuels)

```yaml
# Créer le fichier service-external.yaml
apiVersion: v1
kind: Service
metadata:
  name: external-service
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80

---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-service
subsets:
  - addresses:
      - ip: 8.8.8.8
    ports:
      - port: 53
```

```bash
# Créer le service externe
kubectl apply -f service-external.yaml

# Vérifier les endpoints
kubectl get endpoints external-service
kubectl describe service external-service
```

### 7. Monitoring et debugging des services

```bash
# Vérifier les endpoints des services
kubectl get endpoints

# Débugger un service
kubectl describe service webapp-clusterip

# Vérifier les labels des pods
kubectl get pods --show-labels

# Tester la connectivité réseau
kubectl exec -it dns-test -- netstat -rn
kubectl exec -it dns-test -- cat /etc/resolv.conf
```

## Livrables attendus

1. Fichiers YAML de tous les services créés
2. Tests de connectivité pour chaque type de service
3. Validation de la découverte DNS
4. Documentation des observations réseau

## Critères de validation

- [ ] Service ClusterIP accessible en interne
- [ ] Service NodePort accessible depuis l'extérieur
- [ ] Service LoadBalancer fonctionnel avec minikube tunnel
- [ ] Résolution DNS correcte pour tous les services
- [ ] Endpoints correctement assignés aux services
- [ ] Communication inter-pods fonctionnelle

## Durée estimée

25 minutes

## Concepts clés

### Types de Services

- **ClusterIP** : Accès interne au cluster uniquement
- **NodePort** : Exposition sur un port de chaque node
- **LoadBalancer** : IP externe (nécessite cloud provider)
- **ExternalName** : Alias vers un service externe

### DNS Kubernetes

```
<service-name>.<namespace>.svc.cluster.local
```

### Commandes utiles

```bash
# Services
kubectl get services
kubectl describe service <nom>
kubectl get endpoints

# Réseau
kubectl exec -it <pod> -- nslookup <service>
kubectl port-forward service/<nom> <port-local>:<port-service>

# Debug
kubectl get pods -o wide
kubectl describe endpoints <service-name>
```
