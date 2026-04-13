from orbit import Tester, DriveTrain
from time import sleep

def test_forward(dt: DriveTrain) -> None:
    print('forward for 1 second...', end='')
    dt.forward(100, 1)
    print('done.')
    print(repr(dt))
    
def test_backward(dt: DriveTrain) -> None:
    print('Testing backward method...', end='')
    dt.backward(100, 1)
    dt.print_state()
    sleep(2)
    print('done.')
    
def test_stop(dt: DriveTrain) -> None:
    print('Testing stop method...', end='')
    dt.forward(100)
    sleep(1)
    dt.stop()
    dt.print_state()
    sleep(2)
    print('done.')
    
def test_move(dt: DriveTrain) -> None:
    print('Testing move method...', end='')
    dt.move(100, 100)
    dt.print_state()
    sleep(2)
    print('done.')
    
def test_swerve_left(dt: DriveTrain) -> None:
    print('Test swerve left..', end='')
    dt.move(75, 100)
    dt.print_state()
    sleep(2)
    print('done.')
    
def test_swerve_right(dt: DriveTrain) -> None:
    print('Test swerve right..', end='')
    dt.move(100, 75)
    dt.print_state()
    sleep(2)
    print('done.')
    
    

tester = Tester()
dt = DriveTrain()

tester.add("forward", test_forward, dt)
tester.add("backward", test_backward, dt)
tester.add("stop", test_stop, dt)
tester.add("move", test_move, dt)
tester.add("swerve left", test_swerve_left, dt)
tester.add("swerve right", test_swerve_right, dt)
tester.run_tests()

