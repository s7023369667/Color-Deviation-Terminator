import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:6666/")
myclient["iot"].authenticate("iot666","iot666")
mydb = myclient["iot"]
mycol = mydb["test"]

x = mycol.delete_many({})

print(x.deleted_count)
