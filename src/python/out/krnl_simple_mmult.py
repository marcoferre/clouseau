from pynq import Overlay
import pynq
from pynq import allocate
import numpy as np

overlay = Overlay("./design_1_wrapper.bit")


class Krnl_simple_mmult:

    def __init__(self, platform, ip, size_a, size_b, size_c, size_d,
                 size_output, data_type_a, data_type_b, data_type_c,
                 data_type_d, data_type_output):
        self.ip = ip
        self.platform = platform

        self.AXILITES_ADDR_AP_CTRL = 0x00
        self.AXILITES_ADDR_GIE = 0x04
        self.AXILITES_ADDR_IER = 0x08
        self.AXILITES_ADDR_ISR = 0x0c

        self.AXILITES_ADDR_A_DATA = 0x10

        self.AXILITES_ADDR_B_DATA = 0x18

        self.AXILITES_ADDR_C_DATA = 0x20

        self.AXILITES_ADDR_D_DATA = 0x28

        self.AXILITES_ADDR_OUTPUT_DATA = 0x30

        self.AXILITES_ADDR_DIM_DATA = 0x38

        self.buff_a = allocate(size_a, data_type_a)
        self.buff_a_addr = self.buff_a.device_address

        self.buff_b = allocate(size_b, data_type_b)
        self.buff_b_addr = self.buff_b.device_address

        self.buff_c = allocate(size_c, data_type_c)
        self.buff_c_addr = self.buff_c.device_address

        self.buff_d = allocate(size_d, data_type_d)
        self.buff_d_addr = self.buff_d.device_address

        self.buff_output = allocate(size_output, data_type_output)
        self.buff_output_addr = self.buff_output.device_address

    def prepare_a_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_a[:] = data[:]
        self.buff_a.flush()

    def prepare_b_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_b[:] = data[:]
        self.buff_b.flush()

    def prepare_c_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_c[:] = data[:]
        self.buff_c.flush()

    def prepare_d_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_d[:] = data[:]
        self.buff_d.flush()

    def prepare_output_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_output[:] = data[:]
        self.buff_output.flush()

    def write_a_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_A_DATA, self.buff_a_addr)

    def write_b_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_B_DATA, self.buff_b_addr)

    def write_c_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_C_DATA, self.buff_c_addr)

    def write_d_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_D_DATA, self.buff_d_addr)

    def write_output_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_OUTPUT_DATA, self.buff_output_addr)

    def write_dim(self, data):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_DIM_DATA, data)

    def execute(self):
        if self.platform == 'Alveo':
            self.ip.call(self.buff_a, self.buff_b, self.buff_c, self.buff_d,
                         self.buff_output)
        else:
            self.ip.write(self.AXILITES_ADDR_AP_CTRL, 1)
            while self.ip.read(self.AXILITES_ADDR_AP_CTRL) & 0x4 != 0x4:
                pass

    def get_a_result(self):
        self.buff_a.invalidate()
        return self.buff_a

    def get_b_result(self):
        self.buff_b.invalidate()
        return self.buff_b

    def get_c_result(self):
        self.buff_c.invalidate()
        return self.buff_c

    def get_d_result(self):
        self.buff_d.invalidate()
        return self.buff_d

    def get_output_result(self):
        self.buff_output.invalidate()
        return self.buff_output

    def reset_a_result(self):
        del self.buff_a

    def reset_b_result(self):
        del self.buff_b

    def reset_c_result(self):
        del self.buff_c

    def reset_d_result(self):
        del self.buff_d

    def reset_output_result(self):
        del self.buff_output

    def compute_all(self, data_a, data_b, data_c, data_d, data_dim):

        self.prepare_a_buffer(data_a)

        self.prepare_b_buffer(data_b)

        self.prepare_c_buffer(data_c)

        self.prepare_d_buffer(data_d)

        self.write_a_address()

        self.write_b_address()

        self.write_c_address()

        self.write_d_address()

        self.write_output_address()

        self.write_dim(data_dim)

        self.execute()

        self.get_output_result()

        return self.buff_output
