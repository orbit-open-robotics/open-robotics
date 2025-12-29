from orbit import PWMServoMotor
from orbit import Tester
from time import sleep
import uasyncio as asyncio

class PWMServoMotorTester(Tester):
    def __init__(self, pin=10):
        super().__init__()
        self.servo = PWMServoMotor(pin=pin)
        self.add('accessors', self.test_accessors)
        self.add('angle accessors', self.test_angle_accessors)
        self.add('set_angle', self.test_set_angle)
        self.add('move_to_angle', self.test_move_to_angle)
        self.add('move_by', self.test_move_by)
        self.add('home', self.test_home)
        self.add('move_to_start', self.test_move_to_start)
        self.add('move_to_end', self.test_move_to_end)
        self.add('run_loop', self.test_run_loop)
        self.initialize_servo()
        
    def initialize_servo(self):
        self.servo.set_angle(90)
        sleep(1)
        self.servo.off()
        
    def test_accessors(self):
        print(f'name: {self.servo.name}')
        print(f'pin: {self.servo.pin}')
        print(f'angle_start: {self.servo.angle_start}')
        print(f'angle_end: {self.servo.angle_end}')
        print(f'angle_home: {self.servo.angle_home}')
        
    def test_angle_accessors(self):
        print(f'angle = {self.servo.angle}')
        print(f'raw angle = {self.servo.raw_angle}')
        
    def test_set_angle(self):
        self.servo.set_angle(0)
        sleep(2)
        self.servo.set_angle(180)
        sleep(2)
        self.servo.set_angle(90)
        sleep(2)
        self.servo.off()
        
    def test_move_to_angle(self):
        self.servo.move_to_angle(0, 1)
        sleep(2)
        self.servo.move_to_angle(180, 1)
        sleep(2)
        self.servo.move_to_angle(90, 1)
        sleep(2)
        self.servo.off()
        
    def test_move_by(self):
        self.servo.move_to_angle(0)
        sleep(1)
        for _ in range(10):
            self.servo.move_by(10)
            sleep(0.5)
        self.servo.move_to_angle(90)
        sleep(1)
        self.servo.off()
        
    def test_home(self):
        self.servo.home()
        sleep(2)
        self.servo.off()
        
    def test_move_to_start(self):
        self.servo.move_to_start()
        sleep(2)
        self.servo.off()
        
    def test_move_to_end(self):
        self.servo.move_to_end()
        sleep(2)
        self.servo.off()
        
    def test_run_loop(self)-> None:
        asyncio.run(self.async_test_run_loop())
        
    async def run_loop_helper(self):
        await asyncio.sleep_ms(500)
        
        self.servo.start_increasing()
        await asyncio.sleep_ms(500)
        
        self.servo.stop()
        await asyncio.sleep_ms(1000)
        
        self.servo.start_decreasing()
        await asyncio.sleep_ms(500)
        
        self.servo.terminate()
        self.servo.off()
        
    async def async_test_run_loop(self):
        await asyncio.gather(self.servo.run_loop(),
                             self.run_loop_helper())
        

tester = PWMServoMotorTester()
tester.run_tests()



