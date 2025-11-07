# Système de Gestion des Dons de Sang - Microservices

## Architecture

```
demo-ingress/
├── user-service/          # Gestion des donneurs (Port 3001)
├── campaign-service/      # Gestion des campagnes (Port 3002)
├── appointment-service/   # Système de RDV (Port 3003)
├── analytics-service/     # Rapports et stats (Port 3004)
├── admin-service/         # Administration (Port 3005)
├── frontend/              # Interface React donneurs (Port 3100)
├── admin-dashboard/       # Dashboard admin React (Port 3200)
└── database/              # Scripts SQL
```

## Services et Ports

| Service             | Port | Domaine Ingress                  | Fonction           |
| ------------------- | ---- | -------------------------------- | ------------------ |
| User Service        | 3001 | api.dondesang.local/users        | Gestion donneurs   |
| Campaign Service    | 3002 | api.dondesang.local/campaigns    | Gestion campagnes  |
| Appointment Service | 3003 | api.dondesang.local/appointments | Système RDV        |
| Analytics Service   | 3004 | api.dondesang.local/analytics    | Rapports           |
| Admin Service       | 3005 | api.dondesang.local/admin        | Administration     |
| Frontend            | 3100 | dondesang.local                  | Interface donneurs |
| Admin Dashboard     | 3200 | admin.dondesang.local            | Interface admin    |

## Base de données MySQL

Tous les services se connectent à la même base MySQL avec des tables dédiées :

- `users`, `medical_profiles`, `donation_history`
- `campaigns`, `campaign_locations`
- `appointments`, `time_slots`
- `admin_users`, `audit_logs`

## Démarrage des services

```bash
# Démarrer tous les services
npm run start:all

# Ou individuellement
cd user-service && npm start
cd campaign-service && npm start
cd appointment-service && npm start
cd analytics-service && npm start
cd admin-service && npm start
cd frontend && npm start
cd admin-dashboard && npm start
```
