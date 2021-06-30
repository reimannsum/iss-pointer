#!/usr/bin/env python3
# test the motors to show that the drivers will work

#
import pytest
import bin.PointerVector

if __name__ == '__main__':


	testP = PointingVector()
	print(testP)
	testP.azimuth_add(1)
	print(testP)
	testP.elevation_add(1)
	print(testP)


	pass