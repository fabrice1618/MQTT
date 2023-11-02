import paho.mqtt.client as mqtt
import time
from queue import Queue
import json

def message_recu(client, userdata, message):
    print(f"message_recu({client}, {userdata}, {message})")
#    print("RCV ", message.topic, message.payload )
    q.put(message)


# Programme principal
client = mqtt.Client("backend")
client.connect("mosquitto")
#client.subscribe("sensor/#", 1)
client.subscribe("sensor/hello", 1)
client.subscribe("sensor/client", 1)
client.on_message = message_recu

q = Queue()     # FIFO

client.loop_start() 
while True:
    print("boucle...")
    if not q.empty():
        message = q.get()
        print("message_topic: ", message.topic )
        print("message_recu: ", str(message.payload.decode("utf-8")) )
    else:
        time.sleep(1)

client.loop_stop()
client.disconnect()
   