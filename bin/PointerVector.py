#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RPi pointing controller
Project: ISS Pointer
Dev: Reimannsum
Date Created: Dec 19, 2019
"""
from bin.Angle import HalfAngle, Angle
from bin.compass import *


class PointingVector:
    # stores the correction due to compass readings for
    # calibrating the pointer
    #

    def __init__(self):
        self.azimuth = Angle()
        self.elevation = HalfAngle()
        self.base_correction = HalfAngle()
        self.arm_correction = HalfAngle()
        self.last_grav = (0, 0)
        self.compass = Compass()
        self.N_correction = 0
        self.declination = 0
        # self.set_true_north() # not needed as check grav is forced
        self.check_gravity(True)

    def azimuth_set(self, angle):
        angle = float(angle)  # don't worry if you are passed a string number
        self.azimuth = Angle(angle)
        self.azimuth_add(self.base_correction.angle)

    def elevation_set(self, angle):
        angle = float(angle)  # don't worry if you are passed a string number
        self.elevation = HalfAngle(angle)
        self.elevation_add(self.arm_correction)

    # This keeps us from worrying about being given an elevation over 90 degrees

    def azimuth_add(self, angle):
        angle = float(angle)  # don't worry if you are passed a string number
        self.azimuth += angle

    def elevation_add(self, angle):
        angle = float(angle)  # don't worry if you are passed a string number
        total = self.elevation + angle

        if 270 > total > 90:  # Seperate out the angle change from the rotation mechanics
            self.azimuth_add(180)

        if 180 > total > 90:
            print("{0:5.3f} and {1:5.3f} are greater than 90 when added together".format(float(self.elevation), angle))
            print(total)
            leftover = total - 90
            self.elevation = HalfAngle(90 - leftover)
        elif 270 > total > 180:
            print("{0:5.3f} and {1:5.3f} are less than -90 when added together".format(self.elevation, angle))
            leftover = total + 180
            self.elevation = HalfAngle(360 - leftover)
        else:
            self.elevation += angle

    def correct_base(self, cw_angle):
        """
        :param cw_angle: is given the angle from true north
        :return: returns the angle given the current orientation
        """
        return self.base_correction + cw_angle

    def correct_arm(self, cw_angle):
        """
        :param cw_angle: is given the angle from horizontal
        :return: returns the angle given the current orientatio
        """
        return self.arm_correction + cw_angle

    def set_true_north(self):
        self.N_correction = -1 * self.compass.N_correct
        # N correction is measured relative to the device
        self.declination = self.compass.declination
        # Declination is measured in degrees CW from magnetic north
        # to point to true north
        self.base_correction = HalfAngle()
        self.base_correction += self.N_correction
        self.base_correction += self.declination

    def check_gravity(self, forced=False):
        changed = self.compass.check_gravity()
        if changed or forced:
            n_az, n_elev, garbage = self.compass.get_correction()
            self.set_true_north()
            self.last_grav = (n_az, n_elev)
            self.arm_correction = HalfAngle()
            self.arm_correction += n_elev

    def __repr__(self):
        return "Azimuth: {0}\tElevation: {1}\nBase: {2}\tArm: {3}\nDeclenation: {4}".format(self.azimuth,
                                                                                            self.elevation,
                                                                                            self.base_correction,
                                                                                            self.arm_correction,
                                                                                            self.declination)
