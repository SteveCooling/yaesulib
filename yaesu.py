#
# Yaesu FT-7800 control software
#
# This class emulates the radio front panel, and
# lets you programatically control the radio
#
# Author: Morten Johansen (morten@bzzt.no)
# License: CC-BY-SA
#

import serial
import threading
import time
import array
import sys
import queue

class ft7800:
	serial = None
	port = ""
	baud = 19200
	timeout = 0.1
	
	rxlen = 42
	
	thread_terminate = False
	thread_rx = None
	thread_tx = None
	
	displaybits = chr(0x00) * 42
	
	basekeys = [128, 0, 127, 0, 127, 127, 0, 0, 127, 127, 127, 8, 0]
	txkeys   = basekeys

	txloop_wait = 0.02

	keywait_min = 0.08
	keywait_long = 0.75
	
	
	# Map of what bits are set for each character segment in the main display
	mdcharmap = {
		"0": (True, True, True, False, False, True, False, False, True, False, True, True, True),
		"1": (False, False, False, False, False, True, False, False, False, False, False, True, False),
		"2": (True, True, False, False, False, False, True, True, False, False, False, True, True),
		"3": (True, False, False, False, False, True, True, True, False, False, False, True, True),
		"4": (False, False, False, False, False, True, True, True, True, False, False, True, False),
		"5": (True, False, False, False, False, True, True, True, True, False, False, False, True),
		"6": (True, True, False, False, False, True, True, True, True, False, False, False, True),
		"7": (False, False, False, False, False, True, False, False, False, False, False, True, True),
		"8": (True, True, False, False, False, True, True, True, True, False, False, True, True),
		"9": (True, False, False, False, False, True, True, True, True, False, False, True, True),
		"A": (False, True, False, False, False, True, True, True, True, False, False, True, True),
		"B": (True, False, False, True, False, True, False, True, False, False, False, True, True),
		"C": (True, True, False, False, False, False, False, False, True, False, False, False, True),
		"D": (True, False, False, True, False, True, False, False, False, False, False, True, True),
		"E": (True, True, False, False, False, False, True, True, True, False, False, False, True),
		"F": (False, True, False, False, False, False, True, True, True, False, False, False, True),
		"G": (True, True, False, False, False, True, False, True, True, False, False, False, True),
		"H": (False, True, False, False, False, True, True, True, True, False, False, True, False),
		"I": (True, False, False, True, False, False, False, False, False, False, False, False, True),
		"J": (True, True, False, False, False, True, False, False, False, False, False, True, False),
		"K": (False, True, False, False, True, False, True, False, True, False, True, False, False),
		"L": (True, True, False, False, False, False, False, False, True, False, False, False, False),
		"M": (False, True, False, False, False, True, False, False, True, True, True, True, False),
		"N": (False, True, False, False, True, True, False, False, True, True, False, True, False),
		"O": (True, True, False, False, False, True, False, False, True, False, False, True, True),
		"P": (False, True, False, False, False, False, True, True, True, False, False, True, True),
		"Q": (True, True, False, False, True, True, False, False, True, False, False, True, True),
		"R": (False, True, False, False, True, False, True, True, True, False, False, True, True),
		"S": (True, False, False, False, True, False, True, False, True, False, False, False, True),
		"T": (False, False, False, True, False, False, False, False, False, False, False, False, True),
		"U": (True, True, False, False, False, True, False, False, True, False, False, True, False),
		"V": (False, True, True, False, False, False, False, False, True, False, True, False, False),
		"W": (False, True, True, False, True, True, False, False, True, False, False, True, False),
		"X": (False, False, True, False, True, False, False, False, False, True, True, False, False),
		"Y": (True, False, False, False, False, True, True, True, True, False, False, True, False),
		"Z": (True, False, True, False, False, False, False, False, False, False, True, False, True),
		"(": (True, False, True, False, False, False, False, False, False, True, False, False, True),
		")": (True, False, False, False, True, False, False, False, False, False, True, False, True),
		"_": (True, False, False, False, False, False, False, False, False, False, False, False, False),
		" ": (False, False, False, False, False, False, False, False, False, False, False, False, False),
		"*": (False, False, True, False, True, False, True, True, False, True, True, False, False),
		"+": (False, False, False, True, False, False, True, True, False, False, False, False, False),
		"-": (False, False, False, False, False, False, True, True, False, False, False, False, False),
		",": (False, True, False, False, False, False, False, False, False, False, False, False, False),
		"/": (False, False, True, False, False, False, False, False, False, False, True, False, False),
	}

	keymap = {
		# DTMF mic buttons
		"1": [0, 0, 0, 0, 124, 99, 0, 0, 99, 0, 0, 0, 0],
		"2": [0, 0, 0, 0, 124, 76, 0, 0, 76, 0, 0, 0, 0],
		"3": [0, 0, 0, 0, 124, 51, 0, 0, 51, 0, 0, 0, 0],
		"A": [0, 0, 0, 0, 124, 25, 0, 0, 25, 0, 0, 0, 0],
		
		"4": [0, 0, 0, 0, 101, 99, 0, 0, 99, 0, 0, 0, 0],
		"5": [0, 0, 0, 0, 101, 76, 0, 0, 76, 0, 0, 0, 0],
		"6": [0, 0, 0, 0, 101, 51, 0, 0, 51, 0, 0, 0, 0],
		"B": [0, 0, 0, 0, 101, 25, 0, 0, 25, 0, 0, 0, 0],
		
		"7": [0, 0, 0, 0, 77, 99, 0, 0, 99, 0, 0, 0, 0],
		"8": [0, 0, 0, 0, 77, 76, 0, 0, 76, 0, 0, 0, 0],
		"9": [0, 0, 0, 0, 77, 51, 0, 0, 51, 0, 0, 0, 0],
		"C": [0, 0, 0, 0, 77, 25, 0, 0, 25, 0, 0, 0, 0],
		
		"*": [0, 0, 0, 0, 51, 99, 0, 0, 99, 0, 0, 0, 0],
		"0": [0, 0, 0, 0, 51, 76, 0, 0, 76, 0, 0, 0, 0],
		"#": [0, 0, 0, 0, 51, 51, 0, 0, 51, 0, 0, 0, 0],
		"D": [0, 0, 0, 0, 51, 25, 0, 0, 25, 0, 0, 0, 0],
		
		"P1":  [0, 0, 0, 0, 27, 99, 0, 0, 99, 0, 0, 0, 0],
		"P2":  [0, 0, 0, 0, 27, 76, 0, 0, 76, 0, 0, 0, 0],
		"P3":  [0, 0, 0, 0, 27, 51, 0, 0, 51, 0, 0, 0, 0],
		"P4":  [0, 0, 0, 0, 27, 25, 0, 0, 25, 0, 0, 0, 0],
		
		"PTT": [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	
		# Front panel buttons
		"HYP1":     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		"HYP2":     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
		"HYP3":     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
		"INTERNET": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
		"HYP4":     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
		"HYP5":     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
		
		"POWER": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		"MHZ":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
		"TONE":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
		
		"MEMORY": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 0, 0],
		"BAND":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0],
		
		"SCAN":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 0],
		"SMART": [0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0],
		
		"STEPDN": [0, 127, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		"STEPUP": [0,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	}
	
	# Map of main display characters.
	# Characters 0 through 5 are each an array (0-12) of tuples
	# which gives the byte and bit offset to each display segment
	mdmap = [
		[ # character 1
					# segments
			(2, 0),	# 1
			(0, 1), # 2
			(0, 2), # 3
			(1, 2), # 4
			(1, 6), # 5
			(1, 5), # 6
			(0, 3), # 7
			(1, 4), # 8
			(0, 5), # 9
			(0, 4), # 10
			(1, 1), # 11
			(1, 3), # 12
			(0, 6), # 13
		],
		[ # character 2
					# segments
			(4, 2),	# 1
			(2, 3), # 2
			(2, 4), # 3
			(3, 4), # 4
			(4, 1), # 5
			(4, 0), # 6
			(2, 5), # 7
			(3, 6), # 8
			(3, 0), # 9
			(2, 6), # 10
			(3, 3), # 11
			(3, 5), # 12
			(3, 1), # 13
		],
		[ # character 3
					# segments
			(6, 4),	# 1
			(4, 5), # 2
			(4, 6), # 3
			(5, 6), # 4
			(6, 3), # 5
			(6, 2), # 6
			(5, 0), # 7
			(6, 1), # 8
			(5, 2), # 9
			(5, 1), # 10
			(5, 5), # 11
			(6, 0), # 12
			(5, 3), # 13
		],
		[ # character 4
					# segments
			(9, 5),	# 1
			(7, 2), # 2
			(8, 0), # 3
			(9, 0), # 4
			(9, 4), # 5
			(9, 3), # 6
			(8, 1), # 7
			(9, 2), # 8
			(8, 3), # 9
			(8, 2), # 10
			(8, 6), # 11
			(9, 1), # 12
			(8, 4), # 13
		],
		[ # character 5
					# segments
			(12, 0),	# 1
			(10, 1), # 2
			(10, 2), # 3
			(11, 2), # 4
			(11, 6), # 5
			(11, 5), # 6
			(10, 3), # 7
			(11, 4), # 8
			(10, 5), # 9
			(10, 4), # 10
			(11, 1), # 11
			(11, 3), # 12
			(10, 6), # 13
		],
		[ # character 6
					# segments
			(14, 2),	# 1
			(12, 3), # 2
			(12, 4), # 3
			(13, 4), # 4
			(14, 1), # 5
			(14, 0), # 6
			(12, 5), # 7
			(13, 6), # 8
			(13, 0), # 9
			(12, 6), # 10
			(13, 3), # 11
			(13, 5), # 12
			(13, 1), # 13
		],
	]

	SYM_BUSY = ( 4, 4)
	SYM_TX   = (14, 5)
	
	
	
	def __init__(self, port):
		self.port = port
		self._initserial()
		self._init_thread_serial_tx()
		self._init_thread_serial_rx()
		time.sleep(1)
		self._ensureRadioState()

	def getDisplayCharacters(self):
		ret = ""
		for i in range(0,6):
			ret += self.getDisplayCharacter(i)
		return ret

	def getDisplayCharacter(self, char_index):
		bt = self.getDisplayCharacterBitsTuple(char_index)
		return self.getCharacterFromTuple(bt)
		
	def getCharacterFromTuple(self, char_bit_tuple):
		for char in self.mdcharmap:
			if self.mdcharmap[char] == char_bit_tuple:
				return char
		return '?'
	

	def getDisplayCharacterBitsTuple(self, char_index):
		ba = self.getMDCharacterBitArray(char_index)
		return (
			self.isDisplayBitSet(ba[0]),
			self.isDisplayBitSet(ba[1]),
			self.isDisplayBitSet(ba[2]),
			self.isDisplayBitSet(ba[3]),
			self.isDisplayBitSet(ba[4]),
			self.isDisplayBitSet(ba[5]),
			self.isDisplayBitSet(ba[6]),
			self.isDisplayBitSet(ba[7]),
			self.isDisplayBitSet(ba[8]),
			self.isDisplayBitSet(ba[9]),
			self.isDisplayBitSet(ba[10]),
			self.isDisplayBitSet(ba[11]),
			self.isDisplayBitSet(ba[12])
		)
	
	def getMDCharacterBitArray(self, char_index):
		return self.mdmap[char_index]
	
	def getDisplayBits(self):
		return self.displaybits
	
	# Check the state of a specific display bit
	def isDisplayBitSet(self, position):
		return self.isBitSet(self.displaybits, position)
		
	def isBitSet(self, data, position):
		byte = data[position[0]]
		return (byte & (1 << position[1])) != 0

	def isReceiving(self):
		return self.isDisplayBitSet(self.SYM_BUSY)

	def isTransmitting(self):
		return self.isDisplayBitSet(self.SYM_TX)

	def setTxKeys(self, keybits):
		diff = list(self.basekeys)
		for i, val in enumerate(self.basekeys):
			diff[i] = keybits[i] ^ val
		self.txkeys = diff

	def scrollTo(self, string):
		c = 0
		#print("Looing for:", string)
		while True:
			#print(self.getDisplayCharacters())
			if self.getDisplayCharacters() == string:
				return True
			self.pressStepUp()
			time.sleep(0.1)
			# safety
			c += 1
			if c > 100:
				return False

	def setTnFrequency(self, hz):
		self.pressKeyLong("BAND")
		self.scrollTo("TN FRQ")

		self.pressKey("BAND")
		time.sleep(0.1)
		self.scrollTo("% 4.0fHZ" % (hz*10))
		self.pressKeyLong("BAND")


	def resetTxKeys(self):
		self.txkeys = self.basekeys

	def pressStep(self, keyid):
		# a very short kind of keypress, only for the rotary encoder
		self.setTxKeys(self.keymap[keyid])
		time.sleep(self.txloop_wait)
		self.resetTxKeys()
		time.sleep(self.txloop_wait)

	def pressStepUp(self):
		self.pressStep("STEPUP")

	def pressStepDown(self):
		self.pressStep("STEPDN")

	def pressKey(self, keyid):
		self.setTxKeys(self.keymap[keyid])
		time.sleep(self.keywait_min)
		self.resetTxKeys()
		time.sleep(self.keywait_min)

	def pressKeyLong(self, keyid):
		self.setTxKeys(self.keymap[keyid])
		time.sleep(self.keywait_long)
		self.resetTxKeys()
		time.sleep(self.keywait_min)

	def setFrequency(self, frequency):
		freq = "%6.0f" % (frequency*1000)
		for c in freq:
			self.pressKey(c)

	def getFrequency(self):
		return int(self.getDisplayCharacters())/1000

	def getVolume(self):
		return self.basekeys[6]

	def getSquelch(self):
		return self.basekeys[7]

	def setVolume(self, volume):
		if volume > 127:
			volume = 127
		if volume < 0:
			volume = 0
		self.basekeys[6] = volume

	def setSquelch(self, squelch):
		if squelch > 127:
			squelch = 127
		if squelch < 0:
			squelch = 0
		self.basekeys[7] = squelch

	# Attempt to set the squelch to an optimal level automatically
	def setSquelchAuto(self):
		sql = 127
		while True:
			self.setSquelch(sql)
			time.sleep(0.1)
			if self.isReceiving() == False:
				return True
			if self.getSquelch() <= 0:
				return False
			sql -= 5

	def _ensureRadioState(self):
		# Wait until we're sure the voltage display is gone
		time.sleep(2)

		#while True:
		#	d = self.getDisplayCharacters()
		#	#print("'",d[4:],"'")
		#	if d == "      ":
		#		# empty display
		#		pass
		#	elif d[4:] == " V":
		#		# showing voltage
		#		#print("volt")
		#		pass
		#	else:
		#		break
		#	time.sleep(0.1)
		
		# get the radio in VFO mode
		while True:
			self.pressKey("MEMORY")
			time.sleep(0.1)
			if self.getDisplayCharacters() == "MEMORY":
				break
		self.pressKey("MEMORY")
		self.pressKey("MEMORY")
		# allow the display to settle
		time.sleep(0.2)
		return
	

	def _initserial(self):
		self.serial = serial.Serial(self.port, self.baud, timeout=self.timeout,)
		# Toggle RTS to simulate a press of the power button
		# Start by resetting the line in case it was already high,
		# in which case the radio won't turn on.
		self.serial.rts = False
		time.sleep(1)
		self.serial.rts = True
		time.sleep(1)
		self.serial.rts = False
	
	def _serial_rx_sync(self):
		#sys.stdout.write("syncup")
		for i in range(0, self.rxlen):
			#sys.stdout.write('.')
			r = self.serial.read(1)
			if len(r) and (r[0] & (1 << 7)) != 0:
				# we've just read the start byte.
				# this means we just read the first byte from the display bits
				# read the rest (readlen - 1) to make the next read(readlen) sync up
				r = self.serial.read(self.rxlen - 1)
				break
		
	def _init_thread_serial_rx(self):
		self.thread_rx = threading.Thread(target=self._thread_serial_rx)
		self.thread_rx.daemon = True
		
		self._serial_rx_sync()
		self.thread_rx.start()

	def _init_thread_serial_tx(self):
		self.thread_tx = threading.Thread(target=self._thread_serial_tx)
		self.thread_tx.daemon = True
		self.thread_tx.start()
	
	def _thread_serial_rx(self):
		while(self.thread_terminate == False):
			self.displaybits = self.serial.read(self.rxlen)

	def _thread_serial_tx(self):
		#keyready = False
		while(True):
			#if(self.tx_key_queue.empty() == False and keyready == True):
			#	keybits = self.tx_key_queue.get()
			#	diff = list(self.basekeys)
			#	for i, val in enumerate(self.basekeys):
			#		diff[i] = keybits[i] ^ val
			#
			#	#print(diff)
			#	self.serial.write(array.array('B', diff).tostring())
			#	# This makes sure base keys will be sent at least once between keypresses
			#	keyready = False
			#else:
			#	self.serial.write(array.array('B', self.basekeys).tostring())
			#	keyready = True

			self.serial.write(array.array('B', self.txkeys).tostring())
			# this is the optimal loop speed i found
			# 100ms or more and the radio turns off (missing display feedback)
			# 50ms is too quick for reliable keypresses
			# 60ms seems to be reliable				
			time.sleep(self.txloop_wait) #0.06

	def __del__(self):
		self.serial.close()
		self.thread_terminate = True

