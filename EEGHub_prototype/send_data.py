__author__ = 'Mauricio Merino'

# Import required libraries
from pylsl import StreamInfo, StreamOutlet
import random
import time

# Configure data stream
data_format = 'float32'
data_number_channels = 8
data_sampling_rate = 50
data_push_interval = 1/data_sampling_rate
stream_name = 'RandomVectors'
stream_type = 'EEG'
device_name = 'Sample_PC'
stream_info = StreamInfo(stream_name,
                         stream_type,
                         data_number_channels,
                         data_sampling_rate,
                         data_format,
                         device_name)

# Create Outlet
outlet = StreamOutlet(stream_info)

# Using an infinite loop, send data
print("Now sending data through a "+stream_type+" Stream...")
sample_data = list(range(data_number_channels))

while True:
    # Create sample that will be send (a random column vector in this case)
    for loop_var in range(data_number_channels):
        sample_data[loop_var] = random.random()

    # Push the sample on the outlet (creates the streaming)
    outlet.push_sample(sample_data)

    # Wait the required time to generate the desired sampling rate
    time.sleep(data_push_interval)

print('Stream finished')