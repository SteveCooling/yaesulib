# yaesulib

Python library for programmatically controlling Yaesu mobile ham radios without the head unit

It uses a (USB) TTL serial port to emulate the front panel, enabling control of the radio from software.

See it in action here: https://www.youtube.com/watch?v=xfGuzuzAQOk

## connecting

Development is being done using a cheap china-made PL2303 module slightly modified to gain access to the RTS pin.

|	RJ11 connector	|	Color	|	Function	|	Serial Port	|
|-------------------|-----------|---------------|---------------|
|	1				|	Blue	|	TxD			|	RxD			|
|	2				|	Yellow	|	RxD			|	TxD			|
|	3				|	Green	|	GND			|	GND			|
|	4				|	Red		|	9V DC		|	-			|
|	5				|	Black	|	PWR BTN		|	RTS			|
|	6				|	White	|	MIC			|	-			|

## usage

The library gives you easy access to the radio functions. Only the most basic functions are implemented, as things like memory can be implemented in the controlling software instead.

Example:

```python
import yaesu

# Turn on and initialize the radio
radio = yaesu.ft7800('/dev/cu.usbserial')

# Set volume
radio.setVolume(50)

# Set squelch level automatically (yes, really)
radio.setSquelchAuto()

# Set subtone frequency
radio.setTnFrequency(88.5)

# Set operating frequency
radio.setFrequency(433.500)

# Ask user for a new frequency
while True:
	print(radio.getFrequency())
	
	freq = input('Frequency: ')
	radio.setFrequency(float(freq))	

```
