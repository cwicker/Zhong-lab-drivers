import numpy as np
import pyqtgraph as pg
import time

from PyQt5.Qsci import QsciScintilla, QsciLexerPython

from spyre import Spyrelet, Task, Element
from spyre.widgets.task import TaskWidget
from spyre.plotting import LinePlotWidget
from spyre.widgets.rangespace import Rangespace
from spyre.widgets.param_widget import ParamWidget
from spyre.widgets.repository_widget import RepositoryWidget

from lantz import Q_

from lantz.drivers.keysight import Keysight_33622A
from lantz.drivers.tektronix import TDS2024C

class laser_calibration(Spyrelet):

    requires = {
        'fungen': Keysight_33622A,
        'osc': TDS2024C
    }

    @Task()
    def calibrate_amplitude(self, **kwargs):
        self.dataset.clear()
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        current = params['start']
        step = 0
        while current <= params['stop']:
            self.fungen.frequency[1] = current
            print('Changed to {}'.format(current))
            time.sleep(params['wait'])
            values = {
            'sweep_idx': [step],
            'x': self.fungen.voltage[chn],
            'y': self.osc.measure_mean(chn),
            }

            self.calibrate_amplitude.acquire(values)
            current += params['step']
            step += 1

    @calibrate_amplitude.initializer
    def initialize(self):
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        self.fungen.waveform[chn] = 'DC'
        self.fungen.output[chn] = 'ON'
        return

    @calibrate_amplitude.finalizer
    def finalize(self):
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        self.fungen.output[chn] = 'OFF'
        return

    @Task()
    def calibrate_frequency(self, **kwargs):
        self.dataset.clear()
        params = self.sweep_parameters.widget.get()
        current = params['start']
        step = 0
        while current <= params['stop']:
            self.fungen.frequency[1] = current
            print('Changed to {}'.format(current))
            time.sleep(params['wait'])
            values = {
            'sweep_idx': [step],
            'x': self.fungen.voltage[chn],
            'y': self.osc.measure_frequency(chn),
            }

            self.calibrate_frequency.acquire(values)
            current += params['step']
            step += 1

    @calibrate_frequency.initializer
    def initialize(self):
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        self.fungen.waveform[chn] = 'DC'
        self.fungen.output[chn] = 'ON'
        return

    @calibrate_frequency.finalizer
    def finalize(self):
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        self.fungen.output[chn] = 'OFF'
        return

    @Element(name='Sweep parameters')
    def sweep_parameters(self):
        params = [
        ('channel', {'type': dict, 'items': {'1': 1, '2': 2}}),
        ('start', {'type': float, 'default': 0, 'units':'V'}),
        ('stop', {'type': float, 'default': 5, 'units':'V'}),
        ('step', {'type': float, 'default': 1, 'units': 'V', 'positive': True}),
        ('wait', {'type': float, 'default': 1, 'nonnegative': True})
        ]
        w = ParamWidget(params)
        return w

    @Element(name='Calibration')
    def latest(self):
        p = LinePlotWidget()
        p.plot('Amplitude')
        p.plot('Frequency')
        return p

    @latest.on(calibrate_amplitude.acquired)
    def latest_update(self, ev):
        w = ev.widget
        data = self.data
        w.set('Amplitude', xs=data.x, ys=data.y)
        return

    @latest.on(calibrate_frequency.acquired)
    def latest_update(self, ev):
        w = ev.widget
        data = self.data
        w.set('Frequency', xs=data.x, ys=data.y)
        return
 
    @Element()
    def save(self):
        w = RepositoryWidget(self)
        return w