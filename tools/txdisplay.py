#!/usr/bin/python
# coding=utf-8

import threading
import time
import os
import sys
import serial


PORT = '/dev/cu.usbserial'
BAUD = 19200

ser = serial.Serial(PORT, BAUD, timeout=.1, )

ser.baudrate = BAUD
ser.timeout = 3000/BAUD + 0.2

# sample fra radio
t = "a8382062652c1505592a662a192b0500000000000000000000000000000000000000000000600e000006"

# backlight + garble
t = "7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f00000000000000000000000000000000000000600e000006"

# ikke backlight + anna garble
t = "0000000000000000000000000000000000007f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f007f7f7f06"
#print t.decode('hex')

ser.write(t.decode('hex'))
#exit(1)

try:
	while True:
		r = ser.read(13) 
		#for c in r:
			
		sys.stdout.write(r.encode('hex'))
		sys.stdout.write("\r")
except(Exception):
	print("Unexpected error:",  sys.exc_info()[0])
	exit(1)
	ser.close()
	
# for baudrate in (2400, 4800, 9600, 19200, 38400, 57600, 115200):
#     ser.baudrate = baudrate
#     ser.timeout = 3000/baudrate + 0.2
#     print('Trying with ' + str(baudrate) + '...')
#     ser.write("\xff\xff\xff")
#     ser.write('connect')
#     ser.write("\xff\xff\xff")
#     r = ser.read(128)
#     if 'comok' in r:
#         print('Connected with ' + str(baudrate) + '!')
#         no_connect = False
#         status, unknown1, model, unknown2, version, serial, flash_size = r.strip("\xff\x00").split(',')
#         print('Status: ' + status)
#         print('Model: ' + model)
#         print('Version: ' + version)
#         print('Serial: ' + serial)
#         print('Flash size: ' + flash_size)
#         if fsize > flash_size:
#             print('File too big!')
#             break
#         if not CHECK_MODEL in model:
#             print('Wrong Display!')
#             break
#         upload()
#         break
# 
# if no_connect:
#     print('No connection!')
# else:
#     print('File written to Display!')

ser.close()

