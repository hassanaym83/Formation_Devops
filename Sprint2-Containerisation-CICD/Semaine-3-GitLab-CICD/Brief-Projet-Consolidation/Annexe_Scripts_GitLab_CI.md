# Annexe - Scripts GitLab CI/CD

Ce fichier contient tous les scripts de configuration GitLab CI/CD nécessaires pour le projet Coworking Space.

## Table des matières

1. [Configuration GitLab CI pour le packaging .deb](#1-configuration-gitlab-ci-pour-le-packaging-deb)
2. [Pipeline de déploiement production](#2-pipeline-de-déploiement-production)
3. [Playbook Ansible pour déploiement](#3-playbook-ansible-pour-déploiement)
4. [Scripts système et configuration](#4-scripts-système-et-configuration)

---

## 1. Configuration GitLab CI pour le packaging .deb

### Fichier `.gitlab-ci.yml` - Stage packaging

```yaml
# .gitlab-ci.yml - Stage packaging
package:deb:
  stage: package
  image: ubuntu:22.04
  before_script:
    - apt-get update && apt-get install -y dpkg-dev fakeroot
  script:
    - mkdir -p build/coworking-space-app

    # Copie des fichiers dans la structure .deb
    - cp -r DEBIAN/ build/coworking-space-app/
    - mkdir -p build/coworking-space-app/usr/share/coworking-space/
    - cp -r dist/ build/coworking-space-app/usr/share/coworking-space/app/
    - cp -r public/ build/coworking-space-app/usr/share/coworking-space/web/
    - cp -r prisma/migrations/ build/coworking-space-app/usr/share/coworking-space/

    # Création du paquet .deb
    - dpkg-deb --build build/coworking-space-app
    - mv build/coworking-space-app.deb coworking-space-app_${CI_COMMIT_TAG:-$CI_COMMIT_SHORT_SHA}_amd64.deb

  artifacts:
    paths:
      - '*.deb'
    expire_in: 30 days
  only:
    - main
    - tags

# Upload vers Nexus Repository
upload:nexus:
  stage: deploy
  image: curlimages/curl:latest
  script:
    - |
      curl -u $NEXUS_USER:$NEXUS_PASSWORD \
        --upload-file coworking-space-app_*.deb \
        $NEXUS_URL/repository/debian-packages/pool/
  dependencies:
    - package:deb
  only:
    - main
    - tags
```

---

## 2. Pipeline de déploiement production

### Fichier `.gitlab-ci.yml` - Pipeline de mise à jour automatique

```yaml
# Pipeline de mise à jour automatique
deploy:production:
  stage: deploy
  image: ubuntu:22.04
  before_script:
    - apt-get update && apt-get install -y ansible ssh-client
  script:
    # Téléchargement du paquet depuis Nexus
    - wget $NEXUS_URL/repository/debian-packages/pool/coworking-space-app_${CI_COMMIT_TAG}_amd64.deb

    # Déploiement via Ansible
    - ansible-playbook -i inventory/production deploy-deb.yml
      --extra-vars "deb_file=coworking-space-app_${CI_COMMIT_TAG}_amd64.deb"
  environment:
    name: production
    url: https://coworking.production.domain.com
  only:
    - tags
  when: manual
```

---

## 3. Playbook Ansible pour déploiement

### Fichier `deploy-deb.yml`

```yaml
---
- name: Déployer l'application Coworking Space
  hosts: production_servers
  become: yes
  tasks:
    - name: Copier le paquet .deb
      copy:
        src: '{{ deb_file }}'
        dest: '/tmp/{{ deb_file }}'

    - name: Installer/Mettre à jour le paquet
      apt:
        deb: '/tmp/{{ deb_file }}'
        state: present
      notify: restart coworking-space

    - name: Exécuter les migrations de base de données
      command: /usr/share/coworking-space/app/node_modules/.bin/prisma migrate deploy
      become_user: coworking
      environment:
        DATABASE_URL: '{{ database_url }}'

    - name: Vérifier que le service fonctionne
      systemd:
        name: coworking-space
        state: started
        enabled: yes

  handlers:
    - name: restart coworking-space
      systemd:
        name: coworking-space
        state: restarted
```

---

## 4. Scripts système et configuration

### Script postinst (DEBIAN/postinst)

```bash
#!/bin/bash
# Post-installation du paquet coworking-space-app

# Création de l'utilisateur système
if ! getent passwd coworking >/dev/null; then
    useradd --system --home /usr/share/coworking-space --shell /bin/false coworking
fi

# Configuration des permissions
chown -R coworking:coworking /usr/share/coworking-space
chmod +x /usr/share/coworking-space/app/server.js

# Installation des dépendances Node.js
cd /usr/share/coworking-space/app && npm ci --production

# Activation et démarrage du service
systemctl daemon-reload
systemctl enable coworking-space.service
systemctl start coworking-space.service

echo "✅ Coworking Space App installée avec succès"
echo "📋 Configuration: /etc/coworking-space/"
echo "🔧 Logs: journalctl -u coworking-space.service"
```

### Service systemd (coworking-space.service)

```ini
[Unit]
Description=Coworking Space Management Application
After=network.target postgresql.service redis.service
Requires=postgresql.service redis.service

[Service]
Type=simple
User=coworking
Group=coworking
WorkingDirectory=/usr/share/coworking-space/app
Environment=NODE_ENV=production
Environment=CONFIG_FILE=/etc/coworking-space/app.conf
ExecStart=/usr/bin/node server.js
ExecReload=/bin/kill -USR1 $MAINPID
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Fichier DEBIAN/control

```bash
Package: coworking-space-app
Version: 1.0.0
Section: web
Priority: optional
Architecture: amd64
Depends: nodejs (>= 18), postgresql-client (>= 12), redis-tools (>= 6)
Maintainer: DevOps Team <devops@coworking-space.com>
Description: Application de gestion d'espaces de coworking
 Application complète pour la gestion de réservations,
 facturation et administration d'espaces de coworking.
 Inclut l'API REST, l'interface web et les outils d'administration.
```

---

## Pipeline GitLab CI/CD complet recommandé

### Structure complète `.gitlab-ci.yml`

```yaml
# Configuration globale
image: node:18-alpine

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: '/certs'

services:
  - docker:20.10.16-dind
  - postgres:15-alpine
  - redis:7-alpine

stages:
  - prepare
  - test
  - security
  - build
  - package
  - deploy

# Stage 1: Préparation
cache:dependencies:
  stage: prepare
  script:
    - npm ci --cache .npm --prefer-offline
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour

# Stage 2: Tests
unit:tests:
  stage: test
  dependencies:
    - cache:dependencies
  script:
    - npm run test:unit
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

integration:tests:
  stage: test
  dependencies:
    - cache:dependencies
  services:
    - postgres:15-alpine
    - redis:7-alpine
  variables:
    DATABASE_URL: 'postgresql://postgres:postgres@postgres:5432/test'
    REDIS_URL: 'redis://redis:6379'
  script:
    - npm run test:integration

e2e:tests:
  stage: test
  dependencies:
    - cache:dependencies
  script:
    - npm run test:e2e
  artifacts:
    when: on_failure
    paths:
      - tests/e2e/screenshots/
      - tests/e2e/videos/

# Stage 3: Sécurité
lint:security:
  stage: security
  dependencies:
    - cache:dependencies
  script:
    - npm audit --audit-level=high
    - npm run lint:security

sast:
  stage: security
  image: securecodewarrior/docker-sast:latest
  script:
    - sast-scan --src ./ --type nodejs
  artifacts:
    reports:
      sast: sast-report.json

# Stage 4: Build
build:frontend:
  stage: build
  dependencies:
    - cache:dependencies
  script:
    - npm run build:frontend
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

build:backend:
  stage: build
  dependencies:
    - cache:dependencies
  script:
    - npm run build:backend
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

build:docker:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  dependencies:
    - build:frontend
    - build:backend
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest

# Stage 5: Package (Déjà défini ci-dessus)
package:deb:
  # ... (voir section 1)

upload:nexus:
  # ... (voir section 1)

# Stage 6: Deploy
deploy:staging:
  stage: deploy
  image: ubuntu:22.04
  environment:
    name: staging
    url: https://coworking.staging.domain.com
  script:
    - apt-get update && apt-get install -y ansible ssh-client
    - ansible-playbook -i inventory/staging deploy-deb.yml
      --extra-vars "deb_file=coworking-space-app_${CI_COMMIT_SHORT_SHA}_amd64.deb"
  only:
    - develop
    - main

deploy:production:
  # ... (voir section 2)

# Deploy VirtualBox pour développement local
deploy:virtualbox:
  stage: deploy
  image: ubuntu:22.04
  environment:
    name: virtualbox
    url: http://192.168.56.10:3000
  before_script:
    - apt-get update && apt-get install -y ansible virtualbox vagrant
  script:
    - vagrant up
    - ansible-playbook -i inventory/virtualbox deploy-local.yml
  when: manual
  only:
    - feature/*
    - develop
```

---

## Variables d'environnement GitLab CI

### Variables à configurer dans GitLab

```bash
# Nexus Repository
NEXUS_URL=https://nexus.domain.com
NEXUS_USER=gitlab-ci
NEXUS_PASSWORD=secure_password

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/coworking
REDIS_URL=redis://localhost:6379

# Configuration application
NODE_ENV=production
JWT_SECRET=super_secret_key
STRIPE_SECRET_KEY=sk_live_...

# Déploiement
ANSIBLE_VAULT_PASSWORD=vault_password
SSH_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----...

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
```

---

## Instructions d'utilisation

### 1. Configuration initiale

1. Copier le fichier `.gitlab-ci.yml` complet dans la racine du projet
2. Configurer les variables d'environnement dans GitLab CI/CD Settings
3. Créer les fichiers Ansible dans le dossier `ansible/`
4. Configurer les inventaires pour staging et production

### 2. Déploiement

- **Automatique** : Push sur `main` → déploie en staging
- **Manuel** : Tag version → option déploiement production
- **Développement** : Feature branch → option déploiement VirtualBox

### 3. Monitoring

- Logs application : `journalctl -u coworking-space.service`
- Métriques pipeline : GitLab CI/CD Analytics
- Performance : Intégration monitoring (Grafana/Prometheus)

---

_Ce fichier annexe centralise tous les scripts de configuration pour faciliter la maintenance et le déploiement du projet Coworking Space._
