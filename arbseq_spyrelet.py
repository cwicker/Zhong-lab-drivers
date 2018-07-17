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

from lantz.drivers.keysight import Keysight_33622A, Arbseq_Class, SeqBuild

class ArbSeq(Spyrelet):

    requires = {
        'fungen': Keysight_33622A
    }

    @Task(name='send arbitrary waveform')
    def make_arb(self):
        #self.dataset.clear()
        params = self.arbseq_parameters.widget.get()
        print(params)
        seqtype = params['seqtype']
        name = params['seqname']
        timestep = params['timestep']

        seqbuild = SeqBuild(seqtype, params)
        seqbuild.build_arbseq(name, timestep)
        arbseq = seqbuild.arbseq
        
        ydata = arbseq.ydata
        print(ydata)
        xdata = list()
        x = 0
        while x < len(ydata):
            xdata.append(x)
            x += timestep

        print(xdata)

        for i in range(len(ydata)):
            values = {'x': xdata[i], 'y': ydata[i]}
            self.make_arb.acquire(values)

        print(self.data)

        self.fungen.send_arb(arbseq, chn=params['channel'])
        self.dataset.clear()



    @make_arb.initializer
    def initialize(self):
        params = self.arbseq_parameters.widget.get()
        channel = params['channel']
        self.fungen.clear_status()
        self.fungen.clear_mem()
        self.fungen.voltage[channel] = params['voltage']
        self.fungen.output[channel] = 'ON'
        print('initialize')
        return

    @make_arb.finalizer
    def finalize(self):
        print("finalize")
        return

    @Task(name='create arbitrary sequence')
    def make_sequence(self):
        params = self.sequence_parameters.widget.get()
        chn = params['channel']
        seqname = params['seqname']
        del params['channel']
        params['seqname'] = "{}".format(seqname)
        params['init'] = "INT:\\{}".format(params['init'])
        params['write'] = "INT:\\{}".format(params['write'])
        params['read'] = "INT:\\{}".format(params['read'])
        seqstring = str(params.values).strip('[]')
        print(seqstring)
        strlen = len(seqstring.encode('utf-8'))
        numbytes = len(str(strlen))
        self.write('SOURCE{}:DATA:SEQ #{}{}{}'.format(chn, numbytes, strlen, seqstring))
        self.waveform[chn] = 'ARB'
        self.write('SOURCE{}:FUNC:ARB {}'.format(chn, seqname))
        self.write('MMEM:STORE:DATA{} "INT:\\{}.seq"'.format(chn, seqname))
        print('Arb sequence "{}" downloaded to channel {}'.format(seqname, chn))

    @make_sequence.initializer
    def initialize(self):
        print('initialize')
        return

    @make_sequence.finalizer
    def finalize(self):
        print('finalize')
        return

    @Element()
    def arbseq_parameters(self):
        repeatstrings = ['once', 'onceWaitTrig', 'repeat', 'repeatInf', 'repeatTilTrig']
        markerstrings = ['maintain', 'lowAtStart', 'highAtStart', 'highAtStartGoLow']
        params = [
        ('arbname', {'type': str, 'default': 'arbitrary_name'}),
        ('seqtype', {'type': list, 'items': ['dc', 'pulse', 'ramp']}),
        ('channel', {'type': dict, 'items': {'1': 1, '2': 2}}),
        ('voltage', {'type': float, 'default': 0.05, 'units': 'V'}),
        ('timestep', {'type': float, 'default': 1}),
        ('totaltime', {'type': float, 'default': 100}),
        ('width', {'type': float, 'default': 10}),
        ('period', {'type': float, 'default': 10}),
        ('slope', {'type': float, 'default': 0.01})
        ]
        w = ParamWidget(params)
        return w

    @Element()
    def sequence_parameters(self):
        repeatstrings = ['once', 'onceWaitTrig', 'repeat', 'repeatInf', 'repeatTilTrig']
        markerstrings = ['maintain', 'lowAtStart', 'highAtStart', 'highAtStartGoLow']
        arblist = self.fungen.list_arb()
        print(arblist)
        params = [
        ('channel', {'type': dict, 'items': {'1': 1, '2': 2}}),
        ('seqname', {'type': str, 'default': 'sequence_name'}),
        ('init', {'type': list, 'items': arblist}),
        ('repeatstring1', {'type': list, 'items': repeatstrings}),
        ('markerstring1', {'type': list, 'items': markerstrings}),
        ('nrepeats1', {'type': int, 'default': 0}),
        ('markerloc1', {'type': int, 'default': 0}),
        ('write', {'type': list, 'items': arblist}),
        ('repeatstring2', {'type': list, 'items': repeatstrings}),
        ('markerstring2', {'type': list, 'items': markerstrings}),
        ('nrepeats2', {'type': int, 'default': 0}),
        ('markerloc2', {'type': int, 'default': 0}),
        ('read', {'type': list, 'items': arblist}),
        ('repeatstring3', {'type': list, 'items': repeatstrings}),
        ('markerstring3', {'type': list, 'items': markerstrings}),
        ('nrepeats3', {'type': int, 'default': 0}),
        ('markerloc3', {'type': int, 'default': 0})
        ]
        w = ParamWidget(params)
        return w


    @Element()
    def plot(self):
        p = LinePlotWidget()
        p.plot('arbitrary')
        return p

    @plot.on(make_arb.acquired)
    def plot_update(self, ev):
        w = ev.widget
        data = self.data
        w.set('arbitrary', xs=data.x, ys=data.y)
        return

