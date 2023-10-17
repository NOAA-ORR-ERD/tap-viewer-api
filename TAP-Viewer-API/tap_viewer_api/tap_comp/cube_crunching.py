#!/usr/bin/env python
"""
Here are the functions for working with cubes for the TAP viewer
"""
from pathlib import Path
import numpy as np


def getcube(data_dir, season, source_id, cubeshape):
    """
    Returns numpy array of cube with shape [nrec_sites,ntime,n_spills???]
    """
    cubedir = Path(data_dir) / 'TAPDATA' / season
    try:
        cubetag = next(cubedir.glob('*001.bin')).name[:-8]
    except StopIteration:
        raise FileNotFoundError("no cubes found in " + str(cubedir))

    cube_id = source_id + 1  # TAPDATA are 1-base indexed (at least for Arctic/SoCal TAPS)
    cubefile = cubedir / (cubetag + str(cube_id).zfill(4) + '.bin')
    cubesize = np.prod(cubeshape)
    cube = np.fromfile(str(cubefile), np.uint8)

    if cube.size == 4 * cubesize:
        cube = np.frombuffer(cube, np.float32)
    elif cube.size == 2 * cubesize:
        # convert from int16
        raise NotImplementedError
    elif cube.size == cubesize:
        # reverse transfrom done when writing uint8 cubes
        n = 1.5
        max_val = 255
        cube = cube.astype(np.float)
        cube = (cube / max_val)**n  # * num_LE)

    else:
        raise ValueError("cube size not a nice multiple.\n"
                         f"Size of cube in file: {cube.size}\n"
                         f"Size of cube expected: {cubesize}")

    cube.shape = cubeshape
    print('getcube:: max cube value =', np.max(cube))

    return cube


def cube_impact_analysis(self, season, oil_type, source_id, level_of_concern,
                         amount_spilled, output_time_index):

    # construct data_dir
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)

    # get the correct cube
    cube = getcube(self.data_dir, season, source_id, cubeshape)

    # find values greater than LOC
    scale = amount_spilled[0] / self.model_spill[0]
    boolcube = cube[output_time_index, :, :] * scale >= level_of_concern[0]

    # translate to percentage
    imp_cube = np.sum(boolcube, 1) / cubeshape[2]

    return imp_cube


def cube_oiling_analysis(self, season, oil_type, source_id, receptor_id,
                         amount_spilled, output_time_index):

    # get the correct cube
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    cube = getcube(self.data_dir, season, source_id, cubeshape)

    # print(output_time_index)
    scale = amount_spilled[0] / self.model_spill[0]
    print(scale)
    oil_cube = cube[output_time_index, receptor_id, :] * scale
    # print(np.amax(oil_cube))
    # print(oil_cube.shape)

    return oil_cube


def cube_response_time_analysis(self, season, oil_type, source_id, receptor_id,
                                amount_spilled, level_of_concern,
                                response_threshold):

    # get the correct cube
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    cube = getcube(self.data_dir, season, source_id, cubeshape)

    out_times = np.zeros(len(self.output_times))
    for s in range(0, len(self.output_times)):
        out_times[s] = self.output_times[s][0]
    out_times = out_times[::-1] / 24.  # change to days

    resp_time = np.ones(self.num_sites) * out_times[-1] * 2
    # find values greater than LOC
    scale = amount_spilled[0] / self.model_spill[0]
    for ss in range(0, self.num_sites):
        xx1 = np.sum(cube[:, ss, :] * scale >= level_of_concern[0], 1)
        tmp = np.where(
            xx1 > self.num_spills * (100 - response_threshold) / 100., 1, 0)
        if tmp.any(): resp_time[ss] = min(out_times[np.where(tmp)])

    resp_time_receptor = np.sum(
        cube[:, receptor_id, :] * scale >= level_of_concern[0],
        1) / self.num_spills
    print(resp_time_receptor)

    return resp_time, resp_time_receptor


def cube_threat_analysis(
    self,
    season,
    oil_type,
    receptor_id,
    amount_spilled,
    level_of_concern,
    output_time_index,
):

    # # define cubedir and get list of cube files
    # cubedir = Path(self.data_dir)/'TAPDATA'/season
    # cube_list = data_dir.glob('*.bin')

    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    print(receptor_id)

    scale = amount_spilled[0] / self.model_spill[0]
    threat = np.zeros(self.num_sources)
    for s in range(0, self.num_sources):
        cube = getcube(self.data_dir, season, s, cubeshape)
        bool_rec = cube[output_time_index,
                        receptor_id, :] * scale >= level_of_concern[0]
        threat[s] = np.sum(bool_rec) / cubeshape[2]

    return threat


def cube_impact_by_spill(self, season, oil_type, source_id, output_time_index,
                         spill_number):

    # get the correct cube
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    cube = getcube(self.data_dir, season, source_id, cubeshape)

    temp = cube[output_time_index, :, spill_number] / self.model_spill[0]
    print(np.max(temp))
    return temp

    # return cube[output_time_index,:,spill_number]/100


def cube_response_time_by_spill(self, season, oil_type, source_id,
                                amount_spilled, level_of_concern,
                                spill_number):

    # get the correct cube
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    cube = getcube(self.data_dir, season, source_id, cubeshape)
    cube1 = cube[:, :, spill_number]  # only keep the spill of interest

    out_times = np.zeros(len(self.output_times))
    for s in range(0, len(self.output_times)):
        out_times[s] = self.output_times[s][0]
    out_times = out_times[::-1] / 24.  # change to days and flip to lowest first

    resp_time = np.ones(
        self.num_sites
    ) * out_times[-1] * 2  # initial fill with values > longest time
    # find values greater than LOC
    scale = amount_spilled[0] / self.model_spill[0]
    for ss in range(0, self.num_sites):
        tmp = np.where(cube1[:, ss] * scale >= level_of_concern[0], 1, 0)
        if tmp.any(): resp_time[ss] = min(out_times[np.where(tmp)])

    return resp_time
