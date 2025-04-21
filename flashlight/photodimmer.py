import spidev
import RPi.GPIO as GPIO
import time
import sys
import os
sys.path.insert(0, '../utilities')
import utilities

def getLightLevel():
    try:
        #Stall until rising edge detected
        GPIO.wait_for_edge(BREADBOARD_BUTTON_PIN, GPIO.RISING)
        #Only runs in this case
        time.sleep(1)
        to_send = [0b00000001, 0b10000000, 0b00000000]
        #Read device
        dataList = spi.xfer(to_send)
        return (256 * dataList[1] + dataList[2])
    except KeyboardInterrupt:
        endProgram()

def endProgram():
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    GPIO.cleanup()
    sys.exit()

# "Macros"
BUS = 0
DEVICE = 0
MAX_SPEED_HZ = 100000
BYTES_TO_READ = 36
BREADBOARD_LED_PIN = 12
BREADBOARD_BUTTON_PIN = 16

# Settings
spi = spidev.SpiDev()
spi.open(BUS, DEVICE)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BREADBOARD_BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
spi.max_speed_hz = MAX_SPEED_HZ
spi.mode = 0b01

#Initialize running vars
state = 0
# Create PWM object
pwm = utilities.HW_PWM(2000)

#Get dark val
print("Cover the photosensor and press the push button")
darkVal = getLightLevel()
#print("DARKVAL: " + str(darkVal))

#Get light val
print("Shine a flashlight on the photosensor and press the push button")
lightVal = getLightLevel()
#print("LIGHTVAL: " + str(lightVal))

try:
    while(1):
        #8 start bits then SGL/DIFF, D2, D1, D0. Select CH0 by sending 0, 0, 0
        to_send = [0b00000001, 0b10000000, 0b00000000]
        #Read device
        dataList = spi.xfer(to_send)
        #Convert list to voltage val (no idea why 310 works here)
        adcVal = (256 * dataList[1] + dataList[2])
        PWMVal = (100 / (darkVal - lightVal)) * adcVal
        if(PWMVal > 100):
            PWMVal = 100
        elif(PWMVal < 0):
            PWMVal = 0
        pwm.set_duty_cycle(PWMVal)
        time.sleep(.01)
except KeyboardInterrupt:
    endProgram()