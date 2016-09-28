#!/usr/bin/env python3.5

import yaesu
import time

radio = yaesu.ft7800('/dev/cu.usbserial')

radio.setSquelch(127)
radio.setVolume(50)

#time.sleep(1)
print("Auto squelch...")
radio.setSquelchAuto()
print(radio.getSquelch())


radio.setTnFrequency(88.5)
radio.setFrequency(433.500)

while True:
	print(radio.getFrequency())
	
	freq = input('Frequency: ')
	radio.setFrequency(float(freq))	
