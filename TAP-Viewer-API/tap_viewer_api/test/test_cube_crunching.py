
# from pathlib import Path
import pytest
import numpy as np
from tap_viewer_api import LOCATION_DIR
from tap_viewer_api.tap_comp.cube_crunching import (getcube,
                                                    cube_impact_analysis,
                                                    cube_oiling_analysis,
                                                    )
from tap_viewer_api.models import TapLocation


# there *should* be test data -- but if not, let's use the real data
# #

# thisdir = Path(__file__).parent
# print(thisdir)
# data_dir = thisdir.parent / 'locations' / 'arctic'

data_dir = LOCATION_DIR / 'arctic_platforms'


# cubeshape = (13, 12221, 500)   # times * n_cells * n_runs (also the correct order)
cubeshape = (13, 9127, 500
             )  # times * n_cells * n_runs (also the correct order)

amount_spilled = [1000, 'barrels']
loc = [5, 'barrels']


class self:
    pass


self.output_times = (1, 3, 5, 7, 10, 15, 20, 30, 60, 70, 90, 120, 180)
# self.num_sites = 12221
self.num_sites = 9127
self.num_spills = 500
self.data_dir = data_dir


@pytest.fixture
def location():
    return TapLocation(LOCATION_DIR / 'arctic_platforms')



def test_cube_oiling_analysis(location):
    oil_cube = cube_oiling_analysis(location, 'AllYear', None, 3, 111,
                                    amount_spilled, 2)
    assert len(oil_cube) == self.num_spills


def test_cube_impact_analysis(location):

    imp_cube = cube_impact_analysis(location, 'AllYear', None, 1, loc,
                                    amount_spilled, 2)

    assert len(imp_cube) == self.num_sites


def test_getcube():

    cube = getcube(data_dir, 'AllYear', 1, cubeshape)

    assert isinstance(cube, np.ndarray)

    assert cube.shape == cubeshape


def test_cubeexist():
    with pytest.raises(FileNotFoundError):
        cube = getcube(data_dir, 'AllYear', 555, cubeshape)


# # def test_cubesize():

# #     pass
