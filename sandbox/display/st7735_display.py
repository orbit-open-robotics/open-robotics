from display_base import DisplayBase

class ST7735Display(DisplayBase):
    def __init__(self, spi, cs, dc, rst, width=128, height=160):
        super().__init__(spi, cs, dc, rst, width, height)
        self._init_sequence()

    def _init_sequence(self):
        raise NotImplementedError
        # ST7735-specific init commands