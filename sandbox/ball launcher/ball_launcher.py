from orbit import PWMServoMotor
from time import sleep

servo = PWMServoMotor(pin=10)

ANGLE_CATCH = 180.0
ANGLE_RELEASE = 45.0


for i in range(3):
    servo.move_to_angle(ANGLE_CATCH)
    sleep(1)
    servo.move_to_angle(ANGLE_RELEASE)
    sleep(1)
