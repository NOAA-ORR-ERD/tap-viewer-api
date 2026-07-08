"""
tests of the model code
"""

from tap_viewer_api import models

import pytest
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "example_data"

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

def test_location_modelspill_sab(locations_dir):
    loc_name = 'sabine_lake'
    loc = models.TapLocation(locations_dir / loc_name)

    assert loc.model_spill == [1.0, 'barrels']

def test_location_modelspill_sc(locations_dir):
        loc_name = 'south-california'
        loc = models.TapLocation(locations_dir / loc_name)

        assert loc.model_spill == [200, 'barrels/day']

def test_location_modelspill_scupdate():
    loc_name = 'south-california-update'
    loc = models.TapLocation(DATA / loc_name)

    result = loc.model_spill
    print(loc.num_sources)
    assert len(result) == loc.num_sources

    assert loc.model_spill[0] == [2000, 'barrels/day']
    assert loc.model_spill[1] == [6000, 'barrels/day']