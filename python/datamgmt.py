import json
import os

#ACTIVITY-----------------------------------------------------------------------

def new_activity(request):
    if request.method == 'POST':
        if not request.json: # check if the post request has the json part
            return "Invalid Request: No data part in request"
        data = request.json
        append_activity(data)
        return "We recieved your stuff, thank you"

def append_activity(data):
    filename = "data/activities/" + data["grade"] + ".json"
    data["id"] = get_id(data["grade"])
    with open(filename, "r") as f:
        content = json.load(f)
    content["activities"].append(data)
    with open(filename, "w") as f:
        json.dump(content, f, indent=4)

def get_id(grade): #TODO
    return counter(grade)

#IMAGE--------------------------------------------------------------------------

def save_image(request, purpose):
    if request.method == 'POST':
        if 'file' not in request.files: # check if the post request has the file part
            return "Invalid Request: No file part in request"
        file = request.files['file']
        if file.filename == '': #check if no file
            return "Invalid Request: There is no file selected"

        if not allowed_file(file.filename):
            return "Invalid Request: File type is not allowed: " + file.filename

        extension = file.filename.split(".")[1] # check file extension/format
        imagename = get_imagename(purpose, extension) #new filename + old extension
        file.save(os.path.join("data/images", imagename)) #save file with new name
        return json.dumps({"name": imagename, "old_name": file.filename}) #retunr confirmation

def allowed_file(filename):
    ALLOWED_IMAGE_EXTENSIONS = json.load(open("settings.json", "r"))["ALLOWED_IMAGE_EXTENSIONS"]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def get_imagename(purpose, extension):
    number_image = counter("last_image")
    return purpose + "_" + f'{number_image:06d}' + "." + extension # return filenumber for the next image

#COUNTER------------------------------------------------------------------------

def counter(element):
        with open('counter.json', "r", encoding='utf8') as f: # open counter-file
            counter = json.load(f)

        number = counter[element] +1 #get number for next image
        counter[element] = number #write the just used image number

        with open('counter.json', 'w', encoding='utf8') as f: # open counter-file to write number
            json.dump(counter, f, indent=4) #write
        return number
