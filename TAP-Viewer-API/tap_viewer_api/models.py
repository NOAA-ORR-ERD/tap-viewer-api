#!/usr/bin/env python

"""
Here are the models for the actual computation, etc.
"""

import os
import json
import numpy as np

locations = {}


def load_locations(location_dir):
    """
    loads up a set of classes for each location that exists
    """
    locations = os.listdir(location_dir)
    return {loc: TapLocation(os.path.join(location_dir, loc)) for loc in locations}


class TapLocation:
    """
    Class to hold all the location data and logic for a particular location
    """
    def __init__(self, data_dir):
        self.route_name = os.path.split(data_dir)[-1]
        self.data_dir = data_dir
        with open(os.path.join(data_dir, "site.json")) as site_file:
            self.site_data = json.load(site_file)
        self.num_spills = self.site_data["num_spills"]
        self._num_sites = None

    @property
    def location_info(self):
        """
        Returns the core location info required by the WebTAP home page
        as JSON-compatible data
        """
        info = {'route_name': self.route_name,
                'name': self.site_data['name'],
                'bounding_box': self.site_data['bounding_box']
                }
        return info

    @property
    def map(self):
        """
        dynamically load the map from the geojson map
        """
        with open(os.path.join(data_dir, "map.geojson")) as map_file:
            map = json.load(map_file)
        return map

    @property
    def receptors(self):
        """
        dynamically load the receptors from the geojson map
        """
        with open(os.path.join(self.data_dir, "receptors.geojson")) as receptors_file:
            map = json.load(receptors_file)
        return map


    @property
    def num_sites(self):
        if self._num_sites is None:
            # read the site_file
            with open(os.path.join(self.data_dir, "receptors.geojson")) as sites_file:
                sites = json.load(sites_file)
                self._num_sites = len(sites["features"])
        return self._num_sites

    def impact_analysis(self,
                        season=None,
                        oil_type=None,
                        level_of_concern_bbl=None,
                        amount_spilled_bbl=None,
                        time_since_start_hrs=None,
                        source_id=None,
                        ):
        """
        compute an impact analysis

        For now, it only returns random values
        """
        return np.random.random(self.num_sites).tolist()

    def oiling_analysis(self,
                        season=None,
                        oil_type=None,
                        amount_spilled_bbl=None,
                        time_since_start_hrs=None,
                        source_id=None,
                        receptor_id=None
                        ):
        """
        Compute an oiling analysis

        For now, it only returns random values
        """
        return (np.random.random(self.num_spills) * 10000.0).tolist()
