#!/usr/bin/env python3
# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import time
# Import the SSD1306 module.
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
disp.fill(0)

disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()
test = 'ABCDEFGHIJKLMNOPQRSTU'
while True:
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	Strings = ['','','','','','','','']
	for i in range(192):
		# Draw a black filled box to clear the image.
		draw.rectangle((0, 0, width, height), outline=0, fill=0)

		# add a letter to a string
		string = i // 21
		letter = i % 21
		Strings[string] += test[letter]
		draw.text((x, top + 0), Strings[0], font=font, fill=255)
		draw.text((x, top + 8), Strings[1], font=font, fill=255)
		draw.text((x, top + 16), Strings[2], font=font, fill=255)
		draw.text((x, top + 24), Strings[3], font=font, fill=255)
		draw.text((x, top + 32), Strings[4], font=font, fill=255)
		draw.text((x, top + 40), Strings[5], font=font, fill=255)
		draw.text((x, top + 48), Strings[6], font=font, fill=255)
		draw.text((x, top + 56), Strings[7], font=font, fill=255)

		disp.image(image)
		disp.show()
		time.sleep(1)
