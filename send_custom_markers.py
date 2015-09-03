import sys
sys.path.append('..')
from pylsl import StreamInfo, StreamOutlet
import time

# first resolve a marker stream on the lab network
info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'Experiment01')
outlet = StreamOutlet(info)

data_sampling_rate = 512                                # Desired sampling rate
time_reduction_factor = 1.2
data_push_interval = float(1/data_sampling_rate) * ((100-time_reduction_factor)/100)     # To recreate sampling rate
cumulative_time = time.clock()


while True:
        # get a new sample (you can also omit the timestamp part if you're not interested in it)
        outlet.push_sample(['Nothing'])
        cumulative_time = time.clock()

        push_interval_elapsed = time.clock()
        push_interval_target = (push_interval_elapsed + data_push_interval)
        while push_interval_elapsed <= push_interval_target:
            push_interval_elapsed = time.clock()

