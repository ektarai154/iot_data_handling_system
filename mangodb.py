from typing import List
from datetime import datetime
import paho.mqtt.client as mqtt
import pymongo
import pymongo.database
import pymongo.collection
import pymongo.errors
import threading
import os

"""mongo_db.py: Module to handle MongoDB operations."""

# MongoDB configuration variables

MONGO_URI = "mongodb://127.0.0.1:27017"
MONGO_DB = "domotics"
MONGO_COLLECTION = "mqtt"
MONGO_TIMEOUT = 1  # Time in seconds
MONGO_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

# Fetch MongoDB configuration from environment variables if available

MONGO_URI = os.getenv("MONGO_URI", MONGO_URI)
MONGO_DB = os.getenv("MONGO_DB", MONGO_DB)
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", MONGO_COLLECTION)
MONGO_TIMEOUT = float(os.getenv("MONGO_TIMEOUT", MONGO_TIMEOUT))
MONGO_DATETIME_FORMAT = os.getenv("MONGO_DATETIME_FORMAT", MONGO_DATETIME_FORMAT)


class Mongo(object):
    """Class to handle MongoDB operations."""

    def __init__(self):
        self.client: pymongo.MongoClient = None
        self.database: pymongo.database.Database = None
        self.collection: pymongo.collection.Collection = None
        self.queue: List[mqtt.MQTTMessage] = list()

    def connect(self):
        """Connect to MongoDB."""

        print("Connecting Mongo")
        self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT * 1000.0)
        self.database = self.client.get_database(MONGO_DB)
        self.collection = self.database.get_collection(MONGO_COLLECTION)

    def disconnect(self):
        """Disconnect from MongoDB."""

        print("Disconnecting Mongo")
        if self.client:
            self.client.close()
            self.client = None

    def connected(self) -> bool:
        """Check if connected to MongoDB."""

        if not self.client:
            return False
        try:
            self.client.admin.command("ismaster")
        except pymongo.errors.PyMongoError:
            return False
        else:
            return True

    def _enqueue(self, msg: mqtt.MQTTMessage):
        print("Enqueuing")
        self.queue.append(msg)

    def __store_thread_f(self, msg: mqtt.MQTTMessage):
        print("Storing")
        now = datetime.now()
        try:
            document = {
                "topic": msg.topic,
                "payload": msg.payload.decode(),
                "qos": msg.qos,
                "timestamp": int(now.timestamp()),
                "datetime": now.strftime(MONGO_DATETIME_FORMAT),
            }
            result = self.collection.insert_one(document)
            print("Saved in Mongo document ID", result.inserted_id)
            if not result.acknowledged:
                # Enqueue message if it not saved properly
                self._enqueue(msg)
        except Exception as ex:
            print(ex)

    def _store(self, msg):
        th = threading.Thread(target=self.__store_thread_f, args=(msg,))
        th.daemon = True
        th.start()

    def save(self, msg: mqtt.MQTTMessage):
        """Save MQTT message to MongoDB."""

        print("Saving")
        if msg.retain:
            print("Skipping retained message")
            return
        if self.connected():
            self._store(msg)
        else:
            self._enqueue(msg)
