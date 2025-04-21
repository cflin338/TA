import time
import os
import sys
import spidev
import RPi.GPIO as GPIO

sys.path.insert(0, '../utilities')
import utilities as u
pwm = u.HW_PWM(2000)

GPIO.setmode(GPIO.BOARD)
BUTTON_0_PIN = 16
GPIO.setup(BUTTON_0_PIN, GPIO.IN)

bus = 0
device = 0

spi = spidev.SpiDev()
spi.open(bus, device)

spi.max_speed_hz = 100000

try:
    print("Cover the photosensor and press the push button")
    #wait for user to find max_adc
    button_input = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, timeout=20000, bouncetime=10)
    if button_input:
        mosi_data = [1, 0b10000000, 0b00000000]
        miso_data = spi.xfer(mosi_data)
        
        max_adc = ((0b00000011 and miso_data[1]) << 8) + miso_data[2]
        
        
    print("Shine a flashlight on the photosensor and press the push button")
    #wait for user to find min_adc
    button_input = GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, timeout=20000, bouncetime=10)
    if button_input:
        mosi_data = [1, 0b10000000, 0b00000000]
        miso_data = spi.xfer(mosi_data)
        
        min_adc = ((0b00000011 and miso_data[1]) << 8) + miso_data[2]
    
    
    adc_diff = (max_adc - min_adc) / 100
    
    
    while True:
        mosi_data = [1, 0b10000000, 0b00000000]
        miso_data = spi.xfer(mosi_data)

        # Use return value to calculate the raw ADC value
        adc_val = ((0b00000011 and miso_data[1]) << 8) + miso_data[2]
        
        pwm_val = (adc_val - min_adc) / adc_diff
        pwm.set_duty_cycle(pwm_val)

        time.sleep(0.01)
    
    
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(0.0)
    sys.exit()