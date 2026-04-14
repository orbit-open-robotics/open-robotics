#
# Laser
#
from orbit.robot_accessory import RobotAccessory
from machine import Pin

class Laser(RobotAccessory):
    LASER_BUTTON = 6

    def __init__(self, pin: int = 7) -> None:
        super().__init__()
        self._laser = Pin(pin)

    def interpret(self, message: str) -> None:
        values = message.split(sep=',')
        
        # stop if the right button is pressed
        right_button: bool = int(values[self.LASER_BUTTON]) == 0
        if right_button:
            self._laser.off()
        else:
            self._laser.on()