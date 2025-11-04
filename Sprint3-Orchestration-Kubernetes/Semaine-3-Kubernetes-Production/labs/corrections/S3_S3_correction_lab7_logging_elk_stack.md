# LAB 7 - Correction : ELK Stack (Elasticsearch, Logstash, Kibana)

## 📋 Vue d'ensemble de la solution

Cette correction présente le déploiement complet de la stack ELK avec Filebeat pour la collecte centralisée des logs Kubernetes et applications.

---

## 🔧 Solution complète

### Étape 1 : Installation Elasticsearch

```yaml
# elk/elasticsearch.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: logging
---
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch
  namespace: logging
spec:
  version: 8.10.4
  nodeSets:
    - name: default
      count: 3
      config:
        node.store.allow_mmap: false
        xpack.security.enabled: true
        xpack.security.transport.ssl.enabled: true
        xpack.security.http.ssl.enabled: true
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 2Gi
                  cpu: 1000m
                limits:
                  memory: 4Gi
                  cpu: 2000m
              env:
                - name: ES_JAVA_OPTS
                  value: '-Xms2g -Xmx2g'
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 100Gi
            storageClassName: fast-ssd
```

### Étape 2 : Installation Kibana

```yaml
# elk/kibana.yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana
  namespace: logging
spec:
  version: 8.10.4
  count: 1
  elasticsearchRef:
    name: elasticsearch
  config:
    server.publicBaseUrl: 'https://kibana.k8s.local'
    xpack.security.enabled: true
    xpack.monitoring.collection.enabled: true
  podTemplate:
    spec:
      containers:
        - name: kibana
          resources:
            requests:
              memory: 1Gi
              cpu: 500m
            limits:
              memory: 2Gi
              cpu: 1000m
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kibana-ingress
  namespace: logging
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - kibana.k8s.local
      secretName: kibana-tls
  rules:
    - host: kibana.k8s.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: kibana-kb-http
                port:
                  number: 5601
```

### Étape 3 : Configuration Filebeat

```yaml
# elk/filebeat.yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: filebeat
  namespace: logging
spec:
  type: filebeat
  version: 8.10.4
  elasticsearchRef:
    name: elasticsearch
  kibanaRef:
    name: kibana
  config:
    filebeat.inputs:
      - type: container
        paths:
          - /var/log/containers/*.log
        processors:
          - add_kubernetes_metadata:
              host: ${NODE_NAME}
              matchers:
                - logs_path:
                    logs_path: '/var/log/containers/'
          - decode_json_fields:
              fields: ['message']
              target: ''
              overwrite_keys: true

    output.elasticsearch:
      hosts: ['elasticsearch-es-http:9200']
      protocol: https
      ssl.certificate_authorities: ['/mnt/elastic/tls.crt']
      username: ${ELASTICSEARCH_USERNAME}
      password: ${ELASTICSEARCH_PASSWORD}

    setup.kibana:
      host: 'kibana-kb-http:5601'
      protocol: https
      ssl.certificate_authorities: ['/mnt/elastic/tls.crt']
      username: ${ELASTICSEARCH_USERNAME}
      password: ${ELASTICSEARCH_PASSWORD}

    setup.ilm.enabled: true
    setup.template.enabled: true
    setup.dashboards.enabled: true

    logging.level: info
    logging.to_stderr: true

  daemonSet:
    podTemplate:
      spec:
        serviceAccountName: filebeat
        terminationGracePeriodSeconds: 30
        hostNetwork: true
        dnsPolicy: ClusterFirstWithHostNet
        containers:
          - name: filebeat
            securityContext:
              runAsUser: 0
            volumeMounts:
              - name: varlogcontainers
                mountPath: /var/log/containers
                readOnly: true
              - name: varlogpods
                mountPath: /var/log/pods
                readOnly: true
              - name: varlibdockercontainers
                mountPath: /var/lib/docker/containers
                readOnly: true
            env:
              - name: NODE_NAME
                valueFrom:
                  fieldRef:
                    fieldPath: spec.nodeName
              - name: ELASTICSEARCH_USERNAME
                valueFrom:
                  secretKeyRef:
                    name: elasticsearch-es-elastic-user
                    key: elastic
              - name: ELASTICSEARCH_PASSWORD
                valueFrom:
                  secretKeyRef:
                    name: elasticsearch-es-elastic-user
                    key: elastic
        volumes:
          - name: varlogcontainers
            hostPath:
              path: /var/log/containers
          - name: varlogpods
            hostPath:
              path: /var/log/pods
          - name: varlibdockercontainers
            hostPath:
              path: /var/lib/docker/containers
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: filebeat
  namespace: logging
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: filebeat
rules:
  - apiGroups: ['']
    resources:
      - nodes
      - namespaces
      - events
      - pods
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps']
    resources:
      - replicasets
    verbs: ['get', 'list', 'watch']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: filebeat
subjects:
  - kind: ServiceAccount
    name: filebeat
    namespace: logging
roleRef:
  kind: ClusterRole
  name: filebeat
  apiGroup: rbac.authorization.k8s.io
```

### Étape 4 : Index Templates et Policies

```bash
# Scripts de configuration Elasticsearch
#!/bin/bash
# elk/setup-elasticsearch.sh

ELASTIC_PASSWORD=$(kubectl get secret elasticsearch-es-elastic-user -n logging -o jsonpath='{.data.elastic}' | base64 -d)
ES_URL="https://elasticsearch-es-http.logging.svc.cluster.local:9200"

# Index template pour les logs d'applications
curl -k -u "elastic:$ELASTIC_PASSWORD" -X PUT "$ES_URL/_index_template/webapp-logs" \
-H "Content-Type: application/json" -d '{
  "index_patterns": ["webapp-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "webapp-policy",
      "index.lifecycle.rollover_alias": "webapp-logs"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "logger": { "type": "keyword" },
        "message": { "type": "text" },
        "kubernetes": {
          "properties": {
            "namespace": { "type": "keyword" },
            "pod": { "type": "keyword" },
            "container": { "type": "keyword" }
          }
        }
      }
    }
  }
}'

# ILM Policy pour rotation des logs
curl -k -u "elastic:$ELASTIC_PASSWORD" -X PUT "$ES_URL/_ilm/policy/webapp-policy" \
-H "Content-Type: application/json" -d '{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "10GB",
            "max_age": "7d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "allocate": {
            "number_of_replicas": 0
          }
        }
      },
      "delete": {
        "min_age": "30d"
      }
    }
  }
}'
```

### Étape 5 : Tests et validation

```bash
#!/bin/bash
# elk/test-elk-stack.sh

echo "🧪 Test de la stack ELK"

# Vérifier Elasticsearch
kubectl port-forward service/elasticsearch-es-http 9200:9200 -n logging &
ES_PID=$!
sleep 10

ELASTIC_PASSWORD=$(kubectl get secret elasticsearch-es-elastic-user -n logging -o jsonpath='{.data.elastic}' | base64 -d)
ES_HEALTH=$(curl -s -k -u "elastic:$ELASTIC_PASSWORD" https://localhost:9200/_cluster/health | jq -r '.status')

if [ "$ES_HEALTH" = "green" ] || [ "$ES_HEALTH" = "yellow" ]; then
    echo "✅ Elasticsearch cluster status: $ES_HEALTH"
else
    echo "❌ Elasticsearch cluster unhealthy"
fi

# Vérifier les indices
INDICES=$(curl -s -k -u "elastic:$ELASTIC_PASSWORD" https://localhost:9200/_cat/indices | wc -l)
echo "📊 Nombre d'indices: $INDICES"

kill $ES_PID

# Test Kibana
kubectl port-forward service/kibana-kb-http 5601:5601 -n logging &
KB_PID=$!
sleep 10

KIBANA_STATUS=$(curl -s -k -w "%{http_code}" https://localhost:5601/api/status -o /dev/null)
if [ "$KIBANA_STATUS" = "200" ]; then
    echo "✅ Kibana accessible"
else
    echo "❌ Kibana non accessible"
fi

kill $KB_PID

echo "🎉 Tests ELK terminés"
```

---

## 🎯 Résultats

✅ **Stack ELK complète** avec collecte automatique des logs  
✅ **Dashboards Kibana** pour visualisation  
✅ **Rotation automatique** des indices  
✅ **Recherche avancée** dans les logs

---

_Correction réalisée par Hassan ESSADIK - Formation DevOps Kubernetes_
