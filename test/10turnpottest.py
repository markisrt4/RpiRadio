import time

import Adafruit_ADS1x15

# Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

GAIN = 1

print('Reading 10 turn pot values, press Ctrl-C to quit...')

last_val = adc.read_adc(1, gain=GAIN)

# Main loop.
while True:
    # Read all the ADC channel value
    val = adc.read_adc(1, gain=GAIN)
    if (val > last_val + 2 or val < last_val -2):
        print val
        last_val = val
    # Pause for half a second.
    time.sleep(0.5)
