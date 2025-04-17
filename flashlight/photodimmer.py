import time
import sys
import os
import RPi.GPIO as GPIO
import spidev


# INITIALIZATIONS
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

BUTTON_0_PIN = 16
LED_0_PIN = 12

GPIO.setup(LED_0_PIN, GPIO.OUT)
GPIO.output(LED_0_PIN, GPIO.LOW)
GPIO.setup(BUTTON_0_PIN, GPIO.IN)
GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm = GPIO.PWM(LED_0_PIN, 2000)
pwm.start(0)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

previous = GPIO.LOW
current  = GPIO.LOW

# Initializing States
COVER_PHOTO_SENSOR_STATE = True
SHINE_FLASHLIGHT_STATE   = False
LED_LIGHT_LEVELS_STATE   = False


print('Cover the photosensor and press the push button')

try:
    while COVER_PHOTO_SENSOR_STATE:
        current = GPIO.input(BUTTON_0_PIN)
        GPIO.output(LED_0_PIN, GPIO.LOW)

        mosi_data = [0b00000001, 0b10000000, 0b00000000]
        miso_data = spi.xfer(mosi_data)
        maximum = (mosi_data[1] << 8) + mosi_data[2]
        
        if ((current == GPIO.HIGH) and (previous == GPIO.LOW)):
            COVER_PHOTO_SENSOR_STATE = False
            SHINE_FLASHLIGHT_STATE   = True
            print('Shine a flashlight on the photosensor and press the push button')

        previous = current
        time.sleep(0.01)
    

    while SHINE_FLASHLIGHT_STATE:
        current = GPIO.input(BUTTON_0_PIN)

        if ((current == GPIO.HIGH) and (previous == GPIO.LOW)):
            SHINE_FLASHLIGHT_STATE = False
            LED_LIGHT_LEVELS_STATE = True

        mosi_data = [0b00000001, 0b10000000, 0b00000000]
        miso_data = spi.xfer(mosi_data)
        minimum = (mosi_data[1] << 8) + mosi_data[2]

        previous = current
        time.sleep(0.01)


    while LED_LIGHT_LEVELS_STATE:
        mosi_data = [0b00000001, 0b10000000, 0b00000000]
        miso_data = spi.xfer(mosi_data)
        led_brightness = (mosi_data[1] << 8) + mosi_data[2]

        led_brightness = max(min(led_brightness, maximum), minimum)

        if (maximum != minimum):
            light_level = ((led_brightness - maximum) / (minimum - maximum)) * 100
            pwm.ChangeDutyCycle(100 - light_level)
        
        time.sleep(0.01)

except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.ChangeDutyCycle(0)
    GPIO.output(LED_0_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()
    
