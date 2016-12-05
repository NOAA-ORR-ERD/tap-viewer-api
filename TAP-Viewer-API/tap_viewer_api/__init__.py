from pyramid.config import Configurator
from pyramid.events import NewRequest
from tap_viewer_api.views import cors_policy

ALLOWED_ORIGIN = ('http://localhost')


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        if 'Origin' in request.headers:
            origin = request.headers['Origin']
            if origin in ALLOWED_ORIGIN:
                response.headers['Access-Control-Allow-Origin'] = origin
        event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    config = Configurator()
    config.include('tap_viewer_api.routes')
    config.include('tap_viewer_api.views')
    config.add_static_view(name='static', path='static')
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    return config.make_wsgi_app()
