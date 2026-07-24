"""
Simple test script for ILI9341Display.

Wiring assumptions (adjust pin numbers to match your actual wiring):
    SCK  -> GP2
    MOSI -> GP3
    (MISO not used - display is write-only)
    CS   -> GP5
    DC   -> GP6
    RST  -> GP7

Run this directly in Thonny with the Pico connected.
"""

from machine import Pin, SPI
from ili9341_display import ILI9341Display
import time


# ---------------------------------------------------------------------
# 1. Set up SPI bus
# ---------------------------------------------------------------------
spi = SPI(0,
          baudrate=40_000_000,
          polarity=0,
          phase=0,
          sck=Pin(2),
          mosi=Pin(3))

# ---------------------------------------------------------------------
# 2. Instantiate the display
#    (cs, dc, rst are plain pin numbers per our design)
# ---------------------------------------------------------------------
print("Initializing display...")
display = ILI9341Display(spi, cs=5, dc=6, rst=7, width=240, height=320)
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
# ---------------------------------------------------------------------
display.fill(BLACK)
display.rect(10, 10, 100, 60, WHITE)              # hollow rectangle
display.fill_rect(130, 10, 100, 60, GREEN)        # filled rectangle
display.line(10, 100, 220, 100, WHITE)            # horizontal-ish line
display.hline(10, 120, 220, RED)                  # explicit horizontal line
display.vline(10, 140, 100, BLUE)                 # vertical line
display.show()
pause("Test 2: shapes (rect, fill_rect, lines)")


# ---------------------------------------------------------------------
# Test 3: Text (exercises FrameBuffer.text - built-in 8x8 font)
# ---------------------------------------------------------------------
display.fill(BLACK)
display.text("Hello, Pico!", 10, 10, WHITE)
display.text("ILI9341 test", 10, 25, GREEN)
display.show()
pause("Test 3: text rendering")


# ---------------------------------------------------------------------
# Test 4: Pixel-level check + partial blit via block()
#    Draws a small red square directly with block(), bypassing
#    the main framebuffer, to confirm windowed writes work.
# ---------------------------------------------------------------------
display.fill(BLACK)
display.show()

square_size = 20
patch = bytearray(RED.to_bytes(2, 'big') * (square_size * square_size))
display.block(50, 50, 50 + square_size - 1, 50 + square_size - 1, patch)
pause("Test 4: partial blit via block() - red square at (50,50)")


# ---------------------------------------------------------------------
# Test 5: Simple animation loop (exercises repeated show() calls,
#    a basic sanity check for frame rate / flicker)
# ---------------------------------------------------------------------
print("Test 5: bouncing ball animation (5 seconds)...")
ball_x, ball_y = 20, 20
dx, dy = 4, 3
ball_size = 10

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
display.text("Tests complete!", 10, 10, WHITE)
display.show()
print("All tests complete.")