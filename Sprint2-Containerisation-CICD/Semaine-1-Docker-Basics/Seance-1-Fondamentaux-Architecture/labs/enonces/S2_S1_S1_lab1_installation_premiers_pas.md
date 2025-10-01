# LAB 1 : Installation et premiers pas Docker

**Sprint 2 - Semaine 1 - Séance 1**  
**Référence** : `S2_S1_S1_lab1_installation_premiers_pas`  
**Durée** : 20 minutes

## Objectif du LAB

Installer Docker Engine et démontrer les avantages des conteneurs face aux VMs traditionnelles dans un contexte DevOps professionnel.

## Contexte métier

Votre équipe DevOps doit migrer d'une infrastructure basée sur des machines virtuelles vers une approche containerisée. Le manager technique souhaite une démonstration concrète des gains en performance et efficacité.

## Prérequis techniques

- Système d'exploitation compatible (Linux/Windows/macOS)
- Connexion internet stable
- Droits administrateur pour l'installation
- Minimum 4GB RAM disponible

## Énoncé détaillé

### Phase 1 : Installation Docker Engine

**Contexte** : Installation propre selon les bonnes pratiques DevOps

**Instructions** :

1. **Préparation système** :

   - Vérifier les prérequis système pour votre OS
   - Mettre à jour le système d'exploitation
   - Documenter la version du kernel (Linux) ou système

2. **Installation Docker** :

   - Installer Docker Engine via la méthode officielle
   - Configurer le démarrage automatique du service
   - Ajouter votre utilisateur au groupe docker (Linux)

3. **Vérification installation** :
   ```bash
   docker version
   docker system info
   docker run hello-world
   ```

**Validation** :

- Sortie de `docker version` montre client et serveur
- `docker system info` affiche les informations système complètes
- `hello-world` s'exécute sans erreur

**Livrables** :

- Screenshot des commandes de vérification
- Document des étapes d'installation suivies

### Phase 2 : Tests fonctionnels avancés

**Contexte** : Validation des composants Docker essentiels

**Instructions** :

1. **Test des images** :

   ```bash
   docker pull nginx:alpine
   docker pull postgres:13-alpine
   docker images
   ```

2. **Test des conteneurs** :

   ```bash
   docker run -d --name test-web -p 8080:80 nginx:alpine
   docker ps
   curl http://localhost:8080
   ```

3. **Test des logs et monitoring** :

   ```bash
   docker logs test-web
   docker stats test-web --no-stream
   docker exec test-web ps aux
   ```

4. **Nettoyage** :
   ```bash
   docker stop test-web
   docker rm test-web
   docker rmi nginx:alpine postgres:13-alpine
   ```

**Validation** :

- Images téléchargées correctement
- Serveur nginx accessible sur port 8080
- Logs et statistiques récupérées
- Nettoyage complet effectué

**Livrables** :

- Log de toutes les commandes exécutées
- Screenshot de la page nginx dans le navigateur

### Phase 3 : Comparaison performance VM vs Conteneur

**Contexte** : Démonstration quantifiée des avantages conteneurs

**Instructions** :

1. **Mesure temps de démarrage** :

   - Chronométrer le démarrage d'une VM Ubuntu (si disponible)
   - Chronométrer le démarrage d'un conteneur Ubuntu :

   ```bash
   time docker run --rm ubuntu:20.04 echo "Conteneur démarré"
   ```

2. **Mesure consommation ressources** :

   - Vérifier l'usage RAM d'une VM en fonctionnement
   - Mesurer l'usage RAM d'un conteneur :

   ```bash
   docker run -d --name resource-test nginx:alpine
   docker stats resource-test --no-stream
   ```

3. **Test portabilité** :
   - Exporter une image Docker :
   ```bash
   docker save nginx:alpine > nginx-image.tar
   ```
   - Vérifier la taille du fichier
   - Simuler le transfert sur un autre environnement

**Validation** :

- Temps de démarrage conteneur < 5 secondes
- Usage RAM conteneur < 50MB pour nginx
- Image exportée avec succès

**Livrables** :

- Tableau comparatif des métriques VM vs Conteneur
- Analyse des gains obtenus

## Ressources et aide

**Documentation** :

- [Installation Docker officielle](https://docs.docker.com/engine/install/)
- [Post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)

**Dépannage courant** :

- Problème de permissions : `sudo usermod -aG docker $USER`
- Service non démarré : `sudo systemctl start docker`
- Port occupé : `docker ps` pour vérifier les conteneurs actifs

**Commandes de diagnostic** :

```bash
docker system info
docker system df
sudo journalctl -u docker.service
```

## Livrables attendus

1. **Rapport d'installation** (format Markdown) :

   - Étapes suivies
   - Problèmes rencontrés et solutions
   - Screenshots des vérifications

2. **Tableau de comparaison** :

   - Métriques VM vs Conteneur
   - Analyse des gains
   - Recommandations pour l'équipe

3. **Log des commandes** :
   - Historique bash complet
   - Résultats des tests
   - Temps d'exécution mesurés

---

**Aide formateur** : Hassan ESSADIK  
**Durée recommandée** : 20 minutes  
**Prochaine étape** : LAB 2 - Manipulation de conteneurs et images
