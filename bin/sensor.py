#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RPi Gravitational Sensor controller
Project: ISS Pointer

The goal of this class is to read sensor data from the chip

Dev: Reimannsum
Last Modified: Sept 04, 2019
"""
import adafruit_blinka.board as board
import adafruit_lsm9ds1
import busio


class Sensor:
	"""
	This class creates an object that gives readings for the magnetometer and accelerometer

	"""

	def __init__(self, test=False, givenM=(0, 0, 0), givenA=(0,0,0)):
		if not test:
			self.test = False
			# pulling the drivers for the chip
			i2c = busio.I2C(board.SCL, board.SDA)
			self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
		else:
			self.test = True
			self.mag_reading = givenM
			self.accel_reading = givenA

	def read_mag(self):
		if not self.test:  # I believe this is a hack to avoid dealing with the orientation of the chip on the device
			x, z, y = self.sensor.magnetic
		else:
			x, y, z = self.mag_reading
		return x, y, z

	def read_accel(self):
		if not self.test:  # I believe this is a hack to avoid dealing with the orientation of the chip on the device
			x, z, y = self.sensor.acceleration
		else:
			x, y, z = self.accel_reading
		return x, y, z
