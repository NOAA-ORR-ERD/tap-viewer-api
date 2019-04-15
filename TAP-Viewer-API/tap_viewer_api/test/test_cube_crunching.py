import os
from pathlib import Path
import pytest
import numpy as np
from tap_viewer_api.tap_comp.cube_crunching import getcube, cube_impact_analysis


thisdir = Path(__file__).parent
print(thisdir)
data_dir = thisdir.parent/'locations'/'arctic'

# cubeshape = (13, 12221, 500)   # times * n_cells * n_runs (also the correct order)
cubeshape = (13, 9095, 500)   # times * n_cells * n_runs (also the correct order)

class self:
    pass
self.output_times = (1, 3, 5, 7, 10, 15, 20, 30, 60, 70, 90, 120, 180)
# self.num_sites = 12221
self.num_sites = 9095
self.num_spills = 500
self.data_dir = data_dir


def test_cube_impact_analysis():

    imp_cube = cube_impact_analysis(self,'AllYear',None,1,5,1000,2)

    assert len(imp_cube) == self.num_sites

    assert False

def test_getcube():
        
    cube = getcube(data_dir,'AllYear',1,cubeshape)
    
    assert isinstance(cube,np.ndarray)

    assert cube.shape == cubeshape


def test_cubeexist():
    with pytest.raises(FileNotFoundError):
        cube = getcube(data_dir,'AllYear',555, cubeshape)



def test_cubesize():

    pass
