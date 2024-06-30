import config
import time
from datetime import datetime
import pprint
from Messages import Messages
from Mesures import Mesures


def process_normalise(payload):
    if not 'name' in payload or \
       not 'minute' in payload or \
       not 'temperature' in payload:
        print("structure message incorrecte")
        return

    minute = payload['minute']
    temperature = payload['temperature']
    temp_check = Mesures.temperature_normalise(minute)
    status = "correct" if temp_check == temperature else "incorrect"

    message = {
        "user_name": payload['name'],
        "minute": minute,
        "temperature": temperature,
        "temp_check": temp_check,
        "status": status,
    }
    Messages.publish(config.TOPIC_CONTROLE, message)


def process_temperature(payload):
    if not 'timestamp' in payload or not 'temperature' in payload:
        print("structure message incorrecte")
        return

    now_timestamp = datetime.now().timestamp()

    # Filtrer les mesures de plus de 10 secondes et celles du futur
    if payload['timestamp'] > now_timestamp or \
       payload['timestamp'] < now_timestamp - 10:
        #print("message rejected")
        return

    Mesures.stocker(payload)


def process_message(message):
    if message.topic == config.TOPIC_NORMALISE:
        process_normalise(message.payload)
    elif message.topic == config.TOPIC_SENSOR:
        process_temperature(message.payload)


# Programme principal
def main():
    abonnements = [
        config.TOPIC_SENSOR,
        config.TOPIC_NORMALISE,
        config.TOPIC_CONTROLE,
    ]
    Messages.open(config.BROKER_URL, abonnements=abonnements, debug=True)
    Mesures.clear()

    while True:
        if not Messages.empty():
            message = Messages.get()
            process_message(message)
            #pprint.pp(Mesures.values())
        else:
            time.sleep(1)

    Messages.close()

if __name__ == "__main__":
    main()