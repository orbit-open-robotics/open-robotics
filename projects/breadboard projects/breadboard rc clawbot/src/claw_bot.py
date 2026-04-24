#
# ClawBot is a BaseBot with lifter and gripper
#
#
# Rename this to main to deploy on the Raspberry Pi Pico
#
from orbit import RCBaseBot, Lifter, Gripper, PWMServoMotor

def get_gripper() -> Gripper:
    raw_angle_0 = -5.0
    angle_start = 0.0
    angle_end = 65.0
    time = 0.5
    angle_inc = 1.0
    servo = PWMServoMotor(pin=17,
                        raw_angle_0 = raw_angle_0,
                        angle_start = angle_start,
                        angle_end = angle_end,
                        angle_home = angle_start)
    servo.home()
    return Gripper(servo)

def get_lifter() -> Lifter:
    raw_angle_0 = 180.0
    angle_start = 0
    angle_end = 180
    time = 0.5
    angle_inc = 1.0
    
    servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = -1)
    servo.home()
    
    return Lifter(servo)    

if __name__ == "__main__":
    robot = RCBaseBot()
    robot.add_accessory(get_lifter())
    robot.add_accessory(get_gripper())
    robot.initialize()
    robot.start()
