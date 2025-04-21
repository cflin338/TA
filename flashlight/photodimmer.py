import time
import sys
import spidev
import RPi.GPIO as GPIO

sys.path.insert(0, '../utilities')
import utilities

BUTTON_0_PIN = 16
LED_0_PIN = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_0_PIN, GPIO.IN)

pwm = utilities.HW_PWM(2000)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000

recieving_list = [0x00, 0x00, 0x00]
dark_input_value = 0b0
bright_input_value = 0b0
current_input_vaue = 0b0

try:
    print("Cover the photosensor and press the push button")
    while GPIO.input(BUTTON_0_PIN) is not GPIO.HIGH:
        sending_list = [0b00000001, 0b10000000, 0x00]
        recieving_list = spi.xfer(sending_list)
        dark_input_value = recieving_list[2] + ((recieving_list[1] & 0b00000011) << 8)
        time.sleep(.01)
    
    while GPIO.input(BUTTON_0_PIN) is not GPIO.LOW:
        time.sleep(.01)
    
    print("Shine a flashlight on the photosensor and press the push button")
    while GPIO.input(BUTTON_0_PIN) is not GPIO.HIGH:
        sending_list = [0b00000001, 0b10000000, 0x00]
        recieving_list = spi.xfer(sending_list)
        bright_input_value = recieving_list[2] + ((recieving_list[1] & 0b00000011) << 8)
        time.sleep(.01)
    
    print("Engaging the LED!")
    pwm_value = 0.0
    
    while True:
        pwm.set_duty_cycle(pwm_value)
        #print("Light on!")
        
        sending_list = [0b00000001, 0b10000000, 0x00]
        recieving_list = spi.xfer(sending_list)
        current_input_vaue = recieving_list[2] + ((recieving_list[1] & 0b00000011) << 8)
        
        pwm_value = (current_input_vaue - bright_input_value) / ((dark_input_value - bright_input_value) / 100)
        
        time.sleep(.01)

except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    sys.exit()