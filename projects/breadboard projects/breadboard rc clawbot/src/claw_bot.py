#
# ClawBot is a BaseBot with lifter and gripper
#
# Change the server_name to match your Joystick Controller
# Rename this to main to deploy on the Raspberry Pi Pico
#
from orbit import RCBaseBot, Lifter, Gripper

if __name__ == "__main__":
    robot = RCBaseBot(server_name = 'JoystickController')
    robot.add_accessory(Lifter())
    robot.add_accessory(Gripper())
    robot.initialize()
    robot.start()
