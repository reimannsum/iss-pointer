#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RPi Compass controller
Project: ISS Pointer

Dev: Reimannsum
Last Modified: Sept 04, 2019
"""
from math import cos, sin, sqrt, degrees, atan2
import Adafruit_LSM303


class Compass:
	"""
	This class creates an object to read the chip

	"""

	def __init__(self):
		# pulling the drivers for the chip
		self.lsm303 = Adafruit_LSM303.LSM303()

	@property
	def read(self):
		return self.lsm303.read()

	@property
	def read_mag(self):
		accel, mag = self.read()
		return mag

	@property
	def read_mag_sph(self):
		accel, mag = self.read()
		return cart2sph(mag)

	@property
	def read_accel(self):
		accel, mag = self.read()
		return accel

	@property
	def read_accel_sph(self):
		accel, mag = self.read()
		return cart2sph(accel)


def cart2sph(x, y, z):
	"""
	:param x: east is positive
	:param y: up is positive
	:param z: north is positive
	:return:
	"""
	XsqPlusZsq = x ** 2 + z ** 2
	r = sqrt(XsqPlusZsq + y ** 2)  # r
	elev = 90 - degrees(atan2(z, x))  # phi
	az = degrees(atan2(y, sqrt(XsqPlusZsq))) -90  # theta
	if az >= 0:
		return r, az, elev
	else:
		return r, 360 + az, elev

def sph2cart(r, theta, elev):
	x = r * sin(90 - elev) * cos(theta + 90)
	y = r * sin(90 - elev) * sin(theta + 90)
	z = r * cos(90 - elev)
	return x, y, z
