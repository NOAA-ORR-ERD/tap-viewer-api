def includeme(config):
    config.add_route('home', '/')
    config.add_route('locations', '/locations')
    config.add_route('location_setup', '/locations/{location_name}/setup')
