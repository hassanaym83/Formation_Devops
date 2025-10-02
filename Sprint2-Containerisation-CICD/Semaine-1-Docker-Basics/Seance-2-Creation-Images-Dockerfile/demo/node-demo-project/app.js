const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(express.static('public'));

// Base de données en mémoire pour les participants
let participants = [
  {
    id: 1,
    nom: 'ESSADIK',
    prenom: 'Hassan',
    dateInscription: new Date('2025-09-15')
  },
  {
    id: 2,
    nom: 'MARTIN',
    prenom: 'Sophie',
    dateInscription: new Date('2025-09-18')
  },
  {
    id: 3,
    nom: 'BENALI',
    prenom: 'Ahmed',
    dateInscription: new Date('2025-09-20')
  }
];

let nextId = 4;

// Routes

// 1. Endpoint GET : Informations sur la formation DevOps
app.get('/', (req, res) => {
  const formationInfo = {
    titre: 'Formation DevOps - Simplon Maghreb',
    formateur: 'Hassan ESSADIK',
    duree: '6 mois',
    sprints: [
      {
        sprint: 'Sprint 0',
        titre: 'Introduction DevOps',
        duree: '2 semaines',
        objectifs: [
          'Culture DevOps et méthodologies agiles',
          'Installation environnement de développement',
          'Panorama des outils DevOps',
          'Introduction aux tests et qualité'
        ]
      },
      {
        sprint: 'Sprint 1',
        titre: 'Fondations DevOps',
        duree: '3 semaines',
        objectifs: [
          'Systèmes Linux et automatisation',
          'Scripting Bash et Python pour DevOps',
          'Git et workflows avancés'
        ]
      },
      {
        sprint: 'Sprint 2',
        titre: 'Containerisation et CI/CD',
        duree: '4 semaines',
        objectifs: [
          'Docker Basics et architecture',
          "Création d'images avec Dockerfile",
          'Docker Compose et orchestration',
          'GitLab CI/CD et production'
        ]
      },
      {
        sprint: 'Sprint 3',
        titre: 'Orchestration Kubernetes',
        duree: '4 semaines',
        objectifs: [
          'Kubernetes fundamentals',
          "Déploiement d'applications",
          'Kubernetes en production'
        ]
      },
      {
        sprint: 'Sprint 4',
        titre: 'Cloud et Infrastructure',
        duree: '4 semaines',
        objectifs: [
          'Azure Fundamentals',
          'Infrastructure as Code',
          'Azure DevOps et intégration'
        ]
      },
      {
        sprint: 'Sprint 5',
        titre: 'Observabilité et SRE',
        duree: '3 semaines',
        objectifs: [
          'Monitoring et alerting',
          'Logging et tracing',
          'SRE practices et incident management'
        ]
      }
    ],
    technologies: [
      'Docker & Kubernetes',
      'GitLab CI/CD',
      'Azure Cloud Platform',
      'Terraform & Ansible',
      'Prometheus & Grafana',
      'Linux & Bash/Python scripting'
    ],
    participants: {
      total: participants.length,
      inscrits: participants
    },
    contact: {
      formateur: 'Hassan ESSADIK',
      email: 'hassan.essadik@simplon.co',
      organisation: 'Simplon Maghreb'
    }
  };

  res.send(`
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Formation DevOps - Simplon Maghreb (1 ère édition)</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                    min-height: 100vh;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                    color: white;
                    padding: 40px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }
                .header p {
                    margin: 10px 0 0 0;
                    font-size: 1.2em;
                    opacity: 0.9;
                }
                .content {
                    padding: 40px;
                }
                .info-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 30px;
                    margin-bottom: 40px;
                }
                .info-card {
                    background: #f8f9fa;
                    padding: 25px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                }
                .info-card h3 {
                    margin: 0 0 15px 0;
                    color: #2c3e50;
                    font-size: 1.3em;
                }
                .sprint-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }
                .sprint-card {
                    background: white;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    padding: 20px;
                    transition: transform 0.2s, border-color 0.2s;
                }
                .sprint-card:hover {
                    transform: translateY(-5px);
                    border-color: #667eea;
                    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.1);
                }
                .sprint-card h4 {
                    margin: 0 0 10px 0;
                    color: #667eea;
                    font-size: 1.2em;
                }
                .sprint-card .duration {
                    background: #667eea;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    display: inline-block;
                    margin-bottom: 15px;
                }
                .objectives {
                    list-style: none;
                    padding: 0;
                }
                .objectives li {
                    padding: 5px 0;
                    padding-left: 20px;
                    position: relative;
                }
                .objectives li:before {
                    content: "✓";
                    position: absolute;
                    left: 0;
                    color: #28a745;
                    font-weight: bold;
                }
                .technologies {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-top: 15px;
                }
                .tech-tag {
                    background: #e9ecef;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    color: #495057;
                }
                .participants-section {
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 8px;
                    margin: 30px 0;
                }
                .participants-count {
                    font-size: 2em;
                    font-weight: bold;
                    color: #667eea;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .inscription-form {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 8px;
                    margin: 30px 0;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: 500;
                }
                .form-group input {
                    width: 100%;
                    padding: 12px;
                    border: none;
                    border-radius: 6px;
                    font-size: 1em;
                    box-sizing: border-box;
                }
                .btn-submit {
                    background: #28a745;
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 6px;
                    font-size: 1.1em;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                .btn-submit:hover {
                    background: #218838;
                }
                .btn-participants {
                    display: inline-block;
                    background: #17a2b8;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-size: 1.1em;
                    margin: 20px 0;
                    transition: background-color 0.2s;
                }
                .btn-participants:hover {
                    background: #138496;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Formation DevOps</h1>
                    <p>Simplon Maghreb - Formateur: ${
                      formationInfo.formateur
                    }</p>
                </div>
                
                <div class="content">
                    <div class="info-grid">
                        <div class="info-card">
                            <h3>Durée de formation</h3>
                            <p><strong>${
                              formationInfo.duree
                            }</strong> intensifs</p>
                            <p>Formation complète couvrant tous les aspects du DevOps moderne</p>
                        </div>
                        
                        <div class="info-card">
                            <h3>Participants inscrits</h3>
                            <div class="participants-count">${
                              formationInfo.participants.total
                            }</div>
                            <a href="/participants" class="btn-participants">Voir la liste complète</a>
                        </div>
                    </div>

                    <h2>Programme de formation (${
                      formationInfo.sprints.length
                    } Sprints)</h2>
                    <div class="sprint-grid">
                        ${formationInfo.sprints
                          .map(
                            (sprint) => `
                            <div class="sprint-card">
                                <h4>${sprint.sprint}: ${sprint.titre}</h4>
                                <span class="duration">${sprint.duree}</span>
                                <ul class="objectives">
                                    ${sprint.objectifs
                                      .map((obj) => `<li>${obj}</li>`)
                                      .join('')}
                                </ul>
                            </div>
                        `
                          )
                          .join('')}
                    </div>

                    <div class="info-card">
                        <h3>Technologies et outils couverts</h3>
                        <div class="technologies">
                            ${formationInfo.technologies
                              .map(
                                (tech) =>
                                  `<span class="tech-tag">${tech}</span>`
                              )
                              .join('')}
                        </div>
                    </div>

                    <div class="inscription-form">
                        <h2>Inscription à la formation</h2>
                        <p>Rejoignez notre programme de formation DevOps et devenez un expert en automatisation et déploiement !</p>
                        
                        <form action="/inscription" method="POST">
                            <div class="form-group">
                                <label for="nom">Nom :</label>
                                <input type="text" id="nom" name="nom" required placeholder="Votre nom de famille">
                            </div>
                            
                            <div class="form-group">
                                <label for="prenom">Prénom :</label>
                                <input type="text" id="prenom" name="prenom" required placeholder="Votre prénom">
                            </div>
                            
                            <button type="submit" class="btn-submit">S'inscrire à la formation</button>
                        </form>
                    </div>

                    <div class="info-card">
                        <h3>Contact</h3>
                        <p><strong>Formateur:</strong> ${
                          formationInfo.contact.formateur
                        }</p>
                        <p><strong>Email:</strong> ${
                          formationInfo.contact.email
                        }</p>
                        <p><strong>Organisation:</strong> ${
                          formationInfo.contact.organisation
                        }</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
    `);
});

// 2. Endpoint POST : Inscription à la formation
app.post('/inscription', (req, res) => {
  const {nom, prenom} = req.body;

  // Validation des données
  if (!nom || !prenom) {
    return res.status(400).send(`
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Erreur d'inscription</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; background: #f8f9fa; }
                    .error { background: #f8d7da; color: #721c24; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }
                    .btn { display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 15px; }
                </style>
            </head>
            <body>
                <div class="error">
                    <h2>Erreur d'inscription</h2>
                    <p>Veuillez remplir tous les champs obligatoires (nom et prénom).</p>
                    <a href="/" class="btn">Retour au formulaire</a>
                </div>
            </body>
            </html>
        `);
  }

  // Vérifier si la personne n'est pas déjà inscrite
  const existingParticipant = participants.find(
    (p) =>
      p.nom.toLowerCase() === nom.toLowerCase() &&
      p.prenom.toLowerCase() === prenom.toLowerCase()
  );

  if (existingParticipant) {
    return res.send(`
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Inscription existante</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; background: #f8f9fa; }
                    .warning { background: #fff3cd; color: #856404; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; text-align: center; }
                    .btn { display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 15px; }
                </style>
            </head>
            <body>
                <div class="warning">
                    <h2>Inscription déjà existante</h2>
                    <p><strong>${prenom} ${nom}</strong> est déjà inscrit(e) à la formation DevOps.</p>
                    <p>Date d'inscription : ${existingParticipant.dateInscription.toLocaleDateString(
                      'fr-FR'
                    )}</p>
                    <a href="/participants" class="btn">Voir tous les participants</a>
                    <a href="/" class="btn">Retour à l'accueil</a>
                </div>
            </body>
            </html>
        `);
  }

  // Ajouter le nouveau participant
  const nouveauParticipant = {
    id: nextId++,
    nom: nom.toUpperCase(),
    prenom: prenom.charAt(0).toUpperCase() + prenom.slice(1).toLowerCase(),
    dateInscription: new Date()
  };

  participants.push(nouveauParticipant);

  // Redirection avec message de succès
  res.redirect(
    '/participants?nouveau=' +
      encodeURIComponent(
        `${nouveauParticipant.prenom} ${nouveauParticipant.nom}`
      )
  );
});

// 3. Page des participants (après inscription)
app.get('/participants', (req, res) => {
  const nouveauParticipant = req.query.nouveau;

  res.send(`
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Participants - Formation DevOps</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 2.2em;
                    font-weight: 300;
                }
                .content {
                    padding: 40px;
                }
                .success-message {
                    background: #d4edda;
                    color: #155724;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    border-left: 4px solid #28a745;
                }
                .stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .stat-card {
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    border-left: 4px solid #667eea;
                }
                .stat-number {
                    font-size: 2.5em;
                    font-weight: bold;
                    color: #667eea;
                    margin: 0;
                }
                .stat-label {
                    color: #6c757d;
                    margin: 5px 0 0 0;
                }
                .participants-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }
                .participant-card {
                    background: white;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    padding: 20px;
                    transition: transform 0.2s, border-color 0.2s;
                    text-align: center;
                }
                .participant-card:hover {
                    transform: translateY(-3px);
                    border-color: #667eea;
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
                }
                .participant-card.nouveau {
                    border-color: #28a745;
                    background: #f8fff9;
                }
                .participant-name {
                    font-size: 1.3em;
                    font-weight: 600;
                    color: #2c3e50;
                    margin: 0 0 10px 0;
                }
                .participant-date {
                    color: #6c757d;
                    font-size: 0.9em;
                }
                .participant-id {
                    background: #e9ecef;
                    color: #495057;
                    padding: 4px 8px;
                    border-radius: 20px;
                    font-size: 0.8em;
                    display: inline-block;
                    margin-top: 10px;
                }
                .nouveau-badge {
                    background: #28a745;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8em;
                    display: inline-block;
                    margin-top: 10px;
                }
                .actions {
                    margin: 30px 0;
                    text-align: center;
                }
                .btn {
                    display: inline-block;
                    padding: 12px 25px;
                    margin: 0 10px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-size: 1em;
                    transition: background-color 0.2s;
                }
                .btn-primary {
                    background: #667eea;
                    color: white;
                }
                .btn-primary:hover {
                    background: #5a67d8;
                }
                .btn-secondary {
                    background: #6c757d;
                    color: white;
                }
                .btn-secondary:hover {
                    background: #5a6268;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Participants Formation DevOps</h1>
                    <p>Simplon Maghreb - Liste des inscrits</p>
                </div>
                
                <div class="content">
                    ${
                      nouveauParticipant
                        ? `
                        <div class="success-message">
                            <h3>Inscription réussie !</h3>
                            <p><strong>${nouveauParticipant}</strong> a été inscrit(e) avec succès à la formation DevOps.</p>
                            <p>Bienvenue dans notre programme de formation !</p>
                        </div>
                    `
                        : ''
                    }

                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-number">${
                              participants.length
                            }</div>
                            <div class="stat-label">Participants inscrits</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">6</div>
                            <div class="stat-label">Mois de formation</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">6</div>
                            <div class="stat-label">Sprints au programme</div>
                        </div>
                    </div>

                    <h2>Liste des participants (${participants.length})</h2>
                    <div class="participants-grid">
                        ${participants
                          .map(
                            (participant) => `
                            <div class="participant-card ${
                              nouveauParticipant &&
                              nouveauParticipant.includes(participant.nom)
                                ? 'nouveau'
                                : ''
                            }">
                                <div class="participant-name">${
                                  participant.prenom
                                } ${participant.nom}</div>
                                <div class="participant-date">Inscrit le ${participant.dateInscription.toLocaleDateString(
                                  'fr-FR'
                                )}</div>
                                <div class="participant-id">ID: ${
                                  participant.id
                                }</div>
                                ${
                                  nouveauParticipant &&
                                  nouveauParticipant.includes(participant.nom)
                                    ? '<div class="nouveau-badge">NOUVEAU</div>'
                                    : ''
                                }
                            </div>
                        `
                          )
                          .join('')}
                    </div>

                    <div class="actions">
                        <a href="/" class="btn btn-primary">Retour à l'accueil</a>
                        <a href="/?scroll=inscription" class="btn btn-secondary">Nouvelle inscription</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
    `);
});

// 4. API endpoint pour obtenir les données JSON
app.get('/api/participants', (req, res) => {
  res.json({
    total: participants.length,
    participants: participants
  });
});

app.get('/api/formation', (req, res) => {
  res.json({
    titre: 'Formation DevOps - Simplon Maghreb',
    formateur: 'Hassan ESSADIK',
    duree: '6 mois',
    participants_inscrits: participants.length,
    technologies: [
      'Docker & Kubernetes',
      'GitLab CI/CD',
      'Azure Cloud Platform',
      'Terraform & Ansible',
      'Prometheus & Grafana',
      'Linux & Bash/Python scripting'
    ]
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    version: '1.0.0'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).send(`
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Page non trouvée</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 50px; text-align: center; background: #f8f9fa; }
                .error-404 { max-width: 600px; margin: 0 auto; }
                h1 { color: #dc3545; font-size: 4em; margin: 0; }
                p { color: #6c757d; font-size: 1.2em; }
                .btn { display: inline-block; background: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="error-404">
                <h1>404</h1>
                <p>Page non trouvée</p>
                <p>La page que vous recherchez n'existe pas.</p>
                <a href="/" class="btn">Retour à l'accueil</a>
            </div>
        </body>
        </html>
    `);
});

// Démarrage du serveur
app.listen(PORT, '0.0.0.0', () => {
  console.log(`=================================`);
  console.log(`Formation DevOps App`);
  console.log(`Serveur démarré sur le port ${PORT}`);
  console.log(`Accès: http://localhost:${PORT}`);
  console.log(`Participants inscrits: ${participants.length}`);
  console.log(`=================================`);
});
