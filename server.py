from flask import Flask, request, render_template, send_from_directory
import json
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files: # check if the post request has the file part
            #flash('No file part')
            #print("No file part in request")
            return "No file part in request"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '': #check if no file
            #flash('No selected file')
            #print("No file")
            return "there is no file"
        if file and allowed_file(file.filename): # check file extension/format
            imagename = get_imagename() + "." + file.filename.split(".")[1] #new filename + old extension
            file.save(os.path.join("data/images", imagename)) #save file with new name
            return json.dumps({"name": imagename, "old_name": file.filename}) #retunr confirmation


@app.route("/<request>")
def bad_request(request):
    return "Invalid Request: <b>" + request + "</b> does not exist. duu Arsch"  #BAD REQUEST


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_imagename():
    r = 0
    var = ""
    with open('var.json', "r") as f: # open var-file
        var = json.load(f)
        number_image = var["last_image"] +1 #get number for next image

    with open('var.json', 'w') as f: # open var-file to write number
        var["last_image"] = number_image #write the just used image number
        json.dump(var, f) #write
        return "image_" + f'{number_image:06d}' # return filenumber for the next image

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8081", threaded=False)
