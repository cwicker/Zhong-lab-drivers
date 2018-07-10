from Keysight_66322A import Keysight_33622A
from arbseq_class import arbseq_class

class seqbuild(Keysight_33622A):
    pass


if __name__ == '__main__':
    from time import sleep
    from lantz import Q_
    from lantz.log import log_to_screen, DEBUG

    testseq = arbseq_class('testseq', 1)
    testseq.totaltime = 100
    testseq.widths = (5, 5, 5, 5)
    testseq.delays = (5, 20, 20, 20)
    testseq.heights = (0.25, 0.5, 0.75, 1)
    testseq.create_sequence()
    #print('testseq: ' + testseq.ydata)
    testseq.nrepeats = 10
    testseq.repeatstring = 'repeat'
    testseq.markerstring = 'lowAtStart'
    testseq.markerloc = 10

    testseq2 = arbseq_class('testseq2', 1)
    testseq2.totaltime = 100
    testseq2.widths = (5, 5, 5, 5)
    testseq2.delays = (5, 20, 20, 20)
    testseq2.heights = (1, 0.75, 0.5, 0.25)
    testseq2.create_sequence()
    #print('testseq2: ' + testseq2.ydata)
    testseq2.nrepeats = 10
    testseq2.repeatstring = 'repeat'
    testseq2.markerstring = 'lowAtStart'
    testseq2.markerloc = 10

    fulltestseq = [testseq, testseq2]

    with Keysight_33622A('USB0::0x0957::0x5707::MY53801461::0::INSTR') as inst:
        print('The identification of this instrument is :' + inst.idn)
        inst.clear_status()
        inst.output[1] = 'ON'
        #inst.clear_mem()
        #inst.send_arb(testseq)
        #inst.clear_mem()
        #inst.load_arb('testseq')

        inst.clear_mem()
        inst.create_arbseq('fulltestseq',fulltestseq)


