from pynq import Overlay
import pynq
from pynq import allocate
import numpy as np

overlay = Overlay("./design_1_wrapper.bit")


class Clouseau:

    def __init__(self, overlay, ip):
        self.overlay = overlay
        self.ip = ip

        self.AXILITES_ADDR_AP_CTRL = 0x00
        self.AXILITES_ADDR_GIE = 0x04
        self.AXILITES_ADDR_IER = 0x08
        self.AXILITES_ADDR_ISR = 0x0c

        self.AXILITES_ADDR_A_DATA = 0x10

        self.AXILITES_ADDR_B_DATA = 0x18

        self.AXILITES_ADDR_C_DATA = 0x20

    def write_a(self, data):
        self.ip.write(self.AXILITES_ADDR_A_DATA, data)

    def write_b(self, data):
        self.ip.write(self.AXILITES_ADDR_B_DATA, data)

    def write_c(self, data):
        self.ip.write(self.AXILITES_ADDR_C_DATA, data)

    def compute(self):
        self.ip.write(self.AXILITES_ADDR_AP_CTRL, 1)
        while self.ip.read(self.AXILITES_ADDR_AP_CTRL) & 0x4 != 0x4:
            pass
