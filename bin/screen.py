#!/usr/bin/env python3
# Screen class for displaying information
# for the ISSPointer

from adafruit_blinka.board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import time
import adafruit_ssd1306

class Screen:
	"""
	The screen can display 18 characters across\

Azimuth: ###.###*       Line 1
Elevation:-##.##*       Line 2
						Line 3
North: #.###* CCW/CW    Line 4
Gravity:				Line 5
X: -#.##### m/s         Line 6
Y: -#.##### m/s         Line 7
Z: -#.##### m/s         Line 8
	"""

	def __init__(self):
		self.i2c = busio.I2C(SCL, SDA)
		self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=0x3c)
		self.disp.fill(0)
		self.disp.show()
		self.image = Image.new('1', (self.disp.width, self.disp.height))
		self.draw = ImageDraw.Draw(self.image)
		self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
		padding = -2
		self.top = padding
		self.bottom = self.disp.height - padding
		self.font = ImageFont.load_default()
		self.display_info = ['', '', '', '', 'Gravity:', '', '', '']



	def set_pointing(self, az, elev):
		self.display_info[0] = u"Azimuth:{0:8.03f}\u00b0".format(az)
		self.display_info[1] = u"Elevation :{0:6.02f}\u00b0".format(elev)
		self.update_display()

	def set_gravity(self, x, y, z):
		self.display_info[5] = "X:{0: 8.5f} m/s".format(x)
		self.display_info[6] = "Y:{0: 8.5f} m/s".format(y)
		self.display_info[7] = "Z:{0: 8.5f} m/s".format(z)
		self.update_display()

	def set_north(self, declination):
		if declination > 0:
			self.display_info[3] = u"North: {0:5.3f}\u00b0 CCW".format(declination)
		else:
			self.display_info[3] = u"North: {0:5.3f}\u00b0 CW".format(abs(declination))
		self.update_display()

	def set_display(self, string_list):
		for i in range(len(string_list)):
			self.display_info[i] = string_list[i]
		self.update_display()

	def update_display(self):
		self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
		for k in range(8):
			self.draw.text((0, self.top + 8 * k), self.display_info[k], font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.show()

	pass

if __name__ == '__main__':
	i2c = busio.I2C(SCL, SDA)
	disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
	disp.fill(0)
	disp.show()

	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	padding = -2
	top = padding
	bottom = height - padding
	font = ImageFont.load_default()
	test = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	while True:
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		Strings = ['', '', '', '', '', '', '', '']
		for i in range(8):
			for j in range(21):
				# Draw a black filled box to clear the image.
				draw.rectangle((0, 0, width, height), outline=0, fill=0)
				if i % 2 == 0:
					Strings[i] +=  test[j]
				else:
					Strings[i] += test[25-j]
				for k in range(8):
					draw.text((0, top + 8*k), Strings[k], font=font, fill=255)
				disp.image(image)
				disp.show()
				time.sleep(1)
	pass
