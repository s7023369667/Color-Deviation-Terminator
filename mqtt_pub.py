#app.py to mongoDB
#https://cloud.mongodb.com/v2/60dea5002080b87f56f2ec26#clusters
import time
import pymongo

line = [str(n) for n in input().split()]

USERNAME = 's7023369667'
PASSWORD = '7023369667s'
client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@iot-mongodb.qsu7o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.pythondb
mydict = {"userID": line[0], "R": line[1], "G": line[2], "B": line[3], "time": time.time()}
line_sever = db.mydicts
line_sever.insert_one(mydict)

print("Publish on Line Sever : " + "{userID} {R} {G} {B} {time}".format(**mydict))
