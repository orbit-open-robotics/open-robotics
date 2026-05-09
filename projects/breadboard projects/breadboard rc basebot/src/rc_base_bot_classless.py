#
# rc_base_bot
#
# Version: 1.01
# Date: 2025-08-10
# Author Sam Linton
# Description: This script controls a robot that is controlled with 
# Bluetooth Low Energy (BLE) using a BBJoystickController. 
# The robot has two motors, an LED, and a buzzer.
# The robot uses tank-drive with two joysticks.
#
from orbit import BLEClient
from machine import Pin, PWM
from orbit import Buzzer
from time import sleep
from orbit import DriveTrain

# DriveTrain
drive_train = DriveTrain()

# Connection led
led = Pin(6, Pin.OUT)
led.off()

# Buzzer
buzzer = Buzzer(pin = 22)

def connected():
    """Callback function when a BLE connection is established."""
    print('CONNECTED')
    led.on()
    buzzer.begin_sound()
    
def disconnected():
    """Callback function when a BLE connection is disconnected."""
    print('DISCONNECTED')
    led.off()
    buzzer.end_sound()

def receive_message(message):
    """Receive a message from the BLE client and interpret it to 
    control the robot.
    The left and right x and y values should range from 0-100
    """
    drive_train.interpret(message)

    
client = BLEClient(
    server_name='JoystickController', # Must match the name of the JoystickController 
    on_connected_func=connected,
    on_disconnected_func=disconnected,
    receive_message_func=receive_message,
    receive_interval_ms=100)

client.start()

