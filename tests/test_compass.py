#!/usr/bin/env python3

import pytest
from bin.compass import Compass


# def test_compass_init():
#     testing = True
#     initial_mag = (0.123, 0.456, 0.789)
#     initial_grav = (0.0, 0, -9.8)
#     standard_grav = (0.0, -9.8, 0.0)
#     compass = Compass(testing, initial_mag, initial_grav)
#     assert compass.get_grav() == (0.0, -0.1, 0.0)
#     assert compass.correction == (0, 90, 1)
#     assert compass.N_correct == 0
#     compass.update()
#     assert compass.get_grav() == initial_grav
#     assert compass.correction == (0, 90, 1)
#     assert compass.N_correct == 8.011019754273804
#     # test, test2 = compass.orient_up(compass.mag)
#     # print(test)
#     # print(test2)
#     # assert list(test) == (0.0, 0.0, 0.0)



# will need to check initialization

# will need to check that I can update the fields in a way that tests

# will need to show that orient_up works for all cases of new sensor readings





