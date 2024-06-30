import config
import random
import time
from datetime import datetime

from Messages import Messages

def good_data():
    temperature = round(random.uniform(19, 23), 1)
    timestamp = int(datetime.now().timestamp())
    mesure = {
        "timestamp": timestamp,
        "temperature": temperature
    }
    return mesure

def bad_data():
    temperature = random.uniform(19, 23) + random.choice([-10, 10])
    timestamp = int(datetime.now().timestamp()) + random.choice([-150, 150])
    mesure = {
        "timestamp": timestamp,
        "temperature": round(temperature, 1)
    }
    return mesure

# Boucle principale pour envoyer les valeurs de température
def main():
    Messages.open(config.BROKER_URL)

    try:
        while True:
            mesure = good_data()
            Messages.publish(config.TOPIC_SENSOR, mesure)

            if random.randint(0, 10) % 2 == 0:
                mesure = bad_data()
                Messages.publish(config.TOPIC_SENSOR, mesure)

            time.sleep(5)
    finally:
        Messages.close()

if __name__ == "__main__":
    main()
