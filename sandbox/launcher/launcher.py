#
# Launcher
#
from servo import Servo
from time import sleep

# Yaw center is 75deg
# Pitch horizontal = 85 deg
# Trigger vertical = 80 deg (100 cocked) (0 release)
COCKED_ANGLE = 90
RELEASE_ANGLE = 0

class Launcher:
    def __init__(self):
        self.yaw_servo = Servo(pin_id=10)
        self.pitch_servo = Servo(pin_id=11)
        self.trigger = Servo(pin_id=12)
        
        self.initialize()
        
    def initialize(self):
        self.trigger.write(COCKED_ANGLE)
        self.trigger.off()
        
    def yaw(self):
        self.yaw_servo.write(20)
        sleep(1)
        self.yaw_servo.write(170)
        
    def pitch(self, angle):
        self.pitch_servo.write(angle)
        sleep(1)
        
    def shoot(self):
        self.trigger.write(RELEASE_ANGLE)
        sleep(2)
        self.trigger.write(COCKED_ANGLE)
        sleep(1)
        self.trigger.off()
    
    
if __name__ == '__main__':
    launcher = Launcher()
    
    
    launcher.shoot()
    