try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. You can achieve this by using 'sudo' to run your script")
import time
import sys
import os
import spidev

sys.path.insert(0, '../utilities')
import utilities

# Constants
BUTTON_0_PIN = 16

# Press button setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_0_PIN, GPIO.IN)

# SPI set up
bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 1000000
to_send = [0x01, 0b10000000, 0x0]

        time.sleep(0.01)
    
    
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    sys.exit()