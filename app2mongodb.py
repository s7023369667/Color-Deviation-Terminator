#app.py to mongoDB
#https://cloud.mongodb.com/v2/60dea5002080b87f56f2ec26#clusters
import time
import pymongo

line = [str(n) for n in input().split()]
mydict = {"userID": line[0], "R": line[1], "G": line[2], "B": line[3], "time": time.asctime(time.localtime(time.time()))}

USERNAME = 's7023369667'
PASSWORD = '7023369667s'
client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@iot-mongodb.qsu7o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.pythondb
line_sever_db = db.line_sever
line_sever_db.insert_one(mydict)

print("Publish on Line Sever:\n" + f"<UserID> {mydict['userID']}\n<R> {mydict['R']}\n<G> {mydict['G']}\n<B> {mydict['B']}\n<Time>{ mydict['time']}",end='')
#print("Publish on Line Sever : " + "{userID} {R} {G} {B} {time}".format(**mydict))
