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

from arbseq import Arbseq_Class
from seqbuild import SeqBuild

from lantz.drivers.keysight import Keysight_33622A
from lantz.drivers.tektronix import TDS2024C

class Decay_Lifetime(Spyrelet):

    requires = {
        'fungen': Keysight_33622A,
        'osc': TDS2024C
    }

    def createpulses(step, totaltime=10050, voltage1=1000, voltage2=3630):

        chn1 = Arbseq_Class('chn1', 1)
        chn1.totaltime = totaltime
        chn1.widths = (50)
        chn1.delays = (0)
        chn1.heights = (voltage1)
        chn1.create_sequence()

        chn2 = Arbseq_Class('chn2', 2)
        chn2.totaltime = totaltime
        chn2.widths = (50, totaltime-50)
        chn2.delays = (0,0)
        chn2.heights = (voltage2, voltage2 + step)
        chn2.create_sequence()

        return chn1, chn2


    @Task()
    def startpulses(self):
        self.dataset.clear()
        start_time = time.time()
        params = self.pulse_parameters.widget.get()
        timer = params['timer']
        runtime = params['runtime']

        while timer == False or (time.time() - start_time < runtime*60):
            values = {
            'x': time.time() - start_time,
            'y': self.osc.measure_max(1) - self.osc.measure_min(1),
            }
            self.Sweep.acquire(values)

    @startpulses.initializer
    def initialize(self):
        params = self.pulse_parameters.widget.get()
        period = params['period']
        voltage1 = params['ch1 voltage']
        voltage2 = params['ch2 voltage']
        step = params['voltage step']

        ch1, ch2 = createpulses(step, period, voltage1, voltage2)

        self.fungen.send_arb(ch1,chn=1)
        self.fungen.send_arb(ch2,chn=2)
        self.fungen.output[1] = 'ON'
        self.fungen.output[2] = 'ON'
        return

    @startpulses.finalizer
    def finalize(self):
        self.fungen.output[1] = 'OFF'
        self.fungen.output[2] = 'OFF'
        return


    @Element(name='Pulse parameters')
    def pulse_parameters(self):
        params = [
        ('ch1 voltage', {'type': int, 'default': 1000, 'units':'mV'}),
        ('ch2 voltage', {'type': int, 'default': 1000, 'units':'mV'}),
        ('period', {'type': float, 'default': 100, 'units':'ms'}),
        ('voltage step', {'type': int, 'default': 1, 'units':'mV'}),
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