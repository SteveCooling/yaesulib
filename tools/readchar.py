#!/usr/bin/env python3.5

import yaesu
import time

print("starting")

radio = yaesu.ft7800('/dev/cu.usbserial')

print("ready")


with open("charmap","a") as file:
	while True:
		foo = input("char displayed at pos0:")
		bits = radio.getDisplayCharacterBitsTuple(0)
		data = "\"%s\": %s,\n" % (foo, bits)
		print(data)
		file.write(data)

# while True:
# 	print(radio.getDisplayBits().encode('hex'))
# 	print(radio.getDisplayCharacterBitsTuple(0))
# 	#print(radio.isDisplayBitSet(radio.mdmap[0][0]))
# 	time.sleep(0.1)
	
