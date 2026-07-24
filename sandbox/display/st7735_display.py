import time

class ST7735Display(DisplayBase):
    # Command constants (identical protocol family to ILI9341)
    SWRESET = 0x01
    SLPOUT  = 0x11
    NORON   = 0x13
    INVOFF  = 0x20
    DISPON  = 0x29
    CASET   = 0x2A
    RASET   = 0x2B
    RAMWR   = 0x2C
    COLMOD  = 0x3A
    MADCTL  = 0x36
    FRMCTR1 = 0xB1
    FRMCTR2 = 0xB2
    FRMCTR3 = 0xB3
    INVCTR  = 0xB4
    PWCTR1  = 0xC0
    PWCTR2  = 0xC1
    PWCTR3  = 0xC2
    PWCTR4  = 0xC3
    PWCTR5  = 0xC4
    VMCTR1  = 0xC5
    GMCTRP1 = 0xE0
    GMCTRN1 = 0xE1

    def __init__(self, spi, cs, dc, rst, width=128, height=160):
        # Note: reusing DisplayBase's __init__ for buffer/FrameBuffer setup,
        # but this chip's pins need PULL_DOWN mode specifically.
        self.spi = spi
        self.cs = machine.Pin(cs, machine.Pin.OUT, machine.Pin.PULL_DOWN)
        self.dc = machine.Pin(dc, machine.Pin.OUT, machine.Pin.PULL_DOWN)
        self.rst = machine.Pin(rst, machine.Pin.OUT, machine.Pin.PULL_DOWN)
        self.cs(1)

        self.width, self.height = width, height
        self.buf = bytearray(width * height * 2)  # RGB565
        super(DisplayBase, self).__init__(self.buf, width, height, framebuf.RGB565)

        self._init_sequence()

    def write_cmd(self, cmd, *args):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
        if args:
            self.write_data(bytearray(args))

    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def _hard_reset(self):
        self.dc(0)
        self.rst(1)
        time.sleep_us(500)
        self.rst(0)
        time.sleep_us(500)
        self.rst(1)
        time.sleep_us(500)

    def _init_sequence(self):
        '''Initialize a red-tab ST7735 (128x160). Swap for blue/green tab if needed.'''
        self._hard_reset()

        self.write_cmd(self.SWRESET)
        time.sleep_us(150)
        self.write_cmd(self.SLPOUT)
        time.sleep_us(500)

        self.write_cmd(self.FRMCTR1)
        self.write_data(bytearray([0x01, 0x2C, 0x2D]))
        self.write_cmd(self.FRMCTR2)
        self.write_data(bytearray([0x01, 0x2C, 0x2D]))
        self.write_cmd(self.FRMCTR3)
        self.write_data(bytearray([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D]))
        time.sleep_us(10)

        self.write_cmd(self.INVCTR)
        self.write_data(bytearray([0x07]))

        self.write_cmd(self.PWCTR1)
        self.write_data(bytearray([0xA2, 0x02, 0x84]))
        self.write_cmd(self.PWCTR2)
        self.write_data(bytearray([0xC5]))
        self.write_cmd(self.PWCTR3)
        self.write_data(bytearray([0x0A, 0x00]))
        self.write_cmd(self.PWCTR4)
        self.write_data(bytearray([0x8A, 0x2A]))
        self.write_cmd(self.PWCTR5)
        self.write_data(bytearray([0x8A, 0xEE]))
        self.write_cmd(self.VMCTR1)
        self.write_data(bytearray([0x0E]))

        self.write_cmd(self.INVOFF)

        self.write_cmd(self.MADCTL)
        self.write_data(bytearray([0xC8]))

        self.write_cmd(self.COLMOD)
        self.write_data(bytearray([0x05]))

        self.write_cmd(self.CASET)
        self.write_data(bytearray([0x00, 0x00, 0x00, self.width - 1]))
        self.write_cmd(self.RASET)
        self.write_data(bytearray([0x00, 0x00, 0x00, self.height - 1]))

        self.write_cmd(self.GMCTRP1)
        self.write_data(bytearray([0x0f, 0x1a, 0x0f, 0x18, 0x2f, 0x28, 0x20, 0x22,
                                    0x1f, 0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10]))
        self.write_cmd(self.GMCTRN1)
        self.write_data(bytearray([0x0f, 0x1b, 0x0f, 0x17, 0x33, 0x2c, 0x29, 0x2e,
                                    0x30, 0x30, 0x39, 0x3f, 0x00, 0x07, 0x03, 0x10]))
        time.sleep_us(10)

        self.write_cmd(self.DISPON)
        time.sleep_us(100)
        self.write_cmd(self.NORON)
        time.sleep_us(10)

        self.cs(1)

    def block(self, x0, y0, x1, y1, data):
        self.write_cmd(self.CASET)
        self.write_data(bytearray([x0 >> 8, x0 & 0xff, x1 >> 8, x1 & 0xff]))
        self.write_cmd(self.RASET)
        self.write_data(bytearray([y0 >> 8, y0 & 0xff, y1 >> 8, y1 & 0xff]))
        self.write_cmd(self.RAMWR)
        self.write_data(data)

    def show(self):
        self.block(0, 0, self.width - 1, self.height - 1, self.buf)