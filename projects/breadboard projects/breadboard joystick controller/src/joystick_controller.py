#
# Joystick Controller
#
from orbit import BLEServer
from machine import Pin, ADC
from orbit import Buzzer

class JoystickController:
    def __init__(self) -> None:
        self._buzzer = Buzzer(pin = 22)
        self._ble_led = Pin(6, Pin.OUT)
        self._ble_server = BLEServer(
            name='JoystickController',
            create_message_func = self.create_message,
            on_connected_func=self.connected,
            on_disconnected_func=self.disconnected,
            send_interval_ms=50) #50
        
        # Controls
        self._left_x = ADC(26)
        self._left_y = ADC(27)
        self._right_x = ADC(28)
        self._l_button = Pin(2, Pin.IN, Pin.PULL_UP)
        self._r_button = Pin(3, Pin.IN, Pin.PULL_UP)

        self._ble_led.off()

    def connected(self) -> None:
        """Callback function when a BLE connection is established."""
        print('CONNECTED')
        self._ble_led.on()
        self._buzzer.begin_sound()
        
    def disconnected(self) -> None:
        """Callback function when a BLE connection is disconnected."""
        print('DISCONNECTED')
        self._ble_led.off()
        self._buzzer.end_sound()
        
    def create_message(self) -> str:
        """Create a message to send to the connected BLE client."""
        left_x_value = self._left_x.read_u16() // 655
        left_y_value = self._left_y.read_u16() // 655
        right_x_value = self._right_x.read_u16() // 655
        right_y_value = 0
        
        message = f'{left_x_value},{left_y_value},{right_x_value},{right_y_value},{self._l_button.value()},{self._r_button.value()}'
        return message

    def start(self) -> None:
        self.__ble_serverserver.start()