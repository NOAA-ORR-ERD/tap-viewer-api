from wsgiref.simple_server import make_server
from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator()
    config.include('tap_viewer_api.routes')
    config.include('tap_viewer_api.views')
    config.add_static_view(name='static', path='static')
    return config.make_wsgi_app()
