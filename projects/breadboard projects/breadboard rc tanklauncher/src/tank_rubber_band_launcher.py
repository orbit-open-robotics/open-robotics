#
# To deploy this on your robot:
# Change the server_name value to match your joystick controller
# Rename this file to main
#
from orbit.rc_base_bot import RCBaseBot
from orbit.pan_tilt import PanTilt
from orbit.trigger import Trigger

if __name__ == "__main__":
    robot = RCBaseBot(server_name = 'JoystickController')
    robot.add_accessory(PanTilt())
    robot.add_accessory(Trigger())
    robot.initialize()
    robot.start()
