
#  Version 3 of the program now uses Stimulus Arrays instead of individual stimulus


# ---- Include required modules from Psychopy API ----
from psychopy import visual, core, logging
import time
import numpy as np


# ---- Create a full-screen window with invisible mouse, collect real monitor refresh rate ----
window_handle = visual.Window([1920, 1080], fullscr=False, winType='pyglet', monitor='testMonitor',
                              units='norm', screen=0, color=[-1, -1, -1], colorSpace='rgb')

monitor_frame_rate = int(window_handle.getActualFrameRate())
window_handle.setMouseVisible(False)

# --- Create Stimulus Array, pre-allocate and configure square flickers
number_stimulus = 5
stimulus_sizes = np.array([3] * number_stimulus)
stimulus_color_ON = np.array([1, 1, 1] * number_stimulus)
stimulus_color_ON = np.reshape(stimulus_color_ON, [number_stimulus, 3])
stimulus_color_OFF = stimulus_color_ON * -1

stimulus_locations = np.array([[-25, 0], [25, 0], [0, 13], [0, -13], [-25, 13]])
stimulus_array = visual.ElementArrayStim(window_handle, fieldPos=(0.0, 0.0), units='cm', fieldSize=[1920, 1080],
                                   sizes=stimulus_sizes, fieldShape = 'sqr', xys=stimulus_locations,
                                   nElements=number_stimulus, sfs=0, elementTex=None, elementMask=None,
                                   colors=stimulus_color_ON, colorSpace='rgb')



# --- Configure execution time for the flickering loop
target_time = 20
time.clock()                # First clock call that serves as time reference
clock_object = core.Clock()
elapsed_time = clock_object.getTime()

# --- Enable frame monitoring and logging (to detect drop frames)
window_handle.flip()
window_handle.setRecordFrameIntervals(True)
window_handle._refreshThreshold = (1/60.0) + 0.003  # 60Hz monitor and 4 ms of tolerance
logging.console.setLevel(logging.WARNING)
window_handle.flip()

# --- Configure stimulus frequency
frame_counter = 0
stimulus_frame_switch = 2

# --- Run the flickering loop
window_handle.flip()        # Initial screen flip
while elapsed_time <= target_time:

    # Draw stimulus
    stimulus_array.setColors(stimulus_color_ON, 'rgb')
    stimulus_array.draw()
    window_handle.flip()

    stimulus_array.setColors(stimulus_color_OFF, 'rgb')
    stimulus_array.draw()
    window_handle.flip()

    # Count elapsed time
    elapsed_time = clock_object.getTime()

# --- Close window
core.wait(1)                  # Waiting half second improves stability
window_handle.close()
