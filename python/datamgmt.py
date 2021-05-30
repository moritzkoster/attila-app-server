import json
import os
import re

# ACTIVITY ---------------------------------------------------------------------

# creates a new activity
def new_activity(request):
    if request.method == 'POST':
        if not request.json: # check if the post request has the json part
            return "Invalid Request: No data part in request", 400
        new_activity = request.json

        data = test_data(data)

        new_activity["id"] = generate_id(new_activity["group"])
        activities = get_activities(new_activity["group"])
        activities.append(new_activity)

        write_activities(activities)

        return "We recieved your stuff, thank you"

# changes an activity
def adapt_activity(request):
    if request.method == 'POST':
        if not request.json:
            return "Invalid Request: No data part in request", 400
        activity = request.json

        data = test_data(data)

        activities = get_activities(activity["group"])
        old_activity = get_by_id(activity["id"], activities)
        for key, value in activity.items():
            old_activity[key] = value
        write_activities(activities)
        return "We recieved your stuff, thank you"

# deletes an activity
def delete_activity(request):
    if request.method == 'DELETE':
        if not request.json:
            return "Invalid Request: No data part in request", 400

        activity = request.json
        activities = get_activities(activity["group"])
        activity = get_by_id(activity["id"], activities)
        activities.remove(activity)

        write_activities(activities)
        return "We deleted your stuff, thank you"

# appends an activity to an array. NOT USED
def append_activity(data):
    filename = f"data/activities/{data['group']}.json"
    data["id"] = generate_id(data["group"])
    with open(filename, "r") as f:
        content = json.load(f)
    content["activities"].append(data)
    with open(filename, "w") as f:
        json.dump(content, f, indent=4)

# saves an array of activities
def write_activities(data):
    content = {"activities": data}
    filename = f"data/activities/{data[0]['group']}.json" #ugly: group is read of first element
    with open(filename, "w") as f:
        json.dump(content, f, indent=4)

# generates an ID for an activity
def generate_id(group):
    return counter(group)

# returns an the activity with a given ID out of an array of activities
def get_by_id(id, activities):
    for activity in activities:
        if activity["id"] == int(id):
            return activity
    return False

# returns activities of a specific gorup
def get_activities(group):
    return json.load(open(f"data/activities/{group}.json", "r"))["activities"]

# IMAGE ------------------------------------------------------------------------

# saves an image (if correct) with a uniqe name
def save_image(request, purpose):
    if request.method == 'POST':
        if 'file' not in request.files: # check if the post request has the file part
            return "Invalid Request: No file part in request", 400
        file = request.files['file']
        if file.filename == '': #check if no file
            return "Invalid Request: There is no file selected", 400

        if not allowed_file(file.filename):
            return "Invalid Request: File type is not allowed: " + file.filename, 400

        extension = file.filename.split(".")[1] # check file extension/format
        imagename = get_imagename(purpose, extension) #new filename + old extension
        file.save(os.path.join("data/images", imagename)) #save file with new name
        return json.dumps({"name": imagename, "old_name": file.filename}) #retunr confirmation

# tests if a file (image) is allowed (name and extension). returns bool
def allowed_file(filename):
    ALLOWED_IMAGE_EXTENSIONS = json.load(open("settings.json", "r"))["ALLOWED_IMAGE_EXTENSIONS"]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

# creates a unique image name
def get_imagename(purpose, extension):
    number_image = counter("last_image")
    return f'{purpose}_{number_image:06d}.{extension}' # return filenumber for the next image

# TEST -------------------------------------------------------------------------

# tests new data and replaces outdated information
def test_data(data):
    for key in ["name", "place", "take_away", "other"]:
        data[key] = re.sub(r"Übung", "Aktivität", data[key])
        data[key] = re.sub(r"übung", "aktivität", data[key])
    return data

# COUNTER ----------------------------------------------------------------------

# returns a number, increases it every call by one.
def counter(element):
        with open('counter.json', "r", encoding='utf8') as f: # open counter-file
            counter = json.load(f)

        number = counter[element] +1 #get number for next image
        counter[element] = number #write the just used image number

        with open('counter.json', 'w', encoding='utf8') as f: # open counter-file to write number
            json.dump(counter, f, indent=4) #write
        return number
