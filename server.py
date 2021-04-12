from flask import Flask, request, render_template, send_from_directory
import json
import os

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_url_path="/static")

@app.route("/activities/<grade>", methods = ["GET"])
def activities(grade):
    if os.path.isfile("data/activities/" + grade + ".json"):                    #test for file
        with open("data/activities/" + grade + ".json") as file:
            data = json.load(file)
            return json.dumps(data)
    else:
        return "Invalid Request: grade <b>" + grade + "</b> does not exist. duu Arsch" #BAD REQUEST

@app.route('/images/<name>', methods = ["GET"])
def images(name):
    if os.path.isfile("data/images/" + name):                                   #test for file
        return send_from_directory("data/images", name)
    else:
        return "Invalid Request: file <b>" + name + "</b> does not exist. duu Arsch" #BAD REQUEST


@app.route('/imageforactivity', methods=['GET', 'POST'])
def upload_image():
    if not authenticate(): #TODO
        return "You are not allowed to do This"

    if request.method == 'POST':
        if 'file' not in request.files: # check if the post request has the file part
            return "Invalid Request: No file part in request"
        file = request.files['file']
        if file.filename == '': #check if no file
            return "Invalid Request: There is no file selected"

        if file and allowed_file(file.filename):
            extension = file.filename.split(".")[1] # check file extension/format
            imagename = get_imagename(extension) #new filename + old extension
            file.save(os.path.join("data/images", imagename)) #save file with new name
            return json.dumps({"name": imagename, "old_name": file.filename}) #retunr confirmation

@app.route('/newactivity', methods=['GET', 'POST'])
def new_activity():
    if not authenticate(): #TODO
        return "You are not allowed to do This"

    if request.method == 'POST':
        if not request.json: # check if the post request has the json part
            return "Invalid Request: No data part in request"
        data = request.json

        #TODO save data
        return "We recieved your stuff, thank you"



@app.route("/<request>")
def bad_request(request):
    return "Invalid Request: <b>" + request + "</b> does not exist. duu Arsch"  #BAD REQUEST

def authenticate():
    return True

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def get_imagename(extension):
    with open('var.json', "r") as f: # open var-file
        var = json.load(f)

    number_image = var["last_image"] +1 #get number for next image
    var["last_image"] = number_image #write the just used image number

    with open('var.json', 'w') as f: # open var-file to write number
        json.dump(var, f) #write

    return "image_" + f'{number_image:06d}' + "." + extension # return filenumber for the next image

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8081", threaded=False)
