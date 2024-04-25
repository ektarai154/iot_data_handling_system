# MQTT to MongoDB Bridge

This project implements a bridge between MQTT (Message Queuing Telemetry Transport) and MongoDB, allowing messages received via MQTT to be stored in a MongoDB database. It consists of two main components: a MongoDB client (`mongo_db.py`) and an MQTT client (`mqtt.py`), orchestrated by the main script (`__main__.py`).

## Components

### `main.py`

This script serves as the entry point for the application. It initializes instances of the MongoDB and MQTT clients, connects to MongoDB, starts the MQTT client, and waits for a keyboard interrupt to gracefully shut down the application.

### `mongodb.py`

This module provides functionality to interact with MongoDB. It includes a `Mongo` class with methods for connecting to MongoDB, disconnecting, saving messages to the database, and handling message storage asynchronously using threads.

### `mqtt.py`

This module implements the MQTT client. It subscribes to specified MQTT topics, receives messages, and forwards them to the MongoDB client for storage. The `MQTT` class defines callback functions for handling MQTT connection events and message reception.

## Installation and Usage

1. Clone this repository:

   ```bash
   
