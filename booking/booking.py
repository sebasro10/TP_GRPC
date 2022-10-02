from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3003
HOST = '0.0.0.0'

with open('{}/data/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_bookings():
    res = make_response(jsonify(bookings), 200)
    return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_byuserid(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
    return make_response(jsonify({"error":"userid not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def create_booking(userid):
    req = request.get_json()
    times = requests.get('http://showtime:3202/showtimes').json()["schedule"]
    
    existsTime = False
    for time in times:
        if str(time["date"]) == str(req["date"]):
            if str(req["movieid"]) in time["movies"]: existsTime = True
    if not existsTime: return make_response(jsonify({"error":"schedule does not exist"}),400)

    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            for date in booking["dates"]:
                if str(date["date"]) == str(req["date"]):
                    if str(req["movieid"]) in date["movies"]:
                        return make_response(jsonify({"error":"item already exists"}),409)
            booking["dates"].append({"date":req["date"],"movies":[req["movieid"]]})
            return make_response(jsonify(booking),200)

    reqBooking = {"dates":[{"date":req["date"],"movies":[req["movieid"]]}],"userid":userid}
    bookings.append(reqBooking)
    return make_response(jsonify(reqBooking),200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
