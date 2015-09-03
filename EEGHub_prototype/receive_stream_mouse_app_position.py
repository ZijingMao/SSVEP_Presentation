__author__ = 'Mauricio Merino'

# Import required libraries
from pylsl import StreamInlet, resolve_stream


# Use stream information from sender (Either custom script or Windows app)
# Configure data stream
stream_name = 'MouseButtons'
stream_type = 'Position'

# Find out if there is a stream with the requested name and type
streams = resolve_stream('type', stream_type)

# Obtain an inlet (a socket-like object) which has access to the data
inlet = StreamInlet(streams[0])

# Use an infinite loop to receive the data from the Stream
print("Receiving data from a "+stream_type+" Stream...")
while True:

    # Pull sample from Stream
    current_sample, timestamp = inlet.pull_sample()

    # Print current sample
    print(current_sample)