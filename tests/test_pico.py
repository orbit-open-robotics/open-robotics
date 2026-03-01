#
# Print out firmware and library version
#
import os
print('Pico Information:')
info = os.uname()
print("Version:", info.version)      # detailed firmware build info
print("Machine:", info.machine)

print()

from orbit import version
print(f'Orbit library version: {version()}')
