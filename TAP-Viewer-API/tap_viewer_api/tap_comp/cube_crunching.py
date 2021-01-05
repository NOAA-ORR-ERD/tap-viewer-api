#!/usr/bin/env python

"""
Here are the functions for working with cubes for the TAP viewer
"""
import os
from pathlib import Path 
import numpy as np


def getcube(data_dir,season,source_id,cubeshape):
    """
    Returns numpy array of cube with shape [nrec_sites,ntime,n_spills???]
    """
    cubedir = Path(data_dir)/'TAPDATA'/season
    try: 
        cubetag = next(cubedir.glob('*001.bin')).name[:-8]  
    except StopIteration:
        raise FileNotFoundError("no cubes found in "+str(cubedir))

    cube_id = source_id + 1  # TAPDATA are 1-base indexed (at least for Arctic/SoCal TAPS)  
    cubefile = cubedir/(cubetag+str(cube_id).zfill(4)+'.bin')
    # print(cubeshape)
    cubesize = np.prod(cubeshape)

    cube = np.fromfile(str(cubefile),np.uint8)
    # print(np.prod(cubeshape))
    # print(cube.size)

    if cube.size == 4*cubesize:
        cube = np.frombuffer(cube,np.float32)
    elif cube.size == 2*cubesize:
        # convert from int16
        raise NotImplementedError
    elif cube.size == cubesize:
        pass
    else:
        raise ValueError("cube size not a nice multiple")

    cube.shape = cubeshape

    return cube


def cube_impact_analysis(self,season,oil_type,source_id,level_of_concern,
                        amount_spilled,output_time_index):

    # construct data_dir
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)

    # get the correct cube
    cube = getcube(self.data_dir,season,source_id,cubeshape)

    # find values greater than LOC
    boolcube = cube[output_time_index,:,:]*amount_spilled[0] >= level_of_concern[0]

    # translate to percentage
    imp_cube = np.sum(boolcube,1)/cubeshape[2]
    
    # print(imp_cube.shape)
    # print(np.amax(imp_cube))

    return imp_cube


def cube_oiling_analysis(self,season,oil_type,source_id,receptor_id,
                             amount_spilled,output_time_index):


    # get the correct cube
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    cube = getcube(self.data_dir,season,source_id,cubeshape)

    # print(output_time_index)

    oil_cube = cube[output_time_index,receptor_id,:]*amount_spilled[0]
    # print(np.amax(oil_cube))
    # print(oil_cube.shape)

    return oil_cube

def cube_impact_by_spill(self,season,oil_type,source_id,
                             output_time_index,spill_number):

    # get the correct cube
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    cube = getcube(self.data_dir,season,source_id,cubeshape)    

    temp = cube[output_time_index,:,spill_number]
    print(np.amax(temp))
    
    return cube[output_time_index,:,spill_number]/100.

def cube_threat_analysis(self,season,oil_type,receptor_id,amount_spilled,
                            level_of_concern,output_time_index,):

    # # define cubedir and get list of cube files
    # cubedir = Path(self.data_dir)/'TAPDATA'/season
    # cube_list = data_dir.glob('*.bin')

    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)

    threat = np.zeros(self.num_sources)
    for s in range(0,self.num_sources):
        cube = getcube(self.data_dir,season,s,cubeshape)    
        bool_rec = cube[output_time_index,receptor_id,:]*amount_spilled[0] >= level_of_concern[0]        
        threat[s] = np.sum(bool_rec)/cubeshape[2]
    
    return threat

def cube_response_time(self,season,oil_type,source_id,receptor_id,
                        amount_spilled,level_of_concern,response_threshold):

   # get the correct cube
    cubeshape = (len(self.output_times), self.num_sites, self.num_spills)
    cube = getcube(self.data_dir,season,source_id,cubeshape)    



