from pyramid.config import Configurator
from pyramid.events import NewRequest
# from tap_viewer_api.views import cors_policy

ALLOWED_ORIGINS = ('http://localhost',
                   'http://127.0.0.1',
                   'http://0.0.0.0',
                   )

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        print("cors_headers run")
        try:
            origin = request.headers['Origin']
        except KeyError:
            return None
        print("origin:", origin)
        for allowed in ALLOWED_ORIGINS:
            if allowed in origin:
                response.headers['Access-Control-Allow-Origin'] = origin
                break
    event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    config = Configurator()
    config.include('tap_viewer_api.routes')
    config.include('tap_viewer_api.views')
    config.add_static_view(name='static', path='static')
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    return config.make_wsgi_app()
