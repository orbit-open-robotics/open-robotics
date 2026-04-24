#
# Claw
#
# Version: 1.00
# Date: 2025-12-29
# Author: Sam Linton
# Description: claw, consisting of a lifter and a gripper
#
import uasyncio as asyncio
from gripper import Gripper
from lifter import Lifter
from time import sleep

class Claw:
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_BUTTON = 4
    RIGHT_BUTTON = 5
    
    def __init__(self, lifter_servo, gripper_servo) -> None:
        self._lifter = Lifter(lifter_servo)
        self._gripper = Gripper(gripper_servo)
        
        sleep(0.5)
        self._lifter.lift()
        self._gripper.close()
        sleep(0.5)
        
    @property
    def lifter(self) -> Lifter:
        if not self._lifter:
            raise ValueError("Lifter does not exist.")
        return self._lifter
    
    @property
    def gripper(self) -> Gripper:
        if not self._gripper:
            raise ValueError("Gripper does not exist.")
        return self._gripper
        
    def interpret(self, message) -> None:
        values = message.split(',')
        
        flag = 1-int(values[Claw.RIGHT_BUTTON])
        gripper_value = int(values[Claw.LEFT_Y])
        lifter_value  = int(values[Claw.LEFT_X])
        self._lifter.interpret(flag, lifter_value)
        self._gripper.interpret(flag, gripper_value)
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        await asyncio.gather(self._lifter.run_loop(),
                             self._gripper.run_loop())
        

if __name__ == '__main__':
    from orbit import PWMServoMotor
    
    time = 0.5
    angle_inc = 1.0
    
    raw_angle_0 = 130.0
    angle_start = 0.0
    angle_end = 130.0
    lifter_servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = -1)
    
    raw_angle_0 = 115.0
    angle_start = 0.0
    angle_end = 65.0
    gripper_servo = PWMServoMotor(pin=17,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start)
    
    claw = Claw(lifter_servo, gripper_servo)
    lifter = claw.lifter
    gripper = claw.gripper
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('Opening...', end='')
    gripper.open(time = time, angle_inc = angle_inc)
    print('open')
    sleep(2)
    print()
    
    print('Closing...', end='')
    gripper.close(time = time, angle_inc = angle_inc)
    print('closed')
    sleep(2)
    
    lifter.off()
    gripper.off()
