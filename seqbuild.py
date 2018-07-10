from Keysight_66322A import Keysight_33622A
from arbseq_class import arbseq_class

class seqbuild(Keysight_33622A):
	pass


if __name__ == '__main__':
    from time import sleep
    from lantz import Q_
    from lantz.log import log_to_screen, DEBUG

    testseq = arbseq_class('testseq',1)
	testseq.totaltime = 100
	testseq.widths = (5, 5, 5, 5)
	testseq.delays = (5, 20, 20, 20)
	testseq.heights = (1, 1, 1, 1)
	testseq.create_sequence
	testseq.nrepeats = 10
	testseq.repeatstring = 'repeat'
	testseq.markerstring = 'lowAtStart'
	testseq.markerloc = 10

	fulltestseq = list(testseq)

	with Keysight_33622A('USB0::0x0957::0x5707::MY53801461::0::INSTR') as inst:
        print('The identification of this instrument is :' + inst.idn)

        inst.output[1] = 'ON'
        inst.create_arbseq('testseq',fulltestseq)


