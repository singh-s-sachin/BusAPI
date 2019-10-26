from pymongo import MongoClient
from main import server
client=MongoClient("localhost",27017)
db=client.busdata
if len(db.list_collection_names())==0:
    print("Setting up")
    for i in range(12):
        k=db[str(i+1)].insert_one({"booked":0})
        if i==6:
            print("Processing")
    print("Database setup done")
    print("Referring to main")
    server()
else:
    print("Referring to main")
    server()