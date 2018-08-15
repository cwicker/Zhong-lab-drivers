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

from lantz.drivers.bristol import Bristol_771

class Spectrometer(Spyrelet):

     requires = {
        'spectrometer': Bristol_771,
    }

    @Task()
    def wavelength(self):
        self.dataset.clear()
        params = self.params.widget.get()
        wait = params['wait']
        loop = params['loop']
        nrepeats = params['nrepeats']
        start = time.time()
        while loop:
            values = {
            'x': time.time()-start,
            'y': self.spectrometer.measure_wavelength(),
            }
            self.measure.acquire(values)
            time.sleep(wait)

        start = time.time()
        for n in nrepeats:
            values = {
            'x': time.time()-start,
            'y': self.spectrometer.measure_wavelength(),
            }
            self.wavelength.acquire(values)
            time.sleep(wait)

    @wavelength.initializer
    def initialize(self):
        self.spectrometer = Bristol_771(6535)
        self.spectrometer.start_data(1, 10000)
        print('initialize')
        return

    @wavelength.finalizer
    def finalize(self):
        inst.stop_data()
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
        p = LinePlotWidget(name='wavelength over time')
        p.plot('Wavelength')
        return p

    @latest.on(wavelength.acquired)
    def latest_update(self, ev):
        w = ev.widget
        latest_data = self.data
        w.set('Wavelength', xs=latest_data.x, ys=latest_data.y)
        return
 
    @Element()
    def save(self):
        w = RepositoryWidget(self)
        return w


            
