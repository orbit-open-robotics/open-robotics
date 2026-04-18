#
# Laser
#
from orbit.robot_accessory import RobotAccessory
from machine import Pin

class Laser(RobotAccessory):
    LASER_BUTTON = 5

    def __init__(self, pin: int = 7) -> None:
        super().__init__()
        self._laser = Pin(pin, Pin.OUT)
        self.off()
        
    def on(self) -> None:
        self._laser.on()
        
    def off(self) -> None:
        self._laser.off()

    def interpret(self, message: str) -> None:
        values = message.split(',')
        
        # stop if the right button is pressed (value low)
        right_button: bool = int(values[Laser.LASER_BUTTON]) == 0
        if right_button:
            self.on()
        else:
            self.off()