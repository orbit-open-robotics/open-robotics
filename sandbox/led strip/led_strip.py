from machine import Pin
from time import sleep
from neopixel import NeoPixel

class LEDStrip:
    def __init__(self, num_leds = 64)
        self._num_leds = num_leds
        self._np = NeoPixel(Pin(pin), num_leds)
        
    def _set(self, index: int, color: tuple):
        self._np[index] = color
 
    def _show(self):
        self._np.write()
        
if __name__ == '__main__':
    led_strip = LEDStrip()
    