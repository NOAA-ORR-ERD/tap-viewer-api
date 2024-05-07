TAP Viewer API
==============

Python application served up with Pyramid web framework for the new web-based TAP viewer.

## Project TEAM:

Gennady Kachook: Web UI and back-end API developer
Dylan Righi: Back end computation developer and subject matter expert
Chris Barker: Subject mater expert, software architecture support -- maybe some code :-)

## Project Dependecies and Installation Instructions

In order to run the TAP-Viewer-API you need to install the dependencies:

1) create an environment with the dependencies::
   `conda create -n tap python=3.10 --file conda_requirements.txt`

2) active the environment
   `conda activate tap`

3) install the app:

   `cd TAP-Viewer-API`
   `pip install -e ./`

4) start the app

   `pserve --reload development.ini`

   (the --reload is if you want to change the code under development)



* Now your server should be running on the port specified in the development.ini file. The port provided will be displayed after you run the above command.


## Existing API Route Structure

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
  {'locations': [
            {
              'route_name': 'arctic',
              'name': 'US Arctic Waters',
              'bounding_box': [[-122.707986, 38.1523666],
                               [-121.902153, 37.4429131]]
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
