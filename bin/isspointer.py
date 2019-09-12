#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 ___   ____    ____      ____     ____
|_ _| / ___|  / ___|    |  _ \   / ___|
 | |  \___ \  \___ \    | |_) | | |
 | |   ___) |  ___) |   |  __/  | |___
|___| |____/  |____/    |_|      \____|


Name: ISS Pointer Controller
Dev: K4YT3X IZAYOI
Date Created: Jan 15, 2018
Last Modified: December 12, 2018

Dev: Reimannsum
Last Modified: Aug 27, 2019

Description: This is the main script of the ISS Pointer.
It creates objects of the motor contoller and the servo controller.servo
"""

# The motor controller and servo controller
#from vector import Correction
import RPi.GPIO as GPIO
from avalon_framework import Avalon
import compass
from motor import Stepper
from servo import Servo
from skyfield.api import Topos, load
import json, time
import urllib.request
from geomag.geomag import GeoMag as geomag

VERSION = "1.0.1"
lat = 42.5337
lon = -83.7384

def print_icon():
	"""
	This prints the awsome ISS Pointer
	project icon!
	"""
	print('   ___   ____    ____      ____     ____')
	print('  |_ _| / ___|  / ___|    |  _ \   / ___|')
	print('   | |  \___ \  \___ \    | |_) | | |')
	print('   | |   ___) |  ___) |   |  __/  | |___')
	print('  |___| |____/  |____/    |_|      \____|\n')
	desc = "A Simple machine that points to the ISS\n"
	print((42 - len(desc)) // 2 * ' ' + desc)
	print((39 - len(VERSION)) // 2 * ' ' + Avalon.FG.Y + VERSION + Avalon.FM.RST + '\n')


class debug:

	def __init__(self, activated):
		self.activated = activated

	def debugger(self):
		pass

class Pointing_Vector:

	def __init__(self):
		self.compass = compass.Compass()
		self.mag_field = self.compass.read_mag
		self.gravity = self.compass.read_accel
		self.post_angle_correction = 0
		self.arm_angle_correction = 0


	def grav_correction(self, ):
		pass

	@property
	def turn(self):
		return self.post_angle_correction

	@property
	def point(self):
		return self.arm_angle_correction

	def correct_post(self, cw_angle):
		self.post_angle_correction += cw_angle

	def correct_arm(self, cw_angle):
		self.arm_angle_correction += cw_angle






class Isspointer:
	"""
	Dev: K4YT3X IZAYOI
	Date Created: Jan 15, 2018
	Last Modified: Jan 15, 2018

	Dev: Reimannsum
	I think I want to have this save the servo position in a file
	so that I can make sure it doesn't turn over and over in one
	direction and tangle the cords of the motors

	Last Modified: Aug 27, 2019

	This is the class that handles the iss pointer.
	Creating an object of this class will initialize and start
	the iss pointer.


	"""

	def __init__(self):
		"""
		Here I get the position of the pointer, the compass heading
		and implement the geomagnetic declination or north off set

		Dev: Reimannsum
		Last Modified: Aug 27, 2019
		"""

		self.sensor = self._setup_compass()
		# I don't know that this is required
		self.lat, self.lon = self._get_ISS_coordinates()
		self.motor = self._setup_motor()
		self.servo = self._setup_servo()

	def _setup_compass(self):
		"""
		Creates and returns an object
		of the compas correction
		> gm = geomag.GeoMag()
		> mag = gm.GeoMag(42.5337, -83.7384)
		> mag.dec
		-7.12816029842447
		"""
		sensor = Compass()
		gm = geomag.GeoMag()
		mag = gm.GeoMag(42.5337, -83.7384)
		sensor.set_magnetic_variance(mag.dec)

	def _setup_motor(self):
		"""
		Creates and returns an object
		of the Stepper motor controller
		"""
		return Stepper(12, 11, 13, 15)

	def _setup_servo(self):
		"""
		Creates and returns an object
		of the Servo controller
		"""
		return Servo(16)

	def _get_ISS_coordinates(self):
		"""
		Dev: K4YT3X IZAYOI
		Date Created: Jan 15, 2018
		Last Modified: Jan 15, 2018

		This method requests the current coordinate of the ISS
		from open notify in json format and parses it.

		Returns tuple (latitude, longitude)
		"""
		req = urllib.request.Request("http://api.open-notify.org/iss-now.json")
		response = urllib.request.urlopen(req)

		obj = json.loads(response.read().decode('utf-8'))
		return obj['iss_position']['latitude'], obj['iss_position']['longitude']

	def rest(self, seconds):
		new_data = self.sensor.read()


	def start(self):
		"""
		Dev: K4YT3X IZAYOI
		Date Created: Jan 15, 2018
		Last Modified: Jan 16, 2018

		Dev: Reimannsum
		Last Modified: Aug 27, 2019

		This method is the main ISS pointer controller
		it runs infinitively until Ctrl^C is pressed.
		"""
		ts = load.timescale()
		stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
		satellites = load.tle(stations_url)
		satellite = satellites['ISS (ZARYA)']
		observer = Topos('42.5337N', '83.7384W')
		while True:
			t = ts.now()
			days = t - satellite.epoch
			if abs(days) > 14:
				satellites = load.tle(stations_url, reload=True)
				satellite = satellites['ISS (ZARYA)']
			difference = satellite - observer
			topocentric = difference.at(t)
			alt, az, distance = topocentric.altaz()
			elevation =  alt.degrees
			direction = az.degrees

			Avalon.info("ISS Position Update:")
			print('Elevation :{}\nAzimuth :{}'.format(elevation, direction))
			self.motor.set_azimuth(float(direction))
			self.servo.set_angle(float(elevation))
			time.sleep(5)


if __name__ == "__main__":
	print_icon()
	isspointer = Isspointer()  # Creates ISS pointer object
	try:
		isspointer.start()  # Starts the pointer
	except:
		isspointer.motor.__del__()
	finally:
		GPIO.cleanup()
else:
	Avalon.error("This file cannot be imported!")
	Avalon.error("Please run this file independently.")
