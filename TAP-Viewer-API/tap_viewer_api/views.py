from pyramid.response import Response
import os
import json
import numpy as np

data_dir = os.path.dirname(__file__)

cors_policy = {'credentials': True}


def includeme(config):
    config.add_view(home, route_name='home')
    config.add_view(locations, route_name='locations', renderer='json')
    config.add_view(location_setup, route_name='location_setup', renderer='json')
    config.add_view(impact_analysis, route_name='impact_analysis', renderer='json')
    config.add_view(oiling_analysis, route_name='oiling_analysis', renderer='json')


def home(request):
    return Response('Hello!')


def locations(request):
    sf = {'route_name': 'sf', 'name': 'San Francisco', 'lonlat': [-122.42, 37.77]}
    arctic = {'route_name': 'arctic', 'name': 'US Arctic Waters', 'lonlat': [-156.79, 71.29]}
    return {'locations': [sf, arctic]}


def location_setup(request):
    loc = request.matchdict['location_name']
    site_path = os.path.join(data_dir, "locations", loc, "site.json")
    with open(site_path) as site_file:
        return json.load(site_file)


def impact_analysis(request):
    req_obj = request.json_body
    return {'data': tap_impact_analysis(req_obj)}
    # loc_id = req_obj['location_id']
    # season = req_obj['season']
    # oil_type = req_obj['oil_type']
    # level_of_concern = req_obj['level_of_concern']
    # amount_spilled_bbl = req_obj['amount_spilled_bbl']
    # time_since_start_hrs = req_obj['time_since_start_hrs']


def oiling_analysis(request):
    req_obj = request.json_body
    return {'data': tap_oiling_analysis(req_obj)}
    # loc_id = req_obj['location_id']
    # season = req_obj['season']
    # oil_type = req_obj['oil_type']


def tap_impact_analysis(req_obj):
    return np.random.rand(100).tolist()


def tap_oiling_analysis(req_obj):
    return np.random.rand(100).tolist()
