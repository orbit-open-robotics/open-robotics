#
# Noggin
#
# Version: 3.00
# Date: 2025-05-30
# Author: Sam Linton
# Description: A class that runs the noggin mechanism of a claw.
#
from orbit.joystick_controller import JOYSTICK_MIN, JOYSTICK_MAX
from orbit.joystick_controller import JOYSTICK_LEFT_Y, JOYSTICK_RIGHT_BUTTON
from orbit import PWMServoMotor
from orbit import RobotAccessory
import uasyncio as asyncio


class Noggin(RobotAccessory):
    """Implement a noggin mechanism
    
    noggin at its left is considered the start
    noggin at its right is the end

    """
    def __init__(
        self,
        pin: int = 16,
        raw_angle_0: float = 90.0,
        angle_start: float = -90.0,
        angle_end: float = 90.0,
        angle_home: float = 0.0
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
                            angle_home = angle_home,
                            sign = -1)
        
        
    def initialize(self) -> None:
        self.center()
        
    def start_right_rotate(self) -> None:
        self._servo.start_increasing()
        
    def start_left_rotate(self) -> None:
        self._servo.start_decreasing()
        
    def stop(self) -> None:
        self._servo.stop()
        
    def right(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move gripper to the top"""
        self._servo.move_to_end(time=time, angle_inc=angle_inc)
        
    def left(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move gripper to the bottom"""
        self._servo.move_to_start(time=time, angle_inc=angle_inc)
        
    def center(self, time: float = 0.0, angle_inc: float = 1.0) -> None:
        """Move gripper to the bottom"""
        self._servo.home(time=time, angle_inc=angle_inc)
        
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

        value  = int(values[JOYSTICK_LEFT_Y])
        
        if value > 0.2 * JOYSTICK_MAX:
            self.start_right_rotate()
        elif value < 0.2 * JOYSTICK_MIN:
            self.start_left_rotate()
        else:
            self.stop()
     
    async def run_loop(self) -> None:
        print('noggin run_loop')
        await self._servo.run_loop()
        
    def stop_loop(self) -> None:
        self._servo.stop_loop()
        

if __name__ == '__main__':
    from time import sleep

    # Create the noggin
    noggin = Noggin(pin=17)
    
    # Test parameters
    time = 0.5
    angle_inc = 1.0
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('right...', end='')
    noggin.right(time = time, angle_inc = angle_inc)
    print('right done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('left...', end='')
    noggin.left(time = time, angle_inc = angle_inc)
    print('left done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('right...', end='')
    noggin.right(time = time, angle_inc = angle_inc)
    print('right done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('left...', end='')
    noggin.left(time = time, angle_inc = angle_inc)
    print('left done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('off.')
    noggin.off()
