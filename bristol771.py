from lantz.foreign import LibraryDriver
from lantz import Feat, DictFeat, Action, Q_

import time
from ctypes import *

class tsDeviceIPInfo(Structure):
    __fields__ = [('u_ipaddr', c_uint), ('s_ipaddr', c_wchar_p), ('port', c_uint), ('snum', c_uint), ('model', c_wchar_p)]


class Bristol_771(LibraryDriver):

    LIBRARY_NAME = 'libbristol.dll'
    LIBRARY_PREFIX = 'CL'

    def __init__(self, serialnum):
        super().__init__()

        create_inst = self.lib.CreateInstance
        create_inst.restype = c_void_p
        handle = create_inst()

        snum = c_uint(serialnum)
        model = create_string_buffer(20)
        maxlen = c_int(20)

        err = self.lib.OpenDevice(handle, snum, model, maxlen)
        if err != 0:
            raise Exception('Instrument not loaded')
        else:
            print('Instrument loaded: ' + str(model.value).strip('b'))

        self.device = handle

        #Function definitions
        self.lib.GetMeasWLen.argtypes = [c_void_p, POINTER(c_float)]
        self.lib.GetMeasIPwr.argtypes = [c_void_p, POINTER(c_float)]
        self.lib.GetMeasPres.argtypes = [c_void_p, POINTER(c_float)]
        self.lib.GetMeasTemp.argtypes = [c_void_p, POINTER(c_float)]
        return

    def check_error(self, ret):
        if ret != 0:
            raise Exception('Measurement failed')
        return

    def measure_wavelength(self):
        ret_val = c_float()
        self.check_error(self.lib.GetMeasWLen(self.device, pointer(ret_val)))
        return ret_val.value

    def measure_power(self):
        ret_val = c_float()
        self.check_error(self.lib.GetMeasIPwr(self.device, pointer(ret_val)))
        return ret_val.value

    def measure_pressure(self):
        ret_val = c_float()
        self.check_error(self.lib.GetMeasPres(self.device, pointer(ret_val)))
        return ret_val.value

    def measure_temperature(self):
        ret_val = c_float()
        self.check_error(self.lib.GetMeasTemp(self.device, pointer(ret_val)))
        return ret_val.value


if __name__ == '__main__':
    from time import sleep
    from lantz import Q_
    from lantz.log import log_to_screen, DEBUG

    log_to_screen(DEBUG)

    inst = Bristol_771(6535)




