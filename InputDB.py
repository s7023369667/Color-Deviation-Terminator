import pymongo
import time

myclient = pymongo.MongoClient("mongodb://localhost:6666/")
myclient["iot"].authenticate("iot666", "iot666")
mydb = myclient["iot"]
mycol = mydb["test"]

# Call by "mqtt_ServerToDB.py"
line = input().split()

if len(line) == 6:
  # format in mongoDB
  mydict = {"userID": line[0], "sensor": line[1], "R": line[2], "G": line[3], "B": line[4], "time": time.time()}
  x = mycol.insert_one(mydict)
else:
  print(line)
  print("Should be 6 objects!")
  quit(1)



