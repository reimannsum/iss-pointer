#!/usr/bin/env python3
# test using the screen to show the current state of the sensor
import time
from  screen import screen
from compass import compass

myScreen = screen.Screen()
myCompass = compass.Compass()

while True:
	myCompass.last_check_time = 0
	myCompass.calculate_gravity()
	stats = myCompass.print().split('\n')
	myScreen.set_display(stats)
	time.sleep(0.25)
