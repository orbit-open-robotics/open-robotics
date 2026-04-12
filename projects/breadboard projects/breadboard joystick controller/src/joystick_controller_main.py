#
# Rename this to main to deploy on the Raspberry Pi Pico
#
from orbit import JoystickController

if __name__ == "__main__":
    controller = JoystickController()
    controller.start()