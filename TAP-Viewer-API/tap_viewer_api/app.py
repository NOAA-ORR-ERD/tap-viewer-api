from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import views

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.add_view(views.hello_world, route_name='hello')
    config.add_route('locations', '/locations')
    config.add_view(views.locations, route_name='locations', renderer='json')
    config.add_route('location_setup', '/locations/{location_name}/location_setup')
    config.add_view(views.location_setup, route_name='location_setup', renderer='json')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8081, app)
    server.serve_forever()
