from lantz.foreign import LibraryDriver
from lantz import Feat, DictFeat, Action, Q_

import time
from ctypes import *

class Bristol_771(LibraryDriver):

	LIBRARY_NAME = 'libbristol.dll'
    LIBRARY_PREFIX = 'CL'

    def __init__(self, serialnum):
    	super().__init_()

    	handle = c_void_p()
    	handle = self.lib.CreateInstance()
    	snum = c_uint(serialnum)
    	model = c_wchar_p()
    	maxlen = c_int(20)

    	model_no = self.lib.OpenDevice(handle, snum, model, maxlen)
    	print('model: ' + model.value)

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




