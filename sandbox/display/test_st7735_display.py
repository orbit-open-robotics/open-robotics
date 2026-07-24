"""
Simple test script for ST7735Display.

Wiring assumptions (adjust pin numbers to match your actual wiring):
    SCK  -> GP2
    MOSI -> GP3
    (MISO not used - display is write-only)
    CS   -> GP5
    DC   -> GP6
    RST  -> GP7

Run this directly in Thonny with the Pico connected.

Note: ST7735 modules come in different "tab" variants (red/blue/green)
that need slightly different init sequences. This test assumes the
ST7735Display class defaults to the red-tab init sequence. If colors
look wrong (washed out, wrong tint, shifted image), you likely have a
different tab variant - see our earlier discussion on tab colors.
"""

from machine import Pin, SPI
from st7735_display import ST7735Display  # adjust import to match your file/module name
import time


# ---------------------------------------------------------------------
# 1. Set up SPI bus
# ---------------------------------------------------------------------
spi = SPI(0,
          baudrate=20_000_000,   # ST7735 modules are often less tolerant of very high speeds than ILI9341
          polarity=0,
          phase=0,
          sck=Pin(2),
          mosi=Pin(3))

# ---------------------------------------------------------------------
# 2. Instantiate the display
#    (cs, dc, rst are plain pin numbers per our design)
# ---------------------------------------------------------------------
print("Initializing display...")
display = ST7735Display(spi, cs=5, dc=6, rst=7, width=128, height=160)
print("Display initialized.")

# A few RGB565 color constants for the tests
BLACK = 0x0000
WHITE = 0xFFFF
RED   = 0xF800
GREEN = 0x07E0
BLUE  = 0x001F


def pause(label, seconds=1.5):
    """Print a label and give time to visually inspect the screen."""
    print(label)
    time.sleep(seconds)


# ---------------------------------------------------------------------
# Test 1: Full screen fill (exercises FrameBuffer.fill + show/block)
# ---------------------------------------------------------------------
display.fill(RED)
display.show()
pause("Test 1: full screen RED")

display.fill(GREEN)
display.show()
pause("Test 1: full screen GREEN")

display.fill(BLUE)
display.show()
pause("Test 1: full screen BLUE")

display.fill(BLACK)
display.show()
pause("Test 1: full screen BLACK (cleared)")


# ---------------------------------------------------------------------
# Test 2: Basic shapes (exercises FrameBuffer.rect / fill_rect / line)
#    Sized down for the smaller 128x160 screen vs. the ILI9341 test.
# ---------------------------------------------------------------------
display.fill(BLACK)
display.rect(5, 5, 55, 40, WHITE)                 # hollow rectangle
display.fill_rect(70, 5, 50, 40, GREEN)           # filled rectangle
display.line(5, 55, 120, 55, WHITE)               # horizontal-ish line
display.hline(5, 65, 120, RED)                    # explicit horizontal line
display.vline(5, 75, 70, BLUE)                    # vertical line
display.show()
pause("Test 2: shapes (rect, fill_rect, lines)")


# ---------------------------------------------------------------------
# Test 3: Text (exercises FrameBuffer.text - built-in 8x8 font)
# ---------------------------------------------------------------------
display.fill(BLACK)
display.text("Hello, Pico!", 5, 5, WHITE)
display.text("ST7735 test", 5, 20, GREEN)
display.show()
pause("Test 3: text rendering")


# ---------------------------------------------------------------------
# Test 4: Pixel-level check + partial blit via block()
#    Draws a small red square directly with block(), bypassing
#    the main framebuffer, to confirm windowed writes work.
# ---------------------------------------------------------------------
display.fill(BLACK)
display.show()

square_size = 16
patch = bytearray(RED.to_bytes(2, 'big') * (square_size * square_size))
display.block(30, 30, 30 + square_size - 1, 30 + square_size - 1, patch)
pause("Test 4: partial blit via block() - red square at (30,30)")


# ---------------------------------------------------------------------
# Test 5: Simple animation loop (exercises repeated show() calls,
#    a basic sanity check for frame rate / flicker)
# ---------------------------------------------------------------------
print("Test 5: bouncing ball animation (5 seconds)...")
ball_x, ball_y = 10, 10
dx, dy = 3, 2
ball_size = 8

start = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start) < 5000:
    display.fill(BLACK)
    display.fill_rect(ball_x, ball_y, ball_size, ball_size, WHITE)
    display.show()

    ball_x += dx
    ball_y += dy
    if ball_x <= 0 or ball_x + ball_size >= display.width:
        dx = -dx
    if ball_y <= 0 or ball_y + ball_size >= display.height:
        dy = -dy

print("Test 5: done.")

# ---------------------------------------------------------------------
# Wrap up
# ---------------------------------------------------------------------
display.fill(BLACK)
display.text("Tests done!", 5, 5, WHITE)
display.show()
print("All tests complete.")