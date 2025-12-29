#
# RCClaw
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: Radio-controlled claw using a BLE client to receive messages from a joystick controller.
# TODO: Refactor:
# Claw class that only takes lifter/gripper commands, and
# Separate test classes, one including BLEClient and one without.
#
from orbit import BLEClient
import uasyncio as asyncio
from gripper import Gripper
from lifter import Lifter
from time import sleep

class RCClaw:
    gain: float = 30.0
    
    def __init__(self, lifter_servo, gripper_servo) -> None:
        self.ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.on_connected,
            on_disconnected_func=self.on_disconnected,
            receive_interval_ms=50) #50
        self.running = False
        
        self.lifter = Lifter(lifter_servo)
        self.gripper = Gripper(gripper_servo)
        
        sleep(0.5)
        self.lifter.lift()
        self.gripper.close()
        sleep(0.5)
       
    def receive_message(self, message)-> None:
#         print(f'Message: {message}')
        values = message.split(',')
        
        vals = [int(values[i]) for i in range(len(values))]
        
        print(vals)
        
        self.lifter.interpret(vals[0])
        self.gripper.interpret(vals[1])
       
    def on_connected(self):
        print('Connected')
            
    def on_disconnected(self):
        print('Disconnected!')
            
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        await asyncio.gather(self.ble_client.run_loop(),
                             self.lifter.run_loop(),
                             self.gripper.run_loop())
        

if __name__ == '__main__':
    from orbit import PWMServoMotor
    
    raw_angle_0 = 115.0
    angle_start = 0.0
    angle_end = 65.0
    time = 0.5
    angle_inc = 1.0
    
    lifter_servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = -1)
    
    gripper_servo = PWMServoMotor(pin=17,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start)
    
    rc_claw = RCClaw(lifter_servo, gripper_servo)
    rc_claw.start()