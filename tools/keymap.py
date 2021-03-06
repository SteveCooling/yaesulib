# these are values XOR'd from the base bytes
basekeys = [128, 0, 127, 0, 127, 127, 0, 0, 127, 127, 127, 8, 0]
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