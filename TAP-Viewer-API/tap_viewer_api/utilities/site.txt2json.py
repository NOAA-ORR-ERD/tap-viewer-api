#!/usr/bin/env python3

"""
Hacky script to convert a TAP site.txt file to JSON for the Web App

PAss in the path to teh site,txt you want to convert:

site.txt2json locations/sf/stie.txt

"""

import sys
import os
import json
import geojson
from geojson import Polygon, Feature



from pprint import pprint

infilename = sys.argv[1]

location_dir = os.path.dirname(infilename)

def sites2geojson(fp):
    """
    read the sites polygon definitions and write to geojson

    for now,  skip over it..
    """
    fp.readline()
    polys = []
    with open(os.path.join(location_dir, "receptors.json"), 'w') as outfile:
        for line in fp:
            # we're done
            if "CUBES" in line:
                break
            # header line:
            print("processing:", line)
            site_num = line.split('"')[1].strip('#')
            num_points = int(line.split(',')[-1])
            poly = []
            for i in range(num_points):
                poly.append([float(i) for i in fp.readline().split(',')])
            poly = Feature(geometry=Polygon([poly]), site_num=site_num)
            polys.append(poly)
            print(poly)
        geojson.dump(polys, outfile, indent=2)


data = {}
with open(infilename, 'r') as sitefile:
    line = sitefile.readline()
    data['name'] = line.split("//")[0].strip(' "')

    line = sitefile.readline()
    data['map_name'] = line.split('"')[1]

    line = sitefile.readline()
    data['num_spills'] = int(line.split()[0])

    line = sitefile.readline()
    num = int(line.split()[0])
    data['seasons'] = [sitefile.readline().split('"')[1] for i in (range(num))]

    line = sitefile.readline()
    num = int(line.split()[0])
    data["output_times"] = [int(sitefile.readline().split()[0]) for i in (range(num))]

    num = int(sitefile.readline().split()[0])
    data["output_amounts"] = [float(sitefile.readline().split()[0]) for i in (range(num))]

    num = int(sitefile.readline().split()[0])
    data["locs"] = [int(sitefile.readline().split()[0]) for i in (range(num))]

    sites2geojson(sitefile)

    data["source_locations"] = [[float(i) for i in line.split(',')] for line in sitefile]



pprint(data)

with open(os.path.join(location_dir, "site.json"), 'w') as outfile:
    json.dump(data, outfile, indent=2)


