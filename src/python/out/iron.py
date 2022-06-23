from pynq import Overlay
import pynq
from pynq import allocate
import numpy as np

overlay = Overlay("./design_1_wrapper.bit")


class Iron:

    def __init__(self, platform, ip, size_input_img, size_input_ref,
                 size_mutual_info, data_type_input_img, data_type_input_ref,
                 data_type_mutual_info):
        self.ip = ip
        self.platform = platform

        self.AXILITES_ADDR_AP_CTRL = 0x00
        self.AXILITES_ADDR_GIE = 0x04
        self.AXILITES_ADDR_IER = 0x08
        self.AXILITES_ADDR_ISR = 0x0c

        self.AXILITES_ADDR_INPUT_IMG_DATA = 0x10

        self.AXILITES_ADDR_INPUT_REF_DATA = 0x18

        self.AXILITES_ADDR_MUTUAL_INFO_DATA = 0x20

        self.buff_input_img = allocate(size_input_img, data_type_input_img)
        self.buff_input_img_addr = self.buff_input_img.device_address

        self.buff_input_ref = allocate(size_input_ref, data_type_input_ref)
        self.buff_input_ref_addr = self.buff_input_ref.device_address

        self.buff_mutual_info = allocate(size_mutual_info,
                                         data_type_mutual_info)
        self.buff_mutual_info_addr = self.buff_mutual_info.device_address

    def prepare_input_img_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_input_img[:] = data[:]
        self.buff_input_img.flush()

    def prepare_input_ref_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_input_ref[:] = data[:]
        self.buff_input_ref.flush()

    def prepare_mutual_info_buffer(self, data):
        if self.platform == 'Alveo':
            return
        self.buff_mutual_info[:] = data[:]
        self.buff_mutual_info.flush()

    def write_input_img_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_INPUT_IMG_DATA,
                      self.buff_input_img_addr)

    def write_input_ref_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_INPUT_REF_DATA,
                      self.buff_input_ref_addr)

    def write_mutual_info_address(self):
        if self.platform == 'Alveo':
            return
        self.ip.write(self.AXILITES_ADDR_MUTUAL_INFO_DATA,
                      self.buff_mutual_info_addr)

    def execute(self):
        if self.platform == 'Alveo':
            self.ip.call(self.buff_input_img, self.buff_input_ref,
                         self.buff_mutual_info)
        else:
            self.ip.write(self.AXILITES_ADDR_AP_CTRL, 1)
            while self.ip.read(self.AXILITES_ADDR_AP_CTRL) & 0x4 != 0x4:
                pass

    def get_input_img_result(self):
        self.buff_input_img.invalidate()
        return self.buff_input_img

    def get_input_ref_result(self):
        self.buff_input_ref.invalidate()
        return self.buff_input_ref

    def get_mutual_info_result(self):
        self.buff_mutual_info.invalidate()
        return self.buff_mutual_info

    def reset_input_img_result(self):
        del self.buff_input_img

    def reset_input_ref_result(self):
        del self.buff_input_ref

    def reset_mutual_info_result(self):
        del self.buff_mutual_info

    def compute_all(self, data_input_img, data_input_ref):

        self.prepare_input_img_buffer(data_input_img)

        self.prepare_input_ref_buffer(data_input_ref)

        self.write_input_img_address()

        self.write_input_ref_address()

        self.write_mutual_info_address()

        self.execute()

        self.get_mutual_info_result()

        return self.buff_mutual_info
