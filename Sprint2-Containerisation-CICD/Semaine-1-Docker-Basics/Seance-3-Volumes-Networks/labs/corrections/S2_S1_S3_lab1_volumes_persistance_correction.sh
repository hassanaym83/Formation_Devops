#!/bin/bash

# Simplon Maghreb - Formation DevOps
# Sprint 2 - Semaine 1 - Séance 3 : Volumes et Networks Docker
# CORRECTION LAB 1 - Configuration volumes et persistance

echo "=================================================="
echo "CORRECTION LAB 1 - Volumes et Persistance Docker"
echo "=================================================="

# Configuration
VOLUME_NAME="postgres_data"
CONTAINER_NAME="postgres_lab1"
DB_NAME="devops_db"
DB_USER="devops_user"
DB_PASS="SecurePass123"

echo "📋 Configuration utilisée:"
echo "- Volume: $VOLUME_NAME"
echo "- Conteneur: $CONTAINER_NAME"
echo "- Base de données: $DB_NAME"
echo "- Utilisateur: $DB_USER"
echo ""

# Étape 1: Préparation de l'environnement (2 points)
echo "🔧 ÉTAPE 1: Préparation de l'environnement"
echo "-------------------------------------------"

echo "Création du volume dédié PostgreSQL..."
docker volume create $VOLUME_NAME
if [ $? -eq 0 ]; then
    echo "✅ Volume $VOLUME_NAME créé avec succès"
else
    echo "❌ Erreur lors de la création du volume"
    exit 1
fi

echo ""
echo "Vérification de la création du volume:"
docker volume ls | grep $VOLUME_NAME
echo ""

echo "Inspection du volume:"
docker volume inspect $VOLUME_NAME
echo ""

echo "Localisation du point de montage:"
docker volume inspect $VOLUME_NAME | grep Mountpoint
echo ""

# Étape 2: Déploiement PostgreSQL avec persistance (3 points)
echo "🐘 ÉTAPE 2: Déploiement PostgreSQL avec persistance"
echo "----------------------------------------------------"

echo "Déploiement du conteneur PostgreSQL..."
docker run -d \
  --name $CONTAINER_NAME \
  -e POSTGRES_DB=$DB_NAME \
  -e POSTGRES_USER=$DB_USER \
  -e POSTGRES_PASSWORD=$DB_PASS \
  -v $VOLUME_NAME:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

if [ $? -eq 0 ]; then
    echo "✅ Conteneur PostgreSQL déployé avec succès"
else
    echo "❌ Erreur lors du déploiement de PostgreSQL"
    exit 1
fi

echo ""
echo "Attente du démarrage de PostgreSQL (30 secondes)..."
sleep 30

echo "Vérification que le conteneur fonctionne:"
docker ps | grep $CONTAINER_NAME
echo ""

echo "Vérification des logs PostgreSQL:"
docker logs $CONTAINER_NAME | tail -10
echo ""

echo "Test de connexion à PostgreSQL:"
docker exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "\l"
echo ""

echo "Vérification du montage du volume:"
docker inspect $CONTAINER_NAME | grep -A 10 Mounts
echo ""

# Étape 3: Insertion et vérification des données (2 points)
echo "📊 ÉTAPE 3: Insertion et vérification des données"
echo "--------------------------------------------------"

echo "Création de la table de test..."
docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
CREATE TABLE projets (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    environnement VARCHAR(50),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF

if [ $? -eq 0 ]; then
    echo "✅ Table 'projets' créée avec succès"
else
    echo "❌ Erreur lors de la création de la table"
    exit 1
fi

echo ""
echo "Insertion des données de test..."
docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
INSERT INTO projets (nom, environnement) VALUES 
('App-Frontend', 'production'),
('API-Backend', 'staging'),
('Database-Migration', 'development'),
('Monitoring-Stack', 'production');
EOF

if [ $? -eq 0 ]; then
    echo "✅ Données de test insérées avec succès"
else
    echo "❌ Erreur lors de l'insertion des données"
    exit 1
fi

echo ""
echo "Vérification des données insérées:"
docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "SELECT * FROM projets;"
echo ""

echo "Comptage des enregistrements:"
RECORD_COUNT=$(docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM projets;")
echo "Nombre d'enregistrements: $RECORD_COUNT"
echo ""

# Étape 4: Test de persistance après redémarrage (2 points)
echo "🔄 ÉTAPE 4: Test de persistance après redémarrage"
echo "--------------------------------------------------"

echo "Arrêt du conteneur PostgreSQL..."
docker stop $CONTAINER_NAME
if [ $? -eq 0 ]; then
    echo "✅ Conteneur arrêté avec succès"
else
    echo "❌ Erreur lors de l'arrêt du conteneur"
    exit 1
fi

echo ""
echo "Suppression du conteneur (ATTENTION: pas le volume)..."
docker rm $CONTAINER_NAME
if [ $? -eq 0 ]; then
    echo "✅ Conteneur supprimé avec succès"
else
    echo "❌ Erreur lors de la suppression du conteneur"
    exit 1
fi

echo ""
echo "Vérification que le volume existe toujours:"
docker volume ls | grep $VOLUME_NAME
if [ $? -eq 0 ]; then
    echo "✅ Volume toujours présent"
else
    echo "❌ Volume perdu!"
    exit 1
fi

echo ""
echo "Redéploiement du conteneur avec le même volume..."
CONTAINER_NAME_RESTORED="${CONTAINER_NAME}_restored"
docker run -d \
  --name $CONTAINER_NAME_RESTORED \
  -e POSTGRES_DB=$DB_NAME \
  -e POSTGRES_USER=$DB_USER \
  -e POSTGRES_PASSWORD=$DB_PASS \
  -v $VOLUME_NAME:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

if [ $? -eq 0 ]; then
    echo "✅ Conteneur redéployé avec succès"
else
    echo "❌ Erreur lors du redéploiement"
    exit 1
fi

echo ""
echo "Attente que PostgreSQL soit prêt (30 secondes)..."
sleep 30

echo "Vérification de la persistance des données:"
docker exec $CONTAINER_NAME_RESTORED psql -U $DB_USER -d $DB_NAME -c "SELECT * FROM projets;"
echo ""

echo "Vérification du nombre d'enregistrements:"
RESTORED_COUNT=$(docker exec $CONTAINER_NAME_RESTORED psql -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM projets;")
echo "Nombre d'enregistrements après restauration: $RESTORED_COUNT"

if [ "$RECORD_COUNT" -eq "$RESTORED_COUNT" ]; then
    echo "✅ Persistance validée: données conservées"
else
    echo "❌ Persistance échouée: données perdues"
    exit 1
fi

echo ""

# Étape 5: Stratégie de sauvegarde (1 point)
echo "💾 ÉTAPE 5: Stratégie de sauvegarde"
echo "-----------------------------------"

echo "Création d'une sauvegarde des données..."
BACKUP_FILE="backup_devops_db_$(date +%Y%m%d_%H%M%S).sql"
docker exec $CONTAINER_NAME_RESTORED pg_dump -U $DB_USER $DB_NAME > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ Sauvegarde créée: $BACKUP_FILE"
else
    echo "❌ Erreur lors de la création de la sauvegarde"
    exit 1
fi

echo ""
echo "Vérification du fichier de sauvegarde:"
ls -la $BACKUP_FILE
echo ""

echo "Aperçu du contenu de la sauvegarde:"
head -n 20 $BACKUP_FILE
echo ""

echo "Création de la documentation de stratégie de sauvegarde..."
cat > backup_strategy.md << 'EOF'
# Stratégie de sauvegarde PostgreSQL DevOps

## Sauvegarde quotidienne

### Automatisation via crontab
```bash
# Ajouter dans crontab (crontab -e)
0 2 * * * docker exec postgres_container pg_dump -U devops_user devops_db > /backup/devops_db_$(date +\%Y\%m\%d).sql
```

### Rétention des sauvegardes
- **Local**: 7 jours
- **Remote**: 30 jours  
- **Archive**: 1 an (mensuel)

## Commandes de sauvegarde

### Sauvegarde complète
```bash
docker exec postgres_container pg_dump -U devops_user devops_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Sauvegarde compressée
```bash
docker exec postgres_container pg_dump -U devops_user devops_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Sauvegarde avec schéma uniquement
```bash
docker exec postgres_container pg_dump -U devops_user --schema-only devops_db > schema_backup.sql
```

## Restauration

### Restauration complète
```bash
docker exec -i postgres_container psql -U devops_user devops_db < backup_file.sql
```

### Restauration avec DROP/CREATE
```bash
docker exec -i postgres_container psql -U devops_user -c "DROP DATABASE IF EXISTS devops_db; CREATE DATABASE devops_db;"
docker exec -i postgres_container psql -U devops_user devops_db < backup_file.sql
```

## Sauvegarde du volume Docker

### Méthode 1: Sauvegarde du volume
```bash
# Créer un volume de sauvegarde
docker volume create backup_volume

# Copier les données
docker run --rm -v postgres_data:/source -v backup_volume:/backup alpine cp -a /source/. /backup/
```

### Méthode 2: Sauvegarde vers l'hôte
```bash
# Sauvegarder vers un répertoire hôte
docker run --rm -v postgres_data:/source -v /host/backup:/backup alpine tar czf /backup/postgres_data_$(date +%Y%m%d).tar.gz -C /source .
```

## Synchronisation avec stockage externe

### Vers AWS S3
```bash
aws s3 sync /backup/postgres s3://mon-bucket/database-backups/
```

### Vers serveur distant (rsync)
```bash
rsync -avz /backup/ user@backup-server:/backups/postgres/
```

## Monitoring des sauvegardes

### Script de vérification
```bash
#!/bin/bash
BACKUP_DIR="/backup"
ALERT_EMAIL="admin@devops.local"

# Vérifier que la sauvegarde d'aujourd'hui existe
TODAY=$(date +%Y%m%d)
if [ ! -f "$BACKUP_DIR/devops_db_$TODAY.sql" ]; then
    echo "ALERT: Backup missing for $TODAY" | mail -s "Backup Alert" $ALERT_EMAIL
fi
```

## Récupération d'urgence

### Procédure de disaster recovery
1. Déployer nouveau conteneur PostgreSQL
2. Monter volume de sauvegarde ou restaurer depuis fichier
3. Vérifier l'intégrité des données
4. Rediriger les applications

### Test de récupération (mensuel)
```bash
# Script de test automatisé
./test_backup_restore.sh
```

## Conformité et sécurité

- Chiffrement des sauvegardes en transit et au repos
- Accès restreint aux fichiers de sauvegarde
- Audit des accès aux sauvegardes
- Tests de récupération réguliers
EOF

echo "✅ Documentation de stratégie créée: backup_strategy.md"
echo ""

# Validation finale
echo "🎯 VALIDATION FINALE DU LAB 1"
echo "==============================="

echo ""
echo "1. Volume créé et configuré:"
docker volume inspect $VOLUME_NAME | grep -E "(Name|Mountpoint)" 
echo ""

echo "2. PostgreSQL fonctionnel avec persistance:"
docker ps | grep $CONTAINER_NAME_RESTORED
echo ""

echo "3. Volume correctement monté:"
docker inspect $CONTAINER_NAME_RESTORED | grep -A 5 "Mounts"
echo ""

echo "4. Données conservées après redémarrage:"
echo "   Nombre d'enregistrements initial: $RECORD_COUNT"
echo "   Nombre d'enregistrements après redémarrage: $RESTORED_COUNT"
if [ "$RECORD_COUNT" -eq "$RESTORED_COUNT" ]; then
    echo "   ✅ Persistance validée"
else
    echo "   ❌ Persistance échouée"
fi
echo ""

echo "5. Stratégie de sauvegarde documentée:"
ls -la backup_strategy.md $BACKUP_FILE
echo ""

# Résumé des points
echo "📊 RÉSUMÉ DES POINTS"
echo "==================="
echo "✅ Volume créé et configuré: 2/2 points"
echo "✅ PostgreSQL fonctionnel avec persistance: 3/3 points"
echo "✅ Données conservées après redémarrage: 2/2 points"
echo "✅ Stratégie de sauvegarde documentée: 1/1 point"
echo ""
echo "🎉 TOTAL: 8/8 points - LAB 1 RÉUSSI!"
echo ""

# Nettoyage optionnel
echo "🧹 NETTOYAGE (optionnel)"
echo "========================"
echo "Pour nettoyer l'environnement du LAB:"
echo "docker stop $CONTAINER_NAME_RESTORED"
echo "docker rm $CONTAINER_NAME_RESTORED"
echo "docker volume rm $VOLUME_NAME"
echo "rm -f $BACKUP_FILE backup_strategy.md"
echo ""

echo "=================================================="
echo "LAB 1 TERMINÉ AVEC SUCCÈS!"
echo "Durée: 20 minutes | Points: 8/30"
echo "=================================================="