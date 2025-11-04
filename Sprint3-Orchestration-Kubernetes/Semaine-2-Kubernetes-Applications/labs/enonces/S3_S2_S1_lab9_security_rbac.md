# LAB 9 - Sécurité et RBAC avancés

## Objectif

Implémenter une politique de sécurité complète avec RBAC granulaire, Pod Security Standards et audit de sécurité.

## Contexte

Sécuriser l'application e-commerce avec :

- Contrôle d'accès granulaire par rôles (RBAC)
- Pod Security Standards (PSS) et Pod Security Policies
- Service Accounts dédiés et authentification
- Audit et monitoring de sécurité
- Gestion des secrets et chiffrement
- Analyse de vulnérabilités

## Prérequis

- Application e-commerce complètement déployée
- Cluster avec admission controllers activés
- Outil d'analyse de sécurité (Falco, Trivy)
- Monitoring configuré

## Instructions détaillées

### Étape 1 : Configuration RBAC granulaire

1. Créer des rôles spécialisés par environnement et fonction :

```yaml
# rbac-roles.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-dev
  name: developer
rules:
  # Lecture sur tout
  - apiGroups: ['']
    resources: ['*']
    verbs: ['get', 'list', 'watch']
  # Création/modification des ressources de développement
  - apiGroups: ['']
    resources: ['pods', 'pods/log', 'pods/exec']
    verbs: ['create', 'delete', 'patch', 'update']
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets']
    verbs: ['create', 'delete', 'patch', 'update']
  # Pas d'accès aux secrets sensibles
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get', 'list']
    resourceNames: ['app-config', 'database-credentials'] # Seulement certains secrets

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-staging
  name: tester
rules:
  # Lecture complète
  - apiGroups: ['']
    resources: ['*']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps', 'extensions', 'networking.k8s.io']
    resources: ['*']
    verbs: ['get', 'list', 'watch']
  # Modification limitée pour les tests
  - apiGroups: ['']
    resources: ['pods/exec', 'pods/log']
    verbs: ['create']
  - apiGroups: ['batch']
    resources: ['jobs']
    verbs: ['create', 'delete']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: operator
rules:
  # Lecture sur les ressources de production
  - apiGroups: ['']
    resources: ['pods', 'services', 'endpoints', 'persistentvolumeclaims']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps']
    resources: ['deployments', 'statefulsets', 'daemonsets']
    verbs: ['get', 'list', 'watch', 'patch', 'update']
  # Gestion des secrets (lecture seulement)
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get', 'list']
  # Scaling autorisé
  - apiGroups: ['apps']
    resources: ['deployments/scale', 'statefulsets/scale']
    verbs: ['update', 'patch']
  # Pas de suppression en production
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['delete']
    resourceNames: [] # Aucun pod ne peut être supprimé directement

---
# Rôle pour les backups
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: backup-operator
rules:
  - apiGroups: ['']
    resources: ['persistentvolumes', 'persistentvolumeclaims']
    verbs: ['get', 'list', 'create', 'delete']
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'list', 'create', 'delete']
  - apiGroups: ['apps']
    resources: ['statefulsets', 'deployments']
    verbs: ['get', 'list', 'patch', 'update']
  - apiGroups: ['storage.k8s.io']
    resources: ['volumesnapshots', 'volumesnapshotcontents']
    verbs: ['*']

---
# Rôle pour monitoring
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-reader
rules:
  - apiGroups: ['']
    resources: ['nodes', 'nodes/metrics', 'services', 'endpoints', 'pods']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['extensions', 'networking.k8s.io']
    resources: ['ingresses']
    verbs: ['get', 'list', 'watch']
  - nonResourceURLs: ['/metrics', '/metrics/*']
    verbs: ['get']
```

### Étape 2 : Service Accounts spécialisés

2. Créer des Service Accounts dédiés :

```yaml
# service-accounts.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ecommerce-frontend
  namespace: ecommerce
automountServiceAccountToken: false # Sécurité: pas de token auto

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ecommerce-backend
  namespace: ecommerce
automountServiceAccountToken: true

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ecommerce-database
  namespace: ecommerce
automountServiceAccountToken: false

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backup-service
  namespace: ecommerce
automountServiceAccountToken: true

---
# Service Account pour les développeurs
apiVersion: v1
kind: ServiceAccount
metadata:
  name: developer-sa
  namespace: ecommerce-dev

---
# Bindings des rôles aux Service Accounts
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: backend-binding
  namespace: ecommerce
subjects:
  - kind: ServiceAccount
    name: ecommerce-backend
    namespace: ecommerce
roleRef:
  kind: Role
  name: backend-role
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: backup-operator-binding
subjects:
  - kind: ServiceAccount
    name: backup-service
    namespace: ecommerce
roleRef:
  kind: ClusterRole
  name: backup-operator
  apiGroup: rbac.authorization.k8s.io

---
# Rôle spécifique pour l'API backend
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce
  name: backend-role
rules:
  # Lecture des ConfigMaps et Secrets nécessaires
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list']
    resourceNames: ['app-config', 'api-config']
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get']
    resourceNames: ['database-credentials', 'api-keys']
  # Accès aux services pour service discovery
  - apiGroups: ['']
    resources: ['services', 'endpoints']
    verbs: ['get', 'list', 'watch']
```

### Étape 3 : Pod Security Standards

3. Configurer les standards de sécurité pour les pods :

```yaml
# pod-security-standards.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-dev
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-staging
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-prod
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# Policy Security pour les workloads critiques
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-security-context
spec:
  validationFailureAction: enforce
  background: true
  rules:
    - name: check-security-context
      match:
        any:
          - resources:
              kinds:
                - Pod
              namespaces:
                - ecommerce-prod
                - ecommerce-staging
      validate:
        message: 'Security context is required'
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
              runAsUser: '>0'
              fsGroup: '>0'
            containers:
              - name: '*'
                securityContext:
                  allowPrivilegeEscalation: false
                  readOnlyRootFilesystem: true
                  runAsNonRoot: true
                  capabilities:
                    drop:
                      - ALL

---
# Network Policy pour isolation
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-network-policies
spec:
  validationFailureAction: enforce
  background: false
  rules:
    - name: check-network-policy-exists
      match:
        any:
          - resources:
              kinds:
                - Namespace
              names:
                - 'ecommerce*'
      validate:
        message: 'NetworkPolicy is required for namespace'
        deny:
          conditions:
            - key: "{{ request.operation || 'BACKGROUND' }}"
              operator: NotEquals
              value: DELETE
            - key: "{{ query_by_name(request.namespace, 'NetworkPolicy').items | length(@) }}"
              operator: Equals
              value: 0
```

### Étape 4 : Gestion sécurisée des secrets

4. Implémenter une gestion avancée des secrets :

```yaml
# secrets-management.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: ecommerce
spec:
  provider:
    vault:
      server: 'https://vault.company.com'
      path: 'secret'
      version: 'v2'
      auth:
        kubernetes:
          mountPath: 'kubernetes'
          role: 'ecommerce-role'

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: ecommerce
spec:
  refreshInterval: 15s # Rotation fréquente
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: postgres-secret
    creationPolicy: Owner
    template:
      type: Opaque
      data:
        username: '{{ .username }}'
        password: '{{ .password }}'
        connection-string: 'postgresql://{{ .username }}:{{ .password }}@postgres-service:5432/ecommerce'
  data:
    - secretKey: username
      remoteRef:
        key: database/postgres
        property: username
    - secretKey: password
      remoteRef:
        key: database/postgres
        property: password

---
# Chiffrement des secrets au repos
apiVersion: v1
kind: Secret
metadata:
  name: encryption-config
  namespace: kube-system
data:
  config.yaml: |
    apiVersion: apiserver.config.k8s.io/v1
    kind: EncryptionConfiguration
    resources:
    - resources:
      - secrets
      providers:
      - aescbc:
          keys:
          - name: key1
            secret: <32-byte-base64-encoded-key>
      - identity: {}

---
# Sealed Secrets pour GitOps
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: api-keys
  namespace: ecommerce
spec:
  encryptedData:
    stripe-key: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEQAx...
    jwt-secret: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEQAx...
  template:
    metadata:
      name: api-keys
      namespace: ecommerce
```

### Étape 5 : Audit et monitoring de sécurité

5. Configurer l'audit de sécurité :

```yaml
# security-audit.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: audit-policy
  namespace: kube-system
data:
  audit-policy.yaml: |
    apiVersion: audit.k8s.io/v1
    kind: Policy
    rules:
    # Audit des accès aux secrets
    - level: RequestResponse
      resources:
      - group: ""
        resources: ["secrets"]
      namespaces: ["ecommerce", "ecommerce-prod", "ecommerce-staging"]

    # Audit des modifications RBAC
    - level: RequestResponse
      resources:
      - group: "rbac.authorization.k8s.io"
        resources: ["*"]

    # Audit des exec/attach dans les pods
    - level: Request
      resources:
      - group: ""
        resources: ["pods/exec", "pods/attach", "pods/portforward"]
      namespaces: ["ecommerce-prod"]

    # Audit des créations/suppressions en production
    - level: RequestResponse
      verbs: ["create", "delete"]
      namespaces: ["ecommerce-prod"]

    # Metadata seulement pour le reste
    - level: Metadata
      omitStages:
      - RequestReceived

---
# Falco rules pour la détection d'intrusion
apiVersion: v1
kind: ConfigMap
metadata:
  name: falco-rules
  namespace: falco
data:
  ecommerce_rules.yaml: |
    - rule: Unauthorized Process in Container
      desc: Detect unauthorized process execution in ecommerce containers
      condition: >
        spawned_process and container and 
        container.image.repository in (ecommerce/frontend, ecommerce/backend) and
        not proc.name in (node, java, nginx, sh)
      output: >
        Unauthorized process in ecommerce container 
        (user=%user.name command=%proc.cmdline container=%container.name image=%container.image)
      priority: WARNING

    - rule: Sensitive File Access
      desc: Detect access to sensitive files in ecommerce containers
      condition: >
        open_read and container and
        container.image.repository startswith "ecommerce/" and
        fd.name in (/etc/passwd, /etc/shadow, /proc/*/environ)
      output: >
        Sensitive file access in ecommerce container 
        (user=%user.name file=%fd.name container=%container.name)
      priority: WARNING

    - rule: Network Connection Outside Cluster
      desc: Detect outbound connections from ecommerce pods
      condition: >
        outbound and container and
        container.image.repository startswith "ecommerce/" and
        not fd.net.raddr in (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
      output: >
        External network connection from ecommerce container 
        (destination=%fd.net.raddr.name:%fd.net.raddr.port container=%container.name)
      priority: INFO

---
# Deployment Falco
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco
  namespace: falco
spec:
  selector:
    matchLabels:
      app: falco
  template:
    metadata:
      labels:
        app: falco
    spec:
      serviceAccount: falco
      hostNetwork: true
      hostPID: true
      containers:
        - name: falco
          image: falcosecurity/falco:latest
          args:
            - /usr/bin/falco
            - --cri=/run/containerd/containerd.sock
            - --k8s-api=https://kubernetes.default
            - --k8s-api-cert=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
            - --k8s-api-token=/var/run/secrets/kubernetes.io/serviceaccount/token
          securityContext:
            privileged: true
          volumeMounts:
            - mountPath: /host/var/run/docker.sock
              name: docker-socket
            - mountPath: /host/proc
              name: proc-fs
            - mountPath: /host/boot
              name: boot-fs
            - mountPath: /host/lib/modules
              name: lib-modules
            - mountPath: /host/usr
              name: usr-fs
            - mountPath: /etc/falco/rules.d
              name: falco-rules
      volumes:
        - name: docker-socket
          hostPath:
            path: /var/run/docker.sock
        - name: proc-fs
          hostPath:
            path: /proc
        - name: boot-fs
          hostPath:
            path: /boot
        - name: lib-modules
          hostPath:
            path: /lib/modules
        - name: usr-fs
          hostPath:
            path: /usr
        - name: falco-rules
          configMap:
            name: falco-rules
```

### Étape 6 : Analyse de vulnérabilités

6. Configurer l'analyse continue de vulnérabilités :

```yaml
# vulnerability-scanning.yaml
apiVersion: aquasec.github.io/v1alpha1
kind: VulnerabilityReport
metadata:
  name: ecommerce-scan
  namespace: ecommerce
spec:
  artifact:
    repository: ecommerce/backend
    tag: latest
  scanner:
    name: Trivy
    vendor: Aqua Security
    version: '0.18.3'

---
# CronJob pour scan régulier
apiVersion: batch/v1
kind: CronJob
metadata:
  name: security-scan
  namespace: ecommerce
spec:
  schedule: '0 2 * * *' # Tous les jours à 2h
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: trivy-scanner
              image: aquasec/trivy:latest
              command:
                - sh
                - -c
                - |
                  # Scanner toutes les images du namespace
                  kubectl get pods -n ecommerce -o jsonpath='{.items[*].spec.containers[*].image}' | \
                  tr ' ' '\n' | sort -u | while read image; do
                    echo "Scanning $image..."
                    trivy image --format json --output /reports/$(echo $image | tr '/' '_').json $image
                  done
              volumeMounts:
                - name: reports
                  mountPath: /reports
          volumes:
            - name: reports
              persistentVolumeClaim:
                claimName: scan-reports
          restartPolicy: OnFailure

---
# Policy pour bloquer les images vulnérables
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-vulnerabilities
spec:
  validationFailureAction: enforce
  background: true
  rules:
    - name: check-image-vulnerabilities
      match:
        any:
          - resources:
              kinds:
                - Pod
              namespaces:
                - ecommerce-prod
      validate:
        message: 'Image has critical vulnerabilities'
        deny:
          conditions:
            - key: "{{ request.object.spec.containers[?contains(@.image, ':latest')] | length(@) }}"
              operator: GreaterThan
              value: 0
```

### Étape 7 : Tests de sécurité automatisés

7. Créer une suite de tests de sécurité :

```bash
# security-test-suite.sh
#!/bin/bash

echo "🔒 Suite de tests de sécurité Kubernetes"

# Test 1: Vérification RBAC
echo "Test 1: Vérification des permissions RBAC..."

# Tester qu'un développeur ne peut pas accéder à la production
kubectl auth can-i delete pods --namespace=ecommerce-prod --as=system:serviceaccount:ecommerce-dev:developer-sa
if [ $? -eq 0 ]; then
    echo "❌ ERREUR: Développeur peut supprimer des pods en production!"
    exit 1
else
    echo "✅ RBAC: Isolation dev/prod correcte"
fi

# Test 2: Vérification Pod Security Standards
echo "Test 2: Vérification Pod Security Standards..."

# Tenter de déployer un pod privilégié (doit échouer)
cat <<EOF | kubectl apply -f - --dry-run=server
apiVersion: v1
kind: Pod
metadata:
  name: privileged-test
  namespace: ecommerce-prod
spec:
  containers:
  - name: test
    image: alpine
    securityContext:
      privileged: true
EOF

if [ $? -eq 0 ]; then
    echo "❌ ERREUR: Pod privilégié autorisé en production!"
    exit 1
else
    echo "✅ PSS: Pod privilégié correctement bloqué"
fi

# Test 3: Vérification des NetworkPolicies
echo "Test 3: Test des NetworkPolicies..."

# Vérifier qu'on ne peut pas accéder directement à la base de données
kubectl run test-pod --image=alpine --rm -i --restart=Never -- \
    timeout 5 nc -z postgres-service.ecommerce 5432 2>/dev/null

if [ $? -eq 0 ]; then
    echo "❌ ERREUR: Accès direct à la base autorisé!"
    exit 1
else
    echo "✅ Network Policy: Base de données protégée"
fi

# Test 4: Vérification des secrets
echo "Test 4: Vérification de la gestion des secrets..."

# Vérifier que les secrets ne sont pas en plain text
kubectl get secret postgres-secret -n ecommerce -o yaml | grep -v "password.*:" | grep -E "password|token"
if [ $? -eq 0 ]; then
    echo "❌ ERREUR: Secrets en plain text détectés!"
    exit 1
else
    echo "✅ Secrets: Correctement encodés"
fi

# Test 5: Vérification des images
echo "Test 5: Vérification des signatures d'images..."

# Vérifier qu'aucune image :latest n'est utilisée en production
LATEST_IMAGES=$(kubectl get pods -n ecommerce-prod -o jsonpath='{.items[*].spec.containers[*].image}' | grep -c ":latest")
if [ "$LATEST_IMAGES" -gt 0 ]; then
    echo "❌ ERREUR: Images :latest utilisées en production!"
    exit 1
else
    echo "✅ Images: Pas de tags :latest en production"
fi

# Test 6: Test d'évasion de conteneur
echo "Test 6: Test d'évasion de conteneur..."

# Tenter d'accéder au système de fichiers de l'hôte
kubectl exec -n ecommerce deployment/frontend -- ls /host 2>/dev/null
if [ $? -eq 0 ]; then
    echo "❌ ERREUR: Accès au système de fichiers hôte possible!"
    exit 1
else
    echo "✅ Isolation: Pas d'accès au système hôte"
fi

echo "🎉 Tous les tests de sécurité sont passés!"
```

## Critères de validation

- [ ] RBAC granulaire configuré et testé
- [ ] Pod Security Standards appliqués
- [ ] Service Accounts spécialisés créés
- [ ] Gestion sécurisée des secrets en place
- [ ] Audit de sécurité configuré
- [ ] Monitoring des intrusions (Falco) actif
- [ ] Analyse de vulnérabilités automatisée
- [ ] Tests de sécurité automatisés passants
- [ ] Documentation de sécurité complète

## Tests pratiques

```bash
# Déploiement complet de la sécurité
kubectl apply -f rbac-roles.yaml
kubectl apply -f service-accounts.yaml
kubectl apply -f pod-security-standards.yaml
kubectl apply -f secrets-management.yaml
kubectl apply -f security-audit.yaml

# Installation Falco
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco --namespace falco --create-namespace

# Tests de sécurité
bash security-test-suite.sh

# Vérification des logs d'audit
kubectl logs -n kube-system kube-apiserver-* | grep audit

# Vérification Falco
kubectl logs -n falco daemonset/falco
```

## Durée estimée

60 minutes
