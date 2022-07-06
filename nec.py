#!/usr/bin/python
# Import required Python libraries
import RPi.GPIO as GPIO
import math
import os
from datetime import datetime
from time import sleep

#This is for  Raspberry Pi
# This pin is also referred to as GPIO23
INPUT_WIRE = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_WIRE, GPIO.IN,  pull_up_down=GPIO.PUD_UP)

def padhexa(s):
    return '0x' + s[2:].zfill(8)

while True:
	value = 1
	# Loop until we read a 0
	while value:
		value = GPIO.input(INPUT_WIRE)

	# Grab the start time of the command
	startTime = datetime.now()

	# Used to buffer the command pulses
	command = []

	# The end of the "command" happens when we read more than
	# a certain number of 1s (1 is off for my IR receiver)
	numOnes = 0

	# Used to keep track of transitions from 1 to 0
	previousVal = 0

	while True:

		if value != previousVal:
			# The value has changed, so calculate the length of this run
			now = datetime.now()
			pulseLength = now - startTime
			startTime = now

			command.append((previousVal, pulseLength.microseconds))

		if value:
			numOnes = numOnes + 1
		else:
			numOnes = 0

		# 10000 is arbitrary, adjust as necessary
		if numOnes > 10000:
			break

		previousVal = value
		value = GPIO.input(INPUT_WIRE)

	print "----------Start----------"
	for (val, pulse) in command:
		if val == 0:
			print "%+d" % (pulse),
		else:
			print "%+d" % (-pulse),
			
			# print val, pulse,
			# print pulse
	print
	print "-----------End-----------\n"

	print "Size of array is " + str(len(command))

	taille =len(command)
	if taille >66:
		binaryString = "".join(map(lambda x: "1" if x[1] > 1000 else "0", filter(lambda x: x[0] == 1, command)))
		print binaryString
		# codehex= hex((int(binaryString[1:33],2)))
		print str.format('0x{:08X}', int(hex((int(binaryString[1:33],2))), 16)),
		print str.format('0x{:04X}', int(hex((int(binaryString[1:17],2))), 16)),
		print str.format('0x{:04X}', int(hex((int(binaryString[17:33],2))), 16))

	else:
		print "00"

