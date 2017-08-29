#!/usr/bin/env python

"""
Tests the basics of the views

This tests the views' return -- not the response object
"""

import pytest

from pyramid import testing

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
    this one does retrun a response object
    """
    request = testing.DummyRequest()
    response = views.home(request)
    assert response.status_code == 200
    assert response.content_type == "text/html"
    assert "TAP Viewer API" in response.text


def test_locations_all():
    """
    Do all the locations expected end up in the response
    """

    request = testing.DummyRequest()
    result = views.locations(request)

    assert set(result.keys()) == set(['sb', 'sf', 'arctic', 'socal_md'])

