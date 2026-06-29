"""
test config for the pytests
"""
import os
from pathlib import Path

import pytest

HERE = Path(__file__).parent

# get locations for environment variable, if there
LOCATION_DIR = os.getenv("TAP_LOCATIONS_DIR", None)
if LOCATION_DIR is None:
    # assume it's relative to the test dir
    LOCATION_DIR = HERE / "../../../../tap-test-data"
    msg = ("No TAP_LOCATIONS_DIR env var set -- looked relative to test dir,\n"
           f"found: {LOCATION_DIR}")
else:
    msg = f"TAP_LOCATIONS_DIR env var set to: {LOCATION_DIR}"

LOCATION_DIR = Path(LOCATION_DIR)
if not LOCATION_DIR.is_dir():
    raise ValueError(f"{LOCATION_DIR} is not a dir:\n {msg}")

@pytest.fixture(scope="session")
def locations_dir():
    return LOCATION_DIR


