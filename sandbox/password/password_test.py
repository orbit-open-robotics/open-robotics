from machine import Pin
from time import sleep

index = 0
password = [0, 1, 2]

# Create the buttons
buttons = []
buttons.append(Pin(15, Pin.IN, Pin.PULL_DOWN))

while True:
    sleep(0.1)
    
    # Loop over all buttons
    for i in range(len(buttons)):
        if buttons[i].value() == 1:
            
            # Correct guess
            if i == password[index]:
                index++
                if index >= len(password):
                    print('success!')
                    break
                
            # Incorrect: start over
            else:
                index = 0
        sleep(0.2)
                
