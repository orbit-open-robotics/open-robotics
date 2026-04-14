#
# Print out firmware and library version
import os
print('Pico Information:')
info = os.uname()
print("Version:", info.version)      # detailed firmware build info
print("Machine:", info.machine)
print()

# Orbit Library Version
from orbit import version, show_library
show_library()

# Blink (Pico-W)
from machine import Pin
from time import sleep
led = Pin('LED', Pin.OUT)
for _ in range(20):
    led.toggle()
    sleep(0.05)
led.off()