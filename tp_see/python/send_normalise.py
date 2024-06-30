import json
from datetime import datetime
import time
import config
from Messages import Messages

def main():
    Messages.open(config.BROKER_URL)

    # Créer un objet datetime représentant minuit du même jour
    minuit = datetime.combine(datetime.now().date(), datetime.min.time())
    # Calculer la différence en minutes entre maintenant et minuit
    diff = datetime.now() - minuit
    minute = int(diff.total_seconds() / 60) - 1 
    message = {
        "name": "test user",
        "minute": minute,
        "temperature": 20
    }

    Messages.publish(config.TOPIC_NORMALISE, message)
    Messages.close()

if __name__ == "__main__":
    main()
