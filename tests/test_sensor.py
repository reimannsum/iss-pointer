#!/usr/bin/env python3

import pytest
from bin.sensor import Sensor


def test_sensor():
    testing = True
    initial_mag = (0.123, 0.456, 0.789)
    initial_grav = (0.01, -9.8, 0.02)
    sensor = Sensor(testing, initial_mag, initial_grav)

    assert sensor.test
    assert sensor.read_mag() == initial_mag
    assert sensor.read_accel() == initial_grav
