#!/usr/bin/env python

"""
Integration tests for the views.

This can test the actual response objects
"""

import pytest

# from pyramid import testing
import webtest

from tap_viewer_api import LOCATION_DIR

LOCS_TO_TEST = ['south-california', 'sf_bay', 'arctic_platforms']  # what's this?, 'socal_md']
LOCS_TO_TEST = ['south-california', 'sf_bay']


@pytest.fixture
def test_app():
    """
    this fixture provides an application object to test against
    """
    from tap_viewer_api import main
    app = main({})
    test_app = webtest.TestApp(app)
    return test_app


def test_home(test_app):
    """
    This one does return a response object
    """
    response = test_app.get('/', status=200)
    assert response.status_code == 200
    assert response.content_type == "text/html"
    assert "TAP Viewer API" in response.text


def test_locations(test_app):
    """
    Do all the locations expected end up in the response?
    """

    # find all the ones in the locations dir:
    all_locs = {loc.name for loc in LOCATION_DIR.iterdir() if loc.is_dir() and not loc.name == ".git"}

    response = test_app.get('/locations', status=200)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert result.keys() == all_locs


@pytest.mark.parametrize("location", LOCS_TO_TEST)
def test_location_setup(test_app, location):
    response = test_app.get('/locations/{}/setup'.format(location), status=200)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert set(result.keys()) == set(('bounding_box', 'output_times', 'locs', 'name',
                                      'seasons', 'source_locations', 'oil_types',
                                      'num_spills', 'output_amounts'))

    #num_sources[{}] = len(result['source_locations'])


@pytest.mark.parametrize(("location", "season"),[('south-california', 'AllYear'),
                                                 # ('sf_bay', 'AllYear'),
                                                 ('arctic_platforms', 'AllYear'),
                                                 # ('socal_md', 'AllYear'),
                                                  ])
def test_impact_analysis(test_app, location, season):

    params = {"season": season,
              "oil_type": "diesel",
              "source_id": 3,
              "level_of_concern": [1.5, "bbl"],
              "amount_spilled": [1000, "bbl"],
              "output_time_index": 3,
              }


    response = test_app.post_json('/locations/{}/impact_analysis'.format(location), params)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert 'impact_analysis_results' in result
    # assert False

@pytest.mark.parametrize("location", LOCS_TO_TEST)
def test_oiling_analysis(test_app, location):

    params = {"season": "AllYear",
              "oil_type": "diesel",
              "source_id": 3,
              "receptor_id": 111,
              "amount_spilled": [1000, "bbl"],
              "output_time_index": 3,
              }
    
    response = test_app.post_json('/locations/{}/oiling_analysis'.format(location), params)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert 'oiling_analysis_results' in result


    # Fixme: add some more testing -- sizeof result array maybe?

@pytest.mark.parametrize("location", LOCS_TO_TEST)
def test_response_time_analysis(test_app, location):

    params = {"season": "winter",
              "oil_type": "diesel",
              "source_id": 3,
              "receptor_id": 111,
              "amount_spilled": [1000, "bbl"],
              "level_of_concern": [1.5, "bbl"],
              "response_threshold": 95
              }
    
    response = test_app.post_json('/locations/{}/response_time_analysis'.format(location), params)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert 'response_time_analysis_results' in result

@pytest.mark.parametrize("location", LOCS_TO_TEST)
def test_threat_analysis(test_app, location):

    # not all locations have "winter"
    params = {"season": "winter",
              "oil_type": "diesel",
              "receptor_id": 314,
              "amount_spilled": [1000, "bbl"],
              "level_of_concern": [1.5, "bbl"],
              "output_time_index": 3,
              }

    response = test_app.post_json('/locations/{}/threat_analysis'.format(location), params)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert 'threat_analysis_results' in result

@pytest.mark.parametrize("location", LOCS_TO_TEST)
def test_impact_by_spill(test_app, location):

    params = {"season": "winter",
              "oil_type": "diesel",
              "source_id": 3,
              "output_time_index": 3,
              "spill_number": 7
             }
    
    response = test_app.post_json('/locations/{}/impact_by_spill'.format(location), params)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert 'impact_by_spill_results' in result

@pytest.mark.parametrize("location", LOCS_TO_TEST)
def test_response_time_by_spill(test_app, location):

    params = {"season": "winter",
              "oil_type": "diesel",
              "source_id": 3,
              "amount_spilled": [1000, "bbl"],
              "level_of_concern": [1.5, "bbl"],
              "spill_number": 7
             }
    
    response = test_app.post_json('/locations/{}/response_time_by_spill'.format(location), params)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert 'response_time_by_spill_results' in result


