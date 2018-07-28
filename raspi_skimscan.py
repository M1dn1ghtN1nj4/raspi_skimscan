# file: raspi_skimscan.py
# Modified by Noah Greene (m1dn1ghtn1nj4@gmail.com)
# original author: Tyler Winegarner (twinegarner@gmail.com)
# desc: scans for local bluetooth devices with names matching the description of those
#       used in cas pump credit card skimmers. This software is directly derived from 
#       the research done by Nathan Seidle as documented in this article:
#       https://learn.sparkfun.com/tutorials/gas-pump-skimmers
#

import time
import bluetooth
import sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = 24     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
disp.begin()

time.sleep(3)

disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
ellipsis = ".   "
phase = 0

while True:
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	draw.text((0, 24), "Scanning" + ellipsis, font=font, fill=255)
	disp.image(image)
	disp.display()

	nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)

	for addr, name in nearby_devices:
		if (name == "HC-03") or (name == "HC-05") or (name == "HC-06"):
			draw.rectangle((0, 0, width, height), outline=0, fill=0)
			draw.text((0, 0), "found %d devices" % len(nearby_devices), font=font, fill=255)
			draw.text((0, 24), "Potential skimmer", font=font, fill=255)
			draw.text((0, 36), name + " found!", font=font, fill=255)
			draw.text((0, 48), "Skip this location!", font=font, fill=255)

			disp.image(image)
			disp.display()
			time.sleep(7)

	phase += 1
	if phase == 1:
		ellipsis = "..  "
	elif phase == 2:
		ellipsis = "... "
	elif phase == 3:
		ellipsis = "...."
	else:
		ellipsis = ".   "
		phase = 0
