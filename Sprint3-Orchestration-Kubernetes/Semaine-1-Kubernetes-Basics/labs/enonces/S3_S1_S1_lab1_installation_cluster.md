# LAB 1 - Installation et configuration cluster Kubernetes

## Objectifs

- Installer et configurer un cluster Kubernetes local avec minikube
- Vérifier l'état du cluster et de ses composants système
- Configurer l'accès kubectl au cluster

## Contexte

Mise en place de l'environnement de développement Kubernetes pour les exercices suivants.

## Prérequis

- Docker installé
- Virtualization activée (VT-x/AMD-v)
- 4GB RAM minimum
- 20GB espace disque libre

## Instructions

### 1. Installation de minikube

```bash
# Télécharger minikube (Linux)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Vérifier l'installation
minikube version
```

### 2. Installation de kubectl

```bash
# Télécharger kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Installer kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Vérifier l'installation
kubectl version --client
```

### 3. Démarrage du cluster

```bash
# Démarrer minikube avec Docker driver
minikube start --driver=docker --cpus=2 --memory=4096mb

# Vérifier le statut
minikube status
```

### 4. Vérification du cluster

```bash
# Vérifier les nodes
kubectl get nodes

# Vérifier les composants système
kubectl get pods -n kube-system

# Obtenir les informations du cluster
kubectl cluster-info
```

### 5. Configuration kubectl

```bash
# Vérifier la configuration kubectl
kubectl config view

# Obtenir le contexte actuel
kubectl config current-context

# Lister les contextes disponibles
kubectl config get-contexts
```

## Livrables attendus

1. Cluster minikube fonctionnel
2. kubectl configuré et connecté au cluster
3. Capture d'écran des commandes de vérification
4. Documentation des éventuels problèmes rencontrés

## Critères de validation

- [ ] `minikube status` retourne "Running"
- [ ] `kubectl get nodes` affiche le node minikube en status "Ready"
- [ ] `kubectl get pods -n kube-system` affiche tous les pods système en status "Running"
- [ ] `kubectl cluster-info` affiche les URLs des services

## Durée estimée

15 minutes

## Dépannage commun

### Problème : Minikube ne démarre pas

```bash
# Supprimer le cluster existant
minikube delete

# Nettoyer les configurations
minikube delete --all --purge

# Redémarrer avec plus de ressources
minikube start --driver=docker --cpus=2 --memory=4096mb --disk-size=20g
```

### Problème : Kubectl ne se connecte pas

```bash
# Configurer kubectl pour minikube
kubectl config use-context minikube

# Vérifier la connectivité
kubectl get nodes -v=6
```
