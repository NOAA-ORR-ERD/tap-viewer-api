"""
test config for the pytests
"""

from pathlib import Path

import pytest

HERE = Path(__file__).parent

# # get locations for environment variable, if there
# LOCATION_DIR = os.getenv("TAP_LOCATIONS_DIR", None)
# if LOCATION_DIR is None:
#     # assume it's relative to the test dir
#     LOCATION_DIR = HERE / "../../../../tap-test-data"
#     msg = ("No TAP_LOCATIONS_DIR env var set -- looked relative to test dir,\n"
#            f"found: {LOCATION_DIR}")
# else:
#     msg = f"TAP_LOCATIONS_DIR env var set to: {LOCATION_DIR}"

# LOCATION_DIR = Path(LOCATION_DIR)
# if not LOCATION_DIR.is_dir():
#     raise ValueError(f"{LOCATION_DIR} is not a dir:\n {msg}")

def appsettings(ini_file):
    """PyTest fixture: Pyramid deployment configuration (=parsed INI file).

    Requires the '--pyramid' command-line option specifying an INI file with
    an '[app:main]' section.
    """
    import pyramid.paster
    settings = pyramid.paster.get_appsettings(ini_file)
    return settings


@pytest.fixture(scope="session")
def test_settings():
    """
    Get the locations dir:

    If the TAP_LOCATIONS_DIR environment variable is set, it will be used.

    Else if the ini file was passed in to the tests, it will be used

    Else it will look for the development.ini file, relative to this
    file.

    If not, it will look in the development.ini file, relative to this
    test code
    """
    import os

    # get locations for environment variable, if there
    LOCATION_DIR = os.getenv("TAP_LOCATIONS_DIR", None)
    if LOCATION_DIR is not None:
        settings = {"locations_dir": LOCATION_DIR}
        msg = f"found LOCATION_DIR env variable: {LOCATION_DIR}"
    else:
        # use development.ini file
        ini_file = HERE / "../../../development.ini"

        if not ini_file.is_file():
            raise ValueError(f"{ini_file} does not exist.")

        settings = appsettings(os.fspath(ini_file))
        msg = f"settings pulled from ini file: {ini_file}"
    loc_dir = Path(settings['locations_dir'])
    if not loc_dir.is_dir():
        raise ValueError(f"{loc_dir} is not a dir:\n {msg}")

    return settings


@pytest.fixture(scope="session")
def locations_dir(test_settings):
    loc_dir = Path(test_settings['locations_dir'])
    return loc_dir



#     LOCATION_DIR = Path(LOCATION_DIR)
#     msg = ("No TAP_LOCATIONS_DIR env var set -- looked relative to test dir,\n"
#            f"found: {LOCATION_DIR}")
# else:
#     msg = f"TAP_LOCATIONS_DIR env var set to: {LOCATION_DIR}"

#     LOCATION_DIR = Path(LOCATION_DIR)
#     if not LOCATION_DIR.is_dir():
#         raise ValueError(f"{LOCATION_DIR} is not a dir:\n {msg}")



#     return LOCATION_DIR


