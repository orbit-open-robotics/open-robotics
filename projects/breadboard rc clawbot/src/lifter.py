#
# Lifter
#
# Version: 2.00
# Date: 2025-12-28
# Author: Sam Linton
# Description: A class that runs the lifter mechanism of a claw.
# This uses the ServoMotor class
#
from orbit import ServoMotor
import uasyncio as asyncio


class Lifter:
    """Implement a lifter mechanism
    
    lift at bottom is considered the start
    lift at top is considered the end

    """
     
    def __init__(self, servo) -> None:
        """Initializer

        Args:
           servo - ServoMotor derived class
        """
        self._servo = servo
        
    def start_lift(self) -> None:
        self._servo.start_increasing()
        
    def start_lower(self) -> None:
        self._servo.start_decreasing()
        
    def stop(self) -> None:
        self._servo.stop()
        
    def lift(self, time: float | None = None, angle_inc: float = 1.0) -> None:
        """Move gripper to the top
        """
        self._servo.move_to_end(time=time, angle_inc=angle_inc)
        
    def lower(self, time: float | None = None, angle_inc: float = 1.0) -> None:
        """Move gripper to the bottom
        """
        self._servo.move_to_start(time=time, angle_inc=angle_inc)
        
    def off(self) -> None:
        self._servo.off()
        
    def interpret(self, flag, value) -> None:
        if flag == 0:
            self.stop()
            return
        
        if value > 70:
            self.start_lower()
        elif value < 30:
            self.start_lift()
        else:
            self.stop()
        
    async def run_loop(self) -> None:
        print('lifter run_loop')
        await self._servo.run_loop()
        

if __name__ == '__main__':
    from orbit import PWMServoMotor
    from time import sleep
    
    raw_angle_0 = 150.0
    angle_start = 0
    angle_end = 150
    time = 0.5
    angle_inc = 1.0
    
    servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = -1)
    servo.home()
    
    lifter = Lifter(servo)
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)