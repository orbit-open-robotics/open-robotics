#
# rc_base_bot
#
# Version: 2
# Date: 2026-04-08
# Author Sam Linton
# Description: This script controls a robot that is controlled with 
# Bluetooth Low Energy (BLE) using a JoystickController. 
# The robot uses a DriveTrain object and a Buzzer object. The Buzzer and 
# LED indicate the state of the Bluetooth connection.
# The robot uses tank-drive with two joysticks.
#
from orbit.ble_client import BLEClient
from machine import Pin
from orbit.buzzer import Buzzer
from orbit.drive_train import DriveTrain

class RCBaseBot:
    def __init__(self) -> None:
        self._buzzer = Buzzer(pin = 22)
        self._ble_led = Pin(6, Pin.OUT)
        self._drive_train = DriveTrain()
        self._ble_client = BLEClient(
            server_name='JoystickController',
            receive_message_func=self._receive_message,
            on_connected_func=self._connected,
            on_disconnected_func=self._disconnected,
            receive_interval_ms=50) #50
        
        self._ble_led.off()

    @property
    def drive_train(self) -> DriveTrain:
        return self._drive_train

    def _connected(self) -> None:
        """This function is the default method for BLE connection"""
        print('CONNECTED')
        self._ble_led.on()
        self._buzzer.begin_sound()
    
    def _disconnected(self) -> None:
        """This function is the default method for BLE disconnection"""
        print('DISCONNECTED')
        self._ble_led.off()
        self._buzzer.end_sound()

    def _receive_message(self, message: str) -> None:
        """Default method called when a message is received.

        Args:
            message (str): method received from server
        """
        self._drive_train.interpret(message)
    
    def start(self)-> None:
        """Method to start the robot running"""
        self._ble_client.start()
        

if __name__ == '__main__':
    rc_basebot = RCBaseBot()
    rc_basebot.start()

