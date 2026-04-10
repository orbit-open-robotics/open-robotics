from orbit import Tester


tester = Tester()
dt = DriveTrain()

tester.add("Forward", dt.forward, 100, 1)



'''
from time import sleep
from orbit import DriveTrain

    
# Test the DriveTrain class
if __name__ == "__main__":
    print('Testing DriveTrain class')
    # Create the DriveTrain object
    #dt = DriveTrain((1, 2), (3, 4))
    dt = DriveTrain()
    print(repr(dt))
    sleep(1)
    
    # Test the forward method
    print("Testing forward method")
    dt.forward(100, 1)
    dt.print_state()
    sleep(2)
    
    # Test the backward method
    print("Testing backward method")
    dt.backward(100, 1)
    dt.print_state()
    sleep(2)
    
    # Test the stop method
    print("Testing stop method")
    dt.forward(100)
    sleep(1)
    dt.stop()
    dt.print_state()
    sleep(2)
    
    # Test the move method
    print("Testing move method")
    dt.move(100, 100)
    dt.print_state()
    sleep(2)
    
    print("Testing stop method")
    dt.stop()
    dt.print_state()
    sleep(2)
    
    print("Test swerve left")
    dt.move(75, 100)
    dt.print_state()
    sleep(2)
    
    print("Test swerve right")
    dt.move(100, 75)
    dt.print_state()
    sleep(2)
    
    dt.stop()
    
    print("Test complete")
'''