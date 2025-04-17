

import time
import sys
import os
import RPi.GPIO as GPIO
import spidev


sys.path.insert(0, '../utilities')
import utilities

# read ADC function
def get_ADC(spi):
    mosi_data = [0b00000001, 0b10000000, 0b00000000]
    miso_data = spi.xfer(mosi_data)

    upper = mosi_data[1] & 0b00000011
    upper = upper << 8
    raw_ADC = upper + mosi_data[2]

    return raw_ADC


# configure button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
BUTTON_0_PIN = 16
GPIO.setup(BUTTON_0_PIN, GPIO.IN)

# configure pwm
pwm = utilities.HW_PWM(2000)

# configure spi for ADC
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000

try:
    # calibrate dark
    print("Cover the photosensor and press the push button")
    GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=10)
    MAX_ADC = get_ADC(spi)

    #calibrate light
    print("Shine a flashlight on the photosensor and press the push button")
    GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=10)
    MIN_ADC = get_ADC(spi)

    while(True):
        ADC_val = get_ADC(spi)
        duty_cycle_percent = (100/(MAX_ADC - MIN_ADC))*(ADC_val - MIN_ADC)
        pwm.set_duty_cycle(duty_cycle_percent)

        time.sleep(0.001)

except KeyboardInterrupt:
    print('\nGot Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    GPIO.cleanup()
    sys.exit()