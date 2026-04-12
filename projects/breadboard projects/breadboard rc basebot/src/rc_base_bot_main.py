#
# Rename this to main to deploy on the Raspberry Pi Pico
#
from orbit import RCBaseBot

if __name__ == "__main__":
    robot = RCBaseBot()
    robot.start()