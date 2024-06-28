import random
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Configuration du broker MQTT
broker = "mosquitto"  # Remplacez par l'adresse de votre broker MQTT
port = 1883
topic = "sensors/bureau/temperature"

# Fonction pour générer une température aléatoire centrée autour de 21 degrés
def generate_random_temperature():
    return round(random.uniform(19, 23), 1)

# Fonction de rappel (callback) lorsque le client se connecte au broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Création d'une instance de client MQTT
client = mqtt.Client()

# Assignation des fonctions de rappel
client.on_connect = on_connect

# Connexion au broker
client.connect(broker, port, 60)

# Boucle principale pour envoyer les valeurs de température
try:
    while True:
        temperature = generate_random_temperature()
        timestamp = int(datetime.now().timestamp())
        message = {
            "timestamp": timestamp,
            "temperature": temperature
        }
        message_json = json.dumps(message)
        print(f"Publishing message: {message_json}")
        client.publish(topic, message_json)
        if timestamp % 2 == 0:
            temperature += 10 if timestamp % 3 == 0 else -10
            timestamp += 150 if timestamp % 3 == 0 else -150
            message = {
                "timestamp": timestamp,
                "temperature": round(temperature, 1)
            }
            message_json = json.dumps(message)
            print(f"Publishing message: {message_json}")
            client.publish(topic, message_json)

        time.sleep(5)
except KeyboardInterrupt:
    print("Disconnecting from broker")
    client.disconnect()
