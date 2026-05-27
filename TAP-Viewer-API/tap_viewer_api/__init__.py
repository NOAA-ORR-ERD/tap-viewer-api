from pathlib import Path

from pyramid.config import Configurator
from pyramid.events import NewRequest
# from tap_viewer_api.views import cors_policy

ALLOWED_ORIGINS = ()

# FIXME: this should be pulled from the config.ini, not hard-coded here
#        and shouldn't be relative to the code like this, either.
#        then we wouldn't need this hack!

LOCATION_DIR = Path(__file__).parent / 'locations'

# Is there something else to look for?
#if not (LOCATION_DIR / 'san_diego' / 'site.json').is_file():
# fixed (G.K.): only 'arctic_platforms' location is cloned for tests on the server at this moment (GitLab job)
if not (LOCATION_DIR / 'arctic_platforms' / 'site.json').is_file():
    print((LOCATION_DIR / 'arctic_platforms' / 'site.json'))
    print("Can't find locations in with code, looking outside, "
          "alongside this repo")
    # set locations DIR for tests
    LOCATION_DIR = Path(__file__).parents[3] / 'locations'

DATA_DIR = Path(__file__).parent


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin
    event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    global ALLOWED_ORIGINS
    try:
        origins = settings['cors_policy.origins']
        ALLOWED_ORIGINS = origins.split('\n')
    except KeyError:
        pass
    config = Configurator()
    config.include('tap_viewer_api.routes')
    config.include('tap_viewer_api.views')
    config.add_static_view(name='static', path='static')
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    return config.make_wsgi_app()
