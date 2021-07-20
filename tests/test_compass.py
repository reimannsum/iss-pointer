#!/usr/bin/env python3
# the compass and sensor class as well as utility functions
#

import pytest
from bin.compass import *


def test_cart_to_sphere_conversion():
    cart_north = (0,0,1)
    cart_east = (1,0,0)
    cart_up = (0,1,0)
    cart_west = (-1,0,0)
    cart_south = (0,0,-1)
    cart_down = (0,-1,0)

    test = cart2sph(*cart_north)
    print("converting north:\n{}".format(test))
    assert test == (0, 0, 1)  #the confusing as we use north as the starting point for spherical
    test = cart2sph(*cart_south)
    print("converting south:\n{}".format(test))
    assert test == (180, 0, 1)
    test = cart2sph(*cart_east)
    print("converting east:\n{}".format(test))
    assert test == (90, 0, 1)
    test = cart2sph(*cart_west)
    print("converting west:\n{}".format(test))
    assert test == (-90, 0, 1)
    test = cart2sph(*cart_down)
    print("converting down:\n{}".format(test))
    assert test == (0, -90, 1)
    test = cart2sph(*cart_up)
    print("converting up:\n{}".format(test))
    assert test == (0, 90, 1)


def test_sphere_to_cart_conversion():
    sph_north = (0,0,1)
    sph_east = (90,0,1)
    sph_south = (180,0,1)
    sph_west = (270,0,1)
    sph_west2 = (-90,0,1)
    sph_up = (0,90,1)
    sph_down = (0,-90,1)

    test = sph2cart(*sph_north)
    print("converting (0,0):\n{}".format(test))
    assert test == (0, 0, 1)



