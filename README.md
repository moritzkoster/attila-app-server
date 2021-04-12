# Webserver
The webserver for the app of our local scout group.
see also [noahzarro/attila-app](https://github.com/noahzarro/attila-app)
## API
### Get activities
`GET: /activities/beavers` returns the JSON-File with all upcomming avtivities from the group *beavers*  
#### Format response
```
{"activities":[
	{
		"id": 0;  
		"name": "Aktivität",
		"date": "01-01-1970",
		"end_date": "02-01-1970",
		"time": "bis am Halbi",
		"place": "Fadihaim",
		"take_away": "Salz",
		"other": "Othermatt",
		"image": "activity_000123.jpg"
	}, ...
]}
```

### Get images (for the activities card)
`GET: /images/big_chungus.jpg` returns the image with name *big_chungus.jpg*

### New activity
`POST /newactivity` + `data: data for new activity` returns a text message confirming the arrival of a new activity (IMPORTANT: if the activity uses a custom image, the image number has to be specified in the `data` section. see below)
#### Format request
```
{
	"id": 0;  
	"name": "Aktivität",
	"date": "01-01-1970",
	"end_date": "02-01-1970",
	"time": "bis am Halbi",
	"place": "Fadihaim",
	"take_away": "Salz",
	"other": "Othermatt",
	"image": "activity_000123.jpg"
}  
```

### Image for activity
`POST: /imageforactivity` + `"file": "image.jpg"` stores the image for later requests. returns the image number for completing the **new activity**-POST from above
#### Format response
```
{
	"name": "activity_[000000-999999].[jpg, png]",
	"old_name": "the_old_name.[jpg, png]"
}
```

## Concepts

### Request future acitivites
request the list(s) (`/activities/{grade}`) from the desired grades [beavers, wulfes, scouts, pios] and the needed images `/images/{name}`

### Add new activity
1. send `/imageforactivity`. answer contains a name for the uploaded image. format:  
`
example: `activity_042069.jpg`  
1. recieve answer with image name --> put name in field for image-name
1. send `/newactivity` with the image name

## Security
### Set up new activities and images
To set up a new activity, an authentication (but how???) is necessary. This is also necessary for uploading images.
