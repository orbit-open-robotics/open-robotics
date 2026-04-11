#
# test_led.py
#
# 
from machine import Pin, Timer
from time import sleep
import uasyncio as asyncio
from orbit import Led
from orbit import Tester

if __name__ == '__main__':

    def test_blink():
        print('Testing blink 4 times...', end='')
        for _ in range(4):
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.5)
        print('done.')
        sleep(2)
      
    def test_toggle():
        print('Test toggle 4 times...', end='')
        for _ in range(4):
            led.toggle()
            sleep(0.5)
        print('done.')
        sleep(2)
        
    def test_default_blink():
        print('Test default blink, on for 3 seconds...', end='')
        led.blink()
        sleep(5)
        led.off()
        print('done')
        sleep(2)

    def test_blink_with_periods():
        print('Test blink with specified periods (50, 500)...', end='')  
        led.blink(periods=(50, 500), count = 2)
        print('done.')
        sleep(2)
        
    def test_blink_with_multiple_periods():
        print('Blink sequence 1, 2, 3 seconds on, repeated 2 times...', end='')
        led.blink(periods=(1000, 500, 2000, 500, 3000, 500), count=2)
        sleep(10)  # Wait for the blink sequence to complete
        print('done.')
        led.off()
        
    led = Led(pin=6)
    tester = Tester()
    
    tester.add("blink", test_blink)
    tester.add("toggle", test_toggle)
    tester.add("default blink", test_default_blink)
    tester.add("default blink with on/off periods", test_blink_with_periods)
    tester.add("default blink with multiple on/off periods", test_blink_with_multiple_periods)
    tester.run_tests()
        

