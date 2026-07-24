from framebuf import FrameBuffer

class DisplayBase(FrameBuffer):
    """Shared logic: buffer setup, show(), generic block-based blit."""
    def __init__(self, spi, cs, dc, rst, width, height):
        # TODO: default values
        self.spi, self.cs, self.dc, self.rst = spi, cs, dc, rst
        self.width, self.height = width, height
        self.buf = bytearray(width * height * 2)  # RGB565
        super().__init__(self.buf, width, height, framebuf.RGB565)
        self._hard_reset()

    def write_cmd(self, cmd, *args):
        raise NotImplementedError("This feature is not implemented yet.")
        # shared low-level SPI command write (or override in subclass)

    def write_data(self, data):
        raise NotImplementedError("This feature is not implemented yet.")
        # shared low-level SPI data write (or override in subclass)

    def block(self, x0, y0, x1, y1, data):
        raise NotImplementedError("This feature is not implemented yet.")
        # shared — same command structure on both chips (SET_COLUMN/SET_PAGE/WRITE_RAM)

    def show(self):
        self.block(0, 0, self.width - 1, self.height - 1, self.buf)

    def _hard_reset(self):
        raise NotImplementedError("This feature is not implemented yet.")
        # shared reset pin toggling

    def _init_sequence(self):
        raise NotImplementedError  # each chip must supply its own command list