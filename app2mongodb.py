#Goal : app.py to mongoDB
#At : heroku-test sever with coludmongo
#https://cloud.mongodb.com/v2/60dea5002080b87f56f2ec26#clusters
import time
import pymongo
line = [str(n) for n in input().split()]
mydict = {"userID": line[0], "R": line[1], "G": line[2], "B": line[3], "time": time.time()}

USERNAME = 'Add yours'
PASSWORD = 'Add yours'
client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@iot-mongodb.qsu7o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.iot
line_db = db.line
line_db.insert_one(mydict)
##Publish on Line Sever
print(f"UserID: {mydict['userID']}\n(R,G,B): ({mydict['R']},{mydict['G']},{mydict['B']})\nTime: {mydict['time']}",end='')
