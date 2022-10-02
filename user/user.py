from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

import grpc
from concurrent import futures
# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

def existsUser(userId):
   for user in users:
        if str(user["id"]) == str(userId): return True
   return False

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/bookings/<nameorid>", methods=['GET'])
def get_bookings_bynameorid(nameorid):
   for user in users:
        if str(user["name"]) == str(nameorid) or str(user["id"]) == str(nameorid):
            return make_response(jsonify(requests.get('http://booking:3201/bookings/'+user["id"]).json()),200)
   return make_response(jsonify({"error":"user not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def create_booking(userid):
   req = request.get_json()
   if existsUser(userid):
      return make_response(jsonify(requests.post('http://booking:3201/bookings/'+userid, json=req).json()),200)
   return make_response(jsonify({"error":"user not found"}),400)

@app.route("/movies/<userid>", methods=['GET'])
def get_info_movies(userid):
   if existsUser(userid):
      bookings = requests.get('http://booking:3201/bookings/'+userid).json()
      for date in bookings["dates"]:
         movies= []
         for movieid in date["movies"]:
            movies.append(requests.get('http://movie:3200/movies/'+movieid).json())
         date["movies"] = movies

      return make_response(jsonify(bookings),200)
   return make_response(jsonify({"error":"user not found"}),400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
