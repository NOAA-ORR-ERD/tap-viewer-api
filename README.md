TAP Viewer
==========

This project will hold the design discussion and ultimately code, for the new Web-based TAP vieweer.

Project TEAM:
-------------

Gennady Kachook: Web UI developer

Dylan Righi: Back end computation developer and subject matter expert

Chris Barker: Subject mater expert, software architecture support -- maybe some code :-)

Glen Watabayashi: Making sure we get it done on schedule :-)

Running the API Server
======================

* Make sure to activate a relevant virtualenv (if necessary)
* To install the API package:

```
cd TAP_Viewer_API
python setup.py develop
```

* After successful installation run this command:

```
pserve --reload development.ini
```

* Now your server should be running on the port you specified in the development.ini file. The port provided will be displayed after you run the above command.

Existing API Route Structure
============================

The base url of the API will be represented by:

```
base_url
```
Route responses based on route:

```
base_url
```

Hitting the base url will return a plain text response of "Hello!"

```
base_url/locations
```

Will return a JSON response that contains the supported locations.

Schema of response:

```javascript
{
	'locations': [
		{
			'route_name': 'arctic',
			'name': 'US Arctic Waters',
			'lonlat': [-156.79, 71.29]
		},
		...
	]
}
```

```
base_url/locations/{location_name}/setup
```

Will return a JSON response which contains data from the site.txt for the respective location as a JSON file.

```
base_url/locations/{location_name}/impact_analysis
```

Will return a JSON response which contains a randomized 100 element array of floating point numbers that range between 0 and 1. (For prototyping purposes currently)

```
base_url/locations/{location_name}/oiling_analysis
```

Will return a JSON response which contains a randomized 100 element array of floating point numbers that range between 0 and 1. (For prototyping purposes currently)
