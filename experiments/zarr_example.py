#!/usr/bin/env python

"""
trying out a few things with zarr

this needs the zarr package:

conda install zarr

Should get it from conda-forge
"""

import numpy as np
import zarr

def make_cubes():
    """
    make a zarr dataset with a bunch of cubes in it

    This putting all of the location data in one zarr "file".

    each season is a separate "group", which is really like a directory

    then each cube is an array within that group

    """
    seasons = ["spring", "fall"]
    num_sites = 10
    num_receptors = 10_000
    num_times = 12
    num_runs = 500

    cube_size = (num_times, num_runs, num_receptors)

    cube_dtype = np.uint16
    # how many LEs hit a site if there were 10,000 total
    # scaled to fit in a 16 bit integer
    # create a "group" (like a netcdf Dataset?) on disk
    with zarr.open('some_location.zarr', mode='w') as cubes:

        for season in seasons:
            for site_num in range(num_sites):
                cube_name = f"{season}/site{site_num:04d}"
                z_arr = cubes.empty(name=cube_name, shape=cube_size, dtype=cube_dtype)
                # give it some random data:
                z_arr[:] = np.random.randint(0, 10_000, cube_size)


def read_cube(season, site_num):
    with zarr.open('some_location.zarr', mode='r') as cubes:
        cube_name = f"{season}/site{site_num:04d}"
        zcube = cubes[cube_name]
        # Make an array for the data
        # acube = np.empty(zcube.shape, dtype=np.float32)
        if zcube.dtype == np.uint16:
            acube = zcube.astype(np.float32)[:]
            acube /= 10_000
        else:
            raise TypeError("I only know how to deal with uint16 cubes")
        return acube

if __name__ == "__main__":

    try:
        print('checking for existing zar "file"')
        site_data = zarr.open('some_location.zarr', mode='r')
        print("looks like it's there")
    except ValueError:
        print('zarr "file" not there, creating it')
        make_cubes()

    print("accessing a single cube, just for fun")

    cube = read_cube("spring", 3)

    print(f"cube info: shape:{cube.shape}, dytpe:{cube.dtype}")
