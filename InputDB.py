import pymongo
import time
#insert one data into mongodb

USERNAME = 's7023369667'
PASSWORD = '7023369667s'
client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@iot-mongodb.qsu7o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.iot
input_db = db.sensor_input

# Call by "mqtt_ServerToDB.py"
line = input().split()

if len(line) == 6:
  # format in mongoDB
  mydict = {"userID": line[0], "sensor": line[1], "R": line[2], "G": line[3], "B": line[4], "time": time.asctime(time.localtime(time.time()))}
  x = input_db.insert_one(mydict)
else:
  print(line)
  print("Should be 6 objects!")
  quit(1)



