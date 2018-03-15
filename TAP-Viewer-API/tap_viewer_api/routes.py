print("loading new routes")

def includeme(config):
    config.add_route('home', '/')
    config.add_route('locations', '/locations{slash:/?}')
    config.add_route('location_setup', '/locations/{location_name}/setup')
    config.add_route('location_map', '/locations/{location_name}/map')
    config.add_route('location_receptors', '/locations/{location_name}/receptors')
    config.add_route('impact_analysis', '/locations/{location_name}/impact_analysis')
    config.add_route('oiling_analysis', '/locations/{location_name}/oiling_analysis')
    config.add_route('response_time_analysis', '/locations/{location_name}/response_time_analysis')
