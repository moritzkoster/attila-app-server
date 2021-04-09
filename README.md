# Webserver
The webserver for the Scout App of "Pfadi Attila"
see also noahzarro/attila-app
## API
### get activities
`GET: /activities/beavers` returns the JSON-File with all upcomming avtivities from the group *beavers*  
### get images (for the activities card)
`GET: /images/big_chungus.jpg` returns the image with name *big_chungus.jpg*

### new activity
`POST /newactivity` + `data: data for new activity` returns a text message confirming the arrival of a new activity (IMPORTANT: if the activity uses a custom image, the image number has to be specified in the `data` section. see below)

### image for activity
`POST: /imageforactivity` + `data: image` stores the image for later requests. returns the image number for completing the `new activity`-POST from above

## Concepts

### show future acitivites
request the list(s) (`/activities/{grade}`) from the desired grades [beavers, wulfes, scouts, pios] and the needed images `/images/{name}`

### add new activity
send `/imageforactivity`. answer contains a name for the uploaded image. format: `activity_[000000-999999].[jpg, png]` example: `activity_042069.jpg`
recieve answer with image name --> put name in field for image-name
send `/newactivity` with the image name

## Security
### send new activities and images
To set up a new activity, an authentication (but how???) is necessary. This is also necessary for uploading images to protect the server from attacks.
