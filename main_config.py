
# Device List
devices = {
    'fungen':[
        'lantz.drivers.keysight.Keysight_33622A',
        ['USB0::0x0957::0x5707::MY53801461::INSTR'],
        {}
    ],
    'osc':[
        'lantz.drivers.tektronix.TDS2024C',
        ['USB0::0x0699::0x03A6::C030873::INSTR'],
        {}
    ]
}

# Experiment List
spyrelets = {
    'lasercalibration':[
        'spyre.spyrelets.laser_calibration',
        {'fungen': 'fungen', 'osc': 'osc'},
        {'lasercalibration': 'lasercalibration'}
    ]
}