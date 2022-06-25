from pynq import Overlay
import pynq
from pynq import allocate
import numpy as np

overlay = Overlay("./design_1_wrapper.bit")


class Fir_shift_register:

    def __init__(self, platform, ip, size_output_r, size_signal_r, size_coeff,
                 data_type_output_r, data_type_signal_r, data_type_coeff):
        self.ip = ip
        self.platform = platform

        self.AXILITES_ADDR_AP_CTRL = 0x00
        self.AXILITES_ADDR_GIE = 0x04
        self.AXILITES_ADDR_IER = 0x08
        self.AXILITES_ADDR_ISR = 0x0c

        self.AXILITES_ADDR_OUTPUT_R_DATA = 0x10

        self.AXILITES_ADDR_SIGNAL_R_DATA = 0x18

        self.AXILITES_ADDR_COEFF_DATA = 0x20

        self.AXILITES_ADDR_SIGNAL_LENGTH_DATA = 0x28

        self.buff_output_r = allocate(size_output_r, data_type_output_r)
        self.buff_output_r_addr = self.buff_output_r.device_address

        self.buff_signal_r = allocate(size_signal_r, data_type_signal_r)
        self.buff_signal_r_addr = self.buff_signal_r.device_address

        self.buff_coeff = allocate(size_coeff, data_type_coeff)
        self.buff_coeff_addr = self.buff_coeff.device_address

    def prepare_output_r_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_output_r[:] = data[:]
        self.buff_output_r.flush()

    def prepare_signal_r_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_signal_r[:] = data[:]
        self.buff_signal_r.flush()

    def prepare_coeff_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_coeff[:] = data[:]
        self.buff_coeff.flush()

    def write_output_r_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_OUTPUT_R_DATA,
                      self.buff_output_r_addr)

    def write_signal_r_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_SIGNAL_R_DATA,
                      self.buff_signal_r_addr)

    def write_coeff_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_COEFF_DATA, self.buff_coeff_addr)

    def write_signal_length(self, data):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_SIGNAL_LENGTH_DATA, data)

    def execute(self):
        if self.platform == 'Alveo':
            self.ip.call(self.buff_output_r, self.buff_signal_r,
                         self.buff_coeff)
        else:
            self.ip.write(self.AXILITES_ADDR_AP_CTRL, 1)
            while self.ip.read(self.AXILITES_ADDR_AP_CTRL) & 0x4 != 0x4:
                pass

    def get_output_r_result(self):
        self.buff_output_r.invalidate()
        return self.buff_output_r

    def get_signal_r_result(self):
        self.buff_signal_r.invalidate()
        return self.buff_signal_r

    def get_coeff_result(self):
        self.buff_coeff.invalidate()
        return self.buff_coeff

    def reset_output_r_result(self):
        del self.buff_output_r

    def reset_signal_r_result(self):
        del self.buff_signal_r

    def reset_coeff_result(self):
        del self.buff_coeff

    def compute_all(self, data_signal_r, data_coeff, data_signal_length):

        self.prepare_signal_r_buffer(data_signal_r)

        self.prepare_coeff_buffer(data_coeff)

        self.write_output_r_address()

        self.write_signal_r_address()

        self.write_coeff_address()

        self.write_signal_length(data_signal_length)

        self.execute()

        self.get_output_r_result()

        return self.buff_output_r
