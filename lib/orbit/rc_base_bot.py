#
# rc_base_bot
#
# Version: 2
# Date: 2026-04-09
# Author Sam Linton
# Description: This script controls a robot that is controlled with 
# Bluetooth Low Energy (BLE) using a JoystickController. 
# The robot uses a DriveTrain object and a Buzzer object. The Buzzer and 
# LED indicate the state of the Bluetooth connection.
# The robot uses tank-drive with two joysticks.
#
from orbit.ble_client import BLEClient
from orbit.robot_accessory import RobotAccessory
from machine import Pin
from orbit.buzzer import Buzzer
from orbit.drive_train import DriveTrain
import uasyncio as asyncio

class RCBaseBot:
    def __init__(self, server_name: str = 'JoystickController') -> None:
        self._buzzer = Buzzer(pin = 22)
        self._ble_led = Pin(6, Pin.OUT)
        self._drive_train = DriveTrain()
        self._ble_client = BLEClient(
            server_name=server_name,
            receive_message_func=self._receive_message,
            on_connected_func=self._connected,
            on_disconnected_func=self._disconnected,
            receive_interval_ms=50) #50
        self._accessories = []
        
        self._ble_led.off()        


    @property
    def drive_train(self) -> DriveTrain:
        return self._drive_train
    
    def initialize(self) -> None:
        print('initialize')
        for accessory in self._accessories:
            accessory.initialize()
    
    def add_accessory(self, accessory: RobotAccessory) -> None:
        """Add accessory to the robot
        Args:
            accessory (RobotAccessory): RobotAccessory to add
        """
        self._accessories.append(accessory)

    def _connected(self) -> None:
        """This function is the default method for BLE connection"""
        print('CONNECTED')
        self._ble_led.on()
        self._buzzer.begin_sound()
        for accessory in self._accessories:
            accessory.connected
    
    def _disconnected(self) -> None:
        """This function is the default method for BLE disconnection"""
        print('DISCONNECTED')
        self._ble_led.off()
        self._buzzer.end_sound()
        for accessory in self._accessories:
            accessory.disconnected()

    def _receive_message(self, message: str) -> None:
        """Default method called when a message is received.
        Args:
            message (str): method received from server
        """
        self._drive_train.interpret(message)
        for accessory in self._accessories:
            accessory.interpret(message)

    async def run_loop(self) -> None:
        print('run_loop started')
        tasks = []
        tasks.append(asyncio.create_task(self._ble_client.run_loop()))
        for accessory in self._accessories:
            if accessory.run_loop:
                print('Adding a function')
                tasks.append(asyncio.create_task(accessory.run_loop()))
        await asyncio.gather(*tasks)

    def start(self) -> None:
        print('start')
        asyncio.run(self.run_loop())

    def stop(self) -> None:
        """Method to stop the robot"""
        # TODO: stop the BLEClient?
        # t.cancel()
        for accessory in self._accessories:
            accessory.stop()

        
if __name__ == '__main__':
    rc_basebot = RCBaseBot()
    rc_basebot.start()

