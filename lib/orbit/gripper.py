#
# Gripper
#
# Version: 3.00
# Date: 2026-05-30
# Author: Sam Linton
#
# Description: A class that runs the gripper mechanism of a claw.
#
from orbit.joystick_controller import JOYSTICK_MIN, JOYSTICK_MAX
from orbit.joystick_controller import JOYSTICK_LEFT_Y, JOYSTICK_RIGHT_BUTTON
from orbit import PWMServoMotor
from orbit import RobotAccessory
import uasyncio as asyncio

class Gripper(RobotAccessory):
    """Implement gripper mechanism"""
        
    def __init__(
        self,
        pin: int = 17,
        raw_angle_0: float = 0.0,
        angle_start: float = 0.0,
        angle_end: float = 65.0) -> None:
        """Initializer

        Gripper angle goes from 0 (closed) to angle_end (fully open)

        Args:
            servo - PWMServoMotor, subclass of ServoMotor
        """
        self._servo: PWMServoMotor = PWMServoMotor(pin=17,
            raw_angle_0 = raw_angle_0,
            angle_start = angle_start,
            angle_end = angle_end,
            angle_home = angle_start)
        
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
            self.start_close()
        elif value < 0.2 * JOYSTICK_MIN:
            self.start_open()
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
    
    # Create the gripper
    pin: int = 17,
    raw_angle_0: float = 0.0
    angle_start: float = 0.0
    angle_end: float = 65.0
    gripper = Gripper(pin, raw_angle_0, angle_start, angle_end)
    
    # Test variables
    time:float = 0.5
    angle_inc: float = 1.0
    
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