TAP Viewer API
==============

This application is a JSON API -- no nifty html here


Running the API Server
----------------------

You must have already done this or you wouldn't be seeing this page :-)

Make sure to activate a relevant virtualenv (if necessary)

To install the API package::

  cd TAP_Viewer_API
  python setup.py develop

After successful installation run this command:

::

  pserve --reload development.ini


Now your server should be running on the port you specified in the development.ini file. The port provided will be displayed after you run the above command.

API Route Structure
-------------------

The base url of the API will be represented by::

  base_url

Route responses based on route::

  base_url


Hitting the base url will return this document.

::

  base_url/locations

Will return a JSON response that contains the supported locations.

Schema of response:

.. code-block:: javascript

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

::

  base_url/locations/{location_name}/setup

Will return a JSON response which contains data from the site.txt for the respective location as a JSON file.

::

  base_url/locations/{location_name}/map

Will return a response which contains the base map as land polygons as geoJSON

::

  base_url/locations/{location_name}/receptors

Will return a JSON response which contains the receptors as geoJSON


::

  base_url/locations/{location_name}/impact_analysis

and sending JSON data (example):

::

    {
    "season": "winter",
    "oil_type": "diesel",
    "source_id": 3,
    "amount_spilled": [1000, "bbl"],
    "level_of_concern": [1.5, "bbl"],
    "output_time_index": 3
    }

output_time is an index into the output times array.


Will return a JSON response which contains an approproate sized array of values for the response -- one value for each receptor site.
(For prototyping purposes it will return rundom values currently.)

Example of response:

.. code-block:: javascript

    {
        [
         0.0045762,
         0.0192111,
         0.0799285,
         0.2933418,
         0.4001939,
         ...
        ]
    }

::

  base_url/locations/{location_name}/oiling_analysis

and sending JSON data (example):

::

    {
    "season": "winter",
    "oil_type": "diesel",
    "source_id": 3,
    "receptor_id": 392,
    "amount_spilled": [1000, "bbl"],
    "output_time_index": 3
    }

output_time is an index into the output times array.


Will return a JSON response which contains an approproate sized array of values for response - one value for each spill.
(For prototyping purposes it will return rundom values currently)

Example of response:

.. code-block:: javascript

    {
        [0, 0, 1, 2, 15, 60, 235, 182, 96, 17, 1, 0, 0, 3, 43, 102, ...]
    }


::

  base_url/locations/{location_name}/response_time_analysis

and sending JSON data (example):

::

    {
    "season": "winter",
    "oil_type": "diesel",
    "source_id": 3,
    "receptor_id": 392,
    "amount_spilled": [1000, "bbl"],
    "level_of_concern": [1.5, "bbl"],
    "response_threshold": 95
    }


Will return a JSON response which contains an object of two arrays:
1) response time values -- one value for each receptor site
2) response time values -- one value for each spill
(For prototyping purposes it will return rundom values currently)

Example of response:

.. code-block:: javascript

    {
        "response_time_days": [30, 30, 20, 15, 15, 10, 3, 3, 1, ...],
        "response_time_for_spill_days": [30, 20, 20, 15, 10, 10, 3, 2, 1, ...]
    }

::

  base_url/locations/{location_name}/threat_analysis

and sending JSON data (example):

::

     {
    "season": "winter",
    "oil_type": "diesel",
    "receptor_id": 392,
    "amount_spilled": [1000, "bbl"],
    "level_of_concern": [1.5, "bbl"],
    "output_time_index": 3
    }

output_time is an index into the output times array.


Will return a JSON response which contains a randomized approproate sized array (one value for each source) of floating point numbers that range between 0 and 1. (For prototyping purposes currently)
(For prototyping purposes it will return rundom values currently)

Example of response:

.. code-block:: javascript

    {
        [0.275538, 0.012273, 0.782321, 0.553491, ...]
    }


::

  base_url/locations/{location_name}/impact_by_spill

and sending JSON data (example):

::

    {
    "season": "winter",
    "oil_type": "diesel",
    "source_id": 3,
    "output_time_index": 3,
    "spill_number": 7
    }

output_time is an index into the output times array.


Will return a JSON response which contains an approproate sized array of values for the response -- one value for each receptor site.

Example of response:

.. code-block:: javascript

    {
        [
         0.0045762,
         0.0192111,
         0.0799285,
         0.2933418,
         0.4001939,
         ...
        ]
    }


::

  base_url/locations/{location_name}/response_time_by_spill

and sending JSON data (example):

::

    {
    "season": "winter",
    "oil_type": "diesel",
    "source_id": 3,
    "amount_spilled": [1000, "bbl"],
    "level_of_concern": [1.5, "bbl"],
    "spill_number": 7
    }


Will return a JSON response which contains an array of values for the response time (one value for each receptor site).

Example of response:

.. code-block:: javascript

    {
        [30, 30, 20, 15, 15, 10, 3, 3, 1, ...]
    }


