from display_baes import DisplayBase

class ILI9341Display(DisplayBase):
    def __init__(self, spi, cs, dc, rst, width=240, height=320):
        super().__init__(spi, cs, dc, rst, width, height)
        self._init_sequence()

    def _init_sequence(self):
        raise NotImplementedError
        # ILI9341-specific init commands

