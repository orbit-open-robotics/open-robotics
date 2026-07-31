#
# TankLauncher is a Tank (BaseBot software) with a BallLauncher
#
# Change the server_name to match your Joystick Controller
# Rename this to main to deploy on the Raspberry Pi Pico
#
from orbit import RCBaseBot, BallLauncher

if __name__ == "__main__":
    robot = RCBaseBot(server_name = 'JoystickController')
    robot.add_accessory(BallLauncher())
    robot.initialize()
    robot.start()
