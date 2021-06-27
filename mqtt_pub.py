import paho.mqtt.client as mqtt
import time


client = mqtt.Client()
client.username_pw_set("iot", "server")
client.connect("34.80.234.217", 1883, 60)

line = [str(n) for n in input().split()]
mydict = {"userID": line[0], "R": line[1], "G": line[2], "B": line[3], "time": time.time()}
client.publish("Line Server", "{userID} {R} {G} {B} {time}".format(**mydict))

print("Published : " + "{userID} {R} {G} {B} {time}".format(**mydict))
