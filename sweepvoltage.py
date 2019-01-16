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
import time

from lantz.drivers.keysight import Keysight_33622A
from lantz.drivers.tektronix import TDS2024C

class SweepVoltage(Spyrelet):
    
    requires = {
        'fungen': Keysight_33622A,
        'osc': TDS2024C
    }

    @Task()
    def Sweep(self):
        self.dataset.clear()
        start_time = time.time()
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        period = params['period']
        voltage = params['voltage']
        timer = params['timer']
        runtime = params['runtime']

        while timer == False or (time.time() - start_time < runtime*60):
            values = {
            'x': self.fungen.voltage[chn],
            'y': self.osc.measure_max(1) - self.osc.measure_min(1),
            }
            self.Sweep.acquire(values)


    @Sweep.initializer
    def initialize(self):
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        period = params['period']
        voltage = params['voltage']
        self.fungen.triangle(period, amplitude=voltage, chn=chn)
        self.fungen.output[chn] = 'ON'
        return

    @Sweep.finalizer
    def finalize(self):
        params = self.sweep_parameters.widget.get()
        chn = params['channel']
        self.fungen.output[chn] = 'OFF'
        return

    @Element(name='Sweep parameters')
    def sweep_parameters(self):
        params = [
        ('channel', {'type': dict, 'items': {'1': 1, '2': 2}}),
        ('period', {'type': float, 'default': 100e-6, 'units':'s'}),
        ('voltage', {'type': float, 'default': 1, 'units':'V'}),
        ('timer', {'type': bool}),
        ('runtime', {'type': int, 'default': 5, 'units': 'min'})
        ]
        w = ParamWidget(params)
        return w

    @Element(name='Oscilloscope Reading')
    def latest(self):
        p = LinePlotWidget()
        p.plot('Amplitude')
        return p

    @latest.on(Sweep.acquired)
    def latest_update(self, ev):
        w = ev.widget
        data = self.data
        w.set('Amplitude', xs=data.x, ys=data.y)
        return

    @Element()
    def save(self):
        w = RepositoryWidget(self)
        return w
