import RPi.GPIO as GPIO
import spidev
import time
import sys
import os
sys.path.insert(0, '/home/pi/WataseRPIFiles/WataseRPIFiles-1/utilities')
import utilities

GPIO.setmode(GPIO.BOARD)

BUTTON_0_PIN = 16

GPIO.setup(BUTTON_0_PIN, GPIO.IN)

#resistor values in dark 10.5k ambient 1.156K light 95
spi = spidev.SpiDev()
spi.open(0,0)

# Settings (for example)
spi.max_speed_hz = 100000

pwm = utilities.HW_PWM(2000)
minValue = 0
maxValue = 0
print('Cover the photosensor and press the push button')
while maxValue == 0:
    channel = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, timeout=1000, bouncetime = 100)
    if channel is None:
         maxValue = 0
    else:   
        to_send = [1, 128, 0]
        output_vals = spi.xfer(to_send)
        adc_val = (output_vals[1] << 8) + output_vals[2]
        maxValue = (adc_val/1023)*3.3
        print(maxValue)

print('Shine a flashlight on the photosensor and press the push button')
while minValue == 0:
    channel = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, timeout=1000, bouncetime = 100)
    if channel is None:
        minValue = 0
    else:   
        to_send = [1, 128, 0]
        output_vals = spi.xfer(to_send)
        adc_val = (output_vals[1] << 8) + output_vals[2]
        minValue = (adc_val/1023)*3.3
        print(minValue)

try:
    while True:
        to_send = [1, 128, 0]
        output_vals = spi.xfer(to_send)
        adc_val = (output_vals[1] << 8) + output_vals[2]
        currentValue = (adc_val/1023)*3.3
        if currentValue < minValue:
            currentValue = minValue
        if currentValue > maxValue:
            currentValue = maxValue
        pwmValue = ((maxValue - currentValue)/(maxValue - minValue))*100
        pwm.set_duty_cycle(pwmValue)
        time.sleep(.001)

except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    time.sleep(1)
    print('turning off light')
    pwm.set_duty_cycle(0.0)
    sys.exit()