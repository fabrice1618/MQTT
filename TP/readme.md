# TP MQTT – Installation et utilisation de Mosquitto

## Objectifs

Ce TP vous guide dans la mise en place complète d'une communication MQTT, du broker jusqu'aux clients programmés en C. A l'issue de ce TP, vous serez capable de :

- Installer et configurer un broker MQTT (Mosquitto)
- Mettre en place une authentification par utilisateur et mot de passe
- Gérer le service Mosquitto (démarrage, arrêt, surveillance)
- Publier et recevoir des messages à l'aide des outils en ligne de commande
- Développer des clients MQTT en langage C avec la bibliothèque Paho

---

# 1. Installation de Mosquitto

Mosquitto est un broker MQTT open source, léger et largement utilisé. Le paquet `mosquitto` fournit le broker (le serveur), tandis que `mosquitto-clients` fournit les outils en ligne de commande `mosquitto_pub` et `mosquitto_sub` pour publier et souscrire à des messages.

### Sous Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients -y
```

### Vérifier l’installation

La commande suivante lance Mosquitto en mode verbose (affichage détaillé). Elle permet de vérifier que le programme est correctement installé et affiche la version utilisée.

```bash
mosquitto -v
```

Quittez avec `Ctrl+C` après vérification.

---

# 2. Gestion du service Mosquitto

Mosquitto fonctionne comme un service systemd. Cela signifie qu’il peut tourner en arrière-plan et démarrer automatiquement avec le système. Voici les commandes principales pour gérer ce service.

### Démarrer le service

Cette commande lance le broker Mosquitto. Il commence alors à écouter les connexions MQTT sur le port par défaut (1883).

```bash
sudo systemctl start mosquitto
```

### Activer le démarrage automatique

Pour que Mosquitto se lance automatiquement à chaque redémarrage de la machine :

```bash
sudo systemctl enable mosquitto
```

### Vérifier l’état du service

Cette commande affiche si le service est actif, depuis combien de temps il tourne, et les derniers messages du journal :

```bash
sudo systemctl status mosquitto
```

### Arrêter le service

Pour stopper le broker (utile lors d’un changement de configuration par exemple) :

```bash
sudo systemctl stop mosquitto
```

---

# 3. Configuration de l'authentification

Par défaut, Mosquitto accepte les connexions anonymes (sans identifiant). Pour sécuriser le broker, il est nécessaire de configurer une authentification par nom d'utilisateur et mot de passe. Cela empêche des clients non autorisés de publier ou lire des messages.

### Créer un fichier de mots de passe

L'outil `mosquitto_passwd` gère un fichier contenant les identifiants chiffrés. L'option `-c` crée un nouveau fichier (attention : elle écrase un fichier existant). La commande vous demandera de saisir et confirmer un mot de passe.

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd user1
```

Pour ajouter un utilisateur supplémentaire sans écraser le fichier existant, utilisez la commande sans l'option `-c` :

```bash
sudo mosquitto_passwd /etc/mosquitto/passwd user2
```

### Modifier la configuration Mosquitto

Editez le fichier de configuration principal de Mosquitto :

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Ajoutez les lignes suivantes :

```conf
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 1883
```

Explication de chaque directive :
- `allow_anonymous false` : interdit les connexions sans identifiant
- `password_file /etc/mosquitto/passwd` : indique le fichier contenant les identifiants autorisés
- `listener 1883` : configure le broker pour écouter sur le port standard MQTT

### Redémarrer Mosquitto

Après toute modification de la configuration, il faut redémarrer le service pour que les changements soient pris en compte :

```bash
sudo systemctl restart mosquitto
```

---

# 4. Test avec les outils en ligne de commande

Avant de passer à la programmation, il est important de vérifier que le broker fonctionne correctement. Les outils `mosquitto_sub` (souscription) et `mosquitto_pub` (publication) permettent de tester la communication MQTT directement depuis le terminal.

Pour ce test, vous aurez besoin de **deux terminaux ouverts simultanément** : un pour le récepteur, un pour l'émetteur.

## Souscription (récepteur)

Dans le premier terminal, lancez la commande suivante. Elle reste en attente et affiche chaque message reçu sur le topic `test/topic` :

```bash
mosquitto_sub -h localhost -t "test/topic" -u user1 -P "motdepasse"
```

Options utilisées :
- `-h localhost` : adresse du broker (ici la machine locale)
- `-t "test/topic"` : le topic sur lequel écouter
- `-u user1` : nom d'utilisateur pour l'authentification
- `-P "motdepasse"` : mot de passe associé (attention, `-P` en majuscule)

## Publication (émetteur)

Dans le second terminal, publiez un message :

```bash
mosquitto_pub -h localhost -t "test/topic" -m "Bonjour MQTT" -u user1 -P "motdepasse"
```

L'option `-m` spécifie le contenu du message à envoyer.

Vérifiez que le message "Bonjour MQTT" apparaît dans le premier terminal (côté subscriber). Si c'est le cas, le broker fonctionne correctement avec l'authentification.

---

# 5. Programmation en C avec MQTT

Dans cette partie, vous allez développer des clients MQTT en langage C. La bibliothèque utilisée est **Paho MQTT C**, développée par la fondation Eclipse. Elle fournit une API complète pour se connecter à un broker, publier des messages et souscrire à des topics.

## Installation de la bibliothèque

Le paquet `libpaho-mqtt-dev` contient les fichiers d'en-tête et les bibliothèques nécessaires à la compilation :

```bash
sudo apt install libpaho-mqtt-dev -y
```

---

# 6. Programme C – Publisher

Ce programme se connecte au broker MQTT, publie un unique message sur le topic `test/topic`, puis se déconnecte. Il illustre le fonctionnement de base d'un client éditeur (publisher).

Créez un fichier `pub.c` avec le contenu suivant :

```c
#include <stdio.h>
#include <string.h>
#include "MQTTClient.h"

#define ADDRESS     "tcp://localhost:1883"
#define CLIENTID    "ClientPub"
#define TOPIC       "test/topic"
#define PAYLOAD     "Message depuis C"
#define QOS         1
#define TIMEOUT     10000L

int main() {
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    MQTTClient_deliveryToken token;

    MQTTClient_create(&client, ADDRESS, CLIENTID,
                      MQTTCLIENT_PERSISTENCE_NONE, NULL);

    conn_opts.username = "user1";
    conn_opts.password = "motdepasse";

    MQTTClient_connect(client, &conn_opts);

    pubmsg.payload = PAYLOAD;
    pubmsg.payloadlen = strlen(PAYLOAD);
    pubmsg.qos = QOS;
    pubmsg.retained = 0;

    MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);
    MQTTClient_waitForCompletion(client, token, TIMEOUT);

    MQTTClient_disconnect(client, 1000);
    MQTTClient_destroy(&client);

    return 0;
}
```

---

## Compilation

L'option `-lpaho-mqtt3c` lie le programme avec la bibliothèque Paho MQTT (version synchrone en C) :

```bash
gcc pub.c -o pub -lpaho-mqtt3c
```

---

# 7. Programme C – Subscriber

Ce programme se connecte au broker et souscrit au topic `test/topic`. Il utilise un mécanisme de **callbacks** (fonctions de rappel) : des fonctions que la bibliothèque appelle automatiquement lorsqu'un événement se produit (réception d'un message, perte de connexion, confirmation de livraison).

Créez un fichier `sub.c` avec le contenu suivant :

```c
#include <stdio.h>
#include <stdlib.h>
#include "MQTTClient.h"

#define ADDRESS     "tcp://localhost:1883"
#define CLIENTID    "ClientSub"
#define TOPIC       "test/topic"

void delivered(void *context, MQTTClient_deliveryToken dt) {}

int msgarrvd(void *context, char *topicName, int topicLen, MQTTClient_message *message) {
    printf("Message reçu : %.*s\n", message->payloadlen, (char*)message->payload);
    MQTTClient_freeMessage(&message);
    MQTTClient_free(topicName);
    return 1;
}

void connlost(void *context, char *cause) {
    printf("Connexion perdue\n");
}

int main() {
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;

    MQTTClient_create(&client, ADDRESS, CLIENTID,
                      MQTTCLIENT_PERSISTENCE_NONE, NULL);

    MQTTClient_setCallbacks(client, NULL, connlost, msgarrvd, delivered);

    conn_opts.username = "user1";
    conn_opts.password = "motdepasse";

    MQTTClient_connect(client, &conn_opts);

    MQTTClient_subscribe(client, TOPIC, 1);

    while(1); // boucle infinie

    MQTTClient_disconnect(client, 1000);
    MQTTClient_destroy(&client);

    return 0;
}
```

---

## Compilation

```bash
gcc sub.c -o sub -lpaho-mqtt3c
```

---

# 8. Tests des programmes C

Cette étape permet de vérifier que vos deux programmes communiquent correctement via le broker Mosquitto. Ouvrez deux terminaux distincts.

1. Dans le premier terminal, lancez le subscriber. Il se met en attente de messages :

```bash
./sub
```

2. Dans le second terminal, lancez le publisher. Il envoie un message et se termine :

```bash
./pub
```

3. Observez le premier terminal : le message "Message depuis C" doit s'afficher, confirmant que la communication MQTT fonctionne entre vos deux programmes.

Pour arrêter le subscriber, utilisez `Ctrl+C`.

---

# 9. Questions

Répondez aux questions suivantes en vous appuyant sur le TP et sur vos recherches complémentaires :

1. Quelle est la différence entre les niveaux de qualité de service QoS 0, QoS 1 et QoS 2 en MQTT ?
2. Quel est le rôle du broker dans l'architecture MQTT ? Pourquoi les clients ne communiquent-ils pas directement entre eux ?
3. Pourquoi est-il important de sécuriser l'accès au broker avec une authentification par mot de passe ?
4. Que se passe-t-il pour les clients (publisher et subscriber) si le broker est arrêté ?

---

# 10. Pour aller plus loin

- Ajouter le chiffrement TLS pour sécuriser les échanges entre les clients et le broker
- Implémenter la publication et la souscription sur plusieurs topics différents
- Installer des applications MQTT sur smartphone pour tester depuis un appareil mobile
- Installer les outils graphiques MQTT Explorer et MQTTX pour visualiser les messages échangés

