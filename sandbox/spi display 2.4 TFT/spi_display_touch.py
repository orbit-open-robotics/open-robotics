from machine import Pin, SPI
from ili9341 import Display, color565
from xpt2046 import Touch

# TFT on SPI0
spi_tft = SPI(0, baudrate=40000000, sck=Pin(6), mosi=Pin(7))
display = Display(spi_tft, dc=Pin(15), cs=Pin(13), rst=Pin(14))

# Touch on SPI1
def touch_handler(x, y):
    print(f"Touch at: x={x}, y={y}")
    display.fill_circle(x, y, 5, color565(255, 0, 0))

spi_touch = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
touch = Touch(spi_touch, cs=Pin(12), int_pin=Pin(0), int_handler=touch_handler)

display.clear(color565(0, 0, 0))

# Main loop — touch events fire via interrupt
while True:
    pass