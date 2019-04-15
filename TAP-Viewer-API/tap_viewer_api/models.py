#!/usr/bin/env python

"""
Here are the models for the actual computation, etc.
"""

import os
import json
import numpy as np

from tap_viewer_api.tap_comp.cube_crunching import cube_impact_analysis

locations = {}


def load_locations(location_dir):
    """
    loads up a set of classes for each location that exists
    """
    locations = os.listdir(location_dir)
    locations = [name for name in locations if os.path.isdir(os.path.join(location_dir, name))]
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
        self.num_sources = len(self.site_data["source_locations"])
        self.output_times = self.site_data["output_times"]
        print(self.data_dir)
        print(self.site_data["num_sites"])
        self.num_sites = self.site_data["num_sites"]

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

        returns a string object with the geojson in it
        """
        return open(os.path.join(self.data_dir, "map.geojson")).read()

    @property
    def receptors(self):
        """
        dynamically load the receptors from the geojson map

        returns a string object with the geojson in it
        """
        return open(os.path.join(self.data_dir, "receptors.geojson")).read()


    # @property
    # def num_sites(self):
    #     if self._num_sites is None:
    #         # read the site_file
    #         with open(os.path.join(self.data_dir, "receptors.geojson")) as sites_file:
    #             sites = json.load(sites_file)
    #             self._num_sites = len(sites["features"])
    #     return self._num_sites


    def impact_analysis(self,
                        season=None,
                        oil_type=None,
                        source_id=None,
                        level_of_concern=None,
                        amount_spilled=None,
                        output_time_index=None,
                        ):

        """
        compute an impact analysis

        For now, it only returns random values

        example input:
            {"season": "winter",
             "oil_type": "diesel",
             "source_id":3,
             "level_of_concern":[1.5, "bbl"],
             "amount_spilled": [1000, "bbl"],
             "output_time_index": 3,
             }
        """
       
        return cube_impact_analysis(self,season,oil_type,source_id,level_of_concern,
                        amount_spilled,output_time_index).tolist()
        # return np.random.random(self.num_sites).tolist()

    def oiling_analysis(self,
                        season=None,
                        oil_type=None,
                        source_id=None,
                        receptor_id=None,
                        amount_spilled=None,
                        output_time_index=None,
                        ):
        """
        Compute an oiling analysis

        For now, it only returns random values

        example input:
            {"season": "winter",
             "oil_type": "diesel",
             "source_id": 3,
             "receptor_id": 111,
             "amount_spilled": [1000, "bbl"],
             "output_time_index": 3,
             }
        """
        return (np.random.random(self.num_spills) * amount_spilled[0]).tolist()

    def response_time_analysis(self,
                               season=None,
                               oil_type=None,
                               source_id=None,
                               receptor_id=None,
                               amount_spilled=None,
                               level_of_concern=None,
                               response_threshold=None,
                               ):

        """
        Compute a response time analysis

        For now, it only returns random values

        example input:
            {"season": "winter",
             "oil_type": "diesel",
             "source_id": 3,
             "receptor_id": 111,
             "amount_spilled": [1000, "bbl"],
             "level_of_concern": [1.5, "bbl"],
             "response_threshold": 95
             }
        """
        max_days = np.array(self.output_times)[:,0].astype(np.float).max()/24
        return (np.random.random(self.num_sites) * max_days).tolist(), (np.random.random(self.num_spills) * max_days).tolist()


    def threat_analysis(self,
                        season=None,
                        oil_type=None,
                        receptor_id=None,
                        amount_spilled=None,
                        level_of_concern=None,
                        output_time_index=None,
                        ):

        """
        Compute a threat analysis

        For now, it only returns random values

        example input:
            {"season": "winter",
             "oil_type": "diesel",
             "receptor_id": 314,
             "amount_spilled": [1000, "bbl"],
             "level_of_concern": [1.5, "bbl"],
             "output_time_index": 3,
             }
        """
        return (np.random.random(self.num_sources)).tolist()

    def impact_by_spill(self,
                        season=None,
                        oil_type=None,
                        source_id=None,
                        output_time_index=None,
                        spill_number=None,
                        ):

        """
        Compute an impact by spill

        For now, it only returns random values

        example input:
            {
            "season": "winter",
            "oil_type": "diesel",
            "source_id": 3,
            "output_time_index": 3,
            "spill_number": 7
            }
        """
        return (np.random.random(self.num_sites)).tolist()

    def response_time_by_spill(self,
                               season=None,
                               oil_type=None,
                               source_id=None,
                               amount_spilled=None,
                               level_of_concern=None,
                               spill_number=None,
                              ):

        """
        Compute a threat analysis

        For now, it only returns random values

        example input:
            {
            "season": "winter",
            "oil_type": "diesel",
            "source_id": 3,
            "amount_spilled": [1000, "bbl"],
            "level_of_concern": [1.5, "bbl"],
            "spill_number": 7
            }
        """
        max_days = np.array(self.output_times)[:,0].astype(np.float).max()/24
        return (np.random.random(self.num_sites) * max_days).tolist()
