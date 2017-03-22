from pyramid.config import Configurator
from pyramid.events import NewRequest
# from tap_viewer_api.views import cors_policy

ALLOWED_ORIGINS = ('http://localhost:8080',
                   'http://127.0.0.1:8080',
                   'http://0.0.0.0:8080',
                   )

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        print("cors_headers run")
        try:
            origin = request.headers['Origin']
        except KeyError:
            return None
        print("origin:", origin)
        if origin in ALLOWED_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin
    event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    config = Configurator()
    config.include('tap_viewer_api.routes')
    config.include('tap_viewer_api.views')
    config.add_static_view(name='static', path='static')
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    return config.make_wsgi_app()
