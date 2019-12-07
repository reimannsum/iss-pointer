#!/usr/bin/env python3
import time
import board
import busio
import adafruit_lsm303dlh_mag
import adafruit_lsm303_accel

i2c = busio.I2C(board.SCL, board.SDA)
mag_sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
acc_sensor = adafruit_lsm303_accel.LSM303_Accel(i2c)




if __name__ == "__main__":
	for i in range(10):
		mag_x, mag_y, mag_z = mag_sensor.magnetic
		acc_x, acc_y, acc_z = acc_sensor.acceleration

		print('Acceleration (m/s^2): ({0:10.3f}, {1:10.3f}, {2:10.3f})'.format(acc_x, acc_y, acc_z))
		print('Magnetometer (gauss): ({0:10.3f}, {1:10.3f}, {2:10.3f})'.format(mag_x, mag_y, mag_z))
		print('')
		time.sleep(1.0)
else:
	pass
