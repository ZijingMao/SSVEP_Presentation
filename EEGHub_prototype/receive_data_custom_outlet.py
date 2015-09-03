__author__ = 'Mauricio Merino'

# Import required libraries
from pylsl import StreamInlet, resolve_stream
import numpy
import scipy
import matplotlib.pyplot as plt
import time


def get_frequency_spectrum(input_data, sampling_rate, frequency_range):

    # TODO: Make the function robust with input checks, exceptions, etc.
    # TODO: Make sure input signal is in Channel x Time shape
    # TODO: Make sure frequency range is valid, ascending and within realistic SSVEP limits

    # Make sure input EEG data in a Numpy array
    input_data = numpy.array(input_data, dtype='float')

    # Check the input frequency range
    if not(len(frequency_range) == 2 and frequency_range[0] < frequency_range[1]):
        print("[get_frequency_spectrum]ERROR: Invalid selection of frequency range, use positive ascending numbers")

    # Get number of Channels and data points
    number_time_points = input_data.shape[1]

    # Compute frequency spectrum using the first half of the mirrored frequency values
    time_points_count = numpy.arange(number_time_points)
    signal_period = number_time_points / float(sampling_rate)
    frequency_values = time_points_count / signal_period
    frequency_values = frequency_values[0: int(number_time_points / 2)]  # Frequencies are mirrored, take the first half
    signal_fft = scipy.fft(input_data) / number_time_points
    signal_fft = abs(signal_fft[:, 0: int(number_time_points / 2)])

    # Extract the frequency values corresponding to the input frequency range
    frequency_range_lower_position = numpy.array((frequency_values >= frequency_range[0]), dtype='int')
    frequency_range_upper_position = numpy.array((frequency_values <= frequency_range[1]), dtype='int')
    valid_frequency_positions = numpy.array((frequency_range_lower_position == frequency_range_upper_position),
                                            dtype='int')
    valid_frequency_positions = valid_frequency_positions.nonzero()

    # Compute the positions for the frequency values within the input range and trim the frequency and fft arrays
    frequency_range_positions = [min(valid_frequency_positions[0]), max(valid_frequency_positions[0])]
    frequency_values = frequency_values[frequency_range_positions[0]:frequency_range_positions[1]]
    signal_fft = signal_fft[:, frequency_range_positions[0]:frequency_range_positions[1]]

    # Return and exit
    return frequency_values, signal_fft


# Use stream information from sender (Either custom script or Windows app)
# Configure data stream
stream_name = 'RandomVectors'
stream_type = 'EEG'

# Find out if there is a stream with the requested name and type
streams = resolve_stream('type', stream_type)

# Obtain an inlet (a socket-like object) which has access to the data
inlet = StreamInlet(streams[0])

# Use an infinite loop to receive the data from the Stream
print("Receiving data from a "+stream_type+" Stream...")
sampling_rate_data = 512
frequency_range_data = [1, 30]
buffer_size = 200
number_channels = 8
buffer_index = -1
buffer = numpy.zeros([number_channels, buffer_size])

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(numpy.arange(10), numpy.arange(10), 'r.')

while True:

    # Pull sample from Stream
    current_sample, timestamp = inlet.pull_sample()
    buffer_index += 1

    # Fill the buffer
    buffer[:, buffer_index] = current_sample

    # Print current sample
    print(current_sample)

    if buffer_index == buffer_size - 1:
        frequency_values_buffer, signal_fft_buffer = \
            get_frequency_spectrum(buffer, sampling_rate_data, frequency_range_data)

        buffer_index = -1

        # Create plot
        # Pre-processed data - frequency spectrum subplot, plot current optimal channel

        line1.set_ydata(signal_fft_buffer[0, :])
        fig.canvas.draw()

        #graph.xlabel('Frequency (Hz)')
        #graph.ylabel('Power')
        #graph.title('Frequency Spectrum [buffer]')
        #graph.grid()
        #plt.show()








