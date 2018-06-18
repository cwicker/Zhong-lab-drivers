import time
import argparse

from lantz import Q_

from Keysight_66322A import Keysight_36622A

parser = argparse.ArgumentParser()
parser.add_argument('start', type=float,
                    help='Start frequency [Hz]')
parser.add_argument('stop', type=float,
                    help='Stop frequency [Hz]')
parser.add_argument('step', type=float,
                    help='Step frequency [Hz]')
parser.add_argument('wait', type=float,
                    help='Waiting time at each step [s]')

args = parser.parse_args()

Hz = Q_(1, 'Hz')
start = args.start * Hz
stop = args.stop * Hz
step = args.step * Hz
wait = args.wait

with Keysight_36622A('USB0::0x0957::0x5707::MY53801461::0::INSTR') as inst:
    print(inst.idn)
    print("BEGIN FREQUENCY SCAN")

    current = start
    while current <= stop:
        inst.frequency[1] = current
        print('Changed to {}'.format(current))
        time.sleep(wait)
        current += step
