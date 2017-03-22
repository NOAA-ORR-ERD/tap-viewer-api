#!/usr/bin/env python

"""
send some sample json requests to server
"""

import requests

base_url = "http://127.0.0.1:9900"

def impact_analysis(location):
    """
    Impact Analysis
    {
       season, str
       oil_type, str
       level_of_concern_bbl, number
       amount_spilled_bbl, number
       time_since_start_hrs, number
       location_id
    }
    """
    url = base_url + "/locations/%s/impact_analysis" % location
    params = {"season": "winter",
               "oil_type": "diesel",
               "level_of_concern_bbl":1.5,
               "amount_spilled_bbl":1000,
               "time_since_start_hrs":72,
               "source_id":3,
               }
    r = requests.post(url, json=params)
    print("made request")

    print("status:", r.status_code)
    print("results:")
    print(r.json())

impact_analysis('sf')
#impact_analysis('arctic')


