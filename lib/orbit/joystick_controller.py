#
# Joystick Controller
# This is the breadboard version
#
from orbit.ble_server import BLEServer
from orbit.buzzer import Buzzer
from machine import Pin, ADC

# Values imported by clients
JOYSTICK_MIN = -10
JOYSTICK_MAX = 10
THRESHOLD = 2

class JoystickController:
    SIGNAL_MAX = 65_535
    SIGNAL_MIN = 0

    def __init__(
        self,
        name: str = 'JoystickController',
        buzzer_pin: int = 22,
        ble_led_pin: int = 6,
        left_x_pin: int = 26,
        left_y_pin: int = 27,
        right_x_pin: int = 28,
        l_button_pin: int = 2,
        r_button_pin: int = 3,
        send_interval_ms = 50
        ) -> None:
        self._buzzer: Buzzer = Buzzer(pin = buzzer_pin)
        self._ble_led: Pin = Pin(ble_led_pin, Pin.OUT)
        self._ble_server: BLEServer = BLEServer(
            name = name,
            create_message_func = self._create_message,
            on_connected_func = self._connected,
            on_disconnected_func = self._disconnected,
            send_interval_ms = send_interval_ms) #50
        
        # Controls
        self._left_x = ADC(left_x_pin)
        self._left_y = ADC(left_y_pin)
        self._right_x = ADC(right_x_pin)
        self._l_button = Pin(l_button_pin, Pin.IN, Pin.PULL_UP)
        self._r_button = Pin(r_button_pin, Pin.IN, Pin.PULL_UP)

        self._ble_led.off()

    def _connected(self) -> None:
        """Callback function when a BLE connection is established."""
        print('CONNECTED')
        self._ble_led.on()
        self._buzzer.begin_sound()
        
    def _disconnected(self) -> None:
        """Callback function when a BLE connection is disconnected."""
        print('DISCONNECTED')
        self._ble_led.off()
        self._buzzer.end_sound()
        
    def _create_message(self) -> str:
        """Create a message to send to the connected BLE client."""
        lx = self._signal_to_value(self._left_x.read_u16())
        ly = self._signal_to_value(self._left_y.read_u16())
        rx = self._signal_to_value(self._right_x.read_u16())
        ry = 0
        lb = self._l_button.value()
        rb = self._r_button.value()
        
        message = f'{lx},{ly},{rx},{ry},{lb},{rb}'
        return message
    
    def _signal_to_value(self, signal: int) -> int:
        """Convert a signal [0-65,535] to the value to be transmitted"""
        signal_range = JoystickController.SIGNAL_MAX - JoystickController.SIGNAL_MIN
        slope = (JOYSTICK_MAX-JOYSTICK_MIN)/signal_range
        value = JOYSTICK_MIN + slope * (signal - JoystickController.SIGNAL_MIN)
        value = 0 if abs(value) < THRESHOLD else value
        return int(value)

    def start(self) -> None:
        """Start transmitting the joystick values"""
        self._ble_server.start()