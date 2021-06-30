#!/usr/bin/env python3
# calibrate.py
"""
Name: RPi Compass controller
Project: ISS Pointer

Dev: Reimannsum
Last Modified: Oct 16, 2019
"""
import time
import board
import busio
import lsm303dlh_mag
import lsm303_accel
from math import sqrt as root
from time import time

# pulling the drivers for the chip
i2c = busio.I2C(board.SCL, board.SDA)
mag_sensor = lsm303dlh_mag.LSM303DLH_Mag(i2c)
acc_sensor = lsm303_accel.LSM303_Accel(i2c)
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

max_acc_x, max_acc_y, max_acc_z = 0,0,0
max_mag_x, max_mag_y, max_mag_z = 0,0,0
min_acc_x, min_acc_y, min_acc_z = 0,0,0
min_mag_x, min_mag_y, min_mag_z = 0,0,0

acc_x_range, acc_y_range, acc_z_range = 0,0,0
mag_x_range, mag_y_range, mag_z_range = 0,0,0

max_acc_magnitude = 0
max_mag_magnitude = 0

count = 0
t_end = time() + 60 * 3 # run for 3 minutes
while time() < t_end:
	acc_x, acc_y, acc_z = acc_sensor.acceleration
	mag_x, mag_y, mag_z = mag_sensor.magnetic
	acc_magnitude = root((acc_x ** 2) + (acc_y ** 2) + (acc_z ** 2))
	mag_magnitude = root((mag_x ** 2) + (mag_y ** 2) + (mag_z ** 2))

	if max_acc_x < acc_x:
		max_acc_x = acc_x
	if max_acc_y < acc_y:
		max_acc_y = acc_y
	if max_acc_z < acc_z:
		max_acc_z = acc_z
	if max_mag_x < mag_x:
		max_mag_x = mag_x
	if max_mag_y < mag_y:
		max_mag_y = mag_y
	if max_mag_z < mag_z:
		max_mag_z = mag_z

	if min_acc_x > acc_x:
		min_acc_x = acc_x
	if min_acc_y > acc_y:
		min_acc_y = acc_y
	if min_acc_z > acc_z:
		min_acc_z = acc_z
	if min_mag_x > mag_x:
		min_mag_x = mag_x
	if min_mag_y > mag_y:
		min_mag_y = mag_y
	if min_mag_z > mag_z:
		min_mag_z = mag_z

	if max_acc_magnitude < acc_magnitude:
		max_acc_magnitude = acc_magnitude
	if max_mag_magnitude < mag_magnitude:
		max_mag_magnitude = mag_magnitude
		
	if round(time()) % 2 == 0:
		print("Readings from the sensor:")
		print("Acceleration: ({0.3}, {1}, {2}) magnatude {3}".format(acc_x, acc_y, acc_z, acc_magnitude))
		print("Magnetism: ({0}, {1}, {2}) magnatude {3}".format(mag_x, mag_y, mag_z, mag_magnitude))
	count += 1

range_acc_x = max_acc_x - min_acc_x
range_acc_y = max_acc_y - min_acc_y
range_acc_z = max_acc_z - min_acc_z

range_mag_x = max_mag_x - min_mag_x
range_mag_y = max_mag_y - min_mag_y
range_mag_z = max_mag_z - min_mag_z

print("There were {} data points collected {}.\n\n".format(count))
print("Acceleration:\n")
print("_X min:{0}\t_X max:{1}\tRange: {2}".format(min_acc_x,max_acc_x,range_acc_x))
print("_Y min:{0}\t_Y max:{1}\tRange: {2}".format(min_acc_y,max_acc_y,range_acc_y))
print("_Z min:{0}\t_Z max:{1}\tRange: {2}".format(min_acc_z,max_acc_z,range_acc_z))
print("Magnitism:\n")
print("_X min:{0}\t_X max:{1}\tRange: {2}".format(min_mag_x,max_mag_x,range_mag_x))
print("_Y min:{0}\t_Y max:{1}\tRange: {2}".format(min_mag_y,max_mag_y,range_mag_y))
print("_Z min:{0}\t_Z max:{1}\tRange: {2}".format(min_mag_z,max_mag_z,range_mag_z))

o_file = open("/home/pi/.issconfig/calibration", 'w')
o_file.write("Acceleration: min, max, range")
o_file.write("x: {} {}".format(min_acc_x, range_acc_x))
o_file.write("y: {} {}".format(min_acc_y, range_acc_y))
o_file.write("z: {} {}".format(min_acc_z, range_acc_z))
o_file.write("Magnetic: min, max, range")
o_file.write("x: {} {}".format(min_mag_x, range_mag_x))
o_file.write("y: {} {}".format(min_mag_y, range_mag_y))
o_file.write("z: {} {}".format(min_mag_z, range_mag_z))


