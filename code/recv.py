import paho.mqtt.client as mqtt
import time
from queue import Queue

def message_recu(client, userdata, message):
   q.put(message)
   #print("message_recu")

client = mqtt.Client("lecteur")
client.connect("127.0.0.1")
client.subscribe("proc/message", 1)
client.on_message = message_recu

q = Queue()

client.loop_start() 
while True:
    if not q.empty():
        message = q.get()
        print("message_recu: ", str(message.payload.decode("utf-8")) )
    else:
        time.sleep(1)

client.loop_stop()
client.disconnect()
   