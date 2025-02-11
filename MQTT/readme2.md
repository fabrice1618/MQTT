Protocole MQTT
MQTT (Message Queuing Telemetry Transport) est un protocole de messagerie léger et efficace, particulièrement adapté pour l'Internet des Objets (IoT) et la communication Machine-to-Machine (M2M)1
2
Caractéristiques principales

    Protocole basé sur TCP/IP
    Modèle de communication publish/subscribe
    Faible consommation de bande passante
    Adapté aux réseaux peu fiables ou à ressources limitées
    Utilise un broker central pour la gestion des messages

Fonctionnement

    Clients : Peuvent être publishers (émetteurs) ou subscribers (récepteurs)
    Broker : Serveur central qui gère la communication
    Topics : Canaux de communication hiérarchiques

Le modèle de publication/abonnement dans MQTT fonctionne selon les principes suivants :

    Trois composants principaux sont impliqués :
        Publishers (éditeurs) : envoient des messages sur des topics spécifiques
        Subscribers (abonnés) : reçoivent les messages des topics auxquels ils sont abonnés
        Broker (courtier) : élément central qui gère la communication entre publishers et subscribers1
        2
    Le broker découple les publishers des subscribers :
        Les publishers n'ont pas besoin de connaître les subscribers et vice versa
        Le broker filtre et distribue les messages entrants aux subscribers appropriés2
        3
    Processus de communication :
        Les clients MQTT se connectent au broker
        Les clients peuvent publier des messages, s'abonner à des topics, ou les deux
        Lorsqu'un publisher envoie un message sur un topic, le broker le transmet à tous les subscribers abonnés à ce topic3
        4
    Gestion des connexions :
        Si un subscriber est déconnecté, le broker met en mémoire tampon les messages
        Les messages sont transmis au subscriber lors de sa reconnexion4
    Structure des topics :
        Les topics forment une arborescence hiérarchique
        Les clients peuvent s'abonner à des niveaux spécifiques ou utiliser des caractères génériques pour s'abonner à plusieurs niveaux6

Ce modèle permet une communication efficace et flexible entre de nombreux appareils, ce qui en fait une solution idéale pour les applications IoT

Structure des topics

    Utilisation de "/" pour créer une hiérarchie
    Exemple : "capteurs/temperature/salon"
    Wildcards :
        "+" : remplace un niveau
        "#" : remplace plusieurs niveaux

Qualité de Service (QoS)
MQTT offre trois niveaux de QoS4
:

    QoS 0 : Au plus une fois
    QoS 1 : Au moins une fois
    QoS 2 : Exactement une fois

MQTT propose trois niveaux de Qualité de Service (QoS) pour la transmission des messages :
QoS 0 : Au plus une fois

    Le message est envoyé une seule fois, sans garantie de réception1
    2
    .
    Aucun accusé de réception n'est attendu3
    .
    Adapté aux connexions fiables ou lorsque la perte occasionnelle de messages est acceptable3
    5
    .
    Ne nécessite pas de stockage des messages pour les clients déconnectés3
    .

QoS 1 : Au moins une fois

    Garantit que le message est livré au moins une fois, mais peut être reçu plusieurs fois1
    2
    .
    Le broker attend un accusé de réception et renvoie le message si nécessaire3
    .
    Offre un bon compromis entre fiabilité et performance3
    5
    .
    Les messages sont stockés pour les clients déconnectés avec une session permanente3
    .

QoS 2 : Exactement une fois

    Assure que chaque message est reçu une seule fois par le destinataire1
    2
    .
    Utilise un mécanisme de handshake en quatre étapes pour garantir la livraison unique5
    .
    Offre le plus haut niveau de fiabilité, mais avec une surcharge de communication plus importante3
    5
    .
    Recommandé lorsque la duplication des messages peut avoir des conséquences négatives5
    .

Le choix du niveau de QoS dépend des besoins spécifiques de l'application, de la fiabilité du réseau et de la tolérance aux duplicatas ou aux pertes de messages


Mise en pratique
Installation du broker Mosquitto

bash
sudo apt-get install mosquitto

Installation des clients MQTT

bash
sudo apt-get install mosquitto-clients

Commandes de base

    Subscriber : mosquitto_sub -t "topic"
    Publisher : mosquitto_pub -t "topic" -m "message"

Exemple pratique

    Terminal subscriber :

bash
mosquitto_sub -h 192.168.52.12 -t "capteurs/#" -v

Terminal publisher :

    bash
    mosquitto_pub -h 192.168.52.12 -t capteurs/temperature/salon -m 23.0
    mosquitto_pub -h 192.168.52.12 -t capteurs/temperature/chambre -m 21.0

Programmation

    En C : Utiliser la bibliothèque Mosquitto
    En Python : Bibliothèque paho-mqtt recommandée

Avantages de MQTT

    Léger et efficace
    Adapté aux environnements à ressources limitées
    Flexible grâce au système de topics
    Gestion de la qualité de service

