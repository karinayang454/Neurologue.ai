from flask import Flask
from flask import request
from flask import render_template
import os

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)



import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def send_mqtt(emotion):
    client = mqtt.Client()
    #client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()
    f = open("audio.wav", "rb")
    imagestring = f.read()
    f.close()
    byteArray = bytearray(imagestring)
    client.publish("medesign/demo", byteArray)
    print("audio published!")