"""
tests of the model code
"""

from tap_viewer_api import models

import pytest


def test_locations(locations_dir):
    """
    not so much a test of the model code, but rather, of the test locations

    or kinda both
    """
    # there should be a way to paramtrize this, but it's a bit tricky,
    # aslocations_dir is a fixture.
    failed = {}
    for loc_name in {loc.name for loc in locations_dir.iterdir() if loc.is_dir() and not loc.name == ".git"}:
        print(f"testing location: {loc_name}")
        try:
            loc = models.TapLocation(locations_dir / loc_name)
        except Exception as err:
            failed[loc_name] = str(err)
            print(err)
    if failed:
        print(failed)
        assert False, f"{failed.keys()} did not load."


