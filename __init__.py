#!/usr/bin/env python3

from rflib import RfCat
from registry import DEVICE_TYPES
from paho.mqtt import client as mqtt_client
from yaml import safe_load as yaml_load
from json import loads as json_loads
from random import randint

def load_config():
    global CONFIG
    fh = open("config.yml", "r")
    CONFIG = yaml_load(fh)
    fh.close()
load_config()

client_id = f"rfcat-mqtt-{randint(0, 1000)}"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            exit(1)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(CONFIG["username"], CONFIG["password"])
    client.on_connect = on_connect
    client.connect(CONFIG["broker"], CONFIG["port"])
    return client

def on_message(client, userdata, msg):
    try:
        data = json_loads(msg.payload.decode())
        ctrlDev = DEVICE_TYPES[data["type"]]
        ctrlDev.initRadio(RFCAT_DEV)
        ctrlDev.send(RFCAT_DEV, data)
    except Exception as e:
        print(e)

def run():
    global RFCAT_DEV
    RFCAT_DEV = RfCat()
    RFCAT_DEV.ping()

    client = connect_mqtt()
    client.subscribe(CONFIG["topic"])
    client.on_message = on_message
    client.loop_forever()

if __name__ == "__main__":
    run()
