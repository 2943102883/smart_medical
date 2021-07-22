from threading import Thread

from django.test import TestCase

# Create your tests here.
# encoding: utf-8


import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    # print("Connected with result code " + str(rc))
    client.subscribe("hum")


def on_message(client, userdata, msg):
    # print(msg.topic + " " + ":" + str(msg.payload))
    # print(msg.payload)
    global hum
    hum = str(msg.payload, encoding='utf-8')
    print(hum)
    quit()  # 停止程序


def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("101.201.181.46", 1883, 60)
    client.loop_forever()
