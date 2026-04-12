#
# test_laser
#
from orbit import Laser
from time import sleep

laser = Laser()
# Turn on the laser
print('Turning laser on...', end='')
laser.interpret("0,0,0,0,0,0,0")
sleep(1)
print('Turning laser off...', end='')
laser.interpret("0,0,0,0,0,0,1")
print('Done.')