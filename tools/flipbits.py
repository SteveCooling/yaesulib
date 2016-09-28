#!/usr/bin/env python

import curses
import curses.textpad
import time
import datetime
import thread
import os
import sys
import serial

from curses import wrapper

PORT = '/dev/cu.usbserial'
BAUD = 19200

ser = serial.Serial(PORT, BAUD, timeout=.1, )

ser.baudrate = BAUD
ser.timeout = 3000/BAUD + 0.2

init = "a8382062652c1505592a662a192b0500000000000000000000000000000000000000000000600e000006"
t = init.decode("hex")

x = 0
y = 0

def main(stdscr):
	# Clear screen
	stdscr.clear()
	curses.curs_set(2)
	
	stdscr.nodelay(1)
	

	# This raises ZeroDivisionError when i == 10.
	#for i in range(1, 11):
	while True:
		update_scr(stdscr)
		time.sleep(0.05)
	
def read_serial(ser):
	while True:
		r = ser.read(13)

def update_scr(stdscr):
	global t
	global x,y
	global ser
	
	ser.write(t)
	
	now = datetime.datetime.now()
	stdscr.addstr(0, 0, t.encode("hex"))

	stdscr.addstr(3, 0, now.strftime("%d-%m-%Y %H:%M:%S.%f"))

	stdscr.addstr(4, 0, "%d, %d" % (y, x))
	
	stdscr.addstr(1, x*2, "%08s" % format(ord(t[x]), '08b'))

	key = stdscr.getch(y, x*2)
	#stdscr.addstr(5, 0, "%d" % key)

	if key == 113: #q
		exit()
	elif key == curses.KEY_RIGHT:
		x += 1
		stdscr.addstr(1, 0, " "*(len(t*2)+8))
	elif key == curses.KEY_LEFT:
		x -= 1
		stdscr.addstr(1, 0, " "*(len(t*2)+8))
	elif key == curses.KEY_UP:
		x += 5
		stdscr.addstr(1, 0, " "*(len(t*2)+8))
	elif key == curses.KEY_DOWN:
		x -= 5
		stdscr.addstr(1, 0, " "*(len(t*2)+8))
	elif key == 43: #+
		incdecbyte(stdscr, x, 1)
	elif key == 45: #+
		incdecbyte(stdscr, x, -1)

	elif key in range(49,57):
		flip_bit(stdscr, x, key-48)
			
	if(x < 0): x = 0		
	if(x > len(t)-1): x = len(t)-1
	stdscr.refresh()

def flip_bit(stdscr, pos, num):
	global t
	s = list(t)
	
	#print t[pos]
	data = ord(s[pos])
	bit = 1 << num-1
	data = data ^ bit
	s[pos] = chr(data)
	
	t = "".join(s)

def incdecbyte(stdscr, pos, amount):
	global t
	s = list(t)
	
	#print t[pos]
	data = ord(s[pos])
	
	data += amount
	
	if data > 255:	data = 0
	if data < 0:	data = 255
	s[pos] = chr(data)
	
	t = "".join(s)

thread.start_new_thread(read_serial, (ser,))

wrapper(main)

# stdscr = curses.initscr()
# 
# curses.noecho()
# #curses.echo()
# 
# curses.cbreak()
# stdscr.keypad(True)
# 
# 
# 
# begin_x = 5
# begin_y = 5
# height = 5
# width = 50
# win = curses.newwin(height, width, begin_y, begin_x)
# tb = curses.textpad.Textbox(win)
# text = tb.edit()
# curses.addstr(4,1,text.encode('utf_8'))
# 
# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
# curses.endwin()



