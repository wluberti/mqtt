#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main script for connecting to a MQTT queue """

import paho.mqtt.client as mqtt
import configparser

topic_names = []


def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))


def on_message(mqtt, obj, msg, ):
    # print(msg.topic + " " + str(msg.payload))
    payload = str(msg.payload.decode())
    print(msg.topic + " Payload -> " + payload)
    topic_names.append(msg.topic)


def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


if __name__ == "__main__":
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    client = mqtt.Client()
    client.username_pw_set(cfg['DEFAULT']['user'], cfg['DEFAULT']['pass'])
    client.on_message = on_message

    try:
        client.connect(cfg['DEFAULT']['url'], int(cfg['DEFAULT']['port']), 60)
        client.subscribe("stereo", 0)
        client.subscribe("lights", 0)
        client.loop_forever()

    except KeyboardInterrupt:
        print("Received topics:")
        for topic in topic_names:
            print(topic)

    finally:
        client.disconnect()