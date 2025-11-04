# LAB 7 - Logging avec ELK Stack (Elasticsearch, Logstash, Kibana)

## Objectifs

- Déployer la stack ELK sur Kubernetes
- Configurer la collecte de logs d'applications et d'infrastructure
- Créer des dashboards et visualisations dans Kibana
- Implémenter la recherche et l'analyse de logs
- Configurer des alertes basées sur les logs

## Prérequis

- Cluster Kubernetes fonctionnel
- kubectl configuré
- Helm 3.x installé
- Applications déployées à monitorer
- Connaissances de base d'Elasticsearch et Kibana

## Contexte du LAB

Vous allez déployer une solution de logging centralisée pour :

- Collecter les logs des applications et de l'infrastructure
- Centraliser et structurer les données de logs
- Analyser les logs pour debugging et observabilité
- Créer des alertes basées sur les patterns de logs
- Établir une stratégie de rétention et archivage

## Exercice 1 : Installation d'Elasticsearch

### Étape 1.1 : Ajout du repository Helm

```bash
# Ajouter le repository Elastic
helm repo add elastic https://helm.elastic.co
helm repo update
```

### Étape 1.2 : Création du namespace

```bash
kubectl create namespace logging
```

### Étape 1.3 : Configuration Elasticsearch

Créez `logging/elasticsearch-values.yaml` :

```yaml
# Configuration du cluster Elasticsearch
clusterName: 'elasticsearch'
nodeGroup: 'master'

# Master nodes configuration
masterService: 'elasticsearch-master'
roles:
  master: 'true'
  ingest: 'true'
  data: 'true'

replicas: 3
minimumMasterNodes: 2

# Resources
esJavaOpts: '-Xmx1g -Xms1g'
resources:
  requests:
    cpu: '1000m'
    memory: '2Gi'
  limits:
    cpu: '1000m'
    memory: '2Gi'

# Volume et persistence
volumeClaimTemplate:
  accessModes: ['ReadWriteOnce']
  storageClassName: 'fast-ssd'
  resources:
    requests:
      storage: 30Gi

# Configuration cluster
esConfig:
  elasticsearch.yml: |
    cluster.name: elasticsearch
    node.name: ${HOSTNAME}
    network.host: 0.0.0.0

    # Discovery configuration
    discovery.seed_hosts: ["elasticsearch-master-headless"]
    cluster.initial_master_nodes: ["elasticsearch-master-0", "elasticsearch-master-1", "elasticsearch-master-2"]

    # Index configuration
    action.auto_create_index: true
    action.destructive_requires_name: false

    # Memory settings
    bootstrap.memory_lock: false

    # Security (désactivé pour simplifier)
    xpack.security.enabled: false
    xpack.security.transport.ssl.enabled: false
    xpack.security.http.ssl.enabled: false

    # Monitoring
    xpack.monitoring.collection.enabled: true

# Service configuration
service:
  type: ClusterIP
  httpPort: 9200
  transportPort: 9300

# Ingress pour accès externe
ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: elasticsearch-auth
  hosts:
    - host: elasticsearch.local
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: elasticsearch-tls
      hosts:
        - elasticsearch.local

# Anti-affinity pour distribution
antiAffinity: 'soft'

# Sysctls pour performance
sysctlVmMaxMapCount: 262144

# Readiness et liveness probes
readinessProbe:
  failureThreshold: 3
  initialDelaySeconds: 10
  periodSeconds: 10
  successThreshold: 3
  timeoutSeconds: 5

# Lifecycle hooks
lifecycle:
  preStop:
    exec:
      command:
        [
          '/bin/bash',
          '-c',
          'curl -XPOST localhost:9200/_flush/synced && sleep 30'
        ]
```

### Étape 1.4 : Installation Elasticsearch

```bash
helm install elasticsearch elastic/elasticsearch \
  --namespace logging \
  --values logging/elasticsearch-values.yaml \
  --version 7.17.3
```

### Étape 1.5 : Vérification du déploiement

```bash
# Vérifier les pods
kubectl get pods -n logging -l app=elasticsearch-master

# Vérifier le cluster
kubectl port-forward -n logging svc/elasticsearch-master 9200:9200
curl -X GET "localhost:9200/_cluster/health?pretty"
```

## Exercice 2 : Installation de Kibana

### Étape 2.1 : Configuration Kibana

Créez `logging/kibana-values.yaml` :

```yaml
# Version alignment avec Elasticsearch
elasticsearchHosts: 'http://elasticsearch-master:9200'

replicas: 2

# Resources
resources:
  requests:
    cpu: '500m'
    memory: '1Gi'
  limits:
    cpu: '1000m'
    memory: '2Gi'

# Service configuration
service:
  type: ClusterIP
  port: 5601

# Configuration Kibana
kibanaConfig:
  kibana.yml: |
    server.name: kibana
    server.host: 0.0.0.0
    server.port: 5601

    # Elasticsearch configuration
    elasticsearch.hosts: ["http://elasticsearch-master:9200"]
    elasticsearch.requestTimeout: 60000
    elasticsearch.shardTimeout: 30000

    # Logging
    logging.dest: stdout
    logging.silent: false
    logging.quiet: false
    logging.verbose: false

    # Monitoring
    monitoring.ui.container.elasticsearch.enabled: true

    # Default index pattern
    kibana.defaultAppId: "discover"

    # Security (désactivé pour simplifier)
    xpack.security.enabled: false
    xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters"

# Ingress
ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: kibana-auth
  hosts:
    - host: kibana.local
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: kibana-tls
      hosts:
        - kibana.local

# Health checks
healthCheckPath: '/api/status'

# Pod disruption budget
podDisruptionBudget:
  enabled: true
  minAvailable: 1

# Anti-affinity
antiAffinity: 'soft'

# Environment variables
env:
  NODE_OPTIONS: '--max-old-space-size=1800'
```

### Étape 2.2 : Installation Kibana

```bash
helm install kibana elastic/kibana \
  --namespace logging \
  --values logging/kibana-values.yaml \
  --version 7.17.3
```

## Exercice 3 : Configuration de Logstash

### Étape 3.1 : Configuration Logstash

Créez `logging/logstash-values.yaml` :

```yaml
replicas: 2

# Resources
resources:
  requests:
    cpu: '500m'
    memory: '1.5Gi'
  limits:
    cpu: '1000m'
    memory: '2Gi'

# Logstash configuration
logstashConfig:
  logstash.yml: |
    http.host: 0.0.0.0
    xpack.monitoring.elasticsearch.hosts: ["http://elasticsearch-master:9200"]
    path.config: /usr/share/logstash/pipeline
    path.data: /usr/share/logstash/data
    path.logs: /usr/share/logstash/logs
    pipeline.workers: 2
    pipeline.batch.size: 1000
    pipeline.batch.delay: 5
    queue.type: persisted
    queue.drain: true

# Pipeline configuration
logstashPipeline:
  logstash.conf: |
    input {
      beats {
        port => 5044
      }
      
      # Input pour les logs Kubernetes
      tcp {
        port => 5000
        codec => json
      }
      
      # Input pour les logs d'applications
      http {
        port => 8080
        codec => json
      }
    }

    filter {
      # Parse des logs Kubernetes
      if [kubernetes] {
        mutate {
          add_field => { "log_source" => "kubernetes" }
        }
        
        # Parse du timestamp
        date {
          match => [ "@timestamp", "ISO8601" ]
        }
        
        # Extraction des informations Kubernetes
        if [kubernetes][pod][name] {
          mutate {
            add_field => { "pod_name" => "%{[kubernetes][pod][name]}" }
            add_field => { "namespace" => "%{[kubernetes][namespace]}" }
            add_field => { "container_name" => "%{[kubernetes][container][name]}" }
          }
        }
      }
      
      # Parse des logs d'applications
      if [fields][app] {
        mutate {
          add_field => { "application" => "%{[fields][app]}" }
          add_field => { "log_source" => "application" }
        }
      }
      
      # Parse des logs nginx
      if [fields][log_type] == "nginx" {
        grok {
          match => { 
            "message" => "%{NGINXACCESS}" 
          }
        }
        
        mutate {
          convert => { "response" => "integer" }
          convert => { "bytes" => "integer" }
        }
        
        if [response] >= 400 {
          mutate {
            add_tag => [ "error" ]
          }
        }
      }
      
      # Parse des logs JSON
      if [message] =~ /^\{.*\}$/ {
        json {
          source => "message"
          target => "parsed_json"
        }
      }
      
      # Geolocalization pour les IPs
      if [clientip] {
        geoip {
          source => "clientip"
          target => "geoip"
        }
      }
      
      # Cleanup des champs inutiles
      mutate {
        remove_field => [ "beat", "input_type", "offset", "source" ]
      }
    }

    output {
      elasticsearch {
        hosts => ["http://elasticsearch-master:9200"]
        
        # Index pattern basé sur la source et la date
        index => "%{log_source}-%{+YYYY.MM.dd}"
        
        # Template pour les mappings
        template_name => "logstash"
        template_pattern => "*"
        template => "/usr/share/logstash/templates/logstash.json"
        template_overwrite => true
      }
      
      # Debug output
      stdout {
        codec => rubydebug
      }
    }

# Service configuration
service:
  type: ClusterIP
  ports:
    - name: beats
      port: 5044
      protocol: TCP
      targetPort: 5044
    - name: tcp
      port: 5000
      protocol: TCP
      targetPort: 5000
    - name: http
      port: 8080
      protocol: TCP
      targetPort: 8080

# Persistence pour la queue
persistence:
  enabled: true
  storageClass: 'fast-ssd'
  size: 10Gi

# Anti-affinity
antiAffinity: 'soft'

# Environment variables
env:
  LS_JAVA_OPTS: '-Xmx1g -Xms1g'
```

### Étape 3.2 : Template Elasticsearch

Créez `logging/logstash-template.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: logstash-template
  namespace: logging
data:
  logstash.json: |
    {
      "index_patterns": ["*"],
      "settings": {
        "index": {
          "number_of_shards": 1,
          "number_of_replicas": 1,
          "refresh_interval": "30s"
        }
      },
      "mappings": {
        "properties": {
          "@timestamp": {
            "type": "date"
          },
          "message": {
            "type": "text",
            "analyzer": "standard"
          },
          "log_level": {
            "type": "keyword"
          },
          "application": {
            "type": "keyword"
          },
          "pod_name": {
            "type": "keyword"
          },
          "namespace": {
            "type": "keyword"
          },
          "container_name": {
            "type": "keyword"
          },
          "host": {
            "type": "keyword"
          },
          "clientip": {
            "type": "ip"
          },
          "response": {
            "type": "integer"
          },
          "bytes": {
            "type": "integer"
          },
          "geoip": {
            "properties": {
              "location": {
                "type": "geo_point"
              },
              "country_name": {
                "type": "keyword"
              },
              "city_name": {
                "type": "keyword"
              }
            }
          }
        }
      }
    }
```

### Étape 3.3 : Installation Logstash

```bash
# Appliquer le template
kubectl apply -f logging/logstash-template.yaml

# Installer Logstash
helm install logstash elastic/logstash \
  --namespace logging \
  --values logging/logstash-values.yaml \
  --version 7.17.3
```

## Exercice 4 : Configuration de Filebeat

### Étape 4.1 : Configuration Filebeat

Créez `logging/filebeat-values.yaml` :

```yaml
# DaemonSet configuration pour déployer sur tous les nœuds
daemonset:
  enabled: true

# Resources
resources:
  requests:
    cpu: '100m'
    memory: '100Mi'
  limits:
    cpu: '200m'
    memory: '200Mi'

# Filebeat configuration
filebeatConfig:
  filebeat.yml: |
    # Configuration des inputs
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
          - logs_path:
              logs_path: "/var/log/containers/"
      - drop_event:
          when:
            or:
            - equals:
                kubernetes.namespace: "kube-system"
            - equals:
                kubernetes.namespace: "kube-public"
            - equals:
                kubernetes.namespace: "logging"
      
    # Input pour les logs système
    - type: log
      paths:
        - /var/log/syslog
        - /var/log/messages
      fields:
        log_type: system
      fields_under_root: true

    # Configuration des outputs
    output.logstash:
      hosts: ["logstash:5044"]

    # Configuration des processors
    processors:
    - add_host_metadata:
        when.not.contains.tags: forwarded
    - add_docker_metadata: ~
    - add_kubernetes_metadata: ~

    # Logging configuration
    logging.level: info
    logging.to_files: false
    logging.to_stderr: true

# Volume mounts pour accéder aux logs
extraVolumes:
  - name: varlog
    hostPath:
      path: /var/log
  - name: varlibdockercontainers
    hostPath:
      path: /var/lib/docker/containers

extraVolumeMounts:
  - name: varlog
    mountPath: /var/log
    readOnly: true
  - name: varlibdockercontainers
    mountPath: /var/lib/docker/containers
    readOnly: true

# Security context
securityContext:
  runAsUser: 0
  privileged: false

# Service account permissions
serviceAccount:
  create: true
  name: filebeat

# Cluster role pour accéder aux métadonnées Kubernetes
clusterRole:
  create: true
  rules:
    - apiGroups: ['']
      resources:
        - nodes
        - namespaces
        - pods
      verbs: ['get', 'list', 'watch']

# Node selector pour déployer uniquement sur certains nœuds
nodeSelector: {}

# Tolerations pour déployer sur tous les nœuds
tolerations:
  - key: node-role.kubernetes.io/master
    operator: Exists
    effect: NoSchedule
```

### Étape 4.2 : Installation Filebeat

```bash
helm install filebeat elastic/filebeat \
  --namespace logging \
  --values logging/filebeat-values.yaml \
  --version 7.17.3
```

## Exercice 5 : Application avec logs structurés

### Étape 5.1 : Application Node.js avec Winston

Créez `app/logger-app.js` :

```javascript
const express = require('express');
const winston = require('winston');
const {ElasticsearchTransport} = require('winston-elasticsearch');

const app = express();
const port = process.env.PORT || 3000;

// Configuration Winston
const esTransportOpts = {
  level: 'info',
  clientOpts: {
    node: process.env.ELASTICSEARCH_URL || 'http://elasticsearch-master:9200'
  },
  index: 'application-logs'
};

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({stack: true}),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'ecommerce-api',
    version: process.env.APP_VERSION || '1.0.0',
    environment: process.env.NODE_ENV || 'development'
  },
  transports: [
    // Console transport
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    // File transport
    new winston.transports.File({
      filename: '/var/log/app/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: '/var/log/app/combined.log'
    }),
    // Elasticsearch transport
    new ElasticsearchTransport(esTransportOpts)
  ]
});

// Request logging middleware
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    const logData = {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: duration,
      userAgent: req.get('User-Agent'),
      ip: req.ip,
      timestamp: new Date().toISOString()
    };

    if (res.statusCode >= 400) {
      logger.error('HTTP Error', logData);
    } else {
      logger.info('HTTP Request', logData);
    }
  });

  next();
});

// Routes
app.get('/', (req, res) => {
  logger.info('Home page accessed', {userId: req.query.userId});
  res.json({
    message: 'E-commerce API with structured logging',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/products', (req, res) => {
  const products = [
    {id: 1, name: 'Laptop', price: 999.99},
    {id: 2, name: 'Mouse', price: 29.99},
    {id: 3, name: 'Keyboard', price: 79.99}
  ];

  logger.info('Products retrieved', {
    count: products.length,
    userId: req.query.userId
  });

  res.json(products);
});

app.post('/api/orders', express.json(), (req, res) => {
  const order = {
    id: Date.now(),
    items: req.body.items,
    total: req.body.total,
    userId: req.body.userId,
    timestamp: new Date().toISOString()
  };

  // Simulation d'erreurs aléatoires
  if (Math.random() < 0.1) {
    const error = new Error('Payment processing failed');
    logger.error('Order creation failed', {
      orderId: order.id,
      userId: order.userId,
      error: error.message,
      stack: error.stack
    });
    return res.status(500).json({error: 'Payment processing failed'});
  }

  logger.info('Order created successfully', {
    orderId: order.id,
    userId: order.userId,
    total: order.total,
    itemCount: order.items.length
  });

  res.status(201).json(order);
});

app.get('/api/logs/test', (req, res) => {
  // Générer différents types de logs pour les tests
  logger.debug('Debug message', {debugInfo: 'test data'});
  logger.info('Info message', {infoData: 'test info'});
  logger.warn('Warning message', {warningData: 'test warning'});

  if (req.query.error) {
    logger.error('Intentional error for testing', {
      errorType: 'test',
      userTriggered: true
    });
  }

  res.json({message: 'Test logs generated'});
});

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Error handling
app.use((error, req, res, next) => {
  logger.error('Unhandled error', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method
  });

  res.status(500).json({error: 'Internal server error'});
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('uncaughtException', (error) => {
  logger.error('Uncaught exception', {
    error: error.message,
    stack: error.stack
  });
  process.exit(1);
});

app.listen(port, () => {
  logger.info('Server started', {port: port});
});
```

### Étape 5.2 : Package.json avec dépendances

Créez `app/package.json` :

```json
{
  "name": "logger-app",
  "version": "1.0.0",
  "description": "Application with structured logging",
  "main": "logger-app.js",
  "scripts": {
    "start": "node logger-app.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "winston": "^3.8.2",
    "winston-elasticsearch": "^0.17.4"
  }
}
```

### Étape 5.3 : Déploiement de l'application

Créez `k8s/logger-app.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logger-app
  namespace: default
  labels:
    app: logger-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: logger-app
  template:
    metadata:
      labels:
        app: logger-app
      annotations:
        fluentd.io/exclude: 'false'
    spec:
      containers:
        - name: app
          image: logger-app:latest
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: 'production'
            - name: ELASTICSEARCH_URL
              value: 'http://elasticsearch-master.logging.svc.cluster.local:9200'
          volumeMounts:
            - name: app-logs
              mountPath: /var/log/app
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
      volumes:
        - name: app-logs
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: logger-app
  namespace: default
spec:
  selector:
    app: logger-app
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

## Exercice 6 : Dashboards et visualisations Kibana

### Étape 6.1 : Index patterns

Connectez-vous à Kibana et créez les index patterns :

```bash
# Port-forward pour accéder à Kibana
kubectl port-forward -n logging svc/kibana-kibana 5601:5601
```

1. Accédez à http://localhost:5601
2. Allez dans **Stack Management** > **Index Patterns**
3. Créez les patterns :
   - `application-*` pour les logs d'applications
   - `kubernetes-*` pour les logs Kubernetes
   - `system-*` pour les logs système

### Étape 6.2 : Dashboard infrastructure

Créez un dashboard "Infrastructure Logs" avec :

1. **Log Volume par Namespace** (Line chart)

```json
{
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "5m"
      },
      "aggs": {
        "3": {
          "terms": {
            "field": "namespace.keyword",
            "size": 10
          }
        }
      }
    }
  }
}
```

2. **Top Pods avec Erreurs** (Data table)

```json
{
  "aggs": {
    "2": {
      "terms": {
        "field": "pod_name.keyword",
        "size": 10
      },
      "aggs": {
        "3": {
          "filter": {
            "match": {
              "log_level": "error"
            }
          }
        }
      }
    }
  }
}
```

3. **Map des Erreurs par Géolocalisation** (Maps)

```json
{
  "aggs": {
    "2": {
      "geohash_grid": {
        "field": "geoip.location",
        "precision": 3
      },
      "aggs": {
        "3": {
          "filter": {
            "range": {
              "response": {
                "gte": 400
              }
            }
          }
        }
      }
    }
  }
}
```

### Étape 6.3 : Dashboard application

Créez un dashboard "Application Monitoring" avec :

1. **Erreurs d'application** (Metric)
2. **Timeline des requêtes HTTP** (Area chart)
3. **Top des erreurs** (Tag cloud)
4. **Géolocalisation des utilisateurs** (Maps)

## Exercice 7 : Alerting avec Watcher

### Étape 7.1 : Configuration Watcher

Créez `logging/watcher-config.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: watcher-config
  namespace: logging
data:
  high-error-rate.json: |
    {
      "trigger": {
        "schedule": {
          "interval": "1m"
        }
      },
      "input": {
        "search": {
          "request": {
            "search_type": "query_then_fetch",
            "indices": ["application-*"],
            "body": {
              "query": {
                "bool": {
                  "must": [
                    {
                      "range": {
                        "@timestamp": {
                          "gte": "now-5m"
                        }
                      }
                    },
                    {
                      "match": {
                        "log_level": "error"
                      }
                    }
                  ]
                }
              },
              "aggs": {
                "error_count": {
                  "cardinality": {
                    "field": "message.keyword"
                  }
                }
              }
            }
          }
        }
      },
      "condition": {
        "compare": {
          "ctx.payload.aggregations.error_count.value": {
            "gt": 10
          }
        }
      },
      "actions": {
        "send_slack": {
          "webhook": {
            "scheme": "https",
            "host": "hooks.slack.com",
            "port": 443,
            "method": "post",
            "path": "/services/YOUR/SLACK/WEBHOOK",
            "params": {},
            "headers": {
              "Content-Type": "application/json"
            },
            "body": "{\"text\":\"High error rate detected: {{ctx.payload.aggregations.error_count.value}} errors in the last 5 minutes\"}"
          }
        }
      }
    }

  pod-crash-loop.json: |
    {
      "trigger": {
        "schedule": {
          "interval": "2m"
        }
      },
      "input": {
        "search": {
          "request": {
            "indices": ["kubernetes-*"],
            "body": {
              "query": {
                "bool": {
                  "must": [
                    {
                      "range": {
                        "@timestamp": {
                          "gte": "now-10m"
                        }
                      }
                    },
                    {
                      "match": {
                        "message": "CrashLoopBackOff"
                      }
                    }
                  ]
                }
              },
              "aggs": {
                "pods": {
                  "terms": {
                    "field": "pod_name.keyword",
                    "size": 10
                  }
                }
              }
            }
          }
        }
      },
      "condition": {
        "compare": {
          "ctx.payload.hits.total": {
            "gt": 0
          }
        }
      },
      "actions": {
        "send_email": {
          "email": {
            "to": ["devops@company.com"],
            "subject": "Pod CrashLoopBackOff Detected",
            "body": "The following pods are in CrashLoopBackOff state: {{#ctx.payload.aggregations.pods.buckets}}{{key}} {{/ctx.payload.aggregations.pods.buckets}}"
          }
        }
      }
    }
```

### Étape 7.2 : Script de création des watchers

Créez `scripts/create-watchers.sh` :

```bash
#!/bin/bash

ELASTICSEARCH_URL="http://localhost:9200"

echo "Creating Elasticsearch watchers..."

# High error rate watcher
curl -X PUT "$ELASTICSEARCH_URL/_watcher/watch/high-error-rate" \
  -H "Content-Type: application/json" \
  -d @logging/watcher-config/high-error-rate.json

# Pod crash loop watcher
curl -X PUT "$ELASTICSEARCH_URL/_watcher/watch/pod-crash-loop" \
  -H "Content-Type: application/json" \
  -d @logging/watcher-config/pod-crash-loop.json

echo "Watchers created successfully!"
```

## Exercice 8 : Gestion des logs et rétention

### Étape 8.1 : Index Lifecycle Management (ILM)

Créez `logging/ilm-policy.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ilm-policy
  namespace: logging
data:
  logs-policy.json: |
    {
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
              },
              "forcemerge": {
                "max_num_segments": 1
              }
            }
          },
          "cold": {
            "min_age": "30d",
            "actions": {
              "allocate": {
                "number_of_replicas": 0
              }
            }
          },
          "delete": {
            "min_age": "90d",
            "actions": {
              "delete": {}
            }
          }
        }
      }
    }
```

### Étape 8.2 : Index templates avec ILM

Créez `logging/index-template.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: index-template
  namespace: logging
data:
  logs-template.json: |
    {
      "index_patterns": ["logs-*"],
      "template": {
        "settings": {
          "number_of_shards": 1,
          "number_of_replicas": 1,
          "index.lifecycle.name": "logs-policy",
          "index.lifecycle.rollover_alias": "logs"
        },
        "mappings": {
          "properties": {
            "@timestamp": {
              "type": "date"
            },
            "log_level": {
              "type": "keyword"
            },
            "message": {
              "type": "text",
              "analyzer": "standard"
            },
            "application": {
              "type": "keyword"
            },
            "namespace": {
              "type": "keyword"
            },
            "pod_name": {
              "type": "keyword"
            }
          }
        }
      }
    }
```

## Exercice 9 : Monitoring de la stack ELK

### Étape 9.1 : Métriques Elasticsearch

Configurez un monitoring avec Prometheus pour Elasticsearch :

```yaml
# elasticsearch-exporter.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elasticsearch-exporter
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch-exporter
  template:
    metadata:
      labels:
        app: elasticsearch-exporter
    spec:
      containers:
        - name: elasticsearch-exporter
          image: prometheuscommunity/elasticsearch-exporter:latest
          ports:
            - containerPort: 9114
          env:
            - name: ES_URI
              value: 'http://elasticsearch-master:9200'
          args:
            - --es.uri=$(ES_URI)
            - --es.all
            - --es.indices
            - --es.timeout=30s
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-exporter
  namespace: logging
  labels:
    app: elasticsearch-exporter
spec:
  selector:
    app: elasticsearch-exporter
  ports:
    - port: 9114
      name: metrics
```

### Étape 9.2 : ServiceMonitor pour Prometheus

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: elasticsearch-metrics
  namespace: logging
spec:
  selector:
    matchLabels:
      app: elasticsearch-exporter
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

## Exercice 10 : Cas pratique complet

### Objectif

Déployez une stack de logging complète qui :

1. **Collecte** tous les logs d'infrastructure et d'applications
2. **Parse et structure** les logs selon leur type
3. **Stocke** les logs avec une stratégie de rétention
4. **Alerte** sur les anomalies et erreurs critiques
5. **Visualise** les données dans des dashboards utiles

### Tests à effectuer

1. **Génération de logs** d'erreur dans l'application
2. **Vérification** de la collecte dans Elasticsearch
3. **Création** de visualisations dans Kibana
4. **Test** des alertes Watcher
5. **Validation** de la rétention ILM

## Questions de validation

1. Quelle est la différence entre Logstash et Filebeat ?
2. Comment optimiser les performances d'Elasticsearch pour les logs ?
3. Expliquez le concept d'Index Lifecycle Management
4. Comment sécuriser une stack ELK en production ?
5. Quelles sont les bonnes pratiques pour les logs structurés ?

## Livrables attendus

1. **Stack ELK** complète déployée
2. **Configuration Filebeat** pour collecte automatique
3. **Logstash pipelines** pour parsing des logs
4. **Index patterns** et dashboards Kibana
5. **Alertes Watcher** configurées
6. **Politique ILM** pour gestion du cycle de vie
7. **Application** avec logs structurés
8. **Monitoring** de la stack ELK
9. **Documentation** complète d'utilisation

## Critères d'évaluation

- **Installation** : Stack complète fonctionnelle
- **Collecte** : Logs d'infrastructure et applications collectés
- **Parsing** : Logs correctement structurés
- **Visualisation** : Dashboards utiles et informatifs
- **Alerting** : Alertes pertinentes configurées
- **Performance** : Configuration optimisée
- **Documentation** : Guide d'utilisation complet

## Ressources utiles

- [Elastic Stack Documentation](https://www.elastic.co/guide/index.html)
- [Filebeat Configuration](https://www.elastic.co/guide/en/beats/filebeat/current/configuring-howto-filebeat.html)
- [Logstash Configuration](https://www.elastic.co/guide/en/logstash/current/configuration.html)
- [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/index.html)

---

**Durée estimée : 8-9 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
