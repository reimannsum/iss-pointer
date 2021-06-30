#!/usr/bin/env python3
# test the motors to show that the drivers will work

#
import pytest
from bin.PointerVector import Angle

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