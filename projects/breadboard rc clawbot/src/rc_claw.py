#
# RCClaw2
#
# Version: 1.00
# Date: 2025-12-29
# Author: Sam Linton
# Description: Radio-controlled claw using a BLE client to receive messages from a joystick controller.
#
from orbit import BLEClient
import uasyncio as asyncio
from claw import Claw
from time import sleep

class RCClaw:
    def __init__(self, claw) -> None:
        self._ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.on_connected,
            on_disconnected_func=self.on_disconnected,
            receive_interval_ms=50) #50
 
        self._claw = claw
        
        sleep(0.5)
        self._claw.lifter.lift()
        self._claw.gripper.close()
        sleep(0.5)
       
    def receive_message(self, message)-> None:
        self._claw.interpret(message)
               
    def on_connected(self):
        print('Connected')
            
    def on_disconnected(self):
        print('Disconnected!')
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        await asyncio.gather(self._ble_client.run_loop(),
                             self._claw.run_loop())
        

if __name__ == '__main__':
    from orbit import PWMServoMotor
    
    # 130 - 0
    raw_angle_0 = 130.0
    angle_start = 0.0
    angle_end = 130.0
    lifter_servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = -1)
    
    # 
    raw_angle_0 = 115.0
    angle_start = 0.0
    angle_end = 65.0
    gripper_servo = PWMServoMotor(pin=17,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start)
    
    claw = Claw(lifter_servo, gripper_servo)
    
    rc_claw = RCClaw(claw)
    rc_claw.start()
