import RPi.GPIO as GPIO
import time
import spidev
import sys
import os

GPIO.setmode(GPIO.BOARD)

BUTTON_0_PIN = 16
LED_0_PIN = 12


GPIO.setup(BUTTON_0_PIN,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LED_0_PIN, GPIO.OUT, initial = GPIO.LOW)

pwm = GPIO.PWM(LED_0_PIN, 2000)
pwm.start(0)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

prev = GPIO.input(BUTTON_0_PIN)
prev = GPIO.LOW
currLvl = GPIO.LOW

GPIO.output(LED_0_PIN, GPIO.LOW)

def read_data():
    to_send = [0b00000001, 0b10000000 ,0b00000000]
    val = spi.xfer(to_send)
    val = (val[1] * 256) + val[2]
    
    return val


print("Cover the photosensor and press the push button")
coverphotosensor = True
shineflashlight = False
ledbrightness = False

try:
    while coverphotosensor:

        currLvl = GPIO.input(BUTTON_0_PIN)
        GPIO.output(LED_0_PIN,GPIO.LOW)

        maximum = read_data()
        

        if(currLvl == GPIO.HIGH) and (prev == GPIO.LOW):
            coverphotosensor = False
            shineflashlight = True
            print("Shine a flashlight on the photosensor and press the push button")
        
        prev = currLvl
        
        time.sleep(0.1)

    while shineflashlight:
        
        currLvl = GPIO.input(BUTTON_0_PIN)
        
        

        if(currLvl == GPIO.HIGH) and (prev == GPIO.LOW):
            shineflashlight = False
            ledbrightness = True

        minimum = read_data()
        
        prev = currLvl

        time.sleep(0.1)
    
    while ledbrightness:
        

        currLvl = GPIO.input(BUTTON_0_PIN)

        brightness = read_data()
        brightness = max(min(brightness,maximum),minimum)
        if(maximum != minimum):

        
            light = ((brightness - maximum)/(minimum - maximum)) * 100
    
            pwm.ChangeDutyCycle(100-light)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.ChangeDutyCycle(0)
    GPIO.output(LED_0_PIN,GPIO.LOW)
    GPIO.cleanup()
    sys.exit()



    