from pynq import Overlay
import pynq
from pynq import allocate
import numpy as np

overlay = Overlay("./design_1_wrapper.bit")


class Vadd:

    def __init__(self, ip, size_in1, size_in2, size_out, data_type_in1,
                 data_type_in2, data_type_out):
        self.ip = ip

        self.AXILITES_ADDR_AP_CTRL = 0x00
        self.AXILITES_ADDR_GIE = 0x04
        self.AXILITES_ADDR_IER = 0x08
        self.AXILITES_ADDR_ISR = 0x0c

        self.AXILITES_ADDR_IN1_DATA = 0x10

        self.AXILITES_ADDR_IN2_DATA = 0x18

        self.AXILITES_ADDR_OUT_DATA = 0x20

        self.AXILITES_ADDR_SIZE_DATA = 0x28

        self.buff_in1 = allocate(size_in1, data_type_in1)
        self.buff_in1_addr = self.buff_in1.device_address

        self.buff_in2 = allocate(size_in2, data_type_in2)
        self.buff_in2_addr = self.buff_in2.device_address

        self.buff_out = allocate(size_out, data_type_out)
        self.buff_out_addr = self.buff_out.device_address

    def prepare_in1_buffer(self, data):
        self.buff_in1[:] = data[:]
        self.buff_in1.flush()

    def prepare_in2_buffer(self, data):
        self.buff_in2[:] = data[:]
        self.buff_in2.flush()

    def prepare_out_buffer(self, data):
        self.buff_out[:] = data[:]
        self.buff_out.flush()

    def write_in1_address(self):
        self.ip.write(self.AXILITES_ADDR_IN1_DATA, self.buff_in1_addr)

    def write_in2_address(self):
        self.ip.write(self.AXILITES_ADDR_IN2_DATA, self.buff_in2_addr)

    def write_out_address(self):
        self.ip.write(self.AXILITES_ADDR_OUT_DATA, self.buff_out_addr)

    def write_size(self, data):
        self.ip.write(self.AXILITES_ADDR_SIZE_DATA, data)

    def execute(self):
        self.ip.write(self.AXILITES_ADDR_AP_CTRL, 1)
        while self.ip.read(self.AXILITES_ADDR_AP_CTRL) & 0x4 != 0x4:
            pass

    def get_in1_result(self):
        self.buff_in1.invalidate()
        return self.buff_in1

    def get_in2_result(self):
        self.buff_in2.invalidate()
        return self.buff_in2

    def get_out_result(self):
        self.buff_out.invalidate()
        return self.buff_out

    def reset_in1_result(self):
        del self.buff_in1

    def reset_in2_result(self):
        del self.buff_in2

    def reset_out_result(self):
        del self.buff_out

    def compute_all(self, data_in1, data_in2, data_size):

        self.prepare_in1_buffer(data_in1)

        self.prepare_in2_buffer(data_in2)

        self.write_in1_address()

        self.write_in2_address()

        self.write_out_address()

        self.write_size(data_size)

        self.execute()

        self.get_out_result()

        return 0, self.buff_out
