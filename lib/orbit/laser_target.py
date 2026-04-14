#
# LaserTarget
#
import uasyncio as asyncio
from orbit.robot_accessory import RobotAccessory
from orbit.buzzer import Buzzer
from machine import ADC, Pin

class LaserTarget(RobotAccessory):
    MAX_VALUE = 65_535
    CHECK_INTERVAL_MS = 100
    HIT_DURATION_MS = 2000

    class State:
        NOT_HIT = 0
        HIT = 1

    def __init__(self, 
                 pin: int = 26,
                 threshold: float = 0.4, 
                 buzzer_pin: int = 22,
                 state: State = State.NOT_HIT,
                 max_hits: int = 4,
                 hit_function = None,
                 max_hit_function = None) -> None:
        super().__init__()
        self._light = ADC(pin)
        self._buzzer: Buzzer = Buzzer(pin = buzzer_pin)
        self._baseline: int = 0 
        self._threshold = threshold
        self._state = state
        self._hit_function = hit_function
        self._max_hits = max_hits
        self._max_hit_function = max_hit_function
        self._hit_count: int = 0

    @property
    def hit_count(self) -> int:
        return self._hit_count

    def is_hit(self) -> bool:
        value: float = (self._light.read_u16() - self._baseline) / (self.MAX_VALUE - self._baseline)
        print(value)
        return value >= self._threshold 
    
    def reset(self) -> None:
        self._state = self.State.NOT_HIT

    def initialize(self) -> None:
        count: int = 5
        for _ in range(count):
            self._baseline += self._light.read_u16()
        self._baseline //= count
        print(f'baseline: {self._baseline}')

    def start(self)-> None:
        """Start waiting for laser hits."""
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        """Run the main loop to check for laser hits. """
        while True:
            if self._state == self.State.NOT_HIT and self.is_hit():
                self._hit_count += 1
                print(f'>>>>HIT {self._hit_count}')

                # Check if max hits reached
                if self._hit_count >= self._max_hits:
                    self._buzzer.beep(freq = 440, repeat = 3, duration = 0.1, delay = 0.1)
                    if self._max_hit_function:
                        self._max_hit_function()
                    await asyncio.sleep_ms(self.HIT_DURATION_MS)
                    return

                # React to hit
                else:
                    self._buzzer.beep(freq = 440)
                    self._state = self.State.HIT
                    if self._hit_function:
                        self._hit_function()
                    # Recover
                    await asyncio.sleep_ms(self.HIT_DURATION_MS)
                    self._state = self.State.NOT_HIT
               
            await asyncio.sleep_ms(self.CHECK_INTERVAL_MS)