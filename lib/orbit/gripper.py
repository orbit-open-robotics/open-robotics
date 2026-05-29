#
# Gripper
#
# Version: 2.00
# Date: 2025-12-28
# Author: Sam Linton
#
# Description: A class that runs the gripper mechanism of a claw.
# This version uses the ServoController class
#
from orbit.joystick_controller import JOYSTICK_MIN, JOYSTICK_MAX
from orbit.joystick_controller import JOYSTICK_LEFT_Y, JOYSTICK_RIGHT_BUTTON
from orbit import ServoMotor
from orbit import RobotAccessory
import uasyncio as asyncio

class Gripper(RobotAccessory):
    """Implement gripper mechanism"""
        
    def __init__(self, servo) -> None:
        """Initializer

        Gripper angle goes from 0 (closed) to open_angle (fully open)
        These angles correspond with the servo_close_angle and servo_open_angle, respectively

        Args:
            servo - Subclass of ServoMotor
        """
        self._servo = servo
        
        
    def initialize(self) -> None:
        self.close()
        
    def open(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Open the gripper completely"""
        self._servo.move_to_end(time = time, angle_inc = angle_inc)
        
    def close(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Close the gripper completely"""
        self._servo.move_to_start(time = time, angle_inc = angle_inc)
            
    def start_open(self) -> None:
        self._servo.start_increasing()
  
    def start_close(self) -> None:
        self._servo.start_decreasing()
        
    def stop(self) -> None:
        self._servo.stop()
        
    def off(self) -> None:
        self._servo.off()
        
    def interpret(self, message) -> None:
        """Interpret message from JoystickController"""
        values = message.split(',')
        
        flag = 1 - int(values[JOYSTICK_RIGHT_BUTTON])
        value = int(values[JOYSTICK_LEFT_Y])

        if flag == 0:
            self.stop()
            return
        
        if value > 0.2 * JOYSTICK_MAX:
            self.start_open()
        elif value < 0.2 * JOYSTICK_MIN:
            self.start_close()
        else:
            self.stop()
        
    async def run_loop(self) -> None:
        print('gripper run_loop')
        await self._servo.run_loop()
        
        
    def stop_loop(self) -> None:
        self._servo.stop_loop()
        
        
if __name__ == '__main__':
    from orbit import PWMServoMotor
    from time import sleep
    
    raw_angle_0 = 115.0
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
    
    gripper = Gripper(servo)
    
    print('Opening...', end='')
    gripper.open(time = time, angle_inc = angle_inc)
    print('open')
    sleep(2)
    print()
    
    print('Closing...', end='')
    gripper.close(time = time, angle_inc = angle_inc)
    print('closed')
    sleep(2)
    
    gripper.off()