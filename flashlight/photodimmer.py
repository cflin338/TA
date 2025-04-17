import time
import sys
import os
import spidev
spi = spidev.SpiDev()
spi.open(0, 0)

sys.path.insert(0, '../utilities')
import utilities
import RPi.GPIO as GPIO

pwm = utilities.HW_PWM(2000)

spi.max_speed_hz = 100000
mosi_data = [1, 128, 0]
miso_data = spi.xfer(mosi_data)


BUTTON_0_PIN = 16
LED_0_PIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

max_val = 0
min_val = 0
try:
    print("Cover the photosensor and press the push button")
    while True:
        
        pressed = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, timeout = 100, bouncetime = 10)
        if pressed is not None:
             mosi_data = [1, 128, 0]
             miso_data = spi.xfer(mosi_data)
             max_val = (miso_data[1] << 8) + miso_data[2]
             #print(max_val)
             break
    print("Shine a flashlight on the photosensor and press the push button")
    time.sleep(0.5)
    while True:
        pressed = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, timeout = 100, bouncetime = 10)
        if pressed is not None:
             mosi_data = [1, 128, 0]
             miso_data = spi.xfer(mosi_data)
             min_val = (miso_data[1] << 8) + miso_data[2]
             #print(min_val)
             break

    
    factor = 1
    while True:
        mosi_data = [1, 128, 0]
        miso_data = spi.xfer(mosi_data)
        ADC = (miso_data[1] << 8) + miso_data[2]
        #print(ADC-min_val)
        pwm_value = (ADC-min_val) / ((max_val - min_val)/100)
        #print(pwm_value)
        pwm.set_duty_cycle(pwm_value)
        
        
        time.sleep(.01)

except KeyboardInterrupt:
    print(" Got Keyboard Interrupt. Cleaning up and exiting")
    pwm.set_duty_cycle(0.0)
    GPIO.cleanup()
    sys.exit()
