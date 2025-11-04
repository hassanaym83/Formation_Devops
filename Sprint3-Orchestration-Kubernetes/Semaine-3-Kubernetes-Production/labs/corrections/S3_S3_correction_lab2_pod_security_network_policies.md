# Correction LAB 2 - Pod Security Standards et Network Policies

## Vue d'ensemble

Cette correction fournit les solutions complètes pour l'implémentation des Pod Security Standards et Network Policies dans un environnement Kubernetes sécurisé.

## Exercice 1 : Pod Security Standards

### Solution complète : Configuration des namespaces avec Pod Security Standards

```yaml
# pod-security-namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production-apps
  labels:
    # Enforce Restricted pour la production
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/enforce-version: latest
    # Labels additionnels pour l'organisation
    environment: production
    security-level: high
    compliance: pci-dss
  annotations:
    description: 'Namespace pour les applications de production avec sécurité renforcée'
    contact: 'devops-team@company.com'
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging-apps
  labels:
    # Baseline pour staging avec audit Restricted
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/enforce-version: latest
    environment: staging
    security-level: medium
  annotations:
    description: 'Namespace pour les applications de staging'
    contact: 'dev-team@company.com'
---
apiVersion: v1
kind: Namespace
metadata:
  name: development-apps
  labels:
    # Privileged pour development avec warnings
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/warn: baseline
    pod-security.kubernetes.io/enforce-version: latest
    environment: development
    security-level: low
  annotations:
    description: 'Namespace pour le développement avec moins de restrictions'
    contact: 'dev-team@company.com'
---
apiVersion: v1
kind: Namespace
metadata:
  name: legacy-apps
  labels:
    # Baseline pour applications legacy
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/enforce-version: v1.25
    environment: legacy
    security-level: medium
    migration-target: restricted
  annotations:
    description: 'Namespace pour applications legacy en cours de migration'
    migration-plan: 'Migrate to restricted by Q2 2024'
```

### Solution complète : Pods conformes Restricted

```yaml
# secure-pods-restricted.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-web-app
  namespace: production-apps
  labels:
    app: secure-web-app
    security-profile: restricted
    compliance: pci-dss
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-web-app
  template:
    metadata:
      labels:
        app: secure-web-app
        security-profile: restricted
      annotations:
        seccomp.security.alpha.kubernetes.io/pod: runtime/default
    spec:
      # ServiceAccount dédié avec permissions minimales
      serviceAccountName: secure-web-app-sa
      automountServiceAccountToken: false

      # Contexte de sécurité au niveau pod
      securityContext:
        # Utilisateur non-root obligatoire
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
        # Profil seccomp
        seccompProfile:
          type: RuntimeDefault
        # Pas de privilèges supplémentaires
        supplementalGroups: [10001]

      containers:
        - name: web-app
          image: nginx:1.24-alpine
          imagePullPolicy: IfNotPresent

          ports:
            - name: http
              containerPort: 8080 # Port non-privilégié
              protocol: TCP

          # Variables d'environnement sécurisées
          env:
            - name: NGINX_USER
              value: 'nginx'
            - name: NGINX_PORT
              value: '8080'
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace

          # Volumes en lecture seule avec exceptions nécessaires
          volumeMounts:
            - name: tmp-volume
              mountPath: /tmp
            - name: var-cache-nginx
              mountPath: /var/cache/nginx
            - name: var-run
              mountPath: /var/run
            - name: nginx-config
              mountPath: /etc/nginx/nginx.conf
              subPath: nginx.conf
              readOnly: true

          # Contexte de sécurité container
          securityContext:
            # Pas d'escalade de privilèges
            allowPrivilegeEscalation: false
            # Système de fichiers racine en lecture seule
            readOnlyRootFilesystem: true
            # Utilisateur non-root
            runAsNonRoot: true
            runAsUser: 10001
            runAsGroup: 10001
            # Suppression de toutes les capabilities
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE # Seule capability nécessaire
            # Profil seccomp
            seccompProfile:
              type: RuntimeDefault

          # Sondes de santé
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          # Limites de ressources strictes
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi

      # Volumes nécessaires avec types autorisés
      volumes:
        - name: tmp-volume
          emptyDir:
            sizeLimit: 100Mi
        - name: var-cache-nginx
          emptyDir:
            sizeLimit: 50Mi
        - name: var-run
          emptyDir:
            sizeLimit: 10Mi
        - name: nginx-config
          configMap:
            name: nginx-secure-config
            defaultMode: 0444 # Lecture seule

      # Politique de redémarrage
      restartPolicy: Always

      # Délai de grâce pour l'arrêt
      terminationGracePeriodSeconds: 30

      # Affinité pour la répartition
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values: ['secure-web-app']
                topologyKey: kubernetes.io/hostname
---
# ConfigMap pour la configuration NGINX sécurisée
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-secure-config
  namespace: production-apps
data:
  nginx.conf: |
    user nginx;
    worker_processes auto;
    error_log /var/log/nginx/error.log warn;
    pid /var/run/nginx.pid;

    events {
        worker_connections 1024;
        use epoll;
        multi_accept on;
    }

    http {
        include /etc/nginx/mime.types;
        default_type application/octet-stream;
        
        # Sécurité headers
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        
        # Cacher la version nginx
        server_tokens off;
        
        # Configuration de logging
        log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
        
        access_log /var/log/nginx/access.log main;
        
        # Configuration de performance
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        
        # Limites de sécurité
        client_max_body_size 1m;
        client_body_timeout 10s;
        client_header_timeout 10s;
        large_client_header_buffers 2 1k;
        
        server {
            listen 8080;
            server_name _;
            root /usr/share/nginx/html;
            index index.html;
            
            # Health checks
            location /health {
                access_log off;
                return 200 "healthy\n";
                add_header Content-Type text/plain;
            }
            
            location /ready {
                access_log off;
                return 200 "ready\n";
                add_header Content-Type text/plain;
            }
            
            # Configuration principale
            location / {
                try_files $uri $uri/ =404;
            }
            
            # Sécurité - cacher les fichiers sensibles
            location ~ /\. {
                deny all;
                access_log off;
                log_not_found off;
            }
            
            location ~ ~$ {
                deny all;
                access_log off;
                log_not_found off;
            }
        }
    }
---
# ServiceAccount avec permissions minimales
apiVersion: v1
kind: ServiceAccount
metadata:
  name: secure-web-app-sa
  namespace: production-apps
  labels:
    app: secure-web-app
automountServiceAccountToken: false
---
# Service
apiVersion: v1
kind: Service
metadata:
  name: secure-web-app-service
  namespace: production-apps
  labels:
    app: secure-web-app
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
  selector:
    app: secure-web-app
```

### Solution complète : Pods non-conformes (exemples à éviter)

```yaml
# insecure-pods-examples.yaml - NE PAS UTILISER EN PRODUCTION
apiVersion: v1
kind: Pod
metadata:
  name: insecure-pod-example
  namespace: development-apps
  labels:
    security-example: 'violation'
  annotations:
    description: 'Exemple de pod non-conforme - À des fins éducatives uniquement'
spec:
  # VIOLATION: Pas de contexte de sécurité défini
  containers:
    - name: insecure-container
      image: nginx:latest

      # VIOLATION: Port privilégié
      ports:
        - containerPort: 80

      securityContext:
        # VIOLATION: Exécution en tant que root
        runAsUser: 0
        runAsNonRoot: false

        # VIOLATION: Escalade de privilèges autorisée
        allowPrivilegeEscalation: true

        # VIOLATION: Système de fichiers racine en écriture
        readOnlyRootFilesystem: false

        # VIOLATION: Capabilities privilégiées
        capabilities:
          add:
            - SYS_ADMIN
            - NET_ADMIN
            - SYS_TIME

        # VIOLATION: Mode privilégié
        privileged: true

      # VIOLATION: Accès au système de fichiers host
      volumeMounts:
        - name: host-root
          mountPath: /host

  # VIOLATION: Volumes host dangereux
  volumes:
    - name: host-root
      hostPath:
        path: /
        type: Directory

  # VIOLATION: Accès réseau host
  hostNetwork: true
  hostPID: true
  hostIPC: true
```

## Exercice 2 : Network Policies

### Solution complète : Network Policies par défaut

```yaml
# default-network-policies.yaml
# Politique par défaut : Deny All
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-ingress
  namespace: production-apps
  labels:
    security-policy: default
spec:
  podSelector: {} # Applique à tous les pods
  policyTypes:
    - Ingress
  # Pas de règles ingress = deny all
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-egress
  namespace: production-apps
  labels:
    security-policy: default
spec:
  podSelector: {} # Applique à tous les pods
  policyTypes:
    - Egress
  # Règles egress minimales pour fonctionnement de base
  egress:
    # DNS resolution
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
    # HTTPS pour mise à jour certificats, metrics, etc.
    - to: []
      ports:
        - protocol: TCP
          port: 443
```

### Solution complète : Politiques pour applications web

```yaml
# web-app-network-policies.yaml
# Politique pour frontend web
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-frontend-policy
  namespace: production-apps
  labels:
    app: secure-web-app
    tier: frontend
spec:
  podSelector:
    matchLabels:
      app: secure-web-app
      tier: frontend
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Autoriser le trafic depuis l'ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080

    # Autoriser le trafic depuis les Load Balancers
    - from:
        - namespaceSelector:
            matchLabels:
              name: kube-system
        - podSelector:
            matchLabels:
              app: metallb
      ports:
        - protocol: TCP
          port: 8080

    # Autoriser monitoring (Prometheus)
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 9090 # Port métriques

  egress:
    # DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53

    # Communication avec backend API
    - to:
        - podSelector:
            matchLabels:
              app: api-backend
              tier: backend
      ports:
        - protocol: TCP
          port: 3000

    # Communication avec cache Redis
    - to:
        - podSelector:
            matchLabels:
              app: redis
              tier: cache
      ports:
        - protocol: TCP
          port: 6379

    # HTTPS sortant pour APIs externes
    - to: []
      ports:
        - protocol: TCP
          port: 443
---
# Politique pour backend API
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-backend-policy
  namespace: production-apps
  labels:
    app: api-backend
    tier: backend
spec:
  podSelector:
    matchLabels:
      app: api-backend
      tier: backend
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Autoriser le trafic depuis le frontend
    - from:
        - podSelector:
            matchLabels:
              app: secure-web-app
              tier: frontend
      ports:
        - protocol: TCP
          port: 3000

    # Autoriser le trafic depuis l'API Gateway
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
              tier: gateway
      ports:
        - protocol: TCP
          port: 3000

    # Autoriser monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 9090

  egress:
    # DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53

    # Base de données PostgreSQL
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
        - podSelector:
            matchLabels:
              app: postgresql
      ports:
        - protocol: TCP
          port: 5432

    # Cache Redis
    - to:
        - podSelector:
            matchLabels:
              app: redis
              tier: cache
      ports:
        - protocol: TCP
          port: 6379

    # APIs externes (HTTPS)
    - to: []
      ports:
        - protocol: TCP
          port: 443

    # Services internes (autres microservices)
    - to:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 3000
        - protocol: TCP
          port: 8080
---
# Politique pour base de données
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-policy
  namespace: database
  labels:
    app: postgresql
    tier: database
spec:
  podSelector:
    matchLabels:
      app: postgresql
      tier: database
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Autoriser uniquement les backends autorisés
    - from:
        - namespaceSelector:
            matchLabels:
              name: production-apps
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 5432

    # Autoriser monitoring pour métriques DB
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 9187 # postgres_exporter

  egress:
    # DNS seulement
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53

    # Backup vers stockage externe (si nécessaire)
    - to: []
      ports:
        - protocol: TCP
          port: 443
```

### Solution complète : Politiques multi-namespaces

```yaml
# cross-namespace-policies.yaml
# Politique pour communication inter-namespaces
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-monitoring-access
  namespace: production-apps
  labels:
    purpose: monitoring
spec:
  podSelector: {} # Tous les pods du namespace
  policyTypes:
    - Ingress

  ingress:
    # Autoriser Prometheus depuis le namespace monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: prometheus
      ports:
        - protocol: TCP
          port: 9090
        - protocol: TCP
          port: 8080
        - protocol: TCP
          port: 3000

    # Autoriser Grafana pour les dashboards
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: grafana
      ports:
        - protocol: TCP
          port: 9090
---
# Politique pour accès depuis ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-access
  namespace: production-apps
  labels:
    purpose: ingress
spec:
  podSelector:
    matchLabels:
      tier: frontend
  policyTypes:
    - Ingress

  ingress:
    # Autoriser Ingress NGINX
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
        - protocol: TCP
          port: 80

    # Autoriser cert-manager pour les challenges ACME
    - from:
        - namespaceSelector:
            matchLabels:
              name: cert-manager
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: cert-manager
      ports:
        - protocol: TCP
          port: 8089 # ACME challenge port
---
# Politique pour services système
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-system-access
  namespace: production-apps
  labels:
    purpose: system
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Autoriser kubelet pour health checks
    - from:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: TCP
          port: 10250
        - protocol: TCP
          port: 10255

  egress:
    # Autoriser accès au API server pour service discovery
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: TCP
          port: 443
        - protocol: TCP
          port: 6443

    # Autoriser NTP pour synchronisation temps
    - to: []
      ports:
        - protocol: UDP
          port: 123
```

## Exercice 3 : Tests et validation avancés

### Script de validation Pod Security Standards

```bash
#!/bin/bash
# validate-pod-security.sh

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Validation Pod Security Standards ===${NC}"

# Fonction pour tester un pod conforme
test_compliant_pod() {
    local namespace=$1
    local pod_name=$2

    echo "Test de conformité pour $pod_name dans $namespace..."

    # Vérifier que le pod est créé avec succès
    if kubectl get pod $pod_name -n $namespace &>/dev/null; then
        echo -e "${GREEN}✓${NC} Pod $pod_name créé avec succès"

        # Vérifier les paramètres de sécurité
        local run_as_non_root=$(kubectl get pod $pod_name -n $namespace -o jsonpath='{.spec.securityContext.runAsNonRoot}')
        local read_only_root=$(kubectl get pod $pod_name -n $namespace -o jsonpath='{.spec.containers[0].securityContext.readOnlyRootFilesystem}')
        local allow_privilege_escalation=$(kubectl get pod $pod_name -n $namespace -o jsonpath='{.spec.containers[0].securityContext.allowPrivilegeEscalation}')

        if [[ "$run_as_non_root" == "true" ]]; then
            echo -e "${GREEN}✓${NC} runAsNonRoot: true"
        else
            echo -e "${RED}✗${NC} runAsNonRoot: $run_as_non_root"
        fi

        if [[ "$read_only_root" == "true" ]]; then
            echo -e "${GREEN}✓${NC} readOnlyRootFilesystem: true"
        else
            echo -e "${RED}✗${NC} readOnlyRootFilesystem: $read_only_root"
        fi

        if [[ "$allow_privilege_escalation" == "false" ]]; then
            echo -e "${GREEN}✓${NC} allowPrivilegeEscalation: false"
        else
            echo -e "${RED}✗${NC} allowPrivilegeEscalation: $allow_privilege_escalation"
        fi

    else
        echo -e "${RED}✗${NC} Pod $pod_name non trouvé ou non créé"
    fi
    echo ""
}

# Fonction pour tester un pod non-conforme
test_non_compliant_pod() {
    local namespace=$1
    local manifest_file=$2

    echo "Test de rejet pour pod non-conforme dans $namespace..."

    # Essayer de créer le pod non-conforme
    if kubectl apply -f $manifest_file &>/dev/null; then
        echo -e "${RED}✗${NC} Pod non-conforme créé (ne devrait pas être autorisé)"
        kubectl delete -f $manifest_file &>/dev/null
    else
        echo -e "${GREEN}✓${NC} Pod non-conforme rejeté comme attendu"
    fi
    echo ""
}

# Test des namespaces avec différents niveaux de sécurité
echo "1. Vérification des labels Pod Security Standards..."
kubectl get ns production-apps -o jsonpath='{.metadata.labels}' | jq '.'
kubectl get ns staging-apps -o jsonpath='{.metadata.labels}' | jq '.'
kubectl get ns development-apps -o jsonpath='{.metadata.labels}' | jq '.'

echo -e "\n2. Test des pods conformes..."
test_compliant_pod "production-apps" "secure-web-app-*"

echo -e "\n3. Test de création de pod avec violations..."
# Créer un manifeste temporaire non-conforme
cat > /tmp/insecure-pod.yaml << EOF
apiVersion: v1
kind: Pod
metadata:
  name: test-insecure
  namespace: production-apps
spec:
  containers:
  - name: test
    image: nginx
    securityContext:
      runAsUser: 0
      allowPrivilegeEscalation: true
EOF

test_non_compliant_pod "production-apps" "/tmp/insecure-pod.yaml"
rm -f /tmp/insecure-pod.yaml

echo -e "\n4. Validation des ressources déployées..."
kubectl get pods -n production-apps -o wide
kubectl get networkpolicies -n production-apps

echo -e "\n${GREEN}=== Validation terminée ===${NC}"
```

### Script de test Network Policies

```bash
#!/bin/bash
# test-network-policies.sh

set -e

NAMESPACE="production-apps"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Test des Network Policies ===${NC}"

# Fonction pour tester la connectivité réseau
test_network_connectivity() {
    local source_pod=$1
    local target_service=$2
    local target_port=$3
    local expected_result=$4
    local description=$5

    echo "Test: $description"
    echo "  Source: $source_pod"
    echo "  Target: $target_service:$target_port"
    echo "  Attendu: $expected_result"

    # Exécuter le test de connectivité
    if kubectl exec $source_pod -n $NAMESPACE -- timeout 5 nc -zv $target_service $target_port &>/dev/null; then
        result="SUCCESS"
    else
        result="BLOCKED"
    fi

    if [[ "$result" == "$expected_result" ]]; then
        echo -e "${GREEN}✓${NC} Test réussi: $result"
    else
        echo -e "${RED}✗${NC} Test échoué: attendu $expected_result, obtenu $result"
    fi
    echo ""
}

# Créer des pods de test pour les différents scénarios
echo "1. Création des pods de test..."

# Pod frontend
kubectl run test-frontend --image=busybox --rm --restart=Never --labels="app=secure-web-app,tier=frontend" -n $NAMESPACE --command -- sleep 3600 &

# Pod backend
kubectl run test-backend --image=busybox --rm --restart=Never --labels="app=api-backend,tier=backend" -n $NAMESPACE --command -- sleep 3600 &

# Pod non autorisé
kubectl run test-unauthorized --image=busybox --rm --restart=Never --labels="app=unauthorized" -n $NAMESPACE --command -- sleep 3600 &

# Attendre que les pods soient prêts
echo "Attente du démarrage des pods de test..."
sleep 30

echo -e "\n2. Test des communications autorisées..."

# Frontend vers Backend (devrait fonctionner)
test_network_connectivity "test-frontend" "api-backend-service" "3000" "SUCCESS" "Frontend vers Backend API"

# Backend vers Database (devrait fonctionner si DB existe)
# test_network_connectivity "test-backend" "postgresql.database.svc.cluster.local" "5432" "SUCCESS" "Backend vers Database"

echo -e "\n3. Test des communications bloquées..."

# Pod non autorisé vers Backend (devrait être bloqué)
test_network_connectivity "test-unauthorized" "api-backend-service" "3000" "BLOCKED" "Pod non autorisé vers Backend"

# Frontend vers ports non autorisés (devrait être bloqué)
test_network_connectivity "test-frontend" "api-backend-service" "22" "BLOCKED" "Frontend vers port SSH Backend"

echo -e "\n4. Test de l'isolement par défaut..."

# Test que tout est bloqué par défaut
test_network_connectivity "test-unauthorized" "kubernetes.default.svc.cluster.local" "443" "BLOCKED" "Accès non autorisé à l'API K8s"

echo -e "\n5. Nettoyage des pods de test..."
kubectl delete pod test-frontend test-backend test-unauthorized -n $NAMESPACE --ignore-not-found=true

echo -e "\n6. Validation des Network Policies..."
kubectl get networkpolicies -n $NAMESPACE -o wide
kubectl describe networkpolicy default-deny-all-ingress -n $NAMESPACE

echo -e "\n${GREEN}=== Tests Network Policies terminés ===${NC}"
```

### Outils d'audit et monitoring

```bash
#!/bin/bash
# security-audit.sh

echo "=== Audit de sécurité Kubernetes ==="

echo "1. Vérification des Pod Security Standards..."
kubectl get ns -o custom-columns="NAME:.metadata.name,ENFORCE:.metadata.labels.pod-security\.kubernetes\.io/enforce,AUDIT:.metadata.labels.pod-security\.kubernetes\.io/audit,WARN:.metadata.labels.pod-security\.kubernetes\.io/warn"

echo -e "\n2. Pods non-conformes potentiels..."
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.securityContext.runAsNonRoot}{"\t"}{.spec.containers[0].securityContext.allowPrivilegeEscalation}{"\n"}{end}' | awk '$3!="true" || $4!="false" {print "⚠️  " $1 "/" $2 " - runAsNonRoot:" $3 " allowPrivilegeEscalation:" $4}'

echo -e "\n3. Network Policies par namespace..."
kubectl get networkpolicies --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,POD-SELECTOR:.spec.podSelector"

echo -e "\n4. ServiceAccounts avec automount activé..."
kubectl get serviceaccounts --all-namespaces -o jsonpath='{range .items[?(.automountServiceAccountToken!=false)]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.automountServiceAccountToken}{"\n"}{end}' | awk '{print "⚠️  " $1 "/" $2 " - automount:" $3}'

echo -e "\n5. Pods avec capabilities privilégiées..."
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[0].securityContext.capabilities.add}{"\n"}{end}' | grep -v "\t\[\]" | grep -v "\t$"

echo -e "\n6. Résumé des violations de sécurité..."
violation_count=0

# Compter les pods sans runAsNonRoot
violation_count=$((violation_count + $(kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.spec.securityContext.runAsNonRoot}{"\n"}{end}' | grep -c "^$\|false" || true)))

# Compter les Network Policies manquantes
namespaces_without_policies=$(kubectl get ns -o name | while read ns; do
    ns_name=$(echo $ns | cut -d/ -f2)
    if [[ "$ns_name" != "kube-system" && "$ns_name" != "kube-public" && "$ns_name" != "kube-node-lease" ]]; then
        policy_count=$(kubectl get networkpolicies -n $ns_name --no-headers 2>/dev/null | wc -l)
        if [[ $policy_count -eq 0 ]]; then
            echo $ns_name
        fi
    fi
done | wc -l)

violation_count=$((violation_count + namespaces_without_policies))

if [[ $violation_count -eq 0 ]]; then
    echo -e "${GREEN}✓ Aucune violation de sécurité détectée${NC}"
else
    echo -e "${RED}⚠️  $violation_count violations de sécurité détectées${NC}"
fi
```

## Exercice 4 : Monitoring et alerting sécurité

### Solution complète : ServiceMonitor pour métriques de sécurité

```yaml
# security-monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: pod-security-metrics
  namespace: monitoring
  labels:
    app: security-monitoring
spec:
  selector:
    matchLabels:
      app: kube-state-metrics
  endpoints:
    - port: http-metrics
      interval: 30s
      path: /metrics
      relabelings:
        - sourceLabels: [__name__]
          regex: 'kube_pod_security_policy_.*'
          action: keep
---
# Règles d'alerte pour violations de sécurité
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: security-alerts
  namespace: monitoring
  labels:
    app: security-monitoring
spec:
  groups:
    - name: kubernetes.security
      rules:
        - alert: PodSecurityViolation
          expr: |
            increase(kube_pod_status_phase{phase="Failed"}[5m]) > 0
            AND on(pod) kube_pod_info{created_by_kind="ReplicaSet"}
            AND on(pod) kube_pod_labels{label_security_violation="true"}
          for: 0m
          labels:
            severity: warning
            category: security
          annotations:
            summary: 'Pod security violation detected'
            description: 'Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} failed due to security policy violation'

        - alert: UnauthorizedNetworkTraffic
          expr: |
            increase(prometheus_notifications_dropped_total[5m]) > 0
          for: 2m
          labels:
            severity: critical
            category: security
          annotations:
            summary: 'Potential unauthorized network traffic'
            description: 'Increased network policy violations detected in the cluster'

        - alert: PrivilegedPodCreated
          expr: |
            kube_pod_container_status_running == 1
            AND on(pod) kube_pod_spec_containers_security_context_privileged == 1
          for: 0m
          labels:
            severity: critical
            category: security
          annotations:
            summary: 'Privileged pod detected'
            description: 'Privileged pod {{ $labels.pod }} is running in namespace {{ $labels.namespace }}'

        - alert: RootUserPod
          expr: |
            kube_pod_container_status_running == 1
            AND on(pod) kube_pod_spec_containers_security_context_run_as_user == 0
          for: 0m
          labels:
            severity: warning
            category: security
          annotations:
            summary: 'Pod running as root user'
            description: 'Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is running as root user'
```

## Bonnes pratiques démontrées

### 1. **Pod Security Standards**

- **Restricted** pour la production
- **Baseline** pour staging avec audit
- **Privileged** uniquement pour development
- Migration progressive vers Restricted

### 2. **Network Policies**

- Deny-all par défaut
- Principe du moindre privilège
- Segmentation par tier/fonction
- Communication inter-namespaces contrôlée

### 3. **Monitoring et alerting**

- Métriques de sécurité automatisées
- Alertes sur violations
- Audit trails complets
- Dashboards de sécurité

### 4. **Tests automatisés**

- Validation continue des politiques
- Tests de connectivité réseau
- Audit de conformité automatique
- Rapports de sécurité réguliers

## Points de validation

### ✅ Critères de réussite

1. **Pod Security Standards** : Namespaces configurés avec niveaux appropriés
2. **Pods conformes** : Déploiements respectant les standards Restricted
3. **Network Policies** : Isolation réseau effective par défaut
4. **Communication contrôlée** : Flux autorisés uniquement entre services légitimes
5. **Monitoring** : Alertes sur violations de sécurité
6. **Tests automatisés** : Validation continue des politiques

### 🔍 Points de contrôle

- Aucun pod privilégié en production
- Toutes les communications réseau intentionnelles
- Alerts fonctionnelles sur violations
- Documentation des politiques à jour
- Procédures d'incident sécurisé définies

Cette correction fournit une approche complète et production-ready pour sécuriser les workloads Kubernetes avec Pod Security Standards et Network Policies.
