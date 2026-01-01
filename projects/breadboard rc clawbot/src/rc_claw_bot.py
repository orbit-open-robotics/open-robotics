#
# rc_claw_bot
#
# Version: 2
# Date: 2025-12-30
# Author Sam Linton
# Description: This script controls a robot that is controlled with 
# Bluetooth Low Energy (BLE) using a BBJoystickController. 
# The robot has two motors, a buzzer, and (optionally) a launcher.
# The robot uses tank-drive with two joysticks.
#
from orbit import BLEClient
from orbit import PWMServoMotor
from machine import Pin, PWM
from claw import Claw
from orbit import Buzzer
from basic_drive_train import BasicDriveTrain
from time import sleep
import uasyncio as asyncio

class RCClawBot:
    def __init__(self) -> None:
        self._buzzer = Buzzer(pin = 22)
        self._ble_led = Pin(6, Pin.OUT)
        self._drive_train = BasicDriveTrain()
        self._ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.connected,
            on_disconnected_func=self.disconnected,
            receive_interval_ms=50) #50
        # Claw's lifter servo
        raw_angle_0 = 130.0
        angle_start = 0.0
        angle_end = 130.0
        lifter_servo = PWMServoMotor(pin=16,
                              raw_angle_0 = raw_angle_0,
                              angle_start = angle_start,
                              angle_end = angle_end,
                              angle_home = angle_start,
                              sign = -1)
            
        # Claw's gripper servo
        raw_angle_0 = 115.0
        angle_start = 0.0
        angle_end = 65.0
        gripper_servo = PWMServoMotor(pin=17,
                              raw_angle_0 = raw_angle_0,
                              angle_start = angle_start,
                              angle_end = angle_end,
                              angle_home = angle_start)
            
        # Claw
        self._claw = Claw(lifter_servo, gripper_servo) 
        self._ble_led.off()

    def connected(self) -> None:
        print('CONNECTED')
        self._ble_led.on()
        self._buzzer.begin_sound()
    
    def disconnected(self) -> None:
        print('DISCONNECTED')
        self._ble_led.off()
        self._buzzer.end_sound()

    def receive_message(self, message) -> None:
        self._drive_train.interpret(message)
        self._claw.interpret(message)
    
    def start(self)-> None:
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        await asyncio.gather(self._claw.run_loop(),
                             self._ble_client.run_loop())
        

if __name__ == '__main__':
    rc_claw_bot = RCClawBot()
    rc_claw_bot.start()


