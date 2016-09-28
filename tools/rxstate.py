#!/usr/bin/python
# coding=utf-8

import threading
import time
import os
import sys
import serial
from struct import * 

PORT = '/dev/cu.usbserial'
BAUD = 19200

readlen = 13 #42
#r = (128,   0, 127,   0, 127, 127,   0,   0, 127, 127, 127,   8,   0)

ser = serial.Serial(PORT, BAUD, timeout=.1, )

ser.baudrate = BAUD
ser.timeout = 3000/BAUD + 0.2

sys.stdout.write("syncup")
for i in range(0, readlen):
	sys.stdout.write('.')
	r = ser.read(1)
	if r[0] == 128: #(r[0] & (1 << 7)) != 0:
		# we've just read the start byte.
		# this means we just read the first byte from the display bits
		# read the rest (readlen - 1) to make the next read(readlen) sync up
		r = ser.read(readlen - 1)
		break


sys.stdout.write("done.\n")

base = unpack('B'*readlen, ser.read(readlen))

def serial_read_thread():
	global ser
	global r
	global readlen
	
	while True:
		r = unpack('B'*readlen, ser.read(readlen))


# init rx thread
thread_rx = threading.Thread(target=serial_read_thread)
thread_rx.daemon = True
thread_rx.start()
	
# the display continually transmits the following bytes to the head unit
# (128,   0, 127,   0, 127, 127,   0,   0, 127, 127, 127,   8,   0)
# (beg, ???, ???, ???, ???, ???, vol, sql, ???, ???, ???, ???, hyp)
# functions ^
time.sleep(0.5)

#sys.stdout.write("0b"+("76543210"*13)+"\n")
file = open("keymap","a")

while True:
	print(base)
	print(r)
	diff = list(r)
	for i, val in enumerate(r):
		diff[i] = base[i] ^ val
	print(diff)
	if sum(diff) > 0:
		name = input("name pressed key: ")
		str = "\"%s\": %s,\n" % (name, diff)
		print(str)
		file.write(str)
		file.flush()
		os.fsync(file.fileno())
	else:
		sys.stdout.write("\033[F\033[F\033[F")
	time.sleep(0.2)
		
		
	#sys.stdout.write(bin(int.from_bytes(base, 'big'))+"\n") #r.encode('hex'))
	#sys.stdout.write(bin(int.from_bytes(r, 'big'))+"\n") #r.encode('hex'))
	#sys.stdout.write(bin(int.from_bytes(base, 'big') ^ int.from_bytes(r, 'big'))+"\n") #r.encode('hex'))
			
#except(Exception):
#	print("Unexpected error:",  sys.exc_info()[0])
#	exit(1)
#	ser.close()
	
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



#
## determine the average time it takes to read bytes
## by averaging each byte read takes for two display updates
#sys.stdout.write("measure")
#meas = list()
#for i in range(0, readlen*2):
#	sys.stdout.write('.')
#	start = time.perf_counter()
#	r = ser.read(1)
#	stop = time.perf_counter()
#	meas.append(stop - start)
#
#
#avgtime = sum(meas)/len(meas)
#print(meas, avgtime)
#sys.stdout.write("\n")
#
## find the gap between bytes
#sys.stdout.write("syncup")
#for i in range(0, readlen):
#	sys.stdout.write('.')
#	start = time.perf_counter()
#	r = ser.read(1)
#	stop = time.perf_counter()
#	meas = stop - start
#	if meas > avgtime*2:
#		print(meas, i)
#		# we've just read the "slow" byte.
#		# this means we just read the first byte from the display bits
#		# read the rest (readlen - 1) to make the next read(readlen) sync up
#		r = ser.read(readlen - 1)
#		break

