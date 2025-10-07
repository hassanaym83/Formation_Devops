# Simplon Maghreb - Formation DevOps

# Sprint 2 - Semaine 1 - Séance 3 : Volumes et Networks Docker

# 📝 LAB 1 - Configuration volumes et persistance

**Fichier de travail** : `S2_S1_S3_lab1_volumes_persistance.sh`  
**Durée estimée** : 20 minutes  
**Points** : 8/30  
**Objectif** : Maîtriser les volumes Docker pour la persistance des données

---

## Contexte

Vous devez déployer une infrastructure de base de données PostgreSQL pour une application DevOps. La persistance des données est critique car les équipes de développement ne peuvent pas perdre leurs données lors des redémarrages de conteneurs.

## Prérequis

- Docker installé et fonctionnel
- Accès en écriture au système de fichiers
- Connaissances de base SQL

## Instructions détaillées

### Étape 1 : Préparation de l'environnement (2 points)

1. **Créer un volume dédié** :

   ```bash
   # Créer un volume nommé pour PostgreSQL
   docker volume create postgres_data

   # Vérifier la création
   docker volume ls | grep postgres_data

   # Inspecter le volume
   docker volume inspect postgres_data
   ```

2. **Vérifier l'emplacement de stockage** :
   ```bash
   # Localiser le point de montage du volume
   docker volume inspect postgres_data | grep Mountpoint
   ```

### Étape 2 : Déploiement PostgreSQL avec persistance (3 points)

1. **Déployer le conteneur PostgreSQL** :

   ```bash
   docker run -d \
     --name postgres_lab1 \
     -e POSTGRES_DB=devops_db \
     -e POSTGRES_USER=devops_user \
     -e POSTGRES_PASSWORD=SecurePass123 \
     -v postgres_data:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:13
   ```

2. **Vérifier le déploiement** :

   ```bash
   # Vérifier que le conteneur fonctionne
   docker ps | grep postgres_lab1

   # Vérifier les logs
   docker logs postgres_lab1

   # Tester la connexion
   docker exec -it postgres_lab1 psql -U devops_user -d devops_db -c "\l"
   ```

3. **Vérifier le montage du volume** :
   ```bash
   # Vérifier que le volume est monté
   docker inspect postgres_lab1 | grep -A 10 Mounts
   ```

### Étape 3 : Insertion et vérification des données (2 points)

1. **Créer des données de test** :

   ```bash
   # Se connecter à PostgreSQL
   docker exec -it postgres_lab1 psql -U devops_user -d devops_db
   ```

2. **Exécuter dans PostgreSQL** :

   ```sql
   -- Créer une table de test
   CREATE TABLE projets (
       id SERIAL PRIMARY KEY,
       nom VARCHAR(100) NOT NULL,
       environnement VARCHAR(50),
       date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Insérer des données
   INSERT INTO projets (nom, environnement) VALUES
   ('App-Frontend', 'production'),
   ('API-Backend', 'staging'),
   ('Database-Migration', 'development'),
   ('Monitoring-Stack', 'production');

   -- Vérifier les données
   SELECT * FROM projets;

   -- Quitter PostgreSQL
   \q
   ```

3. **Documenter l'état initial** :
   ```bash
   # Compter les enregistrements
   docker exec postgres_lab1 psql -U devops_user -d devops_db -c "SELECT COUNT(*) FROM projets;"
   ```

### Étape 4 : Test de persistance après redémarrage (2 points)

1. **Arrêter et supprimer le conteneur** :

   ```bash
   # Arrêter le conteneur
   docker stop postgres_lab1

   # Supprimer le conteneur (ATTENTION : pas le volume)
   docker rm postgres_lab1

   # Vérifier que le volume existe toujours
   docker volume ls | grep postgres_data
   ```

2. **Redéployer avec le même volume** :

   ```bash
   # Redéployer le conteneur avec le même volume
   docker run -d \
     --name postgres_lab1_restored \
     -e POSTGRES_DB=devops_db \
     -e POSTGRES_USER=devops_user \
     -e POSTGRES_PASSWORD=SecurePass123 \
     -v postgres_data:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:13
   ```

3. **Vérifier la persistance des données** :

   ```bash
   # Attendre que PostgreSQL soit prêt
   sleep 10

   # Vérifier que les données sont toujours là
   docker exec postgres_lab1_restored psql -U devops_user -d devops_db -c "SELECT * FROM projets;"

   # Compter les enregistrements
   docker exec postgres_lab1_restored psql -U devops_user -d devops_db -c "SELECT COUNT(*) FROM projets;"
   ```

### Étape 5 : Stratégie de sauvegarde (1 point)

1. **Créer une sauvegarde des données** :

   ```bash
   # Dump de la base de données
   docker exec postgres_lab1_restored pg_dump -U devops_user devops_db > backup_devops_db.sql

   # Vérifier le fichier de sauvegarde
   ls -la backup_devops_db.sql
   head -n 20 backup_devops_db.sql
   ```

2. **Documenter la stratégie de sauvegarde** :

   ````bash
   # Créer un script de sauvegarde automatique
   cat > backup_strategy.md << 'EOF'
   # Stratégie de sauvegarde PostgreSQL DevOps

   ## Sauvegarde quotidienne
   - Dump SQL automatique via crontab
   - Rétention : 7 jours en local, 30 jours en remote

   ## Commande de sauvegarde
   ```bash
   docker exec postgres_container pg_dump -U devops_user devops_db > backup_$(date +%Y%m%d_%H%M%S).sql
   ````

   ## Restauration

   ```bash
   docker exec -i postgres_container psql -U devops_user devops_db < backup_file.sql
   ```

   ## Volume backup

   - Sauvegarde du volume Docker via rsync
   - Synchronisation avec stockage externe
     EOF

   ```

   ```

## Validation et critères d'évaluation

### Vérifications attendues

1. **Volume créé et configuré (2 points)** :

   ```bash
   # Vérifier l'existence du volume
   docker volume inspect postgres_data

   # Vérifier le type et les propriétés
   docker volume ls -f name=postgres_data
   ```

2. **PostgreSQL fonctionnel avec persistance (3 points)** :

   ```bash
   # Conteneur actif et fonctionnel
   docker ps | grep postgres

   # Volume correctement monté
   docker inspect postgres_lab1_restored | grep -A 5 "Mounts"

   # Base de données accessible
   docker exec postgres_lab1_restored psql -U devops_user -d devops_db -c "\dt"
   ```

3. **Données conservées après redémarrage (2 points)** :

   ```bash
   # Vérifier la présence des 4 enregistrements
   docker exec postgres_lab1_restored psql -U devops_user -d devops_db -c "SELECT COUNT(*) FROM projets;"

   # Vérifier l'intégrité des données
   docker exec postgres_lab1_restored psql -U devops_user -d devops_db -c "SELECT nom, environnement FROM projets ORDER BY id;"
   ```

4. **Stratégie de sauvegarde documentée (1 point)** :

   ```bash
   # Fichier de sauvegarde créé
   ls -la backup_devops_db.sql

   # Documentation de stratégie
   cat backup_strategy.md
   ```

## Livrables attendus

- [ ] Script `S2_S1_S3_lab1_volumes_persistance.sh` complet et exécutable
- [ ] Volume PostgreSQL configuré et persistant
- [ ] Données de test insérées et conservées après redémarrage
- [ ] Fichier de sauvegarde `backup_devops_db.sql`
- [ ] Documentation `backup_strategy.md`

## Ressources

- [Docker Volumes Documentation](https://docs.docker.com/storage/volumes/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html)

---

**Sprint 2 - Semaine 1 - Séance 3 - LAB 1**  
_Formateur : Hassan ESSADIK_
