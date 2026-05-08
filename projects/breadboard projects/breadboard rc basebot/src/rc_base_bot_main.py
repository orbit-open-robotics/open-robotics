#
# To deploy this on your robot:
# Change the server_name value to match your joystick controller
# Rename this file to main
#
from orbit import RCBaseBot

if __name__ == "__main__":
    robot = RCBaseBot(server_name = 'JoystickController')
    robot.start()