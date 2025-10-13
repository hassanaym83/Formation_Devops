# LAB 2 - Configuration avancée jobs et artifacts

**Sprint 2 - Semaine 3 - Séance 1**  
**Référence** : `S2_S3_S1_lab2_jobs_artifacts`  
**Durée** : 25 minutes

## Objectifs

- Maîtriser l'organisation des jobs et l'optimisation des performances
- Configurer des stages complexes avec jobs parallèles
- Implémenter artifacts intelligents et cache avancé
- Générer des rapports de tests et métriques

## Contexte

Application e-commerce avec frontend React et API Node.js. Vous devez créer un pipeline optimisé qui gère les deux composants de manière efficace.

## Pré-requis

- Connaissances du LAB 1
- Compréhension des concepts de jobs, stages et artifacts
- Familiarité avec React et Node.js

## Architecture du projet

```
ecommerce-app/
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   ├── public/
│   └── tests/
├── backend/
│   ├── package.json
│   ├── src/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   └── server.js
│   └── tests/
├── docs/
├── docker-compose.yml
└── .gitlab-ci.yml (à créer)
```

## Fichiers fournis

### frontend/package.json

```json
{
  "name": "ecommerce-frontend",
  "version": "1.0.0",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test --coverage --watchAll=false",
    "lint": "eslint src/",
    "audit": "npm audit --audit-level=moderate"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "eslint": "^8.0.0",
    "@testing-library/react": "^13.0.0",
    "@testing-library/jest-dom": "^5.16.0"
  }
}
```

### backend/package.json

```json
{
  "name": "ecommerce-backend",
  "version": "1.0.0",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js",
    "test": "jest --coverage",
    "lint": "eslint src/",
    "security": "npm audit --audit-level=moderate",
    "docs": "jsdoc src/ -d docs/"
  },
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^7.5.0",
    "jsonwebtoken": "^9.0.0",
    "bcryptjs": "^2.4.3"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "supertest": "^6.3.0",
    "eslint": "^8.0.0",
    "nodemon": "^3.0.0",
    "jsdoc": "^4.0.0"
  }
}
```

### frontend/src/App.js

```javascript
import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get('/api/products');
      setProducts(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Erreur lors du chargement des produits:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className='loading'>Chargement des produits...</div>;
  }

  return (
    <div className='App'>
      <header className='App-header'>
        <h1>E-Commerce Demo</h1>
        <p>Application déployée avec GitLab CI/CD</p>
      </header>
      <main>
        <div className='products-grid'>
          {products.map((product) => (
            <div key={product.id} className='product-card'>
              <h3>{product.name}</h3>
              <p>{product.description}</p>
              <span className='price'>{product.price}€</span>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
```

### backend/src/server.js

```javascript
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());
app.use(express.static(path.join(__dirname, '../../frontend/build')));

// Routes API
app.get('/api/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

app.get('/api/products', (req, res) => {
  const products = [
    {
      id: 1,
      name: 'Ordinateur Portable',
      description: 'Laptop haute performance',
      price: 899
    },
    {
      id: 2,
      name: 'Smartphone',
      description: 'Téléphone dernière génération',
      price: 599
    },
    {
      id: 3,
      name: 'Tablette',
      description: 'Tablette pour le travail et loisirs',
      price: 399
    }
  ];
  res.json(products);
});

// Serve React app pour toutes les autres routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../../frontend/build/index.html'));
});

const server = app.listen(PORT, () => {
  console.log(`Serveur démarré sur le port ${PORT}`);
});

module.exports = {app, server};
```

### Tests fournis

**frontend/src/App.test.js**

```javascript
import {render, screen} from '@testing-library/react';
import App from './App';

test('renders e-commerce title', () => {
  render(<App />);
  const titleElement = screen.getByText(/E-Commerce Demo/i);
  expect(titleElement).toBeInTheDocument();
});

test('shows loading message initially', () => {
  render(<App />);
  const loadingElement = screen.getByText(/Chargement des produits/i);
  expect(loadingElement).toBeInTheDocument();
});
```

**backend/tests/server.test.js**

```javascript
const request = require('supertest');
const {app} = require('../src/server');

describe('API Endpoints', () => {
  test('GET /api/health should return status OK', async () => {
    const response = await request(app).get('/api/health').expect(200);

    expect(response.body.status).toBe('OK');
    expect(response.body.version).toBe('1.0.0');
  });

  test('GET /api/products should return products array', async () => {
    const response = await request(app).get('/api/products').expect(200);

    expect(Array.isArray(response.body)).toBe(true);
    expect(response.body.length).toBeGreaterThan(0);
    expect(response.body[0]).toHaveProperty('id');
    expect(response.body[0]).toHaveProperty('name');
    expect(response.body[0]).toHaveProperty('price');
  });
});
```

## Instructions

### Étape 1 : Analyse de l'architecture pipeline

Réfléchissez à l'organisation optimale pour cette application full-stack :

**Questions d'architecture :**

1. **Combien de stages logiques identifiez-vous ?**

   - Stage 1 : **\*\***\_\_\_\_**\*\***
   - Stage 2 : **\*\***\_\_\_\_**\*\***
   - Stage 3 : **\*\***\_\_\_\_**\*\***
   - Stage 4 : **\*\***\_\_\_\_**\*\***
   - Stage 5 : **\*\***\_\_\_\_**\*\***
   - Stage 6 : **\*\***\_\_\_\_**\*\***

2. **Quels jobs peuvent s'exécuter en parallèle ?**

   - Frontend : **\*\***\_\_\_\_**\*\***
   - Backend : **\*\***\_\_\_\_**\*\***

3. **Quels artifacts faut-il partager entre jobs ?**
   - ***
   - ***
   - ***

### Étape 2 : Configuration des stages

Créez un fichier `.gitlab-ci.yml` avec 6 stages :

1. **install** : Installation des dépendances frontend + backend
2. **lint** : Vérification qualité code (ESLint)
3. **test** : Tests unitaires avec rapports de couverture
4. **security** : Audit de sécurité et vulnérabilités
5. **build** : Construction frontend + backend + documentation
6. **deploy** : Déploiement et tests d'intégration

### Étape 3 : Jobs parallèles et optimisations

**Requirements obligatoires :**

- **2 jobs d'installation** en parallèle (frontend + backend)
- **2 jobs de lint** en parallèle
- **2 jobs de tests** en parallèle avec rapports JUnit
- **Cache intelligent** pour node_modules par composant
- **Artifacts stratégiques** entre stages
- **Variables d'environnement** pour optimisation
- **Conditions d'exécution** selon les changements de fichiers

### Étape 4 : Template de départ

```yaml
# Configuration GitLab CI/CD E-Commerce Full-Stack
# Architecture: Frontend React + Backend Node.js

stages:
  - install
  - lint
  - test
  - security
  - build
  - deploy

variables:
  # À compléter

cache:
  # À compléter

# ========================
# STAGE: INSTALL
# ========================

install_frontend:
  stage: install
  # À compléter

install_backend:
  stage: install
  # À compléter

# ========================
# STAGE: LINT
# ========================

lint_frontend:
  stage: lint
  # À compléter

lint_backend:
  stage: lint
  # À compléter

# ========================
# STAGE: TEST
# ========================

test_frontend:
  stage: test
  # À compléter

test_backend:
  stage: test
  # À compléter

# ========================
# STAGE: SECURITY
# ========================

security_audit:
  stage: security
  # À compléter

# ========================
# STAGE: BUILD
# ========================

build_frontend:
  stage: build
  # À compléter

build_docs:
  stage: build
  # À compléter

# ========================
# STAGE: DEPLOY
# ========================

deploy_staging:
  stage: deploy
  # À compléter

integration_tests:
  stage: deploy
  # À compléter
```

### Étape 5 : Configurations avancées

**Cache intelligent par composant :**

```yaml
cache:
  - key: frontend-$CI_COMMIT_REF_SLUG
    paths:
      - frontend/node_modules/
  - key: backend-$CI_COMMIT_REF_SLUG
    paths:
      - backend/node_modules/
```

**Artifacts avec expiration :**

- Dependencies : 1 heure
- Build artifacts : 1 semaine
- Test reports : 30 jours
- Documentation : 6 mois

**Conditions d'exécution :**

- Frontend jobs : uniquement si changements dans `frontend/`
- Backend jobs : uniquement si changements dans `backend/`
- Deploy : uniquement sur branche `main`

### Étape 6 : Métriques et rapports

Configurez les rapports GitLab pour :

- **Tests JUnit** (frontend + backend)
- **Couverture de code** (coverage)
- **Qualité du code** (ESLint reports)
- **Audit de sécurité** (npm audit)

## Critères d'évaluation (10 points)

- **Organisation logique** (3 points) : 6 stages bien structurés
- **Jobs parallèles** (2 points) : Frontend/Backend en parallèle
- **Artifacts fonctionnels** (2 points) : Partage correct entre jobs
- **Optimisations cache** (2 points) : Cache intelligent par composant
- **Rapports intégrés** (1 point) : Tests et métriques dans GitLab

## Questions de réflexion

1. **Pourquoi séparer les jobs frontend et backend ?**

2. **Comment le cache améliore-t-il les performances ?**

3. **Quel est l'intérêt des conditions d'exécution par fichiers ?**

4. **Comment organiser les artifacts pour minimiser le storage ?**

## Bonus (optionnel)

- Configurez des **review apps** pour les merge requests
- Ajoutez un job de **tests de performance** (Lighthouse)
- Implémentez des **notifications Slack** sur les échecs
- Créez un **pipeline de rollback** automatique

---

**Durée estimée :** 25 minutes
**Fichier de rendu :** `.gitlab-ci.yml` optimisé avec tous les requirements
