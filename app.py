from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.json_util import ObjectId
from helpers import find_activities
import json
import os


##json format for document from MongoDB
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)


app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

app.json_encoder = MyEncoder


@app.route("/", methods=["POST"])
def handle_user_input():
    data = request.json
    results = find_activities(mongo, data)
    return results
