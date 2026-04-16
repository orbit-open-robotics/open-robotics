#
# Rename this to main to deploy on the Raspberry Pi Pico
#
from orbit import RCBaseBot, LaserTarget, Laser

if __name__ == "__main__":
    laserTarget = LaserTarget()
    laser = Laser()
    robot = RCBaseBot()
#     robot.add_accessory(laserTarget)
    robot.add_accessory(laser)
    robot.initialize()
    robot.start()