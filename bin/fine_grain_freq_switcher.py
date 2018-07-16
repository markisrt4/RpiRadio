# This app reads adjustments in the 10 turn pot and changes frequencies 5 hertz at a time

import Adafruit_ADS1x15

# Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# Read initial A/D channel 1 value for 10 turn pot
last_pot_val = adc.read_adc(1, gain=1)

GQRX_IP = sys.argv[1]
GQRX_PORT = 7356
BUFFER_SIZE = 128

# Establish TCP connection to GQRX
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((GQRX_IP, GQRX_PORT))

def pot_read():
	global last_pot_val

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

		# Get current frequency over TCP from SDR CPU
		# send frequency request
		client.send('f\n')

		# receive the response data (4096 is recommended buffer size)
		response = client.recv(BUFFER_SIZE)
		s_freq = int(response)

                # Change frequency by delta * 5Khz.
                s_freq = s_freq + (5000 * delta_pot_val)
                print str(s_freq) + '\r'
                MESSAGE = "F " + str(s_freq)
                s.send(MESSAGE)
                last_pot_val = pot_val

def main():
	while True:
		pot_read()
		sleep (.1)


main()


