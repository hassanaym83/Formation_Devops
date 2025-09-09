# LAB 2 - Configuration Vagrant et VM Linux

## Objectif

Créer des machines virtuelles Linux avec Vagrant et installer un serveur web Apache (httpd).

## Contexte

Automatisation du déploiement d'infrastructure avec Vagrant pour environnement DevOps

## Prérequis

- VirtualBox installé et fonctionnel (LAB 1 terminé)
- 2GB RAM minimum disponible
- Connexion Internet pour téléchargement des boxes

## Instructions détaillées

### Étape 1 : Installation Vagrant

```bash
# Installation via Chocolatey (dans PowerShell Admin)
choco install vagrant

# Vérification installation
vagrant --version

# Installation plugins essentiels
vagrant plugin install vagrant-vbguest
```

### Étape 2 : Téléchargement des boxes Linux

** Source officielle des boxes :** https://app.vagrantup.com/boxes/search

```bash
# Option 1 : CentOS Stream 9 (recommandé pour production)
vagrant box add generic/centos9s

# Option 2 : Ubuntu 22.04 LTS (recommandé pour développement)
vagrant box add ubuntu/jammy64

# Vérifier les boxes installées
vagrant box list
```

### Étape 3 : Création projet Vagrant

```bash
# Créer répertoire projet
mkdir /c/DevOps/vagrant-linux
cd /c/DevOps/vagrant-linux

# Initialiser Vagrant avec CentOS Stream 9
vagrant init generic/centos9s

# Ou initialiser avec Ubuntu 22.04
# vagrant init ubuntu/jammy64
```

### Étape 4 : Configuration Vagrantfile

#### Option A : CentOS Stream 9

```ruby
# Remplacer le contenu du Vagrantfile par :
Vagrant.configure("2") do |config|
  # Box CentOS Stream 9
  config.vm.box = "generic/centos9s"

  # Configuration réseau
  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.network "forwarded_port", guest: 80, host: 8080

  # Configuration VM
  config.vm.provider "virtualbox" do |vb|
    vb.name = "CentOS9-DevOps"
    vb.memory = "1024"
    vb.cpus = 1
  end

  # Installation automatique d'Apache
  config.vm.provision "shell", inline: <<-SHELL
    # Mise à jour du système
    dnf update -y

    # Installation Apache (httpd)
    dnf install -y httpd

    # Démarrage et activation Apache
    systemctl start httpd
    systemctl enable httpd

    # Configuration du firewall
    firewall-cmd --permanent --add-service=http
    firewall-cmd --reload

    # Création d'une page d'accueil personnalisée
    echo "<h1>Serveur Apache CentOS Stream 9</h1>" > /var/www/html/index.html
    echo "<p>Hostname: $(hostname)</p>" >> /var/www/html/index.html
    echo "<p>IP: $(ip addr show eth1 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)</p>" >> /var/www/html/index.html
    echo "<p>Date: $(date)</p>" >> /var/www/html/index.html

    # Vérification du service
    systemctl status httpd
  SHELL
end
```

#### Option B : Ubuntu 22.04 LTS

```ruby
# Alternative avec Ubuntu - Remplacer le contenu du Vagrantfile par :
Vagrant.configure("2") do |config|
  # Box Ubuntu 22.04 LTS
  config.vm.box = "ubuntu/jammy64"

  # Configuration réseau
  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.network "forwarded_port", guest: 80, host: 8080

  # Configuration VM
  config.vm.provider "virtualbox" do |vb|
    vb.name = "Ubuntu22-DevOps"
    vb.memory = "1024"
    vb.cpus = 1
  end

  # Installation automatique d'Apache
  config.vm.provision "shell", inline: <<-SHELL
    # Mise à jour du système
    apt-get update -y

    # Installation Apache2
    apt-get install -y apache2

    # Démarrage et activation Apache
    systemctl start apache2
    systemctl enable apache2

    # Configuration du firewall (UFW)
    ufw allow 'Apache'

    # Création d'une page d'accueil personnalisée
    echo "<h1>Serveur Apache Ubuntu 22.04</h1>" > /var/www/html/index.html
    echo "<p>Hostname: $(hostname)</p>" >> /var/www/html/index.html
    echo "<p>IP: $(ip addr show enp0s8 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)</p>" >> /var/www/html/index.html
    echo "<p>Date: $(date)</p>" >> /var/www/html/index.html

    # Vérification du service
    systemctl status apache2
  SHELL
end
```

### Étape 5 : Démarrage de la VM

```bash
# Démarrer la VM
vagrant up

# Vérifier le statut
vagrant status
```

### Étape 6 : Tests de connectivité

```bash
# Test du serveur web depuis l'hôte
curl http://localhost:8080
curl http://192.168.56.10

# Connexion SSH à la VM
vagrant ssh

# Dans la VM, vérifier Apache
sudo systemctl status httpd
curl http://localhost
exit
```

### Étape 7 : Gestion de la VM

```bash
# Arrêter la VM
vagrant halt

# Redémarrer la VM
vagrant up

# Redémarrer avec re-provisioning
vagrant reload --provision

# Détruire la VM (attention, suppression complète)
vagrant destroy
```

## Livrables attendus

### 1. Fichier Vagrantfile fonctionnel

- Configuration VM CentOS 7
- Réseau privé et port forwarding
- Provisioning Apache automatique

### 2. Tests de fonctionnement

```bash
# Dans la VM, vérifier Apache
vagrant ssh
sudo systemctl status httpd
curl http://localhost
curl http://192.168.56.10
exit

# Depuis l'hôte Windows
curl http://localhost:8080
```

### 3. Documentation

```bash
# Créer un fichier info.txt
echo "=== VM Linux DevOps ===
Hostname: $(vagrant ssh -c 'hostname' 2>/dev/null)
IP: 192.168.56.10
Services: Apache HTTP Server
Accès web: http://localhost:8080
SSH: vagrant ssh
Distribution: CentOS Stream 9 ou Ubuntu 22.04
" > info.txt
```

## Critères d'évaluation

| Critère               | Points    | Détail                                    |
| --------------------- | --------- | ----------------------------------------- |
| Configuration Vagrant | 2 pts     | Vagrantfile correct avec CentOS ou Ubuntu |
| Installation Apache   | 2 pts     | httpd/apache2 installé et démarré         |
| Connectivité réseau   | 1 pt      | Accès web fonctionnel                     |
| **Total**             | **5 pts** |                                           |

## Résolution de problèmes

### Problème : Box CentOS ne se télécharge pas

```bash
# Vérifier la connexion Internet
ping google.com

# Télécharger manuellement
vagrant box add centos/7 --provider virtualbox

# Vérifier les boxes disponibles
vagrant box list
```

### Problème : Apache ne démarre pas

```bash
# Se connecter à la VM
vagrant ssh

# Vérifier le statut
sudo systemctl status httpd

# Vérifier les logs
sudo journalctl -u httpd

# Redémarrer Apache
sudo systemctl restart httpd
```

### Problème : Page web non accessible

```bash
# Vérifier le firewall dans la VM
vagrant ssh
sudo firewall-cmd --list-services
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload

# Vérifier que Apache écoute
sudo netstat -tlnp | grep :80
```

### Problème : SSH ne fonctionne pas

```bash
# Vérifier le statut de la VM
vagrant status

# Redémarrer la VM
vagrant reload

# Debug SSH
vagrant ssh-config
```

## Commandes utiles

```bash
# Gestion VM
vagrant up                  # Démarrer la VM
vagrant halt                # Arrêter la VM
vagrant reload              # Redémarrer la VM
vagrant destroy             # Détruire la VM
vagrant status              # Statut de la VM

# Debug et informations
vagrant ssh-config          # Configuration SSH
vagrant port                # Mapping des ports
vagrant global-status       # Toutes les VMs Vagrant

# Box management
vagrant box list                    # Lister les boxes
vagrant box remove generic/centos9s   # Supprimer une box CentOS
vagrant box remove ubuntu/jammy64   # Supprimer une box Ubuntu
```

## Ressources complémentaires

- **Vagrant Boxes officielles :** https://app.vagrantup.com/boxes/search
- **CentOS Stream 9 Box :** https://app.vagrantup.com/generic/boxes/centos9s
- **Ubuntu 22.04 Box :** https://app.vagrantup.com/ubuntu/boxes/jammy64
- **Documentation Vagrant :** https://www.vagrantup.com/docs
- **Guide Apache CentOS :** https://httpd.apache.org/docs/2.4/
- **Guide Apache Ubuntu :** https://ubuntu.com/tutorials/install-and-configure-apache

## Durée estimée

**15 minutes** (téléchargement box + configuration + tests)
