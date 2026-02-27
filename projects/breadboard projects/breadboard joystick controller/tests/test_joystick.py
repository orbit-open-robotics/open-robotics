#
# test_joystick 
#
from machine import Pin, ADC
from time import sleep


# Joystick x, y, and button
left_x = ADC(26)
left_y = ADC(27)
right_x = ADC(28)
l_button = Pin(2, Pin.IN, Pin.PULL_UP)
r_button = Pin(3, Pin.IN, Pin.PULL_UP)

    
def create_message():
    """Create a message to send to the connected BLE client."""
    left_x_value = left_x.read_u16()
    left_y_value = left_y.read_u16()
    right_x_value = right_x.read_u16()
    right_y_value = 0
    
    message = f'{left_x_value},{left_y_value},{right_x_value},{right_y_value},{l_button.value()},{r_button.value()}'
    return message


while True:
    print(create_message())
    sleep(0.1)
