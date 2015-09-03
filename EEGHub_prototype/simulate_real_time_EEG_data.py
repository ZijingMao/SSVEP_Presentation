__author__ = 'Mauricio Merino'

# Import required libraries
from pylsl import StreamInfo, StreamOutlet
import time
import numpy
from EEGHub import load_data


# Step 1.) Load  Sample EEG Data, save is as a numpy array
raw_data = load_data('EEG_data.mat', 'sample_data')            # Use the raw-data only
raw_data_numpy = numpy.array(raw_data)
raw_data_number_samples = raw_data_numpy.shape[1]

# Step 2.) Configure data stream
data_format = 'float32'
data_number_channels = raw_data_numpy.shape[0]
data_sampling_rate = 512                                # Desired sampling rate
time_reduction_factor = 1.2
data_push_interval = float(1/data_sampling_rate) * ((100-time_reduction_factor)/100)     # To recreate sampling rate
stream_name = 'EEG'
stream_type = 'EEG'                                     # As this type will be identified for other LSL listeners
device_name = 'Sample_PC'                               # Host name
stream_info = StreamInfo(stream_name,                   # Create an data Stream object
                         stream_type,
                         data_number_channels,
                         data_sampling_rate,
                         data_format,
                         device_name)


# Step 3.) Create Outlet to send data using the stream
outlet = StreamOutlet(stream_info)

# Step 4.) Use a loop to send samples until the end of the file
print("Now sending data through a "+stream_type+" Stream...")
current_sample = -1

cumulative_time = time.clock()
sent_samples = 0
num_cycles = 1
cycle_time = 1
time_elapsed = False

while current_sample <= raw_data_number_samples:

    # Extract current sample to be send
    current_sample += 1
    current_EEG_sample = raw_data_numpy[:, current_sample]

    # Push the sample on the outlet (creates the streaming)
    outlet.push_sample(current_EEG_sample)
    cumulative_time = time.clock()
    sent_samples += 1

    # Wait the required time to generate the desired sampling rate
    push_interval_elapsed = time.clock()
    push_interval_target = (push_interval_elapsed + data_push_interval)
    while push_interval_elapsed <= push_interval_target:
        push_interval_elapsed = time.clock()

    # Check samples sent
    time_elapsed = (cumulative_time >= (cycle_time * (num_cycles - 1))) and \
                   (cumulative_time <= cycle_time * num_cycles)

    if time_elapsed:
        print("Current sampling rate is: "+str(sent_samples)+" EEG samples/Second [Elapsed: "+str(num_cycles)+" Seconds]")
        sent_samples = 0
        time_elapsed = False
        num_cycles += 1

print('Stream finished')
