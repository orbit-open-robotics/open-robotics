#
# FlipperBot is a BaseBot with a flipper
#
#
# Rename this to main to deploy on the Raspberry Pi Pico
#
from orbit import RCBaseBot, Flipper, PWMServoMotor

def get_flipper() -> Flipper:
     
    raw_angle_0 = 0.0
    angle_start = 0
    angle_end = 90
    time = 0.5
    angle_inc = 1.0

    servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = 1)
    servo.home()
    return Flipper(servo)


if __name__ == "__main__":
    robot = RCBaseBot()
    robot.add_accessory(get_flipper())
    robot.initialize()
    robot.start()
