import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BOARD)
BUTTON_0_PIN = 16
LED_0_PIN = 18
cur_state = 0
GPIO.setwarnings(False)
GPIO.setup(LED_0_PIN, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(BUTTON_0_PIN, GPIO.FALLING)
try:
    while True:
        edge = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING,bouncetime=10)
        if edge is not None:
            if cur_state == 0:
                print("Light On")
                GPIO.output(LED_0_PIN, GPIO.HIGH)
                cur_state = 1
            else:
                print("Light Off")
                GPIO.output(LED_0_PIN,GPIO.LOW)
                cur_state = 0
            edge = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.FALLING,bouncetime=10)
except KeyboardInterrupt:
    print("\nKeyboard interrupt")
    GPIO.output(LED_0_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()
