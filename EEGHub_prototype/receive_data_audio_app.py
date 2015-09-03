import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import StreamInlet, resolve_stream
import time


# Start Audio stream
print("looking for an Audio stream...")
streams = resolve_stream('type', 'Audio')
inlet = StreamInlet(streams[0])
n_samples = 250
time_interval = 100

# Pre-allocate line
fig, ax = plt.subplots()
line, = ax.plot(numpy.random.rand(n_samples))
ax.set_ylim(-1, 1)


# Create a function to pull N number of samples from the Audio Stream
def pull_stream_samples(number_samples, nt):

    # Pre-allocate variables and output
    buffer_iteration = -1
    time_buffer = numpy.arange(number_samples)
    sample_buffer = numpy.array(time_buffer, dtype='f')
    amplifier_factor = 1000

    # Fill the sample buffer
    while buffer_iteration < len(sample_buffer) - 1:

        # Increase buffer iteration variable
        buffer_iteration = buffer_iteration +1

        # Pull a sample from the stream
        sample, timestamp = inlet.pull_sample()

        # Save current sample on the sample buffer
        sample_buffer[buffer_iteration] = float(sample[0] * amplifier_factor)

    # Return and exit
    time.sleep(1/nt)
    return sample_buffer


def update(data):
    line.set_ydata(data)
    return line,


def data_gen():
    while True:
        yield pull_stream_samples(n_samples, time_interval)

# Create the animation
ani = animation.FuncAnimation(fig, update, data_gen, interval=time_interval)
plt.show()