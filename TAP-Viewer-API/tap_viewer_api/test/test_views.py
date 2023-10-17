#!/usr/bin/env python

"""
Tests the basics of the views

This tests the views' return -- not the response object
"""
from pathlib import Path
import pytest

from pyramid import testing

from tap_viewer_api import views, LOCATION_DIR


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


def test_locations_all():
    """
    Do all the locations expected end up in the response?
    """

    # find all the ones in the locations dir:
    all_locs = {loc.name for loc in LOCATION_DIR.iterdir() if loc.is_dir() and not loc.name == ".git"}

    print(all_locs)
    request = testing.DummyRequest()
    result = views.locations(request)

    print(result.keys())
    assert set(result.keys()) == all_locs

