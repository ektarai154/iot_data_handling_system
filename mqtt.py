import paho.mqtt.client as mqtt
from mongo_db import Mongo
import os

"""mqtt.py: Module to handle MQTT client."""

# MQTT configuration variables
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_QOS = 2
MQTT_TOPICS = ("#",)  # '#' subscribe to ALL available topics

MQTT_BROKER = os.getenv("MQTT_BROKER", MQTT_BROKER)
MQTT_PORT = os.getenv("MQTT_PORT", MQTT_PORT)
MQTT_KEEPALIVE = os.getenv("MQTT_KEEPALIVE", MQTT_KEEPALIVE)
MQTT_QOS = os.getenv("MQTT_QOS", MQTT_QOS)
MQTT_TOPICS = os.getenv("MQTT_TOPICS", MQTT_TOPICS)
if isinstance(MQTT_TOPICS, str):
    MQTT_TOPICS = [e.strip() for e in MQTT_TOPICS.split(",")]


class MQTT(object):
    """Class to handle MQTT client."""

    def __init__(self, mongo: Mongo):
        self.mongo: Mongo = mongo
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    # noinspection PyUnusedLocal
    @staticmethod
    def on_connect(client: mqtt.Client, userdata, flags, rc):
        """Callback function when MQTT client connects."""

        print("Connected MQTT")
        for topic in MQTT_TOPICS:
            client.subscribe(topic, MQTT_QOS)

    # noinspection PyUnusedLocal
    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        """Callback function when MQTT client receives a message."""

        print("Rx MQTT")
        self.mongo.save(msg)

    def run(self):
        """Start MQTT client."""

        print("Running MQTT")
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        self.mqtt_client.loop_start()

    def stop(self):
        """Stop MQTT client."""

        print("Stopping MQTT")
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
