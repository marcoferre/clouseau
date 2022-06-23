from pynq import Overlay
import pynq
from pynq import allocate
import numpy as np

overlay = Overlay("./design_1_wrapper.bit")


class Clouseau:

    def __init__(self, overlay, ip, dma, size_in, size_out, data_type_in,
                 data_type_out, win_in, win_out):
        self.overlay = overlay
        self.ip = ip

        self.dma = dma

        self.size_in = size_in
        self.win_in = win_in
        self.buff_in = allocate(size_in + 2, data_type_in)

        self.buff_out = allocate(size_out - win_out + 1, data_type_out)

    def prepare_in_buffer(self, data):
        self.buff_in[0] = self.size_in
        self.buff_in[1:] = self.win_in
        self.buff_in[2:] = data[:]

    def send_buffer_in(self):
        self.dma.sendchannel.transfer(self.buff_in)
        self.dma.sendchannel.wait()

    def recv_buffer_out(self):
        self.dma.recvchannel.transfer(self.buff_out)
        self.dma.recvchannel.wait()
