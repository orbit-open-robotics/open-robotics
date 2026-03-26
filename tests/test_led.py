#
# test_led.py
#
# 
from machine import Pin, Timer
from time import sleep
import uasyncio as asyncio
from orbit import Led

if __name__ == '__main__':
    try:
        led = Led(pin=6)

        # Test basic on/off functionality
        print('Test basic blink 4 times', end='')
        for _ in range(4):
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.5)
        print('done.')
        sleep(2)

        # Test toggle functionality
        print('Test toggle 4 times', end='')
        for _ in range(4):
            led.toggle()
            sleep(0.5)
        print('done.')
        sleep(2)
        
        # Test default blink
        print('Test default blink, turn on for 3 seconds...', end='')
        led.blink()
        sleep(3)
        led.off()
        print('done.')
        sleep(2)

        # Test blink with custom periods
        print('Test blink with specified periods (50, 500)...', end='')  
        led.blink(periods=(50, 500), count = 2)
        print('done.')
        sleep(2)

        # Test auto blink
        print('Auto blink for 5 seconds', end='')
        led.blink()
        sleep(5)
        led.off()
        print('done.')
        sleep(2)
        
        # Test blink with multiple periods
        print('Blink sequence 1, 2, 3 seconds on, repeated 2 times.', end='')
        led.blink(periods=(1000, 500, 2000, 500, 3000, 500), count=2)
        sleep(10)  # Wait for the blink sequence to complete
        print('done.')
        led.off()
        
        print('All tests completed.')
        
    except KeyboardInterrupt:
        print('Keyboard interrupt.')
        led.off()
        

