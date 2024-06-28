import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

# Configuration du broker MQTT
broker = "mosquitto"  # Remplacez par l'adresse de votre broker MQTT
port = 1883
topic = "user"

# Fonction de rappel (callback) lorsque le client se connecte au broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Création d'une instance de client MQTT
client = mqtt.Client()

# Assignation des fonctions de rappel
client.on_connect = on_connect

# Connexion au broker
client.connect(broker, port, 60)

message = {
    "id": "1573",
}
message_json = json.dumps(message)
print(f"Publishing message: {message_json}")
client.publish(topic, message_json)

print("Disconnecting from broker")
client.disconnect()