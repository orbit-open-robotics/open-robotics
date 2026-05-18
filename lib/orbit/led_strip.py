from machine import Pin
from neopixel import NeoPixel
from time import sleep
from random import randint

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

color_dict = {
        'black': BLACK,
        'red': RED,
        'green': GREEN,
        'blue': BLUE,
        'yellow': YELLOW,
        'magenta': MAGENTA,
        'cyan': CYAN,
        'white': WHITE,
    }

class LEDStrip:
    def __init__(self, num_leds: int = 60, pin: int = 28) -> None:
        self._num_leds: int = num_leds
        self._np: NeoPixel = NeoPixel(Pin(pin), num_leds)
        self._actions: dict = {
            'blink': self.blink,
            'pulse': self.pulse,
            'bounce': self.bounce,
            'random': self.random,
            }
            
    def act(self, action: str, *args, **kwargs) -> None:
        print(f'act: {action}')
        self._dispatch(action, *args, **kwargs)
        
    def fill(self, color: tuple) -> None:
        for i in range(self._num_leds):
            self._np[i] = color
        self._np.write()
        
    def clear(self) -> None:
        self.fill((0, 0, 0))
        
    def blink(self, color: tuple = RED, duration: float = 0.2) -> None:
        self.fill(RED)
        sleep(duration)
        self.clear()

    def pulse(self) -> None:
        self._pulse_color((1, 0, 0))
        self._pulse_color((0, 1, 0))
        self._pulse_color((0, 0, 1))
        self.clear()
        
    def bounce(self, color: tuple = RED) -> None:
        for index in range(0, self._num_leds):
            self._single_led(index = index, color = color)
            sleep(0.01)
        for index in range(self._num_leds-1, 0, -1):
            self._single_led(index = index, color = color)
            sleep(0.01)
        self.clear()
        
    def random(self, num: int = 10) -> None:
        for _ in range(num):
            for i in range(self._num_leds):
                self._np[i] = (
                    randint(0, 255),
                    randint(0, 255),
                    randint(00, 255))
            self._show()
            sleep(0.4)
        self.clear()
        
    def _dispatch(self, name, *args, **kwargs) -> None:
        self._actions[name](*args, **kwargs)
        
    def _pulse_color(self, selector: tuple) -> None:
        for value in range(0, 256, 3):
            self.fill((selector[0]*value, selector[1]*value, selector[2]*value))
            sleep(0.0005)
        for value in range(255, 0, -3):
            self.fill((selector[0]*value, selector[1]*value, selector[2]*value))
            sleep(0.0005)
        
    def _single_led(self, index: int = 0, color: tuple = RED) -> None:
        for i in range(self._num_leds):
            led_color = color if index == i else BLACK
            self._np[i] = led_color
        self._show()
        
    def _set(self, index: int, color: tuple) -> None:
        self._np[index] = color
 
    def _show(self) -> None:
        self._np.write()
        
if __name__ == '__main__':
    led_strip = LEDStrip()
    led_strip.act('blink')
    led_strip.act('bounce', color = BLUE)
#     led_strip.blink()
#     led_strip.bounce(color = BLUE)
#     led_strip.pulse()
#     led_strip.random()
    