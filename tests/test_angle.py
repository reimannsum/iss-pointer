#!/usr/bin/env python3
# test the motors to show that the drivers will work
#
import pytest
from pytest import approx
from bin.Angle import Angle


def test_initial_conditions():
    test_0 = Angle()
    test_180 = Angle(180)
    test_big = Angle(540)
    assert approx(0) == test_0
    assert approx(180) == test_180
    assert approx(180) == test_big


# noinspection PyTypeChecker
def test_addition_and_subtraction():
    test = Angle()
    assert (test + 5) == 5  # angles add
    assert (test + 365) == 5  # angles overflow when adding
    assert (test - 5) == 355  # angles underflow when subtracting
    assert (test + -5) == 355  # angles underflow when adding a negative


def test_adding_Angles_together():
    test_0 = Angle()
    test_180 = Angle(180)
    test_negative_5 = Angle(-5)
    result = test_0 + test_180
    assert result == 180
    result = test_0 + test_negative_5
    assert result == 355
    result += test_180
    assert result == 175
