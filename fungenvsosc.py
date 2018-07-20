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

class FungenVsOsc(Spyrelet):

    requires = {
        'fungen': Keysight_33622A,
        'osc': TDS2024C
    }

    @Task(name='sweep')
    def sweep(self, **kwargs):
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
            'x': self.osc.measure_frequency(1),
            'y': self.osc.measure_mean(1),
            }

            self.sweep.acquire(values)
            current += params['step']
            step += 1

    @sweep.initializer
    def initialize(self):
        params = self.sweep_parameters.widget.get()
        self.fungen.voltage[1] = params['voltage']
        self.fungen.output[1] = 'ON'
        return

    @sweep.finalizer
    def finalize(self):
        self.fungen.output[1] = 'OFF'
        return

    @Element(name='Sweep parameters')
    def sweep_parameters(self):
        params = [
        ('start', {
        'type': float,
        'default': 1,
        'units':'Hz',
        }),
        ('stop', {
        'type': float,
        'default': 20,
        'units':'Hz',
        }),
        ('voltage', {
        'type': float,
        'default': 5,
        'units': 'V',
        }),
        ('step', {
        'type': float,
        'default': 1,
        'units': 'Hz',
        'positive': True,
        }),
        ('wait', {
        'type': float,
        'default': 1,
        'nonnegative': True,
        }),
        ]
        w = ParamWidget(params)
        return w

    @Element(name='Latest frequency vs voltage')
    def latest(self):
        p = LinePlotWidget()
        p.plot('Channel 1')
        return p

    @latest.on(sweep.acquired)
    def latest_update(self, ev):
        w = ev.widget
        latest_data = self.data
        w.set('Channel 1', xs=latest_data.x, ys=latest_data.y)
        return
 
    @Element()
    def save(self):
        w = RepositoryWidget(self)
        return w
