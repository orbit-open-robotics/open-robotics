from orbit import PWMServoMotor, Gripper
from time import sleep
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
    
#raw_angle_0 = 115.0
raw_angle_0 = -5.0
angle_start = 0.0
angle_end = 65.0
time = 0.5
angle_inc = 1.0
    
servo = PWMServoMotor(pin=17,
                        raw_angle_0 = raw_angle_0,
                        angle_start = angle_start,
                        angle_end = angle_end,
                        angle_home = angle_start)
servo.home()
    
gripper = Gripper(servo)
    
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