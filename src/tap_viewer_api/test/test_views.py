#!/usr/bin/env python

"""
Tests the basics of the views

This tests the views' return -- not the response object
"""
from pathlib import Path
import pytest

from pyramid import testing

import tap_viewer_api
# total kludge, so it will work without the config being already run
# which is usually where LOCATION_DIR is set.
from .conftest import LOCATION_DIR
tap_viewer_api.LOCATION_DIR = LOCATION_DIR

from tap_viewer_api import views

@pytest.fixture
def config():
    """
    this fixture provides a config object -- may be needed by some tests

    See pyramid docs (or code) for details
    """
    config = testing.setUp()
    yield config
    testing.tearDown()


def test_home():
    """
    this one does return a response object
    """
    request = testing.DummyRequest()
    response = views.home(request)
    assert response.status_code == 200
    assert response.content_type == "text/html"
    assert "TAP Viewer API" in response.text


def test_locations_all(locations_dir):
    """
    Do all the locations expected end up in the response?
    """

    # find all the ones in the locations dir:
    all_locs = {loc.name for loc in locations_dir.iterdir() if loc.is_dir() and not loc.name == ".git"}

    print(all_locs)
    request = testing.DummyRequest()
    result = views.locations(request)

    print(result.keys())
    assert set(result.keys()) == all_locs

