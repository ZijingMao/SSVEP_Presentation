__author__ = 'Mauricio Merino'

# Import required libraries
from pylsl import StreamInlet, resolve_stream
import numpy as np
import time
import datetime

# Define EEG recording and SSVEP experiment variables
NUMBER_OF_CHANNELS = 57         # When 32 Channels + 2 Ext are connected, 41 appear on the LSL data
SAMPLING_RATE = 512             # Default value for BioSemi Sampling rate is 512Hz
NUMBER_OF_TRIALS = 4            # This value should match the one on the SSVEP experiment
AFTER_TRIAL_PAUSE = 20          # Pause in seconds after each trial is completed
STIMULUS_TIME = 5               # Time in seconds that
STIMULUS_SEQUENCE_LENGTH = 26   # How many stimulus per trial, should match the SSVEP experiment file

# This is a hard-coded approximate value for the trial duration, should match SSVEP experiment file
TRIAL_TIME = ((STIMULUS_SEQUENCE_LENGTH*STIMULUS_TIME)*2)+AFTER_TRIAL_PAUSE

EXTRA_SAMPLES = 50                 # Keep recording to ensure the SSVEP experiment has been completed
MAX_SAMPLE = SAMPLING_RATE*((TRIAL_TIME*NUMBER_OF_TRIALS)+EXTRA_SAMPLES)

# Pre-allocate the matrix to storage EEG recordings and the vector for the time log
sample_matrix = np.zeros([NUMBER_OF_CHANNELS, MAX_SAMPLE])
time_vector = np.zeros([1, MAX_SAMPLE])
index = 0


# Find out if there is a stream with the requested name and type
EEG_stream = resolve_stream('type', 'EEG')
#Marker_stream = resolve_stream('type', 'Markers')

# Obtain an inlet (a socket-like object) which has access to the data
EEG_inlet = StreamInlet(EEG_stream[0])
#Marker_inlet = StreamInlet(Marker_stream[0])

# Use an infinite loop to receive the data from the Stream
print("Receiving data from a EEG and Event Streams...")

# Record the current time as a reference for all the following events' time measurements
time.clock()    # First clock call that serves as time reference
time_now = datetime.datetime.now()
reference_time = [time_now.hour, time_now.minute, time_now.second, time_now.microsecond]

while index < MAX_SAMPLE-1:

    # Pull sample from Stream (EEG)
    current_sample, timestamp_EEG = EEG_inlet.pull_sample()

    # Pull sample from Stream (Marker)
    #event_marker, timestamp_Marker = Marker_inlet.pull_sample()
    #print("Event: ", event_marker[0], " at time: ", timestamp_Marker)

    # Store current sample and time stamp into array
    sample_matrix[:, index] = current_sample
    time_vector[:, index] = time.clock()
    index += 1

    # Print current sample
    print(sample_matrix[20, index-1])


# Save EEG data and time reference list
time_reference_filename = "Recording_reference_time_"+str(reference_time[0])+"_"+str(reference_time[1])+"_"+str(reference_time[2])+".txt"
time_reference_file_handle = open(time_reference_filename, 'w')
for list_item in reference_time:
    time_reference_file_handle.write(str(list_item))
time_reference_file_handle.close()

EEG_data_filename = "EXP_EEG_data_"+str(reference_time[0])+"_"+str(reference_time[1])+"_"+str(reference_time[2])+".csv"
np.savetxt(EEG_data_filename, sample_matrix, delimiter=",")

EEG_time_filename = "EXP_EEG_time_"+str(reference_time[0])+"_"+str(reference_time[1])+"_"+str(reference_time[2])+".csv"
np.savetxt(EEG_time_filename, time_vector, delimiter=",")