#
# test_laser
#
from orbit import Laser
from time import sleep

laser = Laser()

print('Turning laser on.')
laser.on()
sleep(1)

print('Turning laser off.')
laser.off()
sleep(1)

# Turn on the laser
print('Turning laser on.')
laser.interpret("0,0,0,0,0,1")
sleep(1)

print('Turning laser off')
laser.interpret("0,0,0,0,0,0")