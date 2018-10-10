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

from lantz.drivers.tektronix import TDS2024C

class Oscilloscope(Spyrelet):

     requires = {
        'osc': TDS2024C
    }

    @Task()
    def voltage(self):
        self.dataset.clear()
        params = self.params.widget.get()
        wait = params['wait']
        loop = params['loop']
        nrepeats = params['nrepeats']
        start = time.time()
        while loop:
            values = {
            'x': time.time()-start,
            'y': self.osc.measure_max(),
            }
            self.voltage.acquire(values)
            time.sleep(wait)

        start = time.time()
        for n in nrepeats:
            values = {
            'x': time.time()-start,
            'y': self.osc.measure_max(),
            }
            self.voltage.acquire(values)
            time.sleep(wait)

    @voltage.initializer
    def initialize(self):
        self.osc = TDS2024C('USB0::0x0699::0x03A6::C030873::INSTR')
        print('initialize')
        return

    @voltage.finalizer
    def finalize(self):
        print('finalize')
        return

    @Element(name='Sweep parameters')
    def sweep_parameters(self):
        params = [
        ('wait', {
        'type': int,
        'default': 60
        }),
        ('loop', {
        'type': bool
        }),
        ('nrepeats', {
        'type': int,
        'default': 10
        }),
        ]
        w = ParamWidget(params)
        return w

    @Element()
    def latest(self):
        p = LinePlotWidget(name='Voltage over time')
        p.plot('Voltage')
        return p

    @latest.on(voltage.acquired)
    def latest_update(self, ev):
        w = ev.widget
        latest_data = self.data
        w.set('Voltage', xs=latest_data.x, ys=latest_data.y)
        return
 
    @Element()
    def save(self):
        w = RepositoryWidget(self)
        return w


            
