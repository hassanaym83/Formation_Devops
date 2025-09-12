# Quiz - Séance 3 : Réseaux - Fondations Linux

## Question 1 (QCM - 1 point)

**Quelle commande permet d'afficher toutes les interfaces réseau avec leurs adresses IP sur Linux ?**

A) `ifconfig -a`
B) `ip addr show`
C) `netstat -i`
D) `nmcli device status`

---

## Question 2 (QCM - 1 point)

**L'interface `lo` sur Linux représente :**

A) La première interface Ethernet locale
B) L'interface de loopback (127.0.0.1)
C) Une interface WiFi en mode local  
D) L'interface de liaison pour Docker

---

## Question 3 (QCM - 1 point)

**Avec NetworkManager, quelle commande crée une connexion Ethernet avec IP statique ?**

A) `nmcli connection add type ethernet con-name "static" ifname eth0 ip4 192.168.1.10/24`
B) `nmcli device connect eth0 --static 192.168.1.10/24`
C) `ip addr add 192.168.1.10/24 dev eth0`
D) `ifconfig eth0 192.168.1.10 netmask 255.255.255.0`

---

## Question 4 (Vrai/Faux - 1 point)

**NetworkManager est l'outil recommandé pour configurer le réseau sur les serveurs Linux de production.**

□ Vrai
□ Faux

---

## Question 5 (QCM - 2 points)

**Pour tester la connectivité vers la passerelle par défaut, quelle séquence de commandes est correcte ?**

A) `ip route show` puis `ping <IP_passerelle>`
B) `nmcli device show` puis `traceroute <IP_passerelle>`  
C) `netstat -rn` puis `nslookup <IP_passerelle>`
D) `ss -r` puis `dig <IP_passerelle>`

---

## Question 6 (QCM - 2 points)

**Dans le contexte DevOps, pourquoi privilégier une IP statique pour un serveur de développement ?**

A) Pour économiser la bande passante réseau
B) Pour garantir la connectivité des pipelines CI/CD automatisés
C) Pour améliorer les performances réseau du serveur
D) Pour simplifier la configuration du pare-feu local

---

## Question 7 (Question ouverte - 3 points)

**Décrivez la méthodologie de diagnostic réseau en cas de perte de connectivité Internet sur un serveur Linux. Listez les étapes dans l'ordre logique avec les commandes correspondantes.**

_Réponse attendue (3-4 étapes minimum) :_

---

---

---

---

---

## Question 8 (Analyse de cas - 4 points)

**Analyse du cas suivant :**

Un serveur DevOps présente les symptômes suivants :

```bash
$ ping 127.0.0.1
PING 127.0.0.1: 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.045 ms

$ ping 192.168.1.1
PING 192.168.1.1: 56 data bytes
Request timeout for icmp_seq 0

$ nslookup google.com
Server: 127.0.0.53
Address: 127.0.0.53#53
** server can't find google.com: NXDOMAIN
```

**Questions :**

1. **Quel est le problème identifié ? (1 point)**

   ***

2. **Quelle commande utiliseriez-vous pour diagnostiquer davantage ? (1 point)**

   ***

3. **Proposez 2 solutions possibles pour résoudre ce problème : (2 points)**

   Solution 1: ****************\_****************

   Solution 2: ****************\_****************

---

## Question 9 (Pratique - 3 points)

**Configuration NetworkManager - Complétez les commandes manquantes :**

Pour créer une connexion nommée "prod-server" sur l'interface eth0 avec :

- IP statique : 10.0.1.50/24
- Passerelle : 10.0.1.1
- DNS : 8.8.8.8 et 1.1.1.1

```bash
# Étape 1 : Créer la connexion
sudo nmcli connection add _________________ \
     con-name "prod-server" \
     _________________ eth0 \
     _________________ 10.0.1.50/24 \
     _________________ 10.0.1.1

# Étape 2 : Configurer DNS
sudo nmcli connection modify "prod-server" \
     _________________ "8.8.8.8,1.1.1.1"

# Étape 3 : Activer la connexion
sudo nmcli connection _________________ "prod-server"
```

---

## Question 10 (Réflexion DevOps - 2 points)

**Expliquez pourquoi la maîtrise des commandes réseau Linux est essentielle dans un environnement DevOps. Donnez 2 exemples concrets d'utilisation.**

Exemple 1: **********************\_\_\_\_**********************

---

Exemple 2: **********************\_\_\_\_**********************

---

---

## Barème total : 20 points

**Répartition :**

- Questions 1-4 : Connaissances de base (5 points)
- Questions 5-6 : Application pratique (4 points)
- Question 7 : Méthodologie (3 points)
- Question 8 : Analyse de cas (4 points)
- Questions 9-10 : Synthèse et réflexion (4 points)

**Seuil de validation : 12/20**
