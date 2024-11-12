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

# callback function
def button_callback(channel):
    # led on
    GPIO.output(LED_0_PIN, GPIO.HIGH)
    print("button pressed")

    # wait
    while GPIO.input(BUTTON_0_PIN) == GPIO.HIGH:
        print ("abc")
        time.sleep(0.1)

    # led off when released
    GPIO.output(LED_0_PIN, GPIO.LOW)
    print("button released")

# event detection
GPIO.add_event_detect(BUTTON_0_PIN, GPIO.RISING, callback=button_callback, bouncetime=10)

# main loop with counter
counter = 0
try: 
    while True:
        print(f"main program counter: {counter}")
        counter += 1
        time.sleep(1)

except KeyboardInterrupt:
    # cleanup enacted by ctrl+c
    print("Got Keyboard Interrupt. Cleaning up and exiting.")
    GPIO.output(LED_0_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()