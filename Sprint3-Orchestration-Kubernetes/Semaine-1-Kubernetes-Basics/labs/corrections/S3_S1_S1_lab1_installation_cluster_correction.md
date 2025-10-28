# Correction LAB 1 - Installation et configuration cluster Kubernetes

## Solution complète

### 1. Installation de minikube et kubectl

```bash
# Mise à jour du système
sudo apt update

# Installation de Docker (si pas déjà installé)
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Installation de minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Installation de kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Vérification des installations
minikube version
kubectl version --client
```

### 2. Démarrage optimisé du cluster

```bash
# Configuration recommandée pour l'environnement d'apprentissage
minikube start \
  --driver=docker \
  --cpus=2 \
  --memory=4096mb \
  --disk-size=20g \
  --kubernetes-version=v1.28.0 \
  --addons=dashboard,metrics-server

# Vérification du statut
minikube status
```

**Sortie attendue :**

```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

### 3. Validation complète du cluster

```bash
# Vérification des nodes
kubectl get nodes -o wide

# Vérification des composants système
kubectl get pods -n kube-system

# Informations détaillées du cluster
kubectl cluster-info
kubectl cluster-info dump > cluster-info.txt

# Vérification de la connectivité
kubectl get namespaces
kubectl get all --all-namespaces
```

### 4. Configuration kubectl avancée

```bash
# Vérification de la configuration kubectl
kubectl config view

# Configuration du contexte par défaut
kubectl config use-context minikube

# Alias utiles (à ajouter dans ~/.bashrc)
echo 'alias k=kubectl' >> ~/.bashrc
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'complete -F __start_kubectl k' >> ~/.bashrc
source ~/.bashrc

# Test des permissions
kubectl auth can-i create pods
kubectl auth can-i '*' '*' --as=system:admin
```

### 5. Optimisations et bonnes pratiques

```bash
# Configuration des ressources par défaut
minikube config set cpus 2
minikube config set memory 4096
minikube config set disk-size 20g

# Activation des addons utiles
minikube addons enable dashboard
minikube addons enable metrics-server
minikube addons enable ingress
minikube addons list

# Script de démarrage automatique
cat > start-k8s.sh << 'EOF'
#!/bin/bash
echo "Démarrage du cluster Kubernetes..."
minikube start --driver=docker --cpus=2 --memory=4096mb

echo "Vérification du cluster..."
kubectl get nodes
kubectl get pods -n kube-system

echo "Cluster prêt !"
kubectl cluster-info
EOF

chmod +x start-k8s.sh
```

### 6. Tests de fonctionnement

```bash
# Déployer un pod de test
kubectl run test-pod --image=nginx:1.21 --port=80

# Vérifier le déploiement
kubectl get pods test-pod
kubectl describe pod test-pod

# Exposer temporairement pour test
kubectl port-forward test-pod 8080:80 &
curl http://localhost:8080

# Nettoyer
kubectl delete pod test-pod
```

### 7. Monitoring et dashboard

```bash
# Lancer le dashboard Kubernetes
minikube dashboard &

# Obtenir l'URL du dashboard
minikube dashboard --url

# Accès aux métriques
kubectl top nodes
kubectl top pods --all-namespaces
```

### 8. Dépannage avancé

```bash
# Si minikube ne démarre pas
minikube delete --all --purge
docker system prune -af
minikube start --driver=docker --cpus=2 --memory=4096mb --force

# Vérification des logs
minikube logs
journalctl -u docker

# Test de connectivité réseau
kubectl run network-test --image=busybox -it --rm --restart=Never -- nslookup kubernetes.default

# Vérification des certificats
kubectl config view --raw -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d | openssl x509 -text -noout
```

## Points de validation

### ✅ Critères de réussite

1. **Minikube opérationnel**

   ```bash
   minikube status
   # Résultat attendu : host: Running, kubelet: Running, apiserver: Running
   ```

2. **Kubectl configuré**

   ```bash
   kubectl get nodes
   # Résultat attendu : 1 node en status Ready
   ```

3. **Composants système sains**

   ```bash
   kubectl get pods -n kube-system
   # Résultat attendu : Tous les pods en Running
   ```

4. **Connectivité fonctionnelle**
   ```bash
   kubectl cluster-info
   # Résultat attendu : URLs des services master accessibles
   ```

### 🔧 Optimisations production

```bash
# Configuration pour environnement de développement
minikube start \
  --driver=docker \
  --cpus=4 \
  --memory=8192mb \
  --disk-size=50g \
  --kubernetes-version=stable \
  --addons=dashboard,metrics-server,ingress,registry

# Persistence des données
minikube config set WantUpdateNotification false
minikube config set WantReportErrorPrompt false
```

### 📊 Métriques de performance

```bash
# Temps de démarrage typique : 2-5 minutes
# Utilisation RAM : ~1.5GB
# Utilisation CPU : ~20% au repos
# Espace disque : ~2GB installation de base

# Commandes de monitoring
watch kubectl get pods --all-namespaces
watch kubectl top nodes
```

### 🚨 Problèmes courants et solutions

**Problème 1 : Minikube ne démarre pas**

```bash
# Solution :
minikube delete
minikube start --driver=none --extra-config=kubeadm.skip-phases=addon/coredns
```

**Problème 2 : Kubectl ne se connecte pas**

```bash
# Solution :
kubectl config use-context minikube
kubectl config current-context
```

**Problème 3 : Pods système en pending**

```bash
# Solution :
kubectl describe node minikube
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Ressources complémentaires

- [Documentation officielle Minikube](https://minikube.sigs.k8s.io/)
- [Guide kubectl](https://kubernetes.io/docs/reference/kubectl/)
- [Troubleshooting Kubernetes](https://kubernetes.io/docs/tasks/debug-application-cluster/)

## Prochaines étapes

Cluster fonctionnel ✅ → LAB 2 : Premiers pods et conteneurs
