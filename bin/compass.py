#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RPi Compass controller
Project: ISS Pointer

The goal of this class is to take sensor data and be able to act on it to

Dev: Reimannsum
Last Modified: Sept 04, 2019
"""
from math import cos, sin, degrees, atan2, radians
from geomag.geomag import GeoMag as geomag
from bin.sensor import Sensor
from bin.rotateVectors import rotateAbout, find_rotation


def cart2sph(x, y, z):
	"""
	:param x: east is positive
	:param y: up is positive
	:param z: north is positive
	:return: Spherical coordinates
	"""
	XsqPlusZsq = x ** 2 + z ** 2
	r = (XsqPlusZsq + y ** 2) ** 0.5  # r
	elev = degrees(atan2(y, XsqPlusZsq))  # phi
	az = degrees(atan2(x, z))  # theta
	if az == 0:
		az = 0
	if elev == 0:
		elev = 0
	if az >= 360:
		return az, elev, r
	else:
		return 0 + az, elev, r


def sph2cart(az, elev, r):
	"""
	:param az: Rotation east from north
	:param elev: rotation up from horizontal
	:param r: length of vector
	:return: Cartesian coordinates
	"""
	x = round(r * cos(radians(0 + elev)) * sin(radians(az)), 8)
	z = round(r * cos(radians(0 + elev)) * cos(radians(az)), 8)
	y = round(r * sin(radians(0 + elev)), 8)
	return x, y, z


def get_declination():
	gm = geomag()
	mag = gm.GeoMag(42.5337, -83.7384)
	return mag.dec


class Compass:
	"""
	This will handle interpreting all sensor readings
	this holds the last data read and interpreted
	gravity: is the XYZ vector for gravity

	Main function is the orient up function as it will give correction to anything given to it.

	x: east is positive
	y: north is positive
	z: up is positive
	"""

	def __init__(self, test=False, givenM=(0, 0, 0), givenA=(0,0,0)):

		#  Static value, this changes based on LAt, Lon and so is fixed in this implementation
		self.declination = get_declination()
		# > mag.dec
		# -7.12816029842447

		# create a sensor object to read data from the chip.
		if test:
			self.sensors = Sensor(test, givenM, givenA)
		else:
			self.sensors = Sensor()

		# Initialize variables
		self.N_correction = 0  # how many degrees assumed north is from true north
		self.gravity = (0.0, -0.1, 0.0)
		self.mag = (0.0, 0.0, 0.0)
		self.mag_Up = (0.0, 0.0, 0.0)
		self.spherical_correction = cart2sph(0, 1, 0)  # unit vector of up
		self.gravity_rotation_vector = (0, 0, 0)
		self.gravity_rot_angle_radians = 0

		# # There is no reason to call this in the initialization.
		# self.update()
		# print("spherical representation: ")
		# print(cart2sph(self.mag_Up[0], self.mag_Up[1], self.mag_Up[2]))
		# # get the azimuth angle of north to know what to subtract to correct for
		# # not pointing the device north before running.

		pass

	def __repr__(self):
		string = ""
		string += "Gravity:\nx: {0:4.3f}  y: {1:4.3f}  z: {0:4.3f}\n".format(
			self.gravity[0], self.gravity[1], self.gravity[2])
		string += "Spherical Fix:\nAz: {0:4.3f}  Elev: {1:4.3f}\n".format(
			self.spherical_correction[0], self.spherical_correction[1])
		string += "Fix Vect: ({0:4.3f},{1:4.3f},{2:4.3f})  Fix Angle: {3:4.3f}\n".format(
			self.gravity_rotation_vector[0], self.gravity_rotation_vector[1], self.gravity_rotation_vector[2],
			degrees(self.gravity_rot_angle_radians))
		string += "Mag field: \n({0:4.3f},{1:4.3f},{2:4.3f})\n".format(self.mag_Up[0], self.mag_Up[1], self.mag_Up[2])
		return string

	def print(self):
		string = ""
		string += "Gravity:\nx:{0:4.3f}  y:{1:4.3f}  z:{0:4.3f}\n".format(
			self.gravity[0], self.gravity[1], self.gravity[2])
		string += "Az: {0:4.3f}  Elev: {1:4.3f}\n".format(
			self.spherical_correction[0], self.spherical_correction[1])
		string += "Fix Vect: ({0:4.3f},{1:4.3f},{2:4.3f})  Fix Angle: {3:4.3f}\n".format(
			self.gravity_rotation_vector[0], self.gravity_rotation_vector[1], self.gravity_rotation_vector[2],
			degrees(self.gravity_rot_angle_radians))
		string += "Mag field: \n({0:4.3f},{1:4.3f},{2:4.3f})\n".format(self.mag_Up[0], self.mag_Up[1], self.mag_Up[2])
		thing = cart2sph(self.mag_Up[0], self.mag_Up[1], self.mag_Up[2])
		string += "Mag fix: Az: {0:4.3f}  Elev: {1:4.3f}".format(thing[0], thing[1])
		return string

	def update(self):
		old_grav = self.gravity
		self.gravity = self.sensors.read_accel()
		different = self.difference_check(old_grav, self.gravity)
		# Check if gravity has changed by at least 1 degree
		if different:
			# find the vector that must be rotated about, and the angle
			# to rotate about that vector in order to align the gravity
			# vector from the sensor with that of gravity, allowing
			# orientation to true gravity
			self.gravity_rotation_vector, self.gravity_rot_angle_radians = find_rotation((0, 0, -9.8), self.gravity)
		else:
			self.gravity = old_grav
		# set gravity back to not compound changes

		self.mag = self.sensors.read_mag()
		self.mag_Up = list(self.orient_up(self.mag))
		# get the angle of the magnetic field relative to the orientation of gravity
		self.N_correction = cart2sph(self.mag_Up[0], self.mag_Up[1], self.mag_Up[2])[0]
		self.N_correction += self.declination

	def difference_check(self, old_grav, new_grav):
		old_x, old_y, old_z = old_grav
		new_x, new_y, new_z = new_grav
		dx = old_x - new_x
		dy = old_y - new_y
		dz = old_z - new_z

		dev = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

		if dev > 0.15:
			return True  # vector has changed by 1 degree
		return False  # vector is less than 1 degree different from previous value

	def testing_update_mag(self, new_mag):
		testing = self.sensors.test
		if testing:
			grav = self.sensors.read_accel()
			self.sensors = Sensor(testing, new_mag, grav)

	def testing_update_accel(self, new_accel):
		testing = self.sensors.test
		if testing:
			self.sensors = Sensor(testing, self.mag, new_accel)

	def get_grav(self):
		return self.gravity

	def get_correction(self):
		return self.spherical_correction

	@property
	def correction(self):
		return self.get_correction()

	@property
	def N_correct(self):
		return self.N_correction

	def orient_up(self, vector):
		# Reorientates Vector to a gravity up orientation
		return rotateAbout(vector, self.gravity_rotation_vector, self.gravity_rot_angle_radians)


if __name__ == "__main__":
	compass = Compass()
	print(compass)

	print("Magnetic Declination:")
	print(get_declination())
else:
	pass
