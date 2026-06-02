#
# Lifter
#
# Version: 3.00
# Date: 2025-05-30
# Author: Sam Linton
# Description: A class that runs the lifter mechanism of a claw.
#
from orbit.joystick_controller import JOYSTICK_MIN, JOYSTICK_MAX
from orbit.joystick_controller import JOYSTICK_LEFT_X, JOYSTICK_RIGHT_BUTTON
from orbit import PWMServoMotor
from orbit import RobotAccessory
import uasyncio as asyncio


class Lifter(RobotAccessory):
    """Implement a lifter mechanism
    
    lift at bottom is considered the start
    lift at top is considered the end

    """
    def __init__(
        self,
        pin: int = 16,
        raw_angle_0: float = 180.0,
        angle_start: float = 0.0,
        angle_end: float = 180.0
        ) -> None:  
        
        """Initializer

        Args:
           servo - ServoMotor derived class
        """
        self._servo = PWMServoMotor(
                            pin=pin,
                            raw_angle_0 = raw_angle_0,
                            angle_start = angle_start,
                            angle_end = angle_end,
                            angle_home = angle_start,
                            sign = -1)
        
        
    def initialize(self) -> None:
        self.lower()
        
    def start_lift(self) -> None:
        self._servo.start_increasing()
        
    def start_lower(self) -> None:
        self._servo.start_decreasing()
        
    def stop(self) -> None:
        self._servo.stop()
        
    def lift(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move gripper to the top"""
        self._servo.move_to_end(time=time, angle_inc=angle_inc)
        
    def lower(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move gripper to the bottom"""
        self._servo.move_to_start(time=time, angle_inc=angle_inc)
        
    def off(self) -> None:
        """Turn off servo"""
        self._servo.off()
        
    def interpret(self, message) -> None:
        """Interpret JoystickController message"""
        values = message.split(',')
        
        flag = 1 - int(values[JOYSTICK_RIGHT_BUTTON])
        if flag == 0:
            self.stop()
            return

        value  = int(values[JOYSTICK_LEFT_X])
        
        if value > 0.2 * JOYSTICK_MAX:
            self.start_lift()
        elif value < 0.2 * JOYSTICK_MIN:
            self.start_lower()
        else:
            self.stop()
     
    async def run_loop(self) -> None:
        print('lifter run_loop')
        await self._servo.run_loop()
        
    def stop_loop(self) -> None:
        self._servo.stop_loop()
        

if __name__ == '__main__':
    from time import sleep

    # Create the lifter
    raw_angle_0 = 180.0
    angle_start = 0
    angle_end = 180

    lifter = Lifter(pin=16,
                    raw_angle_0 = raw_angle_0,
                    angle_start = angle_start,
                    angle_end = angle_end)
    
    # Test parameters
    time = 0.5
    angle_inc = 1.0
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('lift done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('lowr done')
    sleep(2)
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('lift done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('lower done')
    sleep(2)
    
    print('off.')
    lifter.off()