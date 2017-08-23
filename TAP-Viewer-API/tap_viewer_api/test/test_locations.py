#!/usr/bin/env python

"""
Tests that you get the locations response correctly
"""

import pytest

from pyramid import testing

from tap_viewer_api.views import locations

"""
not sure I'm using the testing framework of pyramid correctly

but it seems to work for now
"""

@pytest.fixture
def config():
    """
    this fixture provides a config object -- may be needed by some tests

    See pyramid docs (or code) for details
    """
    config = testing.setUp()
    yield config
    testing.tearDown()


# this one doesn't need config -- but maybe some will?
def test_locations_return(config):
    """
    does the locations endpoint return successfully
    """

    request = testing.DummyRequest()
    response = locations(request)
    print(response)
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.charset == "UTF-8"


def test_locations_all():
    """
    Do all the locations expected end up in the response
    """

    request = testing.DummyRequest()
    response = locations(request)

    content = response.json
    assert set(content.keys()) == set(['sb', 'sf', 'arctic', 'socal_md'])
    # print(response.content_type)
