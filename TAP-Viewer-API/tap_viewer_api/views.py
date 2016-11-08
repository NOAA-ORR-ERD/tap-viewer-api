from pyramid.response import Response
from pyramid.view import view_config
import os
import json

data_dir = os.path.dirname(__file__)

def includeme(config):
    config.add_view(home, route_name='home')
    config.add_view(locations, route_name='locations', renderer='json')
    config.add_view(location_setup, route_name='location_setup', renderer='json')

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
