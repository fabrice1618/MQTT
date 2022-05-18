import paho.mqtt.client as mqtt
import time
from queue import Queue
import json

def message_recu(client, userdata, message):
    print("RCV ", message.topic, message.payload )
    if message.topic != "alarme/session":
        q.put(message)

def print_zones():
    for i in range(10):
        print(i,zones[i])

def connect_zone(cnx_zone):
    global zones

    if zones[cnx_zone] ==  False:
        zones[cnx_zone] = True
        cnx_status = cnx_zone
    else:
        cnx_status = -cnx_zone

    client.publish("alarme/session", cnx_status)
    print("SND alarme/session", cnx_status )


# Programme principal
client = mqtt.Client("backend")
client.connect("mosquitto")

client.subscribe("alarme/#", 1)
client.on_message = message_recu

# intialisation des zones
zones = []
for zone in range(10):
    zones.append(False)
print_zones()

q = Queue()     # FIFO

client.loop_start() 
while True:
    if not q.empty():
        message = q.get()
        if message.topic == "alarme/connecte":
            connect_zone(int(message.payload))
            print_zones()

        else:
            print("message_topic: ", message.topic )
            print("message_recu: ", str(message.payload.decode("utf-8")) )
    else:
        time.sleep(1)

client.loop_stop()
client.disconnect()
   