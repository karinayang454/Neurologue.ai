"""EE 250L Lab 04 Starter Code
Run vm_subscriber.py in a separate terminal on your VM."""
import requests
import sys
import time
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("medesign/demo")

#Default message callback.
def on_message(client, userdata, msg):
    #emotion = str(msg.payload, "utf-8")
    print("Write")
    f = open('new.wav', 'wb')
    f.write(msg.payload)
    f.close()


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)

