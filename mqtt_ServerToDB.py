import subprocess as sp
import paho.mqtt.client as mqtt
import sys
from collections import Counter, defaultdict
import ast

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Server")

def on_message(client, userdata, msg):
    received = msg.payload
    p = sp.Popen(['python3', 'InputDB.py'], stdout=sp.PIPE, stdin=sp.PIPE)
    p.stdin.write(received)
    
    out = p.communicate()
    p.stdin.close()
    print(out)
    
    #print(msg.topic+" "+ msg.payload.decode('utf-8'))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("iot", "server")
client.connect("localhost", 1883, 60)

client.loop_forever()

