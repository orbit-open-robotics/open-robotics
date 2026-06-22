#
# test_noggin
#
from orbit import Noggin

if __name__ == '__main__':
    from time import sleep

    # Create the noggin
    noggin = Noggin(pin=16)
    
    # Test parameters
    time = 0.5
    angle_inc = 1.0
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('right...', end='')
    noggin.right(time = time, angle_inc = angle_inc)
    print('right done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('left...', end='')
    noggin.left(time = time, angle_inc = angle_inc)
    print('left done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('right...', end='')
    noggin.right(time = time, angle_inc = angle_inc)
    print('right done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('left...', end='')
    noggin.left(time = time, angle_inc = angle_inc)
    print('left done')
    sleep(2)
    
    print('center...', end='')
    noggin.center(time = time, angle_inc = angle_inc)
    print('center done')
    sleep(2)
    
    print('off.')
    noggin.off()