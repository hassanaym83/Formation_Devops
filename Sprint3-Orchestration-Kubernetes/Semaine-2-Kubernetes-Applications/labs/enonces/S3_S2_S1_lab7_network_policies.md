# LAB 7 - Network Policies et Sécurité

## Objectif

Implémenter des politiques de sécurité réseau pour isoler et protéger les workloads Kubernetes.

## Contexte

Sécuriser l'application e-commerce avec :

- Segmentation réseau par micro-segmentation
- Contrôle d'accès inter-pods granulaire
- Isolation des environnements
- Protection contre les attaques latérales
- Audit et logging des connexions

## Prérequis

- Application e-commerce multi-tiers déployée
- Plugin CNI supportant NetworkPolicies (Calico/Cilium)
- Namespaces dev/staging/prod configurés
- Monitoring réseau (optionnel)

## Instructions détaillées

### Étape 1 : Installer Calico pour NetworkPolicies

1. Vérifier ou installer Calico :

```bash
# Vérifier si NetworkPolicies sont supportées
kubectl auth can-i create networkpolicies

# Installer Calico si nécessaire
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/tigera-operator.yaml

# Configuration Calico
cat <<EOF | kubectl apply -f -
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
    - blockSize: 26
      cidr: 192.168.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()
EOF
```

### Étape 2 : Politique de sécurité par défaut (Deny All)

2. Créer politiques restrictives par défaut :

```yaml
# default-deny-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-ingress
  namespace: ecommerce
spec:
  podSelector: {}
  policyTypes:
    - Ingress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-egress
  namespace: ecommerce
spec:
  podSelector: {}
  policyTypes:
    - Egress

---
# Politique globale pour tous les namespaces
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: default-app-policy
spec:
  namespaceSelector: has(name) && name not in {"kube-system", "kube-public", "kube-node-lease"}
  types:
    - Ingress
    - Egress
  egress:
    # Permettre DNS
    - action: Allow
      protocol: UDP
      destination:
        selector: k8s-app == "kube-dns"
        ports:
          - 53
    - action: Allow
      protocol: TCP
      destination:
        selector: k8s-app == "kube-dns"
        ports:
          - 53
    # Permettre accès aux services Kubernetes
    - action: Allow
      protocol: TCP
      destination:
        nets:
          - 10.96.0.0/12 # Service CIDR
```

### Étape 3 : Politiques pour le tier Frontend

3. Autoriser le trafic pour le frontend web :

```yaml
# frontend-network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-ingress-policy
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      tier: frontend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Permettre trafic depuis Ingress Controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 80
        - protocol: TCP
          port: 443
    # Permettre trafic depuis Load Balancer externe
    - from: [] # Tout trafic externe
      ports:
        - protocol: TCP
          port: 80
  egress:
    # Permettre accès au backend API
    - to:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 3000
    # Permettre DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
    # Permettre accès Internet pour CDN/APIs externes
    - to: []
      ports:
        - protocol: TCP
          port: 80
        - protocol: TCP
          port: 443

---
# Politique spécifique pour les assets statiques
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-static-assets
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      app: frontend
      component: static
  policyTypes:
    - Egress
  egress:
    # CDN et services externes
    - to: []
      ports:
        - protocol: TCP
          port: 80
        - protocol: TCP
          port: 443
```

### Étape 4 : Politiques pour le tier Backend

4. Configurer l'accès pour les APIs backend :

```yaml
# backend-network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-api-policy
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Permettre trafic depuis Frontend
    - from:
        - podSelector:
            matchLabels:
              tier: frontend
      ports:
        - protocol: TCP
          port: 3000
    # Permettre trafic depuis autres services backend
    - from:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 3000
    # Permettre health checks depuis Ingress
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 3000
  egress:
    # Accès à la base de données
    - to:
        - podSelector:
            matchLabels:
              tier: database
      ports:
        - protocol: TCP
          port: 5432 # PostgreSQL
        - protocol: TCP
          port: 3306 # MySQL
    # Accès au cache Redis
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379
    # Services externes (APIs partenaires, etc.)
    - to: []
      ports:
        - protocol: TCP
          port: 80
        - protocol: TCP
          port: 443
    # DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53

---
# Politique pour les microservices internes
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: microservices-internal
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      type: microservice
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Communication inter-microservices
    - from:
        - podSelector:
            matchLabels:
              type: microservice
      ports:
        - protocol: TCP
          port: 8080
    # Accès depuis API Gateway
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # Communication vers autres microservices
    - to:
        - podSelector:
            matchLabels:
              type: microservice
      ports:
        - protocol: TCP
          port: 8080
    # Accès aux bases de données dédiées
    - to:
        - podSelector:
            matchLabels:
              tier: database
      ports:
        - protocol: TCP
          port: 5432
```

### Étape 5 : Politiques pour le tier Database

5. Sécuriser l'accès aux bases de données :

```yaml
# database-network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-access-policy
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      tier: database
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Accès uniquement depuis Backend
    - from:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 5432 # PostgreSQL
        - protocol: TCP
          port: 3306 # MySQL
    # Accès pour backup/maintenance
    - from:
        - podSelector:
            matchLabels:
              app: backup-operator
      ports:
        - protocol: TCP
          port: 5432
        - protocol: TCP
          port: 3306
    # Accès monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 9187 # PostgreSQL exporter
  egress:
    # Réplication/backup externes (si applicable)
    - to: []
      ports:
        - protocol: TCP
          port: 5432
    # DNS uniquement
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53

---
# Politique Redis Cache
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: redis-cache-policy
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      app: redis
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Accès depuis Backend uniquement
    - from:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 6379
    # Monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 9121 # Redis exporter
  egress:
    # Pas d'egress nécessaire (cache local)
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

### Étape 6 : Isolation entre environnements

6. Créer des politiques d'isolation inter-environnements :

```yaml
# environment-isolation.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: env-isolation-dev
  namespace: ecommerce-dev
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Autoriser uniquement le trafic interne au namespace dev
    - from:
        - namespaceSelector:
            matchLabels:
              environment: dev
    # Autoriser monitoring depuis namespace dédié
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
  egress:
    # Sortie uniquement vers même environnement
    - to:
        - namespaceSelector:
            matchLabels:
              environment: dev
    # Services système
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
    # Internet pour dev (plus permissif)
    - to: []

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: env-isolation-prod
  namespace: ecommerce-prod
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Trafic production uniquement
    - from:
        - namespaceSelector:
            matchLabels:
              environment: prod
    # Ingress Controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
    # Monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
  egress:
    # Sortie restreinte en production
    - to:
        - namespaceSelector:
            matchLabels:
              environment: prod
    # Services système
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
    # APIs externes spécifiques uniquement
    - to: []
      ports:
        - protocol: TCP
          port: 443
```

### Étape 7 : Monitoring et audit des NetworkPolicies

7. Configurer le monitoring des connexions réseau :

```yaml
# network-monitoring.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: calico-audit-config
  namespace: kube-system
data:
  audit.yaml: |
    apiVersion: audit.k8s.io/v1
    kind: Policy
    rules:
    - level: RequestResponse
      namespaces: ["ecommerce", "ecommerce-dev", "ecommerce-prod"]
      resources:
      - group: "networking.k8s.io"
        resources: ["networkpolicies"]
      - group: "projectcalico.org"
        resources: ["networkpolicies", "globalnetworkpolicies"]

---
# Script de test des politiques
apiVersion: v1
kind: ConfigMap
metadata:
  name: network-policy-tests
  namespace: ecommerce
data:
  test-policies.sh: |
    #!/bin/bash

    echo "🔍 Test des Network Policies"

    # Test 1: Frontend -> Backend (doit réussir)
    echo "Test Frontend -> Backend..."
    kubectl exec -n ecommerce deployment/frontend -- curl -s --connect-timeout 5 http://backend-service:3000/health
    if [ $? -eq 0 ]; then
        echo "✅ Frontend -> Backend: OK"
    else
        echo "❌ Frontend -> Backend: BLOQUÉ"
    fi

    # Test 2: Frontend -> Database (doit échouer)
    echo "Test Frontend -> Database (doit être bloqué)..."
    kubectl exec -n ecommerce deployment/frontend -- timeout 5 nc -z postgres-service 5432
    if [ $? -ne 0 ]; then
        echo "✅ Frontend -> Database: BLOQUÉ (correct)"
    else
        echo "❌ Frontend -> Database: AUTORISÉ (problème de sécurité!)"
    fi

    # Test 3: Backend -> Database (doit réussir)
    echo "Test Backend -> Database..."
    kubectl exec -n ecommerce deployment/backend -- timeout 5 nc -z postgres-service 5432
    if [ $? -eq 0 ]; then
        echo "✅ Backend -> Database: OK"
    else
        echo "❌ Backend -> Database: BLOQUÉ"
    fi

    # Test 4: Cross-environment (doit échouer)
    echo "Test Dev -> Prod (doit être bloqué)..."
    kubectl exec -n ecommerce-dev deployment/frontend -- timeout 5 curl -s http://backend-service.ecommerce-prod:3000/health
    if [ $? -ne 0 ]; then
        echo "✅ Dev -> Prod: BLOQUÉ (correct)"
    else
        echo "❌ Dev -> Prod: AUTORISÉ (problème d'isolation!)"
    fi
```

### Étape 8 : Mise en place de l'audit et logging

8. Configurer le logging des événements réseau :

```bash
# Activer l'audit Calico
kubectl patch felixconfiguration default --type merge --patch '{"spec":{"flowLogsFileEnabled":true}}'

# Configurer Fluent Bit pour collecter les logs réseau
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-network-config
  namespace: kube-system
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         1
        Log_Level     info

    [INPUT]
        Name              tail
        Path              /var/log/calico/flowlogs/*
        Parser            json
        Tag               calico.flow
        Refresh_Interval  5

    [FILTER]
        Name                kubernetes
        Match               calico.flow
        Kube_URL            https://kubernetes.default.svc:443
        Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token

    [OUTPUT]
        Name  stdout
        Match *
EOF

# Déployer Fluent Bit
kubectl apply -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-service-account.yaml
kubectl apply -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-role.yaml
kubectl apply -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-role-binding.yaml
kubectl apply -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-configmap.yaml
kubectl apply -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-daemonset.yaml
```

## Critères de validation

- [ ] Politiques "deny-all" par défaut appliquées
- [ ] Segmentation micro-service fonctionnelle
- [ ] Isolation complète entre environnements
- [ ] Tests de connectivité validés
- [ ] Audit et monitoring configurés
- [ ] Documentation des flux autorisés
- [ ] Procédures de dépannage définies
- [ ] Tests de sécurité passés

## Tests pratiques

```bash
# Appliquer toutes les politiques
kubectl apply -f default-deny-policies.yaml
kubectl apply -f frontend-network-policies.yaml
kubectl apply -f backend-network-policies.yaml
kubectl apply -f database-network-policies.yaml
kubectl apply -f environment-isolation.yaml

# Tester les politiques
kubectl create job network-test --image=busybox -- /bin/sh -c "$(kubectl get configmap network-policy-tests -o jsonpath='{.data.test-policies\.sh}')"

# Vérifier les logs d'audit
kubectl logs -n kube-system -l app=fluent-bit | grep "calico.flow"

# Analyser les connexions refusées
kubectl logs -n kube-system -l app=calico-node | grep "denied"
```

## Durée estimée

50 minutes
