#!/usr/bin/env python3

from os import getenv
from rflib import RfCat
from registry import DEVICE_TYPES
from paho.mqtt import client as mqtt_client
from yaml import safe_load as yaml_load
from json import loads as json_loads
from random import randint

def load_config():
    global _CONFIG
    try:
        fh = open("config.yml", "r")
        _CONFIG = yaml_load(fh)
        fh.close()
    except FileNotFoundError:
        print("Config file not found, hope we got environment variables set...")
        _CONFIG = {}

def config_get(key, default=None):
    env = getenv(f"RFCAT_MQTT_{key.upper()}")
    if env is not None:
        return env
    if key not in _CONFIG:
        return default
    return _CONFIG[key]

def config_get_int(key, default=None):
    return int(config_get(key, default))

client_id = f"rfcat-mqtt-{randint(0, 1000)}"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code", rc)
            exit(1)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(config_get("username"), config_get("password"))
    client.on_connect = on_connect
    client.connect(config_get("broker"), config_get_int("port", 1883))
    return client

def on_message(client, userdata, msg):
    try:
        data_raw = msg.payload.decode()
        print("Got MQTT", data_raw)
        data = json_loads(data_raw)
        ctrlDev = DEVICE_TYPES[data["type"]]
        ctrlDev.send(RFCAT_DEV, data)
    except Exception as e:
        print(e)

def run():
    global RFCAT_DEV
    RFCAT_DEV = RfCat()
    RFCAT_DEV.ping()

    load_config()

    client = connect_mqtt()
    client.subscribe(config_get("topic"))
    client.on_message = on_message
    client.loop_forever()

if __name__ == "__main__":
    run()
