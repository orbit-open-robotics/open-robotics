#
# oled
# Note: may need a little sleep before creating Oled
#
# http://docs.micropython.org/en/latest/library/framebuf.html
#
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from time import sleep

class Oled(SSD1306_I2C):
    WIDTH = 128
    HEIGHT = 32
    def __init__(self, i2c_num=0, scl_pin=1, sda_pin=0) -> None:
        sleep(0.5)
        i2c = I2C(i2c_num, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
        super().__init__(Oled.WIDTH, Oled.HEIGHT, i2c)

    def draw_eyes(self)-> None:
        self.ellipse(28, 4, 8, 3, 1, True)
        self.ellipse(100, 4, 8, 3, 1, True)
        
    def draw_mouth(self)-> None:
        self.rect(15, 20, 98, 5, 1, True)
        
    def draw_neutral(self)-> None:
        self.fill(0)
        self.draw_eyes()
        self.draw_mouth()
        self.show()

if __name__ == '__main__':
    from time import sleep

    oled = Oled()
    oled.draw_neutral()
