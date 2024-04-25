"""Main script to run MongoDB and MQTT clients."""

from mongo_db import Mongo
from mqtt import MQTT
from signal import pause

mongo = Mongo()
mqtt = MQTT(mongo)

mongo.connect()
mqtt.run()

try:
    pause()
except KeyboardInterrupt:
    pass

mqtt.stop()
mongo.disconnect()