from machine import Pin, SPI
from ili9341 import Display, color565

# SPI0 for the TFT display
spi = SPI(0, baudrate=40000000, sck=Pin(6), mosi=Pin(7))
display = Display(spi, dc=Pin(15), cs=Pin(13), rst=Pin(14))

# Clear screen to blue
display.clear(color565(0, 0, 255))

# Draw a white rectangle
display.draw_rectangle(10, 10, 100, 60, color565(255, 255, 255))

# Fill a red rectangle
display.fill_rectangle(20, 20, 80, 40, color565(255, 0, 0))

# Draw text (requires font file)
# display.draw_text8x8(10, 10, "Hello Pico!", color565(255,255,255))