import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

# Configuration du broker MQTT
broker = "mosquitto"  # Remplacez par l'adresse de votre broker MQTT
port = 1883
topic = "bureau/1234"

# Fonction de rappel (callback) lorsque le client se connecte au broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Création d'une instance de client MQTT
client = mqtt.Client()

# Assignation des fonctions de rappel
client.on_connect = on_connect

# Connexion au broker
client.connect(broker, port, 60)

temperature = 20

# Créer un objet datetime représentant minuit du même jour
minuit = datetime.combine(datetime.now().date(), datetime.min.time())
# Calculer la différence en minutes entre le timestamp et minuit
diff = datetime.now() - minuit
minute = int(diff.total_seconds() / 60) - 1 
message = {
    "minute": minute,
    "temperature": temperature
}
message_json = json.dumps(message)
print(f"Publishing message: {message_json}")
client.publish(topic, message_json)

print("Disconnecting from broker")
client.disconnect()