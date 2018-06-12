from lantz import Feat
from lantz.messagebased import MessageBasedDriver

class Keysight_66322A(MessageBasedDriver):
	"""This is the driver for the Keysight 66322A.""" 

	"""For VISA resource types that correspond to a complete 488.2 protocol 
	(GPIB Instr, VXI/GPIB-VXI Instr, USB Instr, and TCPIP Instr), you 
	generally do not need to use termination characters, because the 
	protocol implementation also has a native mechanism to specify the 
	end of the of a message.
	"""
	
	@Feat()
	def idn(self):
		return self.query('*IDN?')

	@Feat()
	def clear_status(self):
		"""This command clears the following registers:
		1. Standard Event Status
		2. Operation Status Event
		3.  Questionable Status Event
		4. Status Byte
		5. Clears the Error Queue
		
		If this *CLS immediately follows a program message terminator (<NL>),
		then the output queue and teh MAV bit are also cleared. 
		
		Command Syntax: *CLS
		Parameters:     (None)
		Query Syntax:   (None)

		"""
		return self.query('*CLS')

	@Feat()
	def event_status_enable(self,NRf):
		"""Programs the Standard Event Status Enable register bits. The 
		programming determines which events of the Standard Event Status
		Event register are allowed to set the ESB (Event Summary Bit) of the
		Status Byte register. A "1" in the bit position enables the 
		corresponding event. All of the enabled events of the Standard Event
		Status Event register are logically ORed to cause the Event Summary
		Bit (ESB) of the Status Byte register to be set. 

		Command Syntax:      *ESE<NRf>
		Parameters:          0 to 255
		Suffix:              (None)
		Example:             *ESE 129
		Query Syntax:        *ESE?
		Returned Parameters: <NRI> (Register value)
		Related Commands:    *ESR? *PSC *STB?

		CAUTION: If PSC is programmed to 0, then the *ESE command causes a 
		write cycle to nonvolatile memory. The nonvolatille memory has a 
		finite maximum number of write cycles. Programs that repeatedly
		cause write cycles to non-volatile memory can eventually exceed the
		maximum number of write cycles and may cause the memory to fail.
		"""
		# NOTE: not sure if the left right angle brackets are necessary here
		return self.('*ESE'+str(NRf))

	@Feat()
	def read_standard_event_status_register(self):
		"""Reads the Standard Event Status Even register. Reading the 
		register clears it. 
		Query Syntax:        *ESR?
		Parameters:          (None)
		Returned Parameters: <NR1> (Register binary value)
		Related Commands:    *CLS *ESE *ESE? *OPC
		"""
		return self.query('*ESR?')

	@Feat()
	def operation_complete(self):
		"""This command causes the interface to set the OPC bit (bit 0) of
		the Standard Event Status register when the power supply has completed
		all pending operations. Pending operations are complete when: 
		- All commands sent before *OPC have been executed. This includes 
		overlapped commands. Most commands are sequential and are completed 
		before the next command is executed. Overlapped commands are 
		executed in parallel with other commands. Commands that affect output
		voltage, current or state, relays, and trigger actions are overlapped
		with subsequent commands sent to the power supply. The *OPC command
		provides notification that all overlapped commands have been completed. 
		- Any change in the output level caused by previous commands has been
		completed. 
		- All triggered actions are completed.
		*OPC does not prevent processing of subsequent commands, but Bit 0 
		will not be set until all pending operations are completed.  
		Command Syntax: *OPC
		Parameters: 	(None)
		Related Commands *OPC? *WAI
		"""
		return self.query('*OPC')
if __name__== '__main__':
	# this is the USB VISA Address:
	with Keysight_66322A('USB0::0x0957::0x5707::MY53801461::0::INSTR') as inst:
		print('The identification of this instrument is :' + inst.idn)