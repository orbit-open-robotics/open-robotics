from orbit import Lifter
import uasyncio as asyncio

async def test_movement():
    await asyncio.sleep(1)
    
    print('start lifting...', end='')
    lifter.start_lift()
    await asyncio.sleep(1)
    lifter.stop()
    print('done')
    
    await asyncio.sleep(1)
  
    print('start lowering...', end='')
    lifter.start_lower()
    await asyncio.sleep(1)
    lifter.stop()
    print('done')
        
    await asyncio.sleep(1)
    lifter.stop_loop()


async def test_async():
    await asyncio.gather(
        lifter.run_loop(),
        test_movement()
        )

if __name__ == '__main__':
    from time import sleep

    # Create the lifter
    raw_angle_0 = 180.0
    angle_start = 0
    angle_end = 180

    lifter = Lifter(pin=16,
                    raw_angle_0 = raw_angle_0,
                    angle_start = angle_start,
                    angle_end = angle_end)
    
    # Test parameters
    time = 0.5
    angle_inc = 1.0
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('lift done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('lower done')
    sleep(2)
    
    print('lift...', end='')
    lifter.lift(time = time, angle_inc = angle_inc)
    print('lift done')
    sleep(2)
    
    print('lower...', end='')
    lifter.lower(time = time, angle_inc = angle_inc)
    print('lower done')
    sleep(2)
    
    asyncio.run(test_async())
    
    print('off.')
    lifter.off()