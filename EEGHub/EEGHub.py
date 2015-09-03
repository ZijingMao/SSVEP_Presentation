__author__ = 'Mauricio Merino <mauriciomdev@gmail.com, March of 2015'

# -----------------------------------------------------------------------------------------------------
'''
- EEGHub is envisioned to be a Complete Suite for EEG statistical signal processing and Analysis
 as well as experiment design, real-time processing, advanced testing, etc. A complete list of
 features will be added over time...

 - This is the very first prototype of EEGHub, it is not even using object oriented programming,
 this is just a single Python 3.4x Script containing some basic functions to used on a SSVEP system.
 A real-time SSVEP-based BCI is the most urgent feature at this time so it will be the first area
 to be develop for EEGHub. EEGHub will continue growing constantly  to be closer and closer to
 its vision and the whole set of functionality that is desired to be offered.
 Updates to EEGHub will come shortly.

 - At this  point EEGHub requires a working implementation of the Lab Streaming Layer library (UCSD)
 found at:  [https://code.google.com/p/labstreaminglayer/]  As well as many popular packages
 for Scientific computation such:  Numpy, Scipy, Matplotlib, Vispy, Scikit learn, etc.  I recommend
 installing a Python distribution such as Anaconda for python 3.4, found at:
 [http://continuum.io/downloads#py34]

- Additionally this requires OpenGL and OpenGL-accelerate packages, I install them using pip
and the 'wheel' files found at: [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl], optionally
I'm using PyCUDA (wheel file from the same website) but ensure you have a CUDA-capable GPU, the
latest NVIDIA drivers and CUDA installed, for windows users also add the Visual Studio Compiler
(cl.exe) to the path.

- EEGHub is develop and maintained by Mauricio Merino (mauriciomdev@gmail.com) A Graduate Student and
 Research Assistant at the University of Texas at San Antonio (www.utsa.edu) working on EEG signal
 processing under the direction of Professor Yufei Huang (basic info about him found at
 [http://ece.utsa.edu/contact/faculty/Yufei-Huang.html]).

- EEGHub has no specific license yet, but it is intended to be free and Open Source

- Special thanks to various collaborators:
    Prasanna Kolar and Zijing Mao (UTSA graduate students) and Dr. Yufei Huang'''
# -----------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------
# Import all the required modules/libraries (for all functions)
import os.path
import scipy.io
import numpy
import scipy.signal
from sklearn.cross_decomposition import CCA
# -----------------------------------------------------------------------------------------------------


# ------------------------------- PUBLIC functions: to be used when EEGHub is imported ---------------------------------
''' 1.) EEGHub: Load Data
A function that imports data/variables from various file formats: .csv, .txt, .xls, .mat, .bdf, etc. '''


def load_data(filename, variable_name):

    # TODO: Use optional arguments
    # TODO: Add support for a list of input files and a list of variable names AND a mixture of list/char
    # TODO: Add functionality: -path, -globalpath, -type, -norm, -scale, -fix, etc.
    # TODO: Make the function robust with input checks, exceptions, dumb-proof, etc.

    # ---
    # Check if the input filename exists on current path
    file_on_path = os.path.isfile(filename)
    if not file_on_path:
        print("[load_data]ERROR: The specified filename is invalid (does not exits on path)")
        return

    # If file exists, proceed only if it belongs to one of the supported file formats
    # Right now ONLY .MAT files are supported!!!
    filename_extension = filename.split('.')            # Obtain the file format from input filename
    filename_extension = filename_extension[1]

    # Check for an input .mat file, the only input format supported at this time
    file_formats = ['txt', 'csv', 'xls', 'mat', 'bdf']  # Supported formats, perform check
    mat_file_input = string_on_list(file_formats, filename_extension, 'mat')[2]
    if not mat_file_input:
        # Exit if file does not have a currently supported format
        print("[load_data]ERROR: The specified filename is invalid (filename not supported)")
        return

    # Proceed to load the .MAT file (more format support will be added later)
    file_data = scipy.io.loadmat(filename)              # Load .mat file using scipy.io module
    file_variables = file_data.keys()                   # Obtain variable list

    # Check if the input variable name is contained on the file, otherwise exit
    string_match_number = string_on_list(file_variables, variable_name, 'none')[0]
    if string_match_number != 1:
        print("[load_data]ERROR: The specified variable name is invalid (does not exits)")

    # Both filename, file load and variable name checks have succeed, extract the data and return (exit function)
    requested_variable = file_data.get(variable_name)
    return requested_variable


''' 2.) EEGHub: Filter Data
Performs low-pass, high-pass, band-pass. and reject-band filters, initially uses FIR filters with Hamming windows
but more advanced filters will be added over time'''


def filter_data(input_data, sampling_rate, filter_type, cutoff_frequency, filter_technique):

    # TODO: Use optional arguments for enhanced functionality
    # TODO: Increased the amount of supported filtering techniques
    # TODO: Make the function robust with input checks, exceptions, dumb-proof, etc.
    # TODO: Add additional and better explained error messages

    # NOTE: At this time only FIR filter (Hamming window) is supported, more filters will be added over time

    # Check inputs for supported functionality
    available_filter_types = ['lowpass', 'highpass', 'bandpass']
    valid_filter_type = string_on_list(available_filter_types, filter_type, 'none')[0]
    valid_filter_technique = string_on_list(['FIR-hamming'], filter_technique, 'FIR-hamming')[2]
    if (valid_filter_type != 1) and valid_filter_technique:
        print("[filter_data]ERROR: Only lowpass, highpass and bandpass filters (FIR hamming) are currently supported")

    # Extract number of EEG Channels and data points
    input_data = numpy.array(input_data, dtype='float')     # Force conversion to Numpy array
    number_channels = input_data.shape[0]
    number_time_points = input_data.shape[1]

    # Check the input filter type, Again FIR-Hamming only so far
    is_low_pass_filter = string_on_list(available_filter_types, filter_type, 'lowpass')[2]
    is_high_pass_filter = string_on_list(available_filter_types, filter_type, 'highpass')[2]
    is_band_pass_filter = string_on_list(available_filter_types, filter_type, 'bandpass')[2]

    # Depending to the filter type, Compute the Filter heuristics (FIR - Hamming case)
    window_width_ratio = 0.25
    amplifier_constant = 10000
    frequency_nyquist = sampling_rate / 2

    if is_low_pass_filter:
            coefficient_list_position = [0, 0]   # Valid only for the low-pass filter case, revise for high-pass
            tb_value = frequency_nyquist - cutoff_frequency
            window_values = 1
            filter_coefficient_df = min([max([cutoff_frequency * window_width_ratio, 2]), tb_value])

    elif is_high_pass_filter:
            coefficient_list_position = [1, 0]   # High-pass uses a different position constant
            window_values = numpy.hamming(number_time_points)
            filter_coefficient_df = min([max([cutoff_frequency * window_width_ratio, 2]), cutoff_frequency])

    elif is_band_pass_filter and (len(cutoff_frequency) == 2):
        # Band-pass: use the small cutoff frequency for the high-pass filter and high cutoff frequency for the low-pass
        high_filtered = filter_data(input_data, sampling_rate, 'highpass', min(cutoff_frequency), 'FIR-hamming')
        band_filtered = filter_data(high_filtered, sampling_rate, 'lowpass', max(cutoff_frequency), 'FIR-hamming')
        return band_filtered

    cutoff_coefficient_list = [[filter_coefficient_df, [-filter_coefficient_df, filter_coefficient_df]],
                               [-filter_coefficient_df, [filter_coefficient_df, -filter_coefficient_df]]]

    ntaps_constant = cutoff_coefficient_list[coefficient_list_position[0]][coefficient_list_position[1]]
    ntaps_constant = cutoff_frequency + (ntaps_constant / 2)
    ntaps_constant = (ntaps_constant / frequency_nyquist) * amplifier_constant

    # Create FIR filter (Hamming window)
    cutoff_coeff = cutoff_frequency / frequency_nyquist
    filter_design = scipy.signal.firwin(ntaps_constant, cutoff=cutoff_coeff, window='hamming')

    # Apply the created filter to each channel of the input data, pre-allocate output
    filtered_data = numpy.zeros([number_channels, number_time_points], dtype='float')
    for loop_var in range(number_channels):

        # Extract current channel data
        current_channel_data = input_data[loop_var, :]

        # Check for maximum padlen length and apply filter
        if ntaps_constant > number_time_points:
            ntaps_constant = number_time_points - 1
        filtered_data[loop_var, :] = scipy.signal.filtfilt(filter_design, window_values, current_channel_data,
                                                           padlen=ntaps_constant)

    # After filtering is done, return and exit
    return filtered_data


''' 3.) EEGHub: Channel Reference
This function perform Re-reference on EEG Data by substracting the mean of a subset of channels (reference channels
indicated on the input) or based on the global mean of all the channels (common average).
Referencing EEG data is a crucial part of EEG pre-processing, it greatly helps to obtain cleaner recordings'''


def channel_reference(input_data, reference_channels):

    # TODO: Make the function robust with input checks, exceptions, etc.
    # TODO: Verify the way the mean is extracted and subtracted from recordings
    # TODO: Add additional and better explained error messages

    # Extract number of EEG Channels and data points
    input_data = numpy.array(input_data, dtype='float')     # Force conversion to Numpy array
    number_channels = input_data.shape[0]
    number_time_points = input_data.shape[1]

    # Check the reference channel input for the 'all' flag or a subset of VALID channels
    # Common average referencing?
    if isinstance(reference_channels, str) and string_on_list(['all'], reference_channels, 'all')[2]:

        # Common reference case, compute the global mean
        all_data = numpy.reshape(input_data, (1, number_channels * number_time_points))
        reference_mean = numpy.mean(all_data)

        # Subtract the mean and return the result
        input_data = (input_data - reference_mean)
        return input_data

    # Check for a subset of numbers (channels)
    elif isinstance(reference_channels, list):

        # Check list for valid EEG Channel selection
        valid_channels = []
        for loop_var in range(len(reference_channels)):

            # Is valid channel? save it
            if isinstance(reference_channels[loop_var], int) and (reference_channels[loop_var] <= number_channels):
                valid_channels.append(reference_channels[loop_var])

        # Extract data from the valid reference channels (Pre-allocate matrix)
        selected_data = numpy.zeros([len(valid_channels), number_time_points])
        for loop_var in range(len(valid_channels)):
            selected_data[loop_var, :] = input_data[valid_channels[loop_var], :]

        # Compute the mean of the extracted data once is reshaped to 1xN
        all_data = numpy.reshape(selected_data, (1, len(valid_channels) * number_time_points))
        reference_mean = numpy.mean(all_data)

        # Subtract the mean and return the result
        input_data = (input_data - reference_mean)
        return input_data

    else:
        # An invalid input value, display an error and exit
        print("[channel_reference]ERROR: Invalid selection of reference channels (use 'all' or a subset of channels")
        return input_data

    return input_data


''' 4.) EEGHub: Frequency Spectrum
Using Fourier Transform and an input frequency range this function compute the frequency values and their respective
amplitude powers, these outputs are used to plot a frequency spectrum of the input signal'''


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
    signal_period = number_time_points / sampling_rate
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


''' 4.) EEGHub: Frequency Spectrum
Using Fourier Transform and an input frequency range this function compute the frequency values and their respective
amplitude powers, these outputs are used to plot a frequency spectrum of the input signal'''


def cca_for_ssvep(input_data, sampling_rate, compared_frequencies):

    # TODO: Strick input checks, exceptions and avoid crashing and processing errors

    # Pre-allocate SSVEP signals matrix to be compared with original EEG recordings using CCA
    number_time_points = input_data.shape[1]
    number_harmonics = 2
    cca_base_signal_matrix = [[] for loop_var in compared_frequencies]

    # Pre-allocate output: one correlation coefficient (Rho) for each target SSVEP frequency
    # Note: Row 1 is for default Rho scores, Row 2 is for the Rho scores After cca transformation
    cca_rho_values = numpy.zeros([1, len(compared_frequencies)], dtype='float')

    # For each target frequency, fill Y matrix with sine and cosine signals for every harmonic
    for loop_frequencies in range(len(compared_frequencies)):

        # For this current SSVEP frequency, pre-allocate the harmonics matrix
        cca_base_signal_matrix[loop_frequencies] = numpy.zeros([number_harmonics * 2, number_time_points])
        time_points_count = numpy.arange(number_time_points, dtype='float')
        time_points_count = time_points_count / sampling_rate

        # Generate sine and cosine reference signals, for every harmonic
        for loop_harmonics in range(number_harmonics):

            # Compute the reference signals for current harmonic
            base_constant = 2 * numpy.pi * (loop_harmonics + 1) * compared_frequencies[loop_frequencies]
            base_sine_signal = numpy.sin((base_constant * time_points_count))
            base_cosine_signal = numpy.cos((base_constant * time_points_count))

            # Copy signals back to reference matrix
            base_position = loop_harmonics + 1
            sine_position = (2 * (base_position - 1) + 1)
            cosine_position = 2 * base_position
            cca_base_signal_matrix[loop_frequencies][sine_position - 1, :] = base_sine_signal
            cca_base_signal_matrix[loop_frequencies][cosine_position - 1, :] = base_cosine_signal

        # After the loop, extract the y_matrix from reference matrix for current SSVEP frequency
        y_matrix = cca_base_signal_matrix[loop_frequencies]

        # Create a CCA object and compute the correlation score
        cca_object = CCA(n_components=number_harmonics)
        cca_object.fit(numpy.transpose(input_data), numpy.transpose(y_matrix))
        values_x, values_y = cca_object.transform(input_data, y_matrix)
        cca_rho_values[0, loop_frequencies] = cca_object.score(input_data, y_matrix, values_y)   # Score = Rho value?

    # After loop return and exit
    return cca_rho_values


# ---------------------------------  Private functions: for internal use only  ------------------------------
# Utility function to check if a list of strings (one dimension) contains a target string
def string_on_list(input_list, input_string, target_element):

    # TODO: Make the function robust with input checks, exceptions, etc.

    # Create a vector for binary check of every string on hte list
    input_list = list(input_list)
    list_check = numpy.zeros([1, len(input_list)])

    # Go through the list for a string comparison
    for loop_var in range(len(input_list)):
        if input_list[loop_var] == input_string:
            list_check[0][loop_var] = 1

    # Obtain the number of occurrences (string matches)
    number_matches = int(sum(list_check[0]))

    # Compute number of matches, position and possible target (flag)
    # Case 1: There was no match
    if not(number_matches >= 1):

        # Return results (no position)
        matches_positions = []
        number_matches = 0

    # Case 2: One or more match found
    else:

        # If there was at least one match, get the position
        matches_positions = list_check[0].nonzero()
        matches_positions = matches_positions[0]

        # Additionally, if the target flag is activated, check whether or not the matching element is the target
        if target_element == 'none':
            # Return normal set of outputs
            target_match = 'disabled'
            return number_matches, matches_positions, target_match

        # Check in the case that the target flag was activated
        else:

            # Perform target comparison
            if (input_list[matches_positions] == input_string) and (input_string == target_element):
                target_match = True             # Target check was positive
                return number_matches, matches_positions, target_match
            else:
                target_match = False            # Terms don't match
                return number_matches, matches_positions, target_match

    print('Check completed!')



