from orbit import ServoMotor, Lifter
import uasyncio as asyncio

# 
# async def run_loop():
#     await asyncio.gather(asyncio.create_task(lifter.start_loop),
#                          asyncio.create_task(terminate_after_delay(lifter)))
# 
# def test_terminate_after_delay():
#     
#     asyncio.run(run_loop())
# 
# async def terminate_after_delay(lifter):
#     print('start terminate_after_delay...', end='')
#     await asyncio.sleep_ms(2000)
#     lifter.stop_loop()
#     print('done')

if __name__ == '__main__':
    from orbit import PWMServoMotor
    from time import sleep
    
    raw_angle_0 = 180.0
    angle_start = 0
    angle_end = 180
    time = 0.5
    angle_inc = 1.0
    
    servo = PWMServoMotor(pin=16,
                          raw_angle_0 = raw_angle_0,
                          angle_start = angle_start,
                          angle_end = angle_end,
                          angle_home = angle_start,
                          sign = -1)
    servo.home()
    
    lifter = Lifter(servo)
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('done')
    sleep(2)
    
#     print('Starting asynchronous mode...', end='')
#     asyncio.run(lifter.run_loop())
#     print('after')
#     sleep(1)
#     lifter.stop_loop()
#     print('done')

    # TODO: add async tests
    #
    
    print('off.')
    lifter.off()