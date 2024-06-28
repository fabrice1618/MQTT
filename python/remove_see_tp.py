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
    if len(temperatures) == 0:
        return None
    temperatures.sort()
    ignore_val = len(temperatures) // 4
    temperatures = temperatures[ignore_val:-ignore_val]
    temp_moyenne = round(sum(temperatures) / len(temperatures), 1)
    return temp_moyenne


def exist_name(name):
    global users

    for key, val in users.items():
        if val['name'] == name:
            return True

    return False

def get_id(name):
    global users

    calc_id = 0
    for car in name:
        calc_id += ord(car)

    while str(calc_id) in users:
        calc_id += 1

    return str(calc_id)

def process_user(topic_parts, payload):
    print(f"{topic_parts=}")
    if len(topic_parts) == 1:
        # Envoyer enregistrement user
        user_id = payload['id']
        print(f"user record {user_id=}")
        if user_id in users:
            user = users[user_id]
            print(f"{user_id=} {user["name"]} {user["correct"]} {user["incorrect"]}")
            message = {
                "id": user_id,
                "name": user["name"],
                "correct": user["correct"],
                "incorrect": user["incorrect"],
            }
            message_json = json.dumps(message)
            print(f"Publishing message: {message_json}")
            client.publish(f"user/{user_id}", message_json)
    else:
        if topic_parts[1] == "join":
            if not 'name' in payload:
                print("structure message incorrecte")
                return
            if exist_name(payload['name']):
                print(f"Duplicate {payload['name']}")
                return

            user_id = get_id(payload['name'])
            users[user_id] = {'name': payload['name'], 'correct': 0, 'incorrect': 0}
            print(users)


def process_bureau(topic_parts, payload):
    user_id = topic_parts[1]

    if not 'minute' in payload or not 'temperature' in payload:
        print("structure message incorrecte")
        return

    temp_check = temperature_check(payload['minute'])
    print(f"Bureau {temp_check=} {payload['temperature']=} {user_id=}")
    if temp_check != payload['temperature']:
        print(f" Différence")
    else:
        print(" OK")

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

    if topic_parts[0] == "user":
        process_user(topic_parts, payload)
    elif topic_parts[0] == "bureau":
        process_bureau(topic_parts, payload)
    elif message.topic == "sensors/bureau/temperature":
        process_temperature(payload)


# Programme principal
client = mqtt.Client()
client.connect("mosquitto")
client.subscribe("user/#", 1)
client.subscribe("sensors/bureau/temperature", 1)
client.subscribe("bureau/#", 1)
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
   