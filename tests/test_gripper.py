from orbit import Gripper
# from time import sleep
import uasyncio as asyncio

async def test_movement():
    await asyncio.sleep(1)
    
    print('start lifting...', end='')
    gripper.start_open()
    await asyncio.sleep(1)
    gripper.stop()
    print('done')
    
    await asyncio.sleep(1)
  
    print('start lowering...', end='')
    gripper.start_close()
    await asyncio.sleep(1)
    gripper.stop()
    print('done')
        
    await asyncio.sleep(1)
    gripper.stop_loop()


async def test_async():
    await asyncio.gather(
        gripper.run_loop(),
        test_movement()
        )
    
if __name__ == '__main__':
    from time import sleep
    
    # Create the gripper
    pin: int = 17,
    raw_angle_0: float = 0.0
    angle_start: float = 0.0
    angle_end: float = 65.0
    gripper = Gripper(pin, raw_angle_0, angle_start, angle_end)
        
    # Test variables
    time:float = 0.5
    angle_inc: float = 1.0

    print('Opening...', end='')
    gripper.open(time = time, angle_inc = angle_inc)
    print('open')
    sleep(2)
    print()
        
    print('Closing...', end='')
    gripper.close(time = time, angle_inc = angle_inc)
    print('closed')
    sleep(2)

    asyncio.run(test_async())

    print('off.')
    gripper.off()
