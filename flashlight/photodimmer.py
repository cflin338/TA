import time
import sys
import os
import RPi.GPIO as GPIO
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000

sys.path.insert(0, '../utilities')
import utilities

BUTTON_0_PIN = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_0_PIN, GPIO.IN)

pwm = utilities.HW_PWM(2000)

print("Cover the photosensor and press the push button")
GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=500)
returned_value = spi.xfer([0x01, 0b10000000, 0x00])
dark_ADC_value = ((returned_value[1] << 8) + (returned_value[2]) & 0b0000001111111111)

print("Shine a flashlight on the photosensor and press the push button")
GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=500)
returned_value = spi.xfer([0x01, 0b10000000, 0x00])
light_ADC_value = ((returned_value[1] << 8) + (returned_value[2]) & 0b0000001111111111)

try:
    while True:
        returned_value = spi.xfer([0x01, 0b10000000, 0x00])
        ADC_value = ((returned_value[1] << 8) + (returned_value[2]) & 0b0000001111111111)
        input_voltage = ADC_value/1023*3.3
        duty_cycle_current = (ADC_value - light_ADC_value)/(dark_ADC_value - light_ADC_value)*100
        pwm.set_duty_cycle(duty_cycle_current)
        time.sleep(0.01)
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    sys.exit()
