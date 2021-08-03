#!/usr/bin/env python3

import pytest
from math import degrees
from bin.rotateVectors import *

def test_find_rotation():
    north = (1, 0, 0)
    east = (0, 1, 0)
    up = (0, 0, 1)
    test_vector, angle = find_rotation(north, east)
    assert tuple(test_vector) == up
    assert degrees(angle) == 90

def test_grav_rotation():
    gravity = (0.0, 0.0, -9.8)
    result_vector, result_angle = find_rotation(gravity, gravity)
    assert result_angle == 0
    assert result_vector == [0, 0, 1]

    pass
