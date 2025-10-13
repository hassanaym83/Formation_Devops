# LAB 1 - Découverte GitLab CI et premier pipeline

**Sprint 2 - Semaine 3 - Séance 1**  
**Référence** : `S2_S3_S1_lab1_premier_pipeline`  
**Durée** : 20 minutes

## Objectifs

- Comprendre la structure YAML et exécution des pipelines GitLab CI/CD
- Créer un premier pipeline fonctionnel avec stages de base
- Observer l'exécution dans l'interface GitLab

## Contexte

Application Node.js simple avec tests Jest et déploiement sur GitLab Pages.

## Pré-requis

- Accès à GitLab (gitlab.com ou instance locale)
- Projet GitLab créé
- Connaissances de base en Node.js et YAML

## Structure du projet

Votre projet doit contenir les fichiers suivants :

```
mon-projet/
├── package.json
├── src/
│   ├── index.js
│   └── calculator.js
├── tests/
│   └── calculator.test.js
├── public/
│   └── index.html
└── .gitlab-ci.yml (à créer)
```

## Fichiers fournis

### package.json

```json
{
  "name": "mon-application-ci",
  "version": "1.0.0",
  "description": "Application de démonstration GitLab CI/CD",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "jest",
    "build": "mkdir -p dist && cp -r src/* dist/ && cp public/index.html dist/"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

### src/calculator.js

```javascript
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    throw new Error('Division par zéro impossible');
  }
  return a / b;
}

module.exports = {add, subtract, multiply, divide};
```

### src/index.js

```javascript
const express = require('express');
const {add, subtract, multiply, divide} = require('./calculator');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

app.get('/api/health', (req, res) => {
  res.json({status: 'OK', message: 'Application fonctionne'});
});

app.post('/api/calculate', (req, res) => {
  const {operation, a, b} = req.body;

  try {
    let result;
    switch (operation) {
      case 'add':
        result = add(a, b);
        break;
      case 'subtract':
        result = subtract(a, b);
        break;
      case 'multiply':
        result = multiply(a, b);
        break;
      case 'divide':
        result = divide(a, b);
        break;
      default:
        return res.status(400).json({error: 'Opération non supportée'});
    }

    res.json({result});
  } catch (error) {
    res.status(400).json({error: error.message});
  }
});

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Serveur démarré sur le port ${port}`);
  });
}

module.exports = app;
```

### tests/calculator.test.js

```javascript
const {add, subtract, multiply, divide} = require('../src/calculator');

describe('Calculator', () => {
  test('addition de 2 + 3 doit donner 5', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('soustraction de 5 - 3 doit donner 2', () => {
    expect(subtract(5, 3)).toBe(2);
  });

  test('multiplication de 4 * 3 doit donner 12', () => {
    expect(multiply(4, 3)).toBe(12);
  });

  test('division de 8 / 2 doit donner 4', () => {
    expect(divide(8, 2)).toBe(4);
  });

  test('division par zéro doit lever une erreur', () => {
    expect(() => divide(5, 0)).toThrow('Division par zéro impossible');
  });
});
```

### public/index.html

```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Calculatrice CI/CD</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        max-width: 600px;
        margin: 50px auto;
        padding: 20px;
      }
      .calculator {
        background: #f5f5f5;
        padding: 20px;
        border-radius: 8px;
      }
      input,
      button {
        margin: 5px;
        padding: 10px;
      }
      .result {
        margin-top: 20px;
        padding: 10px;
        background: #e8f5e8;
        border-radius: 4px;
      }
    </style>
  </head>
  <body>
    <h1>Calculatrice CI/CD Demo</h1>
    <div class="calculator">
      <h2>Test de l'API Calculator</h2>
      <p>Cette application a été déployée automatiquement via GitLab CI/CD!</p>
      <div>
        <input type="number" id="num1" placeholder="Nombre 1" />
        <select id="operation">
          <option value="add">+</option>
          <option value="subtract">-</option>
          <option value="multiply">×</option>
          <option value="divide">÷</option>
        </select>
        <input type="number" id="num2" placeholder="Nombre 2" />
        <button onclick="calculate()">Calculer</button>
      </div>
      <div id="result" class="result" style="display: none;"></div>
    </div>

    <script>
      async function calculate() {
        const num1 = parseFloat(document.getElementById('num1').value);
        const num2 = parseFloat(document.getElementById('num2').value);
        const operation = document.getElementById('operation').value;

        try {
          const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({operation, a: num1, b: num2})
          });

          const data = await response.json();
          const resultDiv = document.getElementById('result');

          if (response.ok) {
            resultDiv.innerHTML = `Résultat: ${data.result}`;
            resultDiv.style.backgroundColor = '#e8f5e8';
          } else {
            resultDiv.innerHTML = `Erreur: ${data.error}`;
            resultDiv.style.backgroundColor = '#ffe8e8';
          }

          resultDiv.style.display = 'block';
        } catch (error) {
          console.error('Erreur:', error);
          document.getElementById('result').innerHTML =
            'Erreur de communication';
        }
      }
    </script>
  </body>
</html>
```

## Instructions

### Étape 1 : Préparation du projet

1. Créez un nouveau projet GitLab
2. Clonez le projet localement
3. Créez la structure de fichiers comme indiquée ci-dessus
4. Ajoutez et commitez tous les fichiers (sauf .gitlab-ci.yml)

### Étape 2 : Analyse de l'architecture CI/CD

Avant de créer le pipeline, répondez aux questions suivantes :

1. **Quels sont les stages logiques pour cette application ?**

   - Stage 1 : ****\*\*****\_****\*\*****
   - Stage 2 : ****\*\*****\_****\*\*****
   - Stage 3 : ****\*\*****\_****\*\*****

2. **Quelles images Docker conviennent pour ce projet ?**

   - Pour les tests : ****\*\*****\_****\*\*****
   - Pour le build : ****\*\*****\_****\*\*****

3. **Quels artifacts doivent être conservés ?**
   - ***
   - ***

### Étape 3 : Création du fichier .gitlab-ci.yml

Créez un fichier `.gitlab-ci.yml` à la racine qui implémente :

**Requirements obligatoires :**

- 3 stages minimum : `install`, `test`, `deploy`
- Job d'installation des dépendances
- Job d'exécution des tests
- Job de build de l'application
- Job de déploiement sur GitLab Pages
- Utilisation d'artifacts pour partager les fichiers entre jobs

**Structure attendue :**

```yaml
# Votre configuration ici
stages:
  -  # À compléter

variables:
  # À compléter

# Job 1: Installation
install_dependencies:
  # À compléter

# Job 2: Tests
run_tests:
  # À compléter

# Job 3: Build
build_app:
  # À compléter

# Job 4: Deploy
deploy_pages:
  # À compléter
```

### Étape 4 : Test et observation

1. Committez et pushez le fichier `.gitlab-ci.yml`
2. Observez l'exécution dans GitLab : Projet > CI/CD > Pipelines
3. Vérifiez que chaque job s'exécute correctement
4. Accédez à votre application déployée via GitLab Pages

### Étape 5 : Debugging (si nécessaire)

Si un job échoue :

1. Cliquez sur le job en échec
2. Analysez les logs d'erreur
3. Corrigez la configuration
4. Commitez et relancez

## Critères d'évaluation (8 points)

- **Pipeline fonctionnel** (3 points) : Tous les jobs s'exécutent sans erreur
- **Syntaxe YAML correcte** (2 points) : Fichier bien structuré et valide
- **Jobs logiques** (2 points) : Organisation cohérente des stages
- **Application accessible** (1 point) : GitLab Pages fonctionne

## Questions de réflexion

1. **Pourquoi séparer l'installation, les tests et le build en jobs différents ?**

2. **Quel est l'avantage d'utiliser des artifacts ?**

3. **Comment optimiser ce pipeline pour des projets plus complexes ?**

4. **Que se passe-t-il si un test échoue ?**

## Bonus (optionnel)

- Ajoutez une condition pour ne déployer que sur la branche `main`
- Configurez un job de build conditionnel selon les changements de fichiers
- Ajoutez des rapports de tests dans l'interface GitLab

---

**Durée estimée :** 20 minutes
**Fichier de rendu :** `.gitlab-ci.yml` dans votre projet GitLab
