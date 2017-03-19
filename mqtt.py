#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main script for connecting to a MQTT queue """

import paho.mqtt.client as mqtt
import configparser

TOPICS = [
    'stereo',
    'lights',
    'homeApp'
]


def on_message(client, userdata, msg, ):
    print("{} Payload -> {}"
        .format(
            msg.topic,
            msg.payload.decode()
        ))

    client.publish('output', msg.payload.decode())


def on_publish(client, userdata, messageId):
    print("MessageID: "+str(messageId))


def on_subscribe(client, userdata, messageId, granted_qos):
    print("Subscribed: "+str(messageId)+" "+str(granted_qos))


def on_log(client, userdata, level, string):
    print(string)


if __name__ == "__main__":
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    client = mqtt.Client()
    client.username_pw_set(cfg['DEFAULT']['user'], cfg['DEFAULT']['pass'])
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    try:
        client.connect(cfg['DEFAULT']['url'], int(cfg['DEFAULT']['port']), 60)

        for topic in TOPICS:
            client.subscribe(topic, 0)

        client.loop_forever()

    except KeyboardInterrupt:
        print("\nMQTT Ended")

    finally:
        client.disconnect()