#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RPi Compass controller
Project: ISS Pointer

Dev: Reimannsum
Last Modified: Sept 04, 2019
"""
import time
from math import cos, sin, sqrt, degrees, atan2, radians
import board
import busio
import adafruit_lsm303dlh_mag
import adafruit_lsm303_accel
from rotateVectors import rotateAbout,find_rotation
from geomag.geomag import GeoMag as geomag




class Sensor:
	"""
	This class creates an object to read the chip

	"""

	def __init__(self):
		# pulling the drivers for the chip
		i2c = busio.I2C(board.SCL, board.SDA)
		self.mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
		self.acc = adafruit_lsm303_accel.LSM303_Accel(i2c)


	@property
	def read_mag(self):
		x, y, z = self.mag.magnetic
		return (x,z,y)


	@property
	def read_accel(self):
		x, y, z = self.acc.acceleration
		return (x,z,y)


def cart2sph(x, y, z):
	"""
	:param x: east is positive
	:param y: north is positive
	:param z: up is positive
	:return: degrees
	"""
	XsqPlusZsq = x ** 2 + z ** 2
	r = sqrt(XsqPlusZsq + y ** 2)  # r
	elev = degrees(atan2(XsqPlusZsq, y))  # phi
	az = degrees(atan2(y, x)) # theta
	if az >= 360:
		return az, elev, r
	else:
		return 0 + az, elev, r

def sph2cart(r, theta, elev):
	x = round(r * cos(radians(0 + elev)) * cos(radians(theta + 90)),8)
	y = round(r * cos(radians(0 + elev)) * sin(radians(theta + 90)),8)
	z = round(r * sin(radians(0 + elev)),8)
	return x, y, z

def get_declenation():
	gm = geomag()
	mag = gm.GeoMag(42.5337, -83.7384)
	return mag.dec

class Compass:
	"""
	This will handle interpreting all sensor readings
	gravity: is the XYZ vector for gravity
	x: east is positive
	y: north is positive
	z: up is positive
	"""

	def __init__(self):
		self.compass = Sensor()
		self.last_check_time = 0
		self.check_sensor()

		self.grav_rot_vect, self.grav_rot_angle = self.grav_align()
		# find the vector that must be rotated about, and the angle
		# to rotate about that vector in order to align the gravity
		# vector from the sensor with that of gravity, allowing
		# orientation to true gravity

		self.correction = self.grav_correct((0,10,0))
		# (0, 10, 0) is the cardinal vector for the spherical coords
		# used for the rest of the program,
		# in spherical this translates to (0, 0, 10)
		#   0 azmith (angle from north),
		#   0 elevation from horizon,
		#   10 distance from observer (discarded)

		self.sph_correction = cart2sph(self.correction)
		# get the angle
		# from assumed north and from assumed horizontal that the real north
		# horizontal is pointing

		self.declination = get_declenation()
		# Creates and returns an object
		# of the compas correction
		# > gm = geomag.GeoMag()
		# > mag = gm.GeoMag(42.5337, -83.7384)
		# > mag.dec
		# -7.12816029842447



		self.mag_N = self.grav_correct(self.compass.read_mag)

		pass

	def check_sensor(self):
		if 5 > (time.time() - self.last_check_time):
			return False, self.__gravity
		else:
			self.__gravity = self.compass.read_accel
			# sets gravity to Cartesian coords (X,Y,Z)
			self.last_check_time = int(time.time())
			return True, self.__gravity

	def update_grav(self):
		"""
		This will check if there is any significant difference
		in grav readings. if there is it will update gravity and
		:return: Boolean
		"""


	def get_grav(self):
		return self.__gravity

	@property
	def gravity(self):
		return self.get_grav()

	def grav_correct(self, other_vector):
		return rotateAbout(other_vector, self.grav_rot_vect, self.grav_rot_angle)

	def grav_align(self):
		return  find_rotation((0,0,-9.8), self.__gravity)

if __name__ == "__main__":
	print("Cardinal Directions:\nEast:")
	print(cart2sph(3,0,0))
	print("North:")
	print(cart2sph(0,3,0))
	print("West:")
	print(cart2sph(-3,0,0))
	print("South:")
	print(cart2sph(0,-3,0))
	print("Up:")
	print(cart2sph(0,0,3))
	print("Down:")
	print(cart2sph(0,0,-3))

	print("Magnetic Declenation:")
	print(get_declenation())
	print("\nNorth:")
	print(sph2cart(3, 0, 0))
	print("East:")
	print(sph2cart(3, 270, 0))
	print("South:")
	print(sph2cart(3, 180, 0))
	print("West:")
	print(sph2cart(3, 90, 0))
	print("Up:")
	print(sph2cart(3, 0, 90))
	print("Down:")
	print(sph2cart(3, 0, -90))
else:
	pass
