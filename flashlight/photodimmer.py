import spidev
import time
import sys
import os
import RPi.GPIO as GPIO  

#I KEPT GETTING I/O ERRORS WHEN I USED UTILITIES
'''sys.path.insert(0, '../utilities')
import utilities
pwm = utilities.HW_PWM(2000)'''

#POTTER, I SCRAPPED MY WHOLE EVENT_DETECT IDEA 
#B/C IT DIDNT WORK AND I DIDNT KNOW HOW TO FIX IT CAUSE IT WAS
#TOO COMPLICATED
#SO I MADE A STATE MACHINE THING :/

#setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#MY PIN 16 ISNT WORKING SO I USED PIN 40. CHANGED IT BACK TO 16 FOR GRADING
BUTTON_0_PIN = 16
LED_0_PIN = 12
GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON_0_PIN, GPIO.IN)
GPIO.setup(LED_0_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_0_PIN, 2000)
pwm.start(0)


#setup SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000

#setup GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#BUTTON_0_PIN = 40
#LED_0_PIN = 12

#setup input and output
#GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#GPIO.setup(BUTTON_0_PIN, GPIO.IN)
#GPIO.setup(LED_0_PIN, GPIO.OUT)

#GPIO.output(LED_0_PIN, GPIO.HIGH)
prev_gpio_state = GPIO.input(BUTTON_0_PIN)
prev_gpio_state = GPIO.LOW
curr_gpio_state = GPIO.LOW
GPIO.output(LED_0_PIN, GPIO.LOW)
#start with LED of
#curr_led_state = GPIO.LOW

#initialize duty cycle to 0
curr_duty_cycle = 0

def get_adc():
    to_send = [0b00000001, 0b10000000, 0b00000000]
    val = spi.xfer(to_send)
    #bit shift operator, 2^8
    adc_val = (val[1] * 256) + val[2]

    return adc_val




#min_val = 0
#max_val = 0

print('Cover the photosensor and press the push button')
#sensor_state = "dark"
covered_state = True
bright_state = False
fluctuating_state = False
try:
    #in covered state
    while covered_state is True:
        #check current gpio state
        curr_gpio_state = GPIO.input(BUTTON_0_PIN)
        GPIO.output(LED_0_PIN, GPIO.LOW)
        max_val = get_adc()

        #if button is pressed, go to bright state
        if(curr_gpio_state == GPIO.HIGH and prev_gpio_state == GPIO.LOW):
            bright_state = True
            covered_state = False
            fluctuating_state = False
            print('Shine a flashlight on the photosensor and press the push button')
        prev_gpio_state = curr_gpio_state
        time.sleep(0.01)

    #in bright state
    while bright_state is True:
        #check current gpio state
        curr_gpio_state = GPIO.input(BUTTON_0_PIN)

        #if button is pressed again, go to fluctuating state
        if(curr_gpio_state == GPIO.HIGH and prev_gpio_state == GPIO.LOW):
            fluctuating_state = True
            bright_state = False
            covered_state = False

        min_val = get_adc()
        prev_gpio_state = curr_gpio_state
        time.sleep(0.01)
    
    #current duty cycle
    pwm.ChangeDutyCycle(curr_duty_cycle)

    #in fluctuating state
    while fluctuating_state is True:
        #print('In fluctuating state')
        curr_gpio_state = GPIO.input(BUTTON_0_PIN)
        fluctuation = get_adc()
        fluctuation = max(min(fluctuation, max_val), min_val)
         
        if(max_val != min_val):
            
            target_duty_cycle = ((fluctuation - min_val) / (max_val - min_val)) * 100
            #led transitions towards target duty cycle 10% for a smoother transition
            curr_duty_cycle += (target_duty_cycle - curr_duty_cycle) * 0.1
            pwm.ChangeDutyCycle(curr_duty_cycle)

        time.sleep(0.01)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.ChangeDutyCycle(0.0)
    #turn off led
    GPIO.output(LED_0_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()
