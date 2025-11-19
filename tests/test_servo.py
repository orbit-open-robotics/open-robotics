#
# servo_test
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
#
from servo import Servo
from time import sleep


while True:
    # Parse command
    answer: str = input('Input servo pin number and optionally list of angles: ')
    values = answer.strip().split(" ")
    values = [val.strip() for val in values]
    
    # Create servo 
    if not values[0].isdigit():
        print(f'{values[0]} is not a valid pin number')
        continue
    s = Servo(pin_id = int(values[0]))
    
    # Default angle values
    if len(values) < 2:
        s.write(0)
        sleep(1)
        s.write(180)
        sleep(1)
        s.write(90)
        s.off()
        continue
    
    for ang in values[1:]:
        if not ang.isdigit():
            print(f'{ang} is not a valid angle')
            continue
        s.write(int(ang))
        sleep(1)
    s.off()

    
print('Test concluded.')