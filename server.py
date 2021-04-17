from flask import Flask, request, render_template, send_from_directory
import json
import os
from flask_cors import CORS

import python.datamgmt as dm
import python.auth as auth

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_url_path="/static")
CORS(app)

@app.route("/activities/<group>", methods = ["GET"])
def activities(group):
    if os.path.isfile("data/activities/" + group + ".json"):                    #test for file
        with open("data/activities/" + group + ".json") as file:
            data = json.load(file)
            return data
    else:
        return "Invalid Request: group <b>" + group + "</b> does not exist. duu Arsch" #BAD REQUEST

@app.route('/images/<name>', methods = ["GET"])
def images(name):
    if os.path.isfile("data/images/" + name):                                   #test for file
        return send_from_directory("data/images", name)
    else:
        return "Invalid Request: file <b>" + name + "</b> does not exist. duu Arsch" #BAD REQUEST


@app.route('/imageforactivity', methods=['GET', 'POST'])
def upload_image():
    if not auth.authenticate(): #TODO
        return "You are not allowed to do This"
    return dm.save_image(request, purpose="activity")


@app.route('/newactivity', methods=['GET', 'POST'])
def new_activity():
    if not auth.authenticate(): #TODO
        return "You are not allowed to do This"
    return dm.new_activity(request)

@app.route('/adaptactivity', methods=['GET', 'POST'])
def adapt_activity():
    if not auth.authenticate(): #TODO
        return "You are not allowed to do This"
    return dm.adapt_activity(request)

@app.route('/deleteactivity', methods=['DELETE'])
def delete_activity():
    if not auth.authenticate(): #TODO
        return "You are not allowed to do This"
    return dm.delete_activity(request)

@app.route("/<request>")
def bad_request(request):
    return "Invalid Request: <b>" + request + "</b> does not exist. duu Arsch"  #BAD REQUEST

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8081", threaded=False)
