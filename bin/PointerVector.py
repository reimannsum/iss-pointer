#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: RPi pointing controller
Project: ISS Pointer
Dev: Reimannsum
Date Created: Dec 19, 2019
"""

from .compass import *

class Half_Angle:
	def __init__(self, measure = 0.0):
		if measure > 180:
			self.angle = measure - 360
		else:
			self.angle = measure
	def __add__(self, other): # Define the  + function
		other = float(other)
		total = self.angle + other
		if total > 180:
			return total - 360
		elif total < -180:
			return total + 360
		else:
			return total
	def __sub__(self, other): # Define the - function
		other = float(other)
		total = self.angle - other
		if total > 180:
			return total - 360
		elif total < -180:
			return total + 360
		else:
			return total
	def __repr__(self): # Define what is displayed when printed
		return str(self.angle)
	def __iadd__(self, other): # Define the += function
		return Half_Angle(self + float(other))
	def __float__(self):
		return self.angle


class Angle:

	def __float__(self):
		return self.angle
	def __init__(self, measure = 0.0):
		self.angle = measure
	def __add__(self, other): # Define the  + function
		other = float(other)
		total = self.angle + other
		if total > 360:
			return total - 360
		elif total < 0:
			return total + 360
		else:
			return total

	def __sub__(self, other): # Define the - function
		other = float(other)
		total = self.angle - other
		if total > 360:
			return total - 360
		elif total < 0:
			return total + 360
		else:
			return total

	def __repr__(self): # Define what is displayed when printed
		if self.angle > 180:
			return str(self.angle-360)
		else:
			return str(self.angle)
	def __iadd__(self, other): # Define the += function
		return Angle(self + float(other))

class Pointing_Vector:
	# stores the correction due to compass readings for
	# calibrating the pointer
	#

	def __init__(self):
		self.azimuth = Angle()
		self.elevation = Half_Angle()
		self.base_correction = Half_Angle()
		self.arm_correction = Half_Angle()
		self.last_grav = (0,0)
		self.compass = Compass()
		self.N_correction = 0
		self.declination = 0
		#self.set_true_north() # not needed as check grav is forced
		self.check_gravity(True)

	def azimuth_set(self, angle):
		angle = float(angle)  # don't worry if you are passed a string number
		self.azimuth = Angle(angle)
		self.azimuth_add(self.base_correction.angle)

	def elevation_set(self, angle):
		angle = float(angle)  # don't worry if you are passed a string number
		self.elevation = Half_Angle(angle)
		self.elevation_add(self.arm_correction)
		# This keeps us from worrying about being given an elevation over 90 degrees

	def azimuth_add(self, angle):
		angle = float(angle)  # don't worry if you are passed a string number
		self.azimuth += angle

	def elevation_add(self, angle):
		angle = float(angle) # don't worry if you are passed a string number
		total = self.elevation + angle

		if 270 > total > 90: # Seperate out the angle change from the rotation mechanics
			self.azimuth_add(180)

		if 180 > total > 90:
			print("{0:5.3f} and {1:5.3f} are greater than 90 when added together".format(float(self.elevation), angle))
			print(total)
			leftover = total - 90
			self.elevation = Half_Angle(90 - leftover)
		elif 270 > total > 180:
			print("{0:5.3f} and {1:5.3f} are less than -90 when added together".format(self.elevation, angle))
			leftover = total + 180
			self.elevation = Half_Angle(360 - leftover)
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
		self.base_correction = Half_Angle()
		self.base_correction += self.N_correction
		self.base_correction += self.declination

	def check_gravity(self, forced=False):
		changed = self.compass.check_gravity()
		if changed or forced:
			n_az, n_elev, garbage = self.compass.get_correction()
			self.set_true_north()
			self.last_grav = (n_az, n_elev)
			self.arm_correction = Half_Angle()
			self.arm_correction += n_elev

	def __repr__(self):
		return "Azimuth: {0}\tElevation: {1}\nBase: {2}\tArm: {3}\nDeclenation: {4}".format(self.azimuth,self.elevation, self.base_correction, self.arm_correction, self.declination)




if __name__ == '__main__':
	test1 = Angle()
	test2 = Angle(180)
	if test1.angle == 0 and test2.angle == 180:
		print("Angle Initializes.")
	if test1 +5 == 5:
		print("Angles Add.")
	if test1 + 365 == 5:
		print("Angles add overflow")
	if test1 + -5 == 355:
		print("Angles add negative and underflow")
	if test1 - 5 == 355:
		print("Angles subtract and underflow")

	test1 = Angle(-50)
	print(test1.angle)
	test1+= 0
	print(test1.angle)

	testP = Pointing_Vector()
	print(testP)
	testP.azimuth_add(1)
	print(testP)
	testP.elevation_add(1)
	print(testP)


	pass
