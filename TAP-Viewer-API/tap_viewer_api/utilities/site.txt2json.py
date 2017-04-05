#!/usr/bin/env python3

"""
Hacky script to convert a TAP site.txt file to JSON for the Web App

Pass in the path to the site.txt you want to convert:

site.txt2json locations/sf/site.txt

It has been tested with sf and arctic SITE.txt files

"""

import sys
import os
import json
import geojson
from geojson import Polygon, Feature, FeatureCollection

from bna2geojson import is_clockwise  # for the clockwise check

infilename = sys.argv[1]
location_dir = os.path.dirname(infilename)


def readline_clean(fp):
    """
    reads a line, striping off the comments and whitespace
    """
    return fp.readline().strip().split('//')[0].strip()


def sites2geojson(fp):
    """
    Read the sites polygon definitions and write to geojson file: recpotors.json

    """
    readline_clean(fp)
    polys = []
    # [[min_lon, max_lat],[max_lon, min_lat]]
    b_box = [[None, None], [None, None]]
    with open(os.path.join(location_dir, "receptors.geojson"), 'w') as outfile:
        for line in fp:
            if "CUBES" in line:  # done with sites
                break
            # header line:
            site_num = int(line.split('"')[1].strip('#')) - 1  # change to zero-based indexing!
            num_points = int(line.split(',')[-1])
            poly = []
            for i in range(num_points):
                lon, lat = [float(i) for i in readline_clean(fp).split(',')]
                b_box[0][0] = lon if b_box[0][0] is None else min(b_box[0][0], lon)
                b_box[0][1] = lat if b_box[0][1] is None else max(b_box[0][1], lat)
                b_box[1][0] = lon if b_box[1][0] is None else max(b_box[1][0], lon)
                b_box[1][1] = lat if b_box[1][1] is None else min(b_box[1][1], lat)
                poly.append([lon, lat])
            # check orientation -- geojson wants "right hand rule"
            if is_clockwise(poly):
                print("poly is clockwise -- reversing")
                poly.reverse()
            poly = Feature(geometry=Polygon([poly]), site_num=site_num)
            polys.append(poly)
        geojson.dump(FeatureCollection(polys), outfile, indent=2)
    return b_box


data = {}
with open(infilename, 'r') as sitefile:
    line = readline_clean(sitefile)
    data['name'] = line.strip('"')
    print("location name:", data['name'])
    # ignore the map name
    line = readline_clean(sitefile)

    line = readline_clean(sitefile)
    data['num_spills'] = int(line.split()[0])
    print("number of spills", data['num_spills'])

    line = readline_clean(sitefile)
    num = int(line.split()[0])
    data['seasons'] = [readline_clean(sitefile).split('"')[1] for i in (range(num))]
    print("seasons", data['seasons'])

    line = readline_clean(sitefile)
    num = int(line.split()[0])
    print ("reading %i output times" % num)
    data["output_times"] = []
    for i in range(num):
        line = readline_clean(sitefile)
        val = line.split(" ", 1)[0]
        s = line.split(" ", 1)[1].strip().strip('"')
        data["output_times"].append([int(val), s])
    print("output times:", data["output_times"])

    num = int(readline_clean(sitefile).split()[0])
    print("reading %i output amounts:" % num)
    data["output_amounts"] = [[int(lin[0]), lin[1]]
                              for lin in (readline_clean(sitefile).split()
                                          for i in range(num))]
    print("output amounts:", data["output_amounts"])

    num = int(readline_clean(sitefile).split()[0])
    # data["locs"] = [int(sitefile.readline().split()[0]) for i in (range(num))]
    data["locs"] = [[float(lin[0]), lin[1].strip()]
                    for lin in (readline_clean(sitefile).split() for i in range(num))]
    print("LOCs:", data["locs"])

    # This should skip over the receptor sites definitions
    data["bounding_box"] = sites2geojson(sitefile)
    print("bounding box of sites is:", data["bounding_box"])

    data["source_locations"] = [["source: %i" % j, [float(i) for i in lin.split(',')]]
                                for j, lin in enumerate(sitefile)]

    # this is the default list
    data["oil_types"] = ["Non-weathering",
                         "Gasoline",
                         "Diesel",
                         "Light Crude",
                         "Medium Crude",
                         "Heavy Crude",
                         "Medium fuel oil",
                         "Fuel oil #6",
                         ]

with open(os.path.join(location_dir, "site.json"), 'w') as outfile:
    json.dump(data, outfile, indent=2)
