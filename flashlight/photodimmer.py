import time
import sys
import os
import adc_test
import utilities
pwm = utilities.HW_PWM(2000)

import RPi.GPIO as GPIO
import sys

BUTTON_0_PIN = 40   

GPIO.setmode(GPIO.BOARD)

GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
    ''' GET MIN'''
    print(f'Cover the photosensor and press the push button')
    GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=10)
    minimum,min_v = adc_test.read_adc_ch0()
    print(min_v)
    '''GET MAX'''
    print(f'Shine a flashlight on the photosensor and press the push button')
    GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=10)
    maximum,max_v = adc_test.read_adc_ch0()
    print(max_v)
    '''SET CONVERSION RATE'''

    while True:
        val, trash = adc_test.read_adc_ch0()
        percent = 100-(((val-minimum)/(maximum-minimum))*100)
        pwm.set_duty_cycle(percent)
        time.sleep(0.001)
    

except KeyboardInterrupt:
    print("\nKeyboard interrupt received.")
    pwm.set_duty_cycle(0)
    GPIO.cleanup()
    sys.exit()




