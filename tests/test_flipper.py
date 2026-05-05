from orbit import ServoMotor, Flipper
import uasyncio as asyncio

if __name__ == '__main__':
    from orbit import PWMServoMotor
    from time import sleep
    
    raw_angle_0 = 0.0
    angle_start = 0
    angle_end = 90
    time = 0.5
    angle_inc = 1.0
    
    servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = 1)
    servo.home()
    
    flipper = Flipper(servo)
    
    print('lift...', end='')
    flipper.lift(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lower...', end='')
    flipper.lower(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lift...', end='')
    flipper.lift(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lower...', end='')
    flipper.lower(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('off.')
    flipper.off()