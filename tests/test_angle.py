#!/usr/bin/env python3
# test the motors to show that the drivers will work

#
import pytest
from bin.PointerVector import Angle

@pytest.fixture
def angle_zero():
	return Angle()

@pytest.fixture
def angle_180():
	return Angle(180)

@pytest.fixture
def angle_negative_five():
	return Angle(-5)

def test_initial_conditions():
	assert angle_zero.angle == 0
	assert angle_180.angle == 180


# noinspection PyTypeChecker
def test_addition_and_subtraction():
	assert angle_zero + 5 == 5 		 # angles add
	assert angle_zero + 365 == 5	 # angles overflow when adding
	assert angle_zero - 5 == 355	 # angles underflow when subtracting
	assert angle_zero + -5 == 355	 # angles underflow when adding a negative






