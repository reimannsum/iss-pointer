#!/usr/bin/env python3
# test using the screen to show the current state of the sensor
import time
from bin.screen import Screen
from bin.compass import Compass

myScreen = Screen()
myCompass = Compass()

while True:
	myCompass.last_check_time = 0
	myCompass.check_sensor()
	stats = myCompass.print()
	print(stats)
	myScreen.set_display(stats.split('\n'))
	time.sleep(0.25)
