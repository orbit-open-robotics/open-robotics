#
# Flipper
#
# Version: 1.00
# Date: 2026-05-02
# Author: Sam Linton
# Description: A class that runs the flipper mechanism
# This uses the ServoMotor class
#
from orbit.joystick_controller import JOYSTICK_MIN, JOYSTICK_MAX
from orbit.joystick_controller import JOYSTICK_LEFT_X, JOYSTICK_RIGHT_BUTTON
from orbit import ServoMotor
from orbit import RobotAccessory
import uasyncio as asyncio


class Flipper(RobotAccessory):
    """Implement a flipper mechanism
    
    flipper at bottom is considered the start
    flipper at top is considered the end

    """
    def __init__(self, servo) -> None:
        """Initializer

        Args:
           servo - ServoMotor derived class
        """
        self._servo = servo
        
    def initialize(self) -> None:
        self.lower()
        
    def start_lift(self) -> None:
        self._servo.start_decreasing()
        
    def start_lower(self) -> None:
        self._servo.start_increasing()
        
    def stop(self) -> None:
        self._servo.stop()
        
    def lift(self, time: float | None = None, angle_inc: float = 1.0) -> None:
        """Move gripper to the top"""
        self._servo.move_to_end(time=time, angle_inc=angle_inc)
        
    def lower(self, time: float | None = None, angle_inc: float = 1.0) -> None:
        """Move gripper to the bottom"""
        self._servo.move_to_start(time=time, angle_inc=angle_inc)
        
    def off(self) -> None:
        """Turn off servo"""
        self._servo.off()
        
    def interpret(self, message) -> None:
        """Interpret JoystickController message"""
        values = message.split(',')
        value  = int(values[JOYSTICK_LEFT_X])
        
        if value > 0.2 * JOYSTICK_MAX:
            self.start_lift()
        elif value < 0.2 * JOYSTICK_MIN:
            self.start_lower()
        else:
            self.stop()
     
    async def run_loop(self) -> None:
        print('flipper run_loop')
        await self._servo.run_loop()
        
    def stop_loop(self) -> None:
        self._servo.stop_loop()
