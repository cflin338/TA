import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BOARD)
BUTTON_0_PIN = 16
LED_0_PIN = 18
cur_state = 0
GPIO.setwarnings(False)
GPIO.setup(LED_0_PIN, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def my_callback(BUTTON_0_PIN):
    print('In rising_edge_callback')
    while GPIO.input(BUTTON_0_PIN) == GPIO.HIGH:
    print('abc')
    time.sleep(0.1)
    print('Leaving callback')
GPIO.add_event_detect(BUTTON_0_PIN, GPIO.RISING, callback=my_callback,bouncetime =
10)
cnt = 0
try:
    while True:
        time.sleep(1)
        print(cnt)
        cnt = cnt + 1
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    GPIO.output(LED_0_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()
