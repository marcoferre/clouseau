from pynq import Overlay
import pynq
from pynq import allocate

overlay = Overlay('myOverlay')

class Clouseau:
    def __init__(self, overlay, size_in, size_out, data_type_in, data_type_out, win_in, win_out):
        self.overlay = overlay
        self.AXILITES_ADDR_AP_CTRL = 0x00
        self.AXILITES_ADDR_GIE = 0x04
        self.AXILITES_ADDR_IER = 0x08
        self.AXILITES_ADDR_ISR = 0x0c

        

        
        self.size_in = size_in
        self.win_in = win_in
        self.buff_in = allocate(size_in + 2, data_type_in)
        self.buff_out = allocate(size_out - win_out + 1, data_type_out)



    

    
    def prepare_in_buffer(self, data):
        self.buff_in[0] = self.size_in
        self.buff_in[1:] = self.win_in
        self.buff_in[2:] = data[:]

    
        dma.sendchannel.transfer(self.buff_in)
        dma.sendchannel.wait()
        dma.recvchannel.transfer(self.buff_out)
        dma.recvchannel.wait()


    


    

    def compute(self):
        self.overlay.write(self.AXILITES_ADDR_AP_CTRL, 0)
        while self.overlay.read(self.AXILITES_ADDR_AP_CTRL) & 0x4 != 0x4:
            pass
    