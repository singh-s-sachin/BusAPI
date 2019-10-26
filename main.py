from flask import Flask,request,jsonify, make_response
import hashlib
import uuid
import jwt
from pymongo import MongoClient
import json
from datetime import date,time,datetime
from functools import wraps
def server():
    app=Flask(__name__)
    @app.route('/ticket',methods=['POST'])
    def get_ticket():
        data=request.get_json()
        name=data["name"]
        qty=data["qty"]
        mobile=data["mobile"]
        email=data["email"]
        busno=data["busno"]
        try:
            client=MongoClient("localhost",27017)
            db=client.tickets
        except:
            return jsonify({"message":"Database denied connection"})
        seats=client.busdata[busno].find_one()
        seats=seats["booked"]
        if (30-seats)<qty:
            return jsonify({"message":"seats not available","error":401})
        dnt=str(date.today())
        start=seats+1
        seats+=qty
        end=seats
        client.busdata[busno].update_one({},{"$set":{"booked":end}})
        final=str(start)+"-"+str(end)
        k=db[dnt].insert({"_id":str(uuid.uuid4()),"time":str(datetime.now()),"name":name,"mobile":mobile,"email":email,"busno":busno,"seats":final})
        return jsonify({"message":"success","pnr":str(k),"seat":final})
    @app.route('/ticket',methods=['GET'])
    def avaiblity():
        l=[]
        for i in range(12):
            busno=str(i+1)
            client=MongoClient("localhost",27017)
            seats=client.busdata[busno].find_one()
            seats=seats["booked"]
            l.append(seats)
        return jsonify({"update":l})
    @app.route('/detail/pnr',methods=['GET'])
    def pnrval():
        data=request.get_json()
        pnr=data["pnr"]
        client=MongoClient("localhost",27017)
        seats=client.tickets[str(date.today())].find_one({"_id":pnr})
        return seats
    app.run(debug=True)
print("Running server\n\t-via main")
server()