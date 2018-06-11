import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Alsa Audio
import alsaaudio
m = alsaaudio.Mixer('PCM')

# Math
import math

# Or create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

GAIN = 1
THRESH  = .35
DIVISOR = 32.96 
V1 = 0

# Main loop.
while True:
    # Read ADC channel 0 for volume.
    V2 = adc.read_adc(0, gain=GAIN) / DIVISOR
    deltaV = V2-V1
    if deltaV > THRESH or deltaV < -THRESH:
        #print deltaV
        V1 = V2
        m.setvolume(int(V2) + 50)
    time.sleep(0.25)

