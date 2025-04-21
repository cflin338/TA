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

print('Cover the photosensor and press the push button')
GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=10)
return_value = spi.xfer([0x01,0b10000000, 0x00])
dark_value = ((return_value[1]<<8)+return_value[2]) & (0b0000001111111111)
print(dark_value)

print('Shine a flashlight on the photosensor and press the push button')
GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime=10)
return_value = spi.xfer([0x01,0b10000000, 0x00])
light_value = ((return_value[1]<<8)+return_value[2]) & (0b0000001111111111)
print(light_value)


try:
    while True:
        return_value = spi.xfer([0x01,0b10000000, 0x00])
        adc_value = ((return_value[1]<<8)+return_value[2]) & (0b0000001111111111)
        print(adc_value)
        duty_cycle_current = (adc_value - light_value)/(dark_value-light_value)*100
        print(duty_cycle_current)
        pwm.set_duty_cycle(duty_cycle_current)
        time.sleep(0.01)

except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    sys.exit()
