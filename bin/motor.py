#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RPi Motor Controller
Project: ISS Pointer
Dev: DJGood
Date Created: Dec 16, 2017
Last Modfied: Dec 18, 2017

Dev: K4YT3X IZAYOI
Last Modified: December 12, 2018

Dev: Reimannsum
Last Modified: Aug 27, 2019
"""
from enum import Enum
from time import sleep

import RPi.GPIO as GPIO
from avalon_framework import Avalon

from exceptions import InvalidDirectionError

VERSION = "1.0.1"


class DIRECTION(Enum):
    CW = 1
    CCW = 0


class Stepper(object):
    #	GEAR_RATIO = 2.5

    MICROSTEP_TRUTH_TABLE = {
        # resolution: (ms1, ms2)
        'full': (0, 0),
        'half': (1, 0),
        'quarter': (0, 1),
        'eigth': (1, 1)
    }

    MICROSTEP_RESOLUTION_MULTIPLIER = {
        'full': 1,
        'half': 0.5,
        'quarter': 0.25,
        'eigth': 0.125
    }

    def __init__(self, pin_array, steps=1000, gearing=1):
        # GPIO.setmode(GPIO.BOARD) # adafruit drivers set this to BCM numbering

        self.dir_pin = pin_array[0]
        self.step_pin = pin_array[1]
        self.ms1_pin = pin_array[2]
        self.ms2_pin = pin_array[3]
        self.step_delay = 0.001
        self._microstep_resolution = 'full'
        self.current_pos = 0
        # This will allow people to customize this for their own setup easily
        self.steps_per_revolution = steps * gearing
        # self.GEAR_RATIO = gearing

        self.setup()

    def __del__(self):
        # Cleans up GPIO after object deleted
        GPIO.cleanup()

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if isinstance(direction, DIRECTION):
            self._direction = direction
        else:
            raise InvalidDirectionError

    @property
    def microstep_resolution(self):
        return self._microstep_resolution

    @microstep_resolution.setter
    def microstep_resolution(self, resolution):
        if resolution not in self.MICROSTEP_TRUTH_TABLE.keys():
            self._microstep_resolution = 'eigth'
        else:
            self._microstep_resolution = resolution
        self.set_microstep_resolution_in_easydriver()

    @property
    def azimuth(self):
        return self._azimuth

    def set_microstep_resolution_in_easydriver(self):
        ms1, ms2 = self.MICROSTEP_TRUTH_TABLE[self._microstep_resolution]
        GPIO.output(self.ms1_pin, ms1)
        GPIO.output(self.ms2_pin, ms2)

    def setup(self):
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.ms1_pin, GPIO.OUT)
        GPIO.setup(self.ms2_pin, GPIO.OUT)

    def step(self):
        """
        Dev: DJGood
        Date Created: Dec 16, 2017
        Last Modfied: Dec 18, 2017

        Dev K4YT3X IZAYOI
        Last Modified: Jan 16, 2018

        Notes from DJGood: 0.9 degrees per step * resolution * gear_ratio
        This is probably the wrong way to do this but it works. It would be
        good to rethink how this could work.
        """

        GPIO.output(self.step_pin, 1)
        sleep(self.step_delay)
        GPIO.output(self.step_pin, 0)
        sleep(self.step_delay)

    def rotate(self, angle, cw=True):
        steps = round(angle * self.steps_per_revolution / 360)
        # print("Currently at : {0}, moving {1}".format(self.current_pos,steps))
        if cw:
            if self.current_pos + steps < self.steps_per_revolution:
                self.current_pos = self.current_pos + steps
            else:
                self.current_pos = self.current_pos + steps - self.steps_per_revolution
        elif not cw:
            if self.current_pos - steps > 0:
                self.current_pos = self.current_pos - steps
            else:
                self.current_pos = self.current_pos - steps + self.steps_per_revolution
        for _ in range(steps):
            self.step()

    # print("moved")

    def set_azimuth(self, azimuth):
        """
        Dev: K4YT3X IZAYOI
        Date Created: Jan 16, 2018
        Last Modified: Jan 16, 2018

        This is the class that handles the iss pointer.
        Creating an object of this class will initialize and start
        the iss pointer.
        """
        # 360 degrees / steps per revolution * current steps
        current_angle = 360 * self.current_pos / (self.steps_per_revolution)
        angle_to_rotate = azimuth - current_angle
        # print("azimuth: {0:4.3f}\tcurrent angle: {1:4.3f}\tTo rotate: {2:4.4f}".format(azimuth,current_angle,angle_to_rotate))
        if angle_to_rotate == 0:  # Do not rotate when change in angle is 0
            pass
        elif angle_to_rotate > 0:  # Rotate clockwise
            GPIO.output(self.dir_pin, 0)
            self.rotate(angle_to_rotate)
        elif angle_to_rotate < 0:  # Rotate counter-clockwise
            # Send signal to the direction pin so it rotates ccw
            GPIO.output(self.dir_pin, 1)
            self.rotate(-1 * angle_to_rotate, False)
            GPIO.output(self.dir_pin, 0)  # Cut signal


# --------------------------------- Begin Self Testing
"""
The code below is for self-testing when this file
is ran independently. It takes an integer and a direction
then rotates the motor.
"""

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    stepper = Stepper([18, 17, 27, 22])
    while True:
        stepper.rotate(int(Avalon.gets("Angle")), Avalon.ask("CW?", True))
