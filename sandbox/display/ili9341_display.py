from time import sleep
from machine import Pin
from micropython import const


class ILI9341Display(DisplayBase):
    """ILI9341 driver, MicroPython-only, framebuffer-based."""

    # Command constants from ILI9341 datasheet
    SWRESET = const(0x01)
    SLPOUT = const(0x11)
    NORON = const(0x13)
    INVOFF = const(0x20)
    INVON = const(0x21)
    GAMMASET = const(0x26)
    DISPLAY_OFF = const(0x28)
    DISPLAY_ON = const(0x29)
    SET_COLUMN = const(0x2A)
    SET_PAGE = const(0x2B)
    WRITE_RAM = const(0x2C)
    MADCTL = const(0x36)
    VSCRSADD = const(0x37)
    PIXFMT = const(0x3A)
    FRMCTR1 = const(0xB1)
    DFUNCTR = const(0xB6)
    PWCTR1 = const(0xC0)
    PWCTR2 = const(0xC1)
    PWCTRA = const(0xCB)
    PWCTRB = const(0xCF)
    VMCTR1 = const(0xC5)
    VMCTR2 = const(0xC7)
    GMCTRP1 = const(0xE0)
    GMCTRN1 = const(0xE1)
    DTCA = const(0xE8)
    DTCB = const(0xEA)
    POSC = const(0xED)
    ENABLE3G = const(0xF2)
    PUMPRC = const(0xF7)

    MIRROR_ROTATE = {
        (False, 0): 0x80, (False, 90): 0xE0,
        (False, 180): 0x40, (False, 270): 0x20,
        (True, 0): 0xC0, (True, 90): 0x60,
        (True, 180): 0x00, (True, 270): 0xA0
    }

    def __init__(self, spi, cs, dc, rst, width=240, height=320,
                 rotation=0, mirror=False, bgr=True, gamma=True,
                 x_offset=0, y_offset=0):
        # cs, dc, rst are pin NUMBERS — this class constructs the Pin objects
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT, value=0)
        self.rst = Pin(rst, Pin.OUT, value=1)
        self.width = width
        self.height = height

        if (mirror, rotation) not in self.MIRROR_ROTATE:
            raise ValueError('Rotation must be 0, 90, 180 or 270.')
        self.rotation = self.MIRROR_ROTATE[mirror, rotation]
        if bgr:
            self.rotation |= 0b00001000

        self.offset = bool(x_offset or y_offset)
        self.x_offset = x_offset
        self.y_offset = y_offset

        # FrameBuffer setup
        self.buf = bytearray(width * height * 2)  # RGB565
        super(DisplayBase, self).__init__(self.buf, width, height, framebuf.RGB565)

        self._init_sequence(gamma)

    def write_cmd(self, command, *args):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if len(args) > 0:
            self.write_data(bytearray(args))

    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def _hard_reset(self):
        self.rst(0)
        sleep(.05)
        self.rst(1)
        sleep(.05)

    def _init_sequence(self, gamma=True):
        self._hard_reset()
        self.write_cmd(self.SWRESET)
        sleep(.1)
        self.write_cmd(self.PWCTRB, 0x00, 0xC1, 0x30)
        self.write_cmd(self.POSC, 0x64, 0x03, 0x12, 0x81)
        self.write_cmd(self.DTCA, 0x85, 0x00, 0x78)
        self.write_cmd(self.PWCTRA, 0x39, 0x2C, 0x00, 0x34, 0x02)
        self.write_cmd(self.PUMPRC, 0x20)
        self.write_cmd(self.DTCB, 0x00, 0x00)
        self.write_cmd(self.PWCTR1, 0x23)
        self.write_cmd(self.PWCTR2, 0x10)