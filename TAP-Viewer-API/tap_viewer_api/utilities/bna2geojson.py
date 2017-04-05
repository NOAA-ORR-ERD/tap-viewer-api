#!/usr/bin/env python3

"""
Hacky script to convert a BNA file (as used by GNOME and TAP)

to geoJSON

"""

import sys
import os
import json
import geojson
from geojson import Polygon, Feature, FeatureCollection


infilename = sys.argv[1]
location_dir = os.path.dirname(infilename)


def GetNextBNAPolygon(f):
    """
    Ported from gnome.utilities.file_tools

    Utility function that returns the next polygon from a BNA file

    returns: (points, poly_type, name, sname) where:
        points:    Nx2numpy array of floats with the points
        poly_type: one of "point", "line", "poly"
        name:      name defined in the BNA
        sname:     secondary name defined in the BNA

    NOTE: It is the BNA standard to duplicate the first and last points.
          In that case, the duplicated last point is removed.

           "holes" in polygons are not supported in this code.
    See:
       http://www.softwright.com/faq/support/boundary_file_bna_format.html

    NOTE: This code doesn't allow extra spaces around the commas in the
          header line.
          If there are no commas allowed in the name, it would be easier to
          simply split on the commas
          (or march through the line looking for the quotes -- regex?)
    """
    while True: # skip blank lines
        header = f.readline()
        if not header: # end of file
            return (None,) * 4
        if header.strip(): # found a header
            break
        else:
            continue
    try:
        fields = header.split('"')
        name = fields[1]
        sname = fields[3]
        num_points = int(fields[4].strip()[1:])
        #header = header.replace('", "', '","') # some bnas have an extra space
        #name, rest = header.strip().split('","')
    except (ValueError, IndexError):
        raise ValueError('something wrong with header line: {0}'
                         .format(header))

    if num_points < 0 or num_points == 2:
        poly_type = 'polyline'
        num_points = abs(num_points)
    elif num_points == 1:
        poly_type = 'point'
    elif num_points > 2:
        poly_type = 'polygon'
    else:
        raise BnaError("polygon {0} does not have a valid number of points"
                       .format(name))

    points = []
    for i in range(num_points):
        points.append([float(j) for j in f.readline().split(',')])

    if poly_type == 'polygon':  # first and last points should be duplicated in geojson
        if not points[0] != points[-1]:
            points.append(points[0])

    return (points, poly_type, name, sname)




def sites2geojson(fp):
    """
    Read the BNA polygon definitions and write to geojson file.
    """

    polys = []

    with open("map.geojson", 'w') as outfile:
        while True:
            points, poly_type, name, sname = GetNextBNAPolygon(fp)
            if points is None:
                break
            if poly_type == "polygon":  # only do polygons for now
                ptype = "land" if sname == "1" else "lake"  # maybe not right, but there is something like that...
                geo_poly = Feature(geometry=Polygon([points]), poly_type=ptype)
                polys.append(geo_poly)
        geojson.dump(FeatureCollection(polys), outfile, indent=2)
    return

if __name__ == "__main__":
    bna_name = sys.argv[1]
    with open(bna_name, 'r') as bna_file:
        sites2geojson(bna_file)

