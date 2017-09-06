#!/usr/bin/env python

import os

from pyramid.response import Response
from pyramid.view import view_config

from docutils.core import publish_string

from . import models

# FixMe: maybe this should be pulled from the ini file??
data_dir = os.path.dirname(__file__)
locations_dir = os.path.join(data_dir, 'locations')

# load up the locations:
all_locations = models.load_locations(locations_dir)

#cors_policy = {'credentials': True}


def includeme(config):
    config.add_view(home, route_name='home', renderer='string')
    config.add_view(locations, route_name='locations', renderer='json')
    config.add_view(location_setup, route_name='location_setup', renderer='json')
    config.add_view(impact_analysis, route_name='impact_analysis', renderer='json')
    config.add_view(oiling_analysis, route_name='oiling_analysis', renderer='json')
    # these two are simply passing json right on through
    config.add_view(location_map, route_name='location_map')
    config.add_view(location_receptors, route_name='location_receptors')


# this should be handled by the json renderer
def json_response(json_obj):
    """
    Creates a json response object from a string that contains the json.

    This does no validating or anything of the json content -- that's up to you.
    """
    resp = Response()
    resp.content_type = "application/json"
    resp.json = json_obj
    return resp


def home(request):
    """
    home page

    renders and returns the API.rst file

    This is the documentation of the API
    """
    request.response.content_type = "text/html"

    return Response(publish_string(open(os.path.join(data_dir, "API.rst")).read(),
                                   writer_name='html'))


@view_config(renderer='json')
def locations(request):
    result = {name: loc.location_info for name, loc in all_locations.items()}
    return result


def location_setup(request):
    loc = request.matchdict['location_name']
    return all_locations[loc].site_data


def location_map(request):
    loc = request.matchdict['location_name']
    return json_response(all_locations[loc].map)


def location_receptors(request):
    loc = request.matchdict['location_name']
    return json_response(all_locations[loc].receptors)


def impact_analysis(request):
    """
    returns impact analysis results for the given json request

    request should have the following fields (example data):

    {
    "season": "winter",
    "oil_type": "diesel",
    "source_id": 3,
    "level_of_concern": [1.5, "bbl"],
    "amount_spilled": [1000, "bbl"],
    "output_time_index": 3,
    }
    """
    loc = request.matchdict['location_name']
    loc_obj = all_locations[loc]
    req_obj = request.json_body
    return {'impact_analysis_results': loc_obj.impact_analysis(**req_obj)}


def oiling_analysis(request):
    """
    returns site oiling analysis for the given parmeters

    JSON request should have the following fields (example data):

    {
    "season": "winter",
    "oil_type": "diesel",
    "source_id": 3,
    "receptor_id": 4
    "amount_spilled": [1000, "bbl"],
    "output_time_index": 2,
    }
    """
    loc = request.matchdict['location_name']
    loc_obj = all_locations[loc]
    req_obj = request.json_body
    return {'oiling_analysis_results': loc_obj.oiling_analysis(**req_obj)}
