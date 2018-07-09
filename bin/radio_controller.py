import curses
import json
import socket
import sys

import RPi.GPIO as GPIO
import threading

from time import sleep
from threading import Thread

import Adafruit_ADS1x15

# Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# GPIO Ports
Enc_B = 16  				# Encoder input B: input GPIO 16
Enc_A = 20  			        # Encoder input A: input GPIO 20
Psh_Btn = 12

Rotary_counter = 0  			# Start counting from 0
Current_A = 1					# Assume that rotary switch is not 
Current_B = 1					# moving while we init software

LockRotary = threading.Lock()		# create lock for rotary switch

#Read JSON data into the datastore variable
with open('radio_config.json') as json_data:
    datastore = json.load(json_data)
    num_records = len(datastore["radio_config"]["stations"])

# Station Indexes
sidx = 0
s_start = datastore["radio_config"]["stations"][sidx]["freq_start"]
s_end   = datastore["radio_config"]["stations"][sidx]["freq_end"]
s_jump = datastore["radio_config"]["stations"][sidx]["freq_jump"]
s_freq   = s_start


# Setup socket stuff for gqrx tcp
#GQRX_IP = '192.168.29.115'
GQRX_IP = sys.argv[1]
GQRX_PORT = 7356
BUFFER_SIZE = 1024

# Establish TCP connection to GQRX
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((GQRX_IP, GQRX_PORT))

# Read initial A/D channel 1 value for 10 turn pot
last_pot_val = adc.read_adc(1, gain=1)

def push_button(self):
	global s_start, s_end, s_jump, s_bcast, s_freq, sidx, s, datastore
	print "Button Pressed"
	sidx += 1
	if sidx > num_records - 1:
		sidx = 0
	s_start = datastore["radio_config"]["stations"][sidx]["freq_start"]
	s_end   = datastore["radio_config"]["stations"][sidx]["freq_end"]
	s_jump = datastore["radio_config"]["stations"][sidx]["freq_jump"]
	s_bcast = datastore["radio_config"]["stations"][sidx]["broadcast"]
	s_freq   = s_start
	print "Tuning to: " + str(datastore["radio_config"]["stations"][sidx]["name"]) + '\r'
	MESSAGE = "M " + s_bcast
	print MESSAGE
	s.send(MESSAGE)
	sleep(0.1)
	MESSAGE = "F " + str(s_freq)
	print MESSAGE
	s.send(MESSAGE)
	return

def pot_read():
	global s_freq, last_pot_val

        # Read new position of pot, change freq if the pot has been moved past a small threshold.
        pot_val = adc.read_adc(1, gain=1)
        if (pot_val > last_pot_val + 2 or pot_val < last_pot_val -2):
                delta_pot_val = pot_val - last_pot_val
                # Check for jumpy, erroneous deltas
                if (delta_pot_val > 100 or delta_pot_val < -100):
                        return
                if delta_pot_val > 0:
                        delta_pot_val -= 2
                elif delta_pot_val < 0:
                        delta_pot_val += 2 
                print delta_pot_val
                # Change frequency by delta * 5Khz.
                s_freq = s_freq + (5000 * delta_pot_val)
                print str(s_freq) + '\r'
                MESSAGE = "F " + str(s_freq)
                s.send(MESSAGE)
                last_pot_val = pot_val

# Rotary encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt(A_or_B):
	global Rotary_counter, Current_A, Current_B, LockRotary
													# read both of the switches
	Switch_A = GPIO.input(Enc_A)
	Switch_B = GPIO.input(Enc_B)
													# now check if state of A or B has changed
													# if not that means that bouncing caused it
	if Current_A == Switch_A and Current_B == Switch_B:		# Same interrupt as before (Bouncing)?
		return										# ignore interrupt!

	Current_A = Switch_A								# remember new state
	Current_B = Switch_B								# for next bouncing check


	if (Switch_A and Switch_B):						# Both one active? Yes -> end of sequence
		LockRotary.acquire()						# get lock 
		if A_or_B == Enc_B:							# Turning direction depends on 
			Rotary_counter += 1						# which input gave last interrupt
		else:										# so depending on direction either
			Rotary_counter -= 1						# increase or decrease counter
		LockRotary.release()						# and release lock
	return											# THAT'S IT


# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():
	global Rotary_counter, LockRotary
	global s_start, s_end, s_jump, s_bcast, s_freq, sidx, s, datastore

	NewCounter = 0                 # for faster reading with locks

        loop_ctr = 0;
	
	# initialize interrupt handler
	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)					# Use BCM mode
										# define the Encoder switch inputs
	GPIO.setup(Enc_A, GPIO.IN) 				
	GPIO.setup(Enc_B, GPIO.IN)
	GPIO.setup(Psh_Btn, GPIO.IN)
										# setup callback thread for the A and B encoder 
										# use interrupts for all inputs
	GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotary_interrupt) 				# NO bouncetime 
	GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotary_interrupt) 				# NO bouncetime 
	GPIO.add_event_detect(Psh_Btn, GPIO.RISING, callback=push_button)				

	while True :								# start test 
		sleep(0.01)							# sleep 10 msec
		
												# because of threading make sure no thread
												# changes value until we get them
												# and reset them
												
		LockRotary.acquire()					# get lock for rotary switch
		NewCounter = Rotary_counter			# get counter value
		Rotary_counter = 0						# RESET IT TO 0
		LockRotary.release()					# and release lock
					
		if (NewCounter !=0):					# Counter has CHANGED
			s_freq = s_freq + ((NewCounter*abs(NewCounter)) * s_jump)
			if s_freq > s_end:
				s_freq = s_start
			if s_freq < s_start:
				s_freq = s_end
			print str(s_freq) + '\r'
			MESSAGE = "F " + str(s_freq)
			s.send(MESSAGE)

                loop_ctr += 1
                if loop_ctr % 10 == 0:
                        pot_read()

                if loop_ctr == 100:
			loop_ctr = 0

# start main demo function
main()
