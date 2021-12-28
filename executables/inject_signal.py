#!/usr/bin/env python
"""
Inject a periodic signal of known properties into a real-world filterbank data file.

Run using the following syntax.
python inject_signal.py -i <Configuration script of inputs> | tee <Log file>
"""
from __future__ import print_function
from __future__ import absolute_import
# Custom packages
from modules.read_config import read_config
from modules.general_utils import setup_logger_stdout, create_dir
# Standard imports
from blimpy import Waterfall
from argparse import ArgumentParser
import os, logging, time, sys
import numpy as np
##############################################################
def myexecute(inputs_cfg):
    """
    Primary function that handles fake signal injection.

    Parameters
    ----------
    inputs_cfg : str
         Path to configuration script of inputs
    """
    # Profile code execution.
    prog_start_time = time.time()

    # Read inputs from config file and set default parameter values, if applicable.
    hotpotato = read_config(inputs_cfg)
    hotpotato = set_defaults(hotpotato)
    logger = setup_logger_stdout() # Set logger output to stdout().

    # Read data from a filterbank file. Set max data load size to 15 GB.
    wat  = Waterfall(hotpotato['DATA_DIR'] + '/' + hotpotato['datafile'], max_load=15.0)
    header = wat.header
    Nchans = header['nchans'] # No. of spectral channels
    Nsamples  = wat.n_ints_in_file # No. of time samples
    tsamp = header['tsamp'] # Sampling time (s)
    times = np.arange(Nsamples)*tsamp # 1D array of times (s)
    data = wat.data[:,0,:].T # Data shape = (Nchans, Nsamples)

    # Median bandpass
    logger.info('Computing median bandpass')
    median_bp = np.median(data, axis=1)
    # Bandpass correction
    data = (data - median_bp[:,None])/median_bp[:,None]
    logger.info('Bandpass correction done.')
    # Normalize the data in each channel to zero median and unit variance.
    data = (data - np.median(data, axis=1)[:,None])/np.std(data, axis=1)[:,None]
    logger.info('Channel-wise data normalized to zero mean and unit variance.')

    # Inject boxcar periodic signals of constant amplitude.
    N_inject = len(hotpotato['inject_channels'])
    for i in range(N_inject):
        chan = hotpotato['inject_channels'][i] # Channel index into which a periodic signal must be injected
        phi = times/hotpotato['periods'][i] % 1.0 # Convert times to phase values.
        indices = np.where( np.logical_and(phi>=hotpotato['initial_phase'][i]-0.5*hotpotato['duty_cycles'][i], phi<hotpotato['initial_phase'][i]+0.5*hotpotato['duty_cycles'][i]) )
        # Injected signal =
        data[chan, indices] += hotpotato['pulse_SNR'][i]
        logger.info('Injected P = %.2f s signal into channel %d.'% (hotpotato['periods'][i], chan))
    wat.data = data.T.reshape((Nsamples, wat.header['nifs'], Nchans))

    create_dir(hotpotato['OUTPUT_DIR'])
    out_filename = hotpotato['OUTPUT_DIR'] + '/' + hotpotato['basename'] + hotpotato['output_ext']
    # Write data to disk.
    if hotpotato['output_ext'] == '.fil':
        wat.write_to_fil(out_filename)
        logger.info('%s written to disk'% (out_filename))
    elif hotpotato['output_ext'] == '.h5':
        wat.write_to_hdf5(out_filename)
        logger.info('%s written to disk'% (out_filename))
    else:
        logger.error('Output file format not recognized. Allowed file formats: .fil, .h5')

    # Calculate total run time for the code.
    prog_end_time = time.time()
    run_time = (prog_end_time - prog_start_time)/60.0
    logger.info('Code run time = %.3f minutes'% (run_time))

def set_defaults(hotpotato):
    """
    Set default values for keys in a dictionary of input parameters.

    Parameters
    ----------
    hotpotato : dictionary
         Dictionary of input parameters gathered from a configuration script
    """
    if hotpotato['output_ext']=='':
        if '.fil' in hotpotato['datafile']:
            hotpotato['output_ext'] = '.fil'
        elif '.h5' in hotpotato['datafile']:
            hotpotato['output_ext'] = '.h5'
        else:
            hotpotato['output_ext'] = '.fil'
    if hotpotato['OUTPUT_DIR']=='':
        hotpotato['OUTPUT_DIR'] = hotpotato['DATA_DIR']
    if hotpotato['inject_channels']=='':
        hotpotato['inject_channels'] = []
    if hotpotato['periods']=='':
        hotpotato['periods'] = []
    if hotpotato['duty_cycles']=='':
        hotpotato['duty_cycles'] = []
    if hotpotato['pulse_SNR']=='':
        hotpotato['pulse_SNR'] = []
    if hotpotato['initial_phase']=='':
        hotpotato['initial_phase'] = []
    return hotpotato
##############################################################
def main():
    """ Command line tool for running inject_signal.py """
    parser = ArgumentParser(description="Inject a fake periodic signal into real-world data.")
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', action='store', required=True, dest='inputs_cfg', type=str,
                            help="Configuration script of inputs")
    parser._action_groups.append(optional)

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    parse_args = parser.parse_args()
    # Initialize parameter values
    inputs_cfg = parse_args.inputs_cfg

    # Run task using inputs from configuration script.
    myexecute(inputs_cfg)
##############################################################
if __name__=='__main__':
    main()
##############################################################
