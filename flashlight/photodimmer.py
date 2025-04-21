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

pwm = utilities.HW_PWM(2000)

print("Cover the photosensor and press the push button")
GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime = 25)
to_send = [0x01, 0b10000000, 0x0]
spi_data = spi.xfer(to_send)
photosensor_max = spi_data[2] + (spi_data[1]*256)
time.sleep(.1)

print("Shine a flashlight on th ephotosensor and press the push button")
GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime = 25)
to_send = [0x01, 0b10000000, 0x0]
spi_data = spi.xfer(to_send)
photosensor_min = spi_data[2] + (spi_data[1]*256)
time.sleep(.1)


try:
    while True:
        to_send = [0x01, 0b10000000, 0x0]
        spi_data = spi.xfer(to_send)
        digital_value = spi_data[2] + (spi_data[1]*256)
        pwm_value = ((digital_value-photosensor_min) / (photosensor_max-photosensor_min)) * 100
        if (digital_value > photosensor_max):
            pwm.set_duty_cycle(100)
        elif (digital_value < photosensor_min):
            pwm.set_duty_cycle(0)
        else:
            pwm.set_duty_cycle(pwm_value)
        


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    sys.exit()