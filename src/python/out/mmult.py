from pynq import Overlay
import pynq
from pynq import allocate
import numpy as np

overlay = Overlay("./design_1_wrapper.bit")


class Mmult:

    def __init__(self, ip, size_a, size_b, size_c, data_type_a, data_type_b,
                 data_type_c):
        self.ip = ip

        self.AXILITES_ADDR_AP_CTRL = 0x00
        self.AXILITES_ADDR_GIE = 0x04
        self.AXILITES_ADDR_IER = 0x08
        self.AXILITES_ADDR_ISR = 0x0c

        self.AXILITES_ADDR_A_DATA = 0x10

        self.AXILITES_ADDR_B_DATA = 0x18

        self.AXILITES_ADDR_C_DATA = 0x20

        self.AXILITES_ADDR_A_ROW_DATA = 0x28

        self.AXILITES_ADDR_A_COL_DATA = 0x30

        self.AXILITES_ADDR_B_COL_DATA = 0x38

        self.buff_a = allocate(size_a, data_type_a)
        self.buff_a_addr = self.buff_a.device_address

        self.buff_b = allocate(size_b, data_type_b)
        self.buff_b_addr = self.buff_b.device_address

        self.buff_c = allocate(size_c, data_type_c)
        self.buff_c_addr = self.buff_c.device_address

    def prepare_a_buffer(self, data):
        self.buff_a[:] = data[:]
        self.buff_a.flush()

    def prepare_b_buffer(self, data):
        self.buff_b[:] = data[:]
        self.buff_b.flush()

    def prepare_c_buffer(self, data):
        self.buff_c[:] = data[:]
        self.buff_c.flush()

    def write_a_address(self):
        self.ip.write(self.AXILITES_ADDR_A_DATA, self.buff_a_addr)

    def write_b_address(self):
        self.ip.write(self.AXILITES_ADDR_B_DATA, self.buff_b_addr)

    def write_c_address(self):
        self.ip.write(self.AXILITES_ADDR_C_DATA, self.buff_c_addr)

    def write_a_row(self, data):
        self.ip.write(self.AXILITES_ADDR_A_ROW_DATA, data)

    def write_a_col(self, data):
        self.ip.write(self.AXILITES_ADDR_A_COL_DATA, data)

    def write_b_col(self, data):
        self.ip.write(self.AXILITES_ADDR_B_COL_DATA, data)

    def execute(self):
        self.ip.write(self.AXILITES_ADDR_AP_CTRL, 1)
        while self.ip.read(self.AXILITES_ADDR_AP_CTRL) & 0x4 != 0x4:
            pass

    def get_a_result(self):
        self.buff_a.invalidate()

    def get_b_result(self):
        self.buff_b.invalidate()

    def get_c_result(self):
        self.buff_c.invalidate()

    def reset_a_result(self):
        del self.buff_a

    def reset_b_result(self):
        del self.buff_b

    def reset_c_result(self):
        del self.buff_c

    def compute_all(self, data_a_row, data_a_col, data_b_col):

        self.write_a_row(data_a_row)

        self.write_a_col(data_a_col)

        self.write_b_col(data_b_col)

        self.execute()

        self.get_a_result()

        self.get_b_result()

        self.get_c_result()

        self.reset_a_result()

        self.reset_b_result()

        self.reset_c_result()

        return 0, self.buff_a, self.buff_b, self.buff_c
