# LAB 1 - Installation VirtualBox et première VM

## Objectif

Installer VirtualBox et créer une première machine virtuelle Ubuntu Server pour environnement DevOps.

## Contexte

Préparation infrastructure pour environnements de test et développement

## Prérequis

- Windows 10/11 avec droits administrateur
- 8GB RAM minimum sur machine hôte
- 50GB espace disque disponible
- Connexion Internet stable

## Instructions détaillées

### Étape 1 : Installation de Chocolatey et VirtualBox

#### 1.1 Installation complète de Chocolatey

```powershell
# Ouvrir PowerShell en tant qu'administrateur
# Vérifier la politique d'exécution actuelle
Get-ExecutionPolicy

# Autoriser l'exécution des scripts (temporaire)
Set-ExecutionPolicy Bypass -Scope Process -Force

# Télécharger et installer Chocolatey
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# Commande d'installation Chocolatey (une seule ligne)
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Vérifier l'installation de Chocolatey
choco --version

# Actualiser l'environnement PowerShell
refreshenv
```

#### 1.2 Installation VirtualBox via Chocolatey

```powershell
# Installer VirtualBox via Chocolatey (recommandé)
choco install virtualbox -y

# Installer VirtualBox Extension Pack (optionnel mais recommandé)
choco install virtualbox.extensionpack -y

# Vérifier l'installation
choco list --local-only | findstr virtualbox
```

#### 1.3 Alternative : Installation manuelle (si Chocolatey échoue)

```powershell
# Option manuelle
# 1. Télécharger depuis https://www.virtualbox.org/wiki/Downloads
# 2. VirtualBox-7.0.x-Win.exe + Extension Pack
# 3. Exécuter l'installateur avec droits administrateur
```

### Étape 2 : Vérification installation

```powershell
# Vérifier version VirtualBox
VBoxManage --version

# Lancer VirtualBox GUI
VirtualBox
```

### Étape 3 : Téléchargement image Ubuntu Server

- URL : https://ubuntu.com/download/server
- Version : Ubuntu Server 22.04.3 LTS
- Fichier : ubuntu-22.04.3-live-server-amd64.iso
- Taille : ~1.4GB

### Étape 4 : Création machine virtuelle

```bash
# Configuration VM Ubuntu DevOps
Nom: devops-ubuntu-server
Type: Linux
Version: Ubuntu (64-bit)
Mémoire: 2048 MB (2GB)
Disque dur: Créer - VDI - Dynamique - 20GB
Processeurs: 2 cores
Vidéo: 16MB
Réseau: NAT
```

### Étape 5 : Configuration réseau avancée

```bash
# Port forwarding pour SSH
Nom: SSH
Protocole: TCP
IP hôte: 127.0.0.1
Port hôte: 2222
IP invité: 10.0.2.15
Port invité: 22
```

### Étape 6 : Installation Ubuntu Server

```bash
# Paramètres installation
Langue: English
Keyboard: French (ou votre layout)
Réseau: DHCP (automatique)
Proxy: (vide)
Mirror: (défaut)
Stockage: Utiliser tout le disque
Profile setup:
  - Nom: DevOps User
  - Server name: devops-server
  - Username: devops
  - Password: DevOps123!
SSH: Installer OpenSSH server ✓
Snaps: (aucun)
```

### Étape 7 : Configuration post-installation

```bash
# Se connecter à la VM
# Username: devops
# Password: DevOps123!

# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer outils essentiels
sudo apt install -y curl wget git htop tree vim

# Vérifier service SSH
sudo systemctl status ssh
sudo systemctl enable ssh
```

### Étape 8 : Test connectivité SSH

```powershell
# Depuis Windows PowerShell
# Connecter via SSH (port forwarding)
ssh devops@127.0.0.1 -p 2222

# Première connexion
# Accepter fingerprint: yes
# Password: DevOps123!

# Test commandes dans VM
lsb_release -a
ip addr show
exit
```

### Étape 9 : Configuration clé SSH (optionnel)

```powershell
# Générer paire clés SSH sur Windows
ssh-keygen -t ed25519 -C "devops@virtualbox"
# Sauvegarder dans: C:\Users\[username]\.ssh\id_ed25519

# Copier clé publique vers VM
type C:\Users\[username]\.ssh\id_ed25519.pub | ssh devops@127.0.0.1 -p 2222 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Test connexion sans mot de passe
ssh devops@127.0.0.1 -p 2222
```

## Livrables attendus

### Captures d'écran à fournir

1. VirtualBox Manager avec VM créée
2. Console Ubuntu Server démarrée
3. Output de `lsb_release -a` dans la VM
4. Connexion SSH réussie depuis Windows

### Fichier de configuration

```bash
# Créer fichier info-vm.txt dans la VM
echo "=== INFORMATIONS VM DEVOPS ===" > ~/info-vm.txt
echo "Hostname: $(hostname)" >> ~/info-vm.txt
echo "OS: $(lsb_release -d | cut -f2)" >> ~/info-vm.txt
echo "IP: $(ip addr show enp0s3 | grep 'inet ' | cut -d' ' -f6)" >> ~/info-vm.txt
echo "Memory: $(free -h | grep Mem | awk '{print $2}')" >> ~/info-vm.txt
echo "Date: $(date)" >> ~/info-vm.txt
cat ~/info-vm.txt
```

## Critères d'évaluation

| Critère                 | Points    | Détail                                 |
| ----------------------- | --------- | -------------------------------------- |
| Installation Chocolatey | 1 pt      | Chocolatey installé et fonctionnel     |
| Installation VirtualBox | 2 pts     | VirtualBox fonctionnel, version 7.0+   |
| Configuration VM        | 2 pts     | Paramètres corrects (RAM, CPU, réseau) |
| Connectivité SSH        | 1 pt      | Connexion SSH depuis Windows réussie   |
| **Total**               | **6 pts** |                                        |

## Résolution de problèmes

### Problème : Chocolatey - Erreur paramètre positionnel

```powershell
# Erreur : "A positional parameter cannot be found that accepts argument"
# Solution : Exécuter les commandes ligne par ligne

# 1. Définir la politique d'exécution
Set-ExecutionPolicy Bypass -Scope Process -Force

# 2. Configurer TLS
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# 3. Installer Chocolatey
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 4. Redémarrer PowerShell en tant qu'administrateur
# 5. Tester Chocolatey
choco --version
```

### Problème : Virtualisation non activée

```bash
# Erreur : VT-x/AMD-V hardware acceleration is not available
# Solution : Activer virtualisation dans BIOS
# - Redémarrer et entrer dans BIOS (F2/F12/Del)
# - Advanced → CPU Configuration → Intel VT-x (Enabled)
# - AMD → SVM Mode (Enabled)
```

### Problème : SSH connexion refusée

```bash
# Vérifier port forwarding VirtualBox
# VM Settings → Network → Advanced → Port Forwarding
# Vérifier service SSH dans VM
sudo systemctl status ssh
sudo systemctl restart ssh
```

### Problème : Performance lente

```bash
# Augmenter mémoire VM (4GB recommandé)
# Activer VT-x/AMD-V
# Installer Guest Additions pour optimisation
```

### Problème : Chocolatey non reconnu après installation

```powershell
# Fermer et rouvrir PowerShell en tant qu'administrateur
# Ou exécuter :
refreshenv
# Ou redémarrer l'ordinateur si nécessaire
```

## Durée estimée

**15 minutes** (installation VirtualBox + création VM + tests)

## Ressources

- [VirtualBox User Manual](https://www.virtualbox.org/manual/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [SSH Configuration Guide](https://www.ssh.com/academy/ssh/config)
