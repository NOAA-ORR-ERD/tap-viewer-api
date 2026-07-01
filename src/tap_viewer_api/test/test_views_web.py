#!/usr/bin/env python

"""
Integration tests for the views.

This can test the actual response objects
"""
import os
from pathlib import Path
import pytest

# from pyramid import testing
import webtest

LOCS_TO_TEST = [
        ('arctic_platforms'),
        ('sabine_lake'),
        ('south-california')
                ]

@pytest.fixture
def test_app(test_settings):
    """
    this fixture provides an application object to test against
    """
    # config_uri = 'development.ini'

    from tap_viewer_api import main
    app = main({}, **test_settings)

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


def test_locations(test_app, locations_dir):
    """
    Do all the locations expected end up in the response?
    """
    # find all the ones in the locations dir:
    all_locs = {loc.name for loc in locations_dir.iterdir() if loc.is_dir() and not loc.name == ".git"}

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

    if location == 'south-california':
        assert set(result.keys()) == set(('bounding_box', 'output_times', 'locs', 'name',
                                        'seasons', 'source_locations', 'num_spills', 
                                        'release_duration', 'num_sites', 
                                        'model_spill', 'spill_rate', 'season_labels'
                                        ))

        #num_sources[{}] = len(result['source_locations'])

    if location == 'arctic_platforms':
        assert set(result.keys()) == set(('bounding_box', 'output_times', 'locs', 'name',
                                        'seasons', 'source_locations', 'num_spills', 
                                        'release_duration', 'num_sites', 
                                        'oil_types', 'spill_rate', 'season_labels'
                                        ))


@pytest.mark.parametrize(("location", "season"),[('arctic_platforms', 'AllYear'),
                                                 # ('sf_bay', 'AllYear')
                                                 # ('socal_md', 'AllYear'),
                                                  ])
def test_impact_analysis(test_app, location, season):

    params = {"season": season,
              "oil_type": "Non-Weathering",
              "source_id": 1,
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
              "oil_type": "Non-Weathering",
              "source_id": 1,
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

    params = {"season": "AllYear",
              "oil_type": "Non-Weathering",
              "source_id": 1,
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

    params = {"season": "AllYear",
              "oil_type": "Non-Weathering",
              "receptor_id": 201,
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

    params = {"season": "AllYear",
              "oil_type": "Non-Weathering",
              "source_id": 1,
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

    params = {"season": "AllYear",
              "oil_type": "Non-Weathering",
              "source_id": 1,
              "amount_spilled": [1000, "bbl"],
              "level_of_concern": [1.5, "bbl"],
              "spill_number": 7
             }
    
    response = test_app.post_json('/locations/{}/response_time_by_spill'.format(location), params)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    result = response.json

    assert 'response_time_by_spill_results' in result


