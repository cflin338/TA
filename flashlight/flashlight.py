import RPi.GPIO as GPIO
import time
import sys

# constants
BUTTON_0_PIN = 16
LED_0_PIN = 18

# gpio setup
GPIO.setmode(GPIO.BOARD)  # physical pins
GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # button is pulldown
GPIO.setup(LED_0_PIN, GPIO.OUT)  # led is output

# enum for led state
# LED_STATE = ['LED_OFF', 'LED_ON']
# led = enumerate(LED_STATE)
led = False

# basic edge detection
current_state = None
prev_state = GPIO.LOW

try:
    while True:
        # button check
        current_state = GPIO.input(BUTTON_0_PIN)
        if current_state == GPIO.HIGH:
            if prev_state == GPIO.LOW:
                led = not led
                GPIO.output(LED_0_PIN, led)
            
        prev_state = current_state
    # sleep for CPU usage
    time.sleep(0.01)

except KeyboardInterrupt:
    # cleanup enacted by ctrl+c
    print("Got Keyboard Interrupt. Cleaning up and exiting.")
    GPIO.output(LED_0_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()