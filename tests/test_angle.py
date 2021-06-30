#!/usr/bin/env python3
# test the motors to show that the drivers will work

#
import pytest
from pytest import approx
from bin.Angle import Angle


@pytest.fixture
def angle_negative_five():
	return Angle(-5)

def test_initial_conditions():
	test_0 = Angle()
	test_180 = Angle(180)
	assert 0.0 == 0.0
	assert test_0.angle == approx(0)
	assert test_180.angle == approx(180)


# noinspection PyTypeChecker
def test_addition_and_subtraction():
	test = Angle()
	assert (test + 5) == 5 		 # angles add
	assert (test + 365) == 5	 # angles overflow when adding
	assert (test - 5) == 355	 # angles underflow when subtracting
	assert (test + -5) == 355	 # angles underflow when adding a negative

def test_adding_Angles_together():
	test = Angle
	test_180 = Angle(180)
	Test_negative_5 = Angle(-5)
	assert (test + test_180).angle == 180






