import paho.mqtt.client as mqtt
from paho.mqtt.enums import MQTTProtocolVersion
from queue import Queue
import json
import config

# Messages MQTT
class Messages:
    _client = None
    _fifo = None
    _debug = None

    @classmethod
    def open(cls, broker_url, broker_port=1883, abonnements=None, debug=False):
        cls._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        cls._client.username_pw_set(username=config.BROKER_USER, password=config.BROKER_PWD)
        cls._client.connect(broker_url, broker_port, 60)

        cls._fifo = Queue()
        cls._client.on_message = cls.message_recu
        cls._debug = debug

        if abonnements is not None:
            for abonnement in abonnements:
                cls._client.subscribe(abonnement, 1)

        cls._client.loop_start() 

    @classmethod
    def message_recu(cls, client, userdata, message):
        message.payload = json.loads( str(message.payload.decode("utf-8")) )
        if cls._debug:
            print(f"message_recu => {message.topic}, {message.payload}" )
        cls._fifo.put(message)

    @classmethod
    def empty(cls):
        return cls._fifo.empty()

    @classmethod
    def get(cls):
        return cls._fifo.get()

    @classmethod
    def publish(cls, topic, message):
        message_json = json.dumps(message)
        if cls._debug:
            print(f"publish => {topic}, {message_json}" )
        cls._client.publish(topic, message_json)

    @classmethod
    def close(cls):
        cls._client.loop_stop()
        cls._client.disconnect()
