import paho.mqtt.client as mqtt
import time

#IP="34.80.234.217"  #GCP
IP = "34.238.108.61" #heroku fixie proxy IP address

client = mqtt.Client()
client.username_pw_set("iot", "server")
client.connect(IP, 1883, 60)
print(f"IP:{IP}")
line = [str(n) for n in input().split()]
mydict = {"userID": line[0], "R": line[1], "G": line[2], "B": line[3], "time": time.time()}
client.publish("Line Server", "{userID} {R} {G} {B} {time}".format(**mydict))

print("Published : " + "{userID} {R} {G} {B} {time}".format(**mydict))
