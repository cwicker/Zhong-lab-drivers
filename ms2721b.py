# -*- coding: utf-8 -*-
"""
    lantz.drivers.anritsu.ms2721b.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Implementation of Anritsu MS2721b spectrum analyzer
    Author: Peter Bevington
    Date: 8/10/2018
"""

from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver

class MS2721B(MessageBasedDriver):
    """Driver for Anritsu MS2721B spectrum analyzer
    """

    DEFAULTS = {'COMMON': {'write_termination': '\n', 'read_termination': '\n'}}

    @Feat()
    def idn(self):
        """This command returns the following information in <string> format separated by commas: 
        manufacturer name (“Anritsu”), model number/options, serial number, firmware package number.
        """
        return self.query('*IDN?')

    @Feat(values={'ON': 1, 'OFF': 0})
    def toggle_tracking(self):
        """Returns tracking generator output state
        """
        return self.query(':INITiate:TGENerator?')

    @toggle_tracking.setter
    def toggle_tracking(self, value):
        """Specifies whether the tracking generator is on or off.
        If the value is set to ON or 1, the tracking generator is turned on.
        If the value is set to OFF or 0, the tracking generator is turned off.  
        Default value is OFF.
        """
        self.write(':INITiate:TGENerator {}'.format(value))

    @Feat(limits=(-40, 0))
    def tracking_amplitude(self):
        """Returns the output power for the Tracking Generator. 
        """
        return self.query(':TGENerator:OUTput:POWer?')

    @tracking_amplitude.setter
    def tracking_amplitude(self, value):
        """Sets the output power for the Tracking Generator. 
        """
        self.write(':TGENerator:OUTput:POWer {}'.format(value))

    @Feat(limits=(10, 7.09e+9), units='Hz')
    def center_freq(self):
        """Returns sweep frequency center
        """
        return self.query(':FREQuency:CENTer?')

    @center_freq.setter
    def center_freq(self, value):
        """Sets sweep frequency center
        """
        self.write(':FREQuency:CENTer {}'.format(value))

    @Feat(limits=(10, 7.09e+9), units='Hz')
    def span_freq(self):
        """Returns sweep frequency span
        """
        return self.query(':FREQuency:SPAN?')

    @span_freq.setter
    def span_freq(self, value):
        """Sets sweep frequency span
        """
        self.write(':FREQuency:SPAN {}'.format(value))

    @Feat(limits=(0, 7.09e+9), units='Hz')
    def start_freq(self):
        """Returns sweep start frequency.
        """
        return self.query(':FREQuency:STARt?')

    @start_freq.setter
    def start_freq(self, value):
        """Sets sweep start frequency.
        """
        self.write(':FREQuency:STARt {}'.format(value))

    @Feat(limits=(10, 7.1e+9), units='Hz')
    def stop_freq(self):
        """Returns sweep stop frequency.
        """
        return self.query(':FREQuency:STOP?')

    @stop_freq.setter
    def stop_freq(self, value):
        """Sets sweep stop frequency.
        """
        self.write(':FREQuency:STOP {}'.format(value))

    @Feat(values={'ON': 1, 'OFF': 0})
    def sweep_toggle(self):
        return self.query(':INITiate:CONTinuous?')

    @sweep_toggle.setter
    def sweep_toggle(self, value):
        """Specifies whether the sweep/measurement is triggered continuously. 
        """
        self.write(':INITiate:CONTinuous {}'.format(value))

    @Action()
    def trigger(self):
        """Initiates a sweep/measurement.
        """
        self.write(':INITiate:IMMediate')

    @Feat()
    def measure_ratio(self):
        """Sets the active measurement to adjacent channel power ratio, 
        sets the default measurement parameters, triggers 
        a new measurement and returns the main channel power 
        lower adjacent and upper adjacent channel power results. 
        """
        return self.query(':MEASure:ACPower?')

    @Feat()
    def measure_power(self):
        """Sets the active measurement to channel power, 
        sets the default measurement parameters, triggers
        a new measurement and returns the channel power result. 
        """
        return self.query(':MEASure:CHPower:CHPower?')

    @Feat()
    def measure_density(self):
        """Sets the active measurement to channel power, 
        sets the default measurement parameters, triggers
        a new measurement and returns the channel power density result.
        """
        return self.query(':MEASure:CHPower:DENSity?')

    @Feat()
    def measure_bandwidth(self):
        """Sets the active measurement to occupied bandwidth, 
        sets the default measurement parameters, triggers a 
        new measurement and returns the occupied bandwidth, 
        percent of power and dB down results.
        """
        return self.query(':MEASure:OBWidth?')




