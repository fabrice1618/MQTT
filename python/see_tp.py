import paho.mqtt.client as mqtt
import time
from queue import Queue
import json
from datetime import datetime, timedelta
import pprint

def message_recu(client, userdata, message):
    #print(f"message_recu({client}, {userdata}, {message})")
    print(f"message_recu {message.topic=}, {message.payload=}" )
    q.put(message)

def minutes_depuis_minuit(timestamp):
    # Convertir le timestamp en objet datetime
    dt = datetime.fromtimestamp(timestamp)
    
    # Créer un objet datetime représentant minuit du même jour
    minuit = datetime.combine(dt.date(), datetime.min.time())
    
    # Calculer la différence en minutes entre le timestamp et minuit
    diff = dt - minuit
    minutes = int(diff.total_seconds() / 60)
    
    return minutes

def temperature_check(minute):
    # Filtrer les mesures, conserver celles de la minute demandée
    temperatures = [x['temperature'] for x in mesures if x['minute'] == minute] 
    pprint.pp(temperatures)
    if len(temperatures) == 0:
        return None
    temperatures.sort()
    ignore_val = len(temperatures) // 4
    temperatures = temperatures[ignore_val:-ignore_val]
    temp_moyenne = round(sum(temperatures) / len(temperatures), 1)
    return temp_moyenne

def process_bureau(topic_parts, payload):
    user_id = topic_parts[1]

    if not 'minute' in payload or not 'temperature' in payload:
        print("structure message incorrecte")
        return

    minute = payload['minute']
    temperature = payload['temperature']
    temp_check = temperature_check(minute)
    print(f"Bureau {temp_check=} {temperature=} {user_id=}")
    if temp_check != temperature:
        print(f" Différence")
    else:
        print(" OK")
    status = "correct" if temp_check == temperature else "incorrect"

    message = {
        "minute": minute,
        "temperature": temperature,
        "temp_check": temp_check,
        "user_id": user_id,
        "status": status,
    }
    message_json = json.dumps(message)
    print(f"Publishing message: {message_json}")
    client.publish("controle", message_json)

def process_temperature(payload):
    global mesures 

    if not 'timestamp' in payload or not 'temperature' in payload:
        print("structure message incorrecte")
        return

    now = datetime.now()
    now_timestamp = now.timestamp()

    if payload['timestamp'] > now_timestamp or \
       payload['timestamp'] < now_timestamp - 10:
        print("message rejected")
        return

    mesure_minute = minutes_depuis_minuit(payload['timestamp'])
    mesure = {"timestamp": payload['timestamp'], "temperature": payload['temperature'], "minute": mesure_minute}
    mesures.append(mesure)

    # Filtrer les mesures pour ne conserver que 2 minutes
    mesures = [x for x in mesures if x['minute'] >= minutes_depuis_minuit(datetime.now().timestamp()) - 2] 


def process_message(message):
    payload = json.loads( str(message.payload.decode("utf-8")) )
    #print(f"{message.topic=} {type(payload)} {payload=}" )
    topic_parts = message.topic.split('/')

    if topic_parts[0] == "bureau":
        process_bureau(topic_parts, payload)
    elif message.topic == "sensors/bureau/temperature":
        process_temperature(payload)


# Programme principal
client = mqtt.Client()
client.connect("mosquitto")
client.subscribe("sensors/bureau/temperature", 1)
client.subscribe("bureau/#", 1)
client.subscribe("controle", 1)
client.on_message = message_recu

q = Queue()     # FIFO
users = dict()
mesures = list()

client.loop_start() 
while True:
    if not q.empty():
        message = q.get()
        process_message(message)
        #pprint.pp(mesures)
    else:
        time.sleep(1)


client.loop_stop()
client.disconnect()
   