#
# rc_base_bot
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
from machine import Pin, PWM
from orbit import Buzzer
from drive_train import DriveTrain
from time import sleep

class RCBaseBot:
    def __init__(self) -> None:
        self._buzzer = Buzzer(pin = 22)
        self._ble_led = Pin(6, Pin.OUT)
        self._drive_train = DriveTrain()
        self._ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self.receive_message,
            on_connected_func=self.connected,
            on_disconnected_func=self.disconnected,
            receive_interval_ms=50) #50
        
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
    
    def start(self)-> None:
        self._ble_client.start()
        

if __name__ == '__main__':
    rc_basebot = RCBaseBot()
    rc_basebot.start()

