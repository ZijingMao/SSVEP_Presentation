"""UTSA SSVEP experiment v1, using a procedural approach and everything exposed into a single file
Author: Mauricio Merino, Yufei Huang EEg Laboratory, University of Texas at San Antonio. April 2015
This code is BASED on the code by John Naulty. This version is hardcoded for a 24 inches monitor or bigger"""

# ---- Include required modules from Psychopy API ----
import sys
from psychopy import visual, core
import time
import numpy as np
import datetime
from pylsl import StreamInfo, StreamOutlet

sys.path.append('..')

# ---- Create a full-screen window with invisible mouse, collect real monitor refresh rate ----
window_handle = visual.Window([1920, 1080], fullscr=False, monitor='testMonitor', units='deg', screen=1, color=[-1, -1, -1], colorSpace='rgb')
monitor_frame_rate = int(window_handle.getActualFrameRate())
window_handle.setMouseVisible(False)
# ----------------------------------------------------------------------------------------------------------------------


# ---- Create FLICKERING SQUARES stimulus (ALL in Invisible mode at first) -----
# Left square (flickers at 10Hz)
square_left_ON = visual.GratingStim(win=window_handle, name='leftON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[-25, 0], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)

square_left_OFF = visual.GratingStim(win=window_handle, name='leftOFF', units='cm', tex=None, mask=None, ori=0,
                                     pos=[-25, 0], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                     opacity=0.93, texRes=256, interpolate=True, depth=-2.0)

square_left_fixation = visual.GratingStim(win=window_handle, size=0.5, pos=[-25, 0], sf=0,
                                          color=[-1, -1, -1], colorSpace='rgb')

# Right square (flickers at 6Hz)
square_right_ON = visual.GratingStim(win=window_handle, name='rightON', units='cm', tex=None, mask=None, ori=0,
                                     pos=[25, 0], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                     opacity=0.93, texRes=256, interpolate=True, depth=-1.0)

square_right_OFF = visual.GratingStim(win=window_handle, name='rightOFF', units='cm', tex=None, mask=None, ori=0,
                                      pos=[25, 0], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                      opacity=0.93, texRes=256, interpolate=True, depth=-2.0)

square_right_fixation = visual.GratingStim(win=window_handle, size=0.5, pos=[25, 0], sf=0,
                                           color=[-1, -1, -1], colorSpace='rgb')

# Up square (flickers at 30Hz)
square_up_ON = visual.GratingStim(win=window_handle, name='upON', units='cm', tex=None, mask=None, ori=0,
                                  pos=[0, 13], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                  opacity=0.93, texRes=256, interpolate=True, depth=-1.0)

square_up_OFF = visual.GratingStim(win=window_handle, name='upOFF', units='cm', tex=None, mask=None, ori=0,
                                   pos=[0, 13], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                   opacity=0.94, texRes=256, interpolate=True, depth=-2.0)

square_up_fixation = visual.GratingStim(win=window_handle, size=0.5, pos=[0, 13], sf=0, rgb=-1)

# Down square (flickers at 15Hz)
square_down_ON = visual.GratingStim(win=window_handle, name='downON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[0, -13], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)

square_down_OFF = visual.GratingStim(win=window_handle, name='downOFF', units='cm', tex=None, mask=None, ori=0,
                                     pos=[0, -13], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                     opacity=0.93, texRes=256, interpolate=True, depth=-2.0)

square_down_fixation = visual.GratingStim(win=window_handle, size=0.5, pos=[0, -13], sf=0, rgb=-1)

# Top left flicker (Face Image)
square_face_ON = visual.ImageStim(win=window_handle, image='face.jpg', mask=None, units='', pos=[-25, 13], size=None,
                                  ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, opacity=1.0, depth=0,
                                  interpolate=False, flipHoriz=False, flipVert=False, texRes=256, name=None,
                                  autoLog=None, maskParams=None)
# ----------------------------------------------------------------------------------------------------------------------


# ---- Create arrow stimulus and big fixation mark (ALL in Invisible mode at first) -----
# Arrows are essentially images which don't flicker and requires no fixation or ON/OFF stimulus
arrow_left = visual.ImageStim(win=window_handle, image='arrow_left.jpg', mask=None, units='', pos=[-20, 0], size=None,
                              ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, opacity=1.0, depth=0,
                              interpolate=False, flipHoriz=False, flipVert=False, texRes=256, name=None,
                              autoLog=None, maskParams=None)

arrow_right = visual.ImageStim(win=window_handle, image='arrow_right.jpg', mask=None, units='', pos=[20, 0], size=None,
                               ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, opacity=1.0, depth=0,
                               interpolate=False, flipHoriz=False, flipVert=False, texRes=256, name=None,
                               autoLog=None, maskParams=None)

arrow_up = visual.ImageStim(win=window_handle, image='arrow_up.jpg', mask=None, units='', pos=[0, 8], size=None,
                            ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, opacity=1.0, depth=0,
                            interpolate=False, flipHoriz=False, flipVert=False, texRes=256, name=None,
                            autoLog=None, maskParams=None)

arrow_down = visual.ImageStim(win=window_handle, image='arrow_down.jpg', mask=None, units='', pos=[0, -8], size=None,
                              ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, opacity=1.0, depth=0,
                              interpolate=False, flipHoriz=False, flipVert=False, texRes=256, name=None,
                              autoLog=None, maskParams=None)

arrow_face = visual.ImageStim(win=window_handle, image='arrow_left.jpg', mask=None, units='', pos=[-20, 13], size=None,
                              ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, opacity=1.0, depth=0,
                              interpolate=False, flipHoriz=False, flipVert=False, texRes=256, name=None,
                              autoLog=None, maskParams=None)

focus_fixation = visual.GratingStim(win=window_handle, mask='cross', name='bigFixation', size=1.2, pos=[0, 0], sf=0)
# ----------------------------------------------------------------------------------------------------------------------


'''
----------------------------------------------------------------------------------------------------------------------
                                            EXPERIMENT DESIGN
- This experiment is run twice
- Each run consist of 4 trials
- 2 of those 4 trials are centered on SSVEP and focus, the other two on SSVEP and face recognition
- Each trial is a hard-coded sequence of 16 commands (either face, left, right, up, down or fixation)
- Participant should look at each command for 5 seconds
----------------------------------------------------------------------------------------------------------------------
'''


# ---- Configure the flickering frequencies of square stimulus and experiment commands and length ----
# Frames to switch stimulus
square_left_number_frames = 3               # 3 frames ON and 3 frames OFF to make 10 Hz
square_right_number_frames = 5              # 5 frames ON and 5 frames OFF to make 6 Hz
square_up_number_frames = 4                 # 4 frames ON and 4 frames OFF to make 7.5 Hz
square_down_number_frames = 4               # 4 frames ON BUT 3 frames OFF to make 8.57 Hz
square_face_number_frames = 3               # 3 frames ON and 3 frames OFF to make 10 Hz

#  Approximate frequency of each stimulus
frequency_square_left = monitor_frame_rate / (2 * square_left_number_frames)
frequency_square_right = monitor_frame_rate / (2 * square_left_number_frames)
frequency_square_up = monitor_frame_rate / (2 * square_left_number_frames)
frequency_square_down = monitor_frame_rate / (2 * square_left_number_frames)
frequency_square_face = monitor_frame_rate / (2 * square_left_number_frames)

# Make invisible arrow stimulus and fixation mark
arrow_left.setAutoDraw(False)
arrow_right.setAutoDraw(False)
arrow_up.setAutoDraw(False)
arrow_down.setAutoDraw(False)
arrow_face.setAutoDraw(False)
focus_fixation.setAutoDraw(False)

# Frame counters and boolean flags for each stimulus
frame_counter_left = 0
switch_flag_left = False

frame_counter_right = 0
switch_flag_right = False

frame_counter_up = 0
switch_flag_up = False

frame_counter_down = 0
switch_flag_down = False

frame_counter_face = 0
switch_flag_face = False

command_sequence = ['Up', 'Left', 'Face', 'Left', 'Face', 'Left', 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Up',
                    'Right', 'Face', 'Up', 'Down', 'Left', 'Face', 'Left', 'Face', 'Face', 'Up', 'Up', 'Left', 'Face']


# ----------------------------------------------------------------------------------------------------------------------
number_of_trials = 4
after_trial_pause = 20            # Pause in seconds
command_display_time = 5          # In seconds
arrow_display = False             # Arrows start being displayed first, show fixation when value is False
command_time_counter = 1

time_flip_counter = 0
trial_indicator_text_stimulus = visual.TextStim(win=window_handle, text=' ', pos=[0, -3])
trial_indicator_text_stimulus.setAutoDraw(True)
executed_command = 0
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Create an outlet to transmit data (event markers) using LSL
info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'Experiment01')
outlet = StreamOutlet(info)
outlet.push_sample(['Waiting...'])
time.sleep(10)
# ----------------------------------------------------------------------------------------------------------------------

# Pre-allocate the event time log matrix
events_per_trial = (len(command_sequence)*2)+1
event_matrix = np.zeros([2, (number_of_trials*events_per_trial)+1])

EVENT_LEFT = 1
EVENT_RIGHT = 2
EVENT_UP = 3
EVENT_DOWN = 4
EVENT_FACE = 5
EVENT_CROSS = 6
EVENT_REST = 7
EVENT_PAUSE = 8
event_index = -1
trial_done = 0
# ----------------------------------------------------------------------------------------------------------------------
'''       Main Loop of the SSVEP presentation program: Trials => Sequence => Time => Monitor frames     '''

# Record the current time as a reference for all the following events' time measurements
window_handle.flip()
time.clock()    # First clock call that serves as time reference
time_now = datetime.datetime.now()
reference_time = [time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute,
                  time_now.second, time_now.microsecond]
clock_object = core.Clock()
countdown_time = core.CountdownTimer(25)      # Introduce artificial wait to sync events

for current_trial in range(number_of_trials):
    # For each trial complete a command sequence

    # An inner loop to navigate through the command sequence, each command last 5 seconds
    while executed_command <= (len(command_sequence) - 1):

        # Activate current command
        current_command = command_sequence[executed_command]
        trial_text = 'Trial: '+str(current_trial+1)+' of '+str(number_of_trials) + \
                     ', Command: '+str(executed_command + 1)+' of '+str(len(command_sequence))
        trial_indicator_text_stimulus.setText(trial_text)

        ''' All checking have been done, at the very end, flip the screen '''
        window_handle.flip()

        '''-----  Activate flickering on 4 squares + face ----'''
        # Increase frame counters
        frame_counter_left += 1
        frame_counter_right += 1
        frame_counter_up += 1
        frame_counter_down += 1
        frame_counter_face += 1

        # When the specified number of frames (per stimulus) is reached, change the boolean flag for switching
        if frame_counter_left == square_left_number_frames:
            frame_counter_left = 0
            switch_flag_left = not switch_flag_left

        if frame_counter_right == square_right_number_frames:
            frame_counter_right = 0
            switch_flag_right = not switch_flag_right

        if frame_counter_up == square_up_number_frames:
            frame_counter_up = 0
            switch_flag_up = not switch_flag_up

        # ======================== Here I just modified for the odd period 4(ON) 3(OFF) period =========================
        if (frame_counter_down == square_down_number_frames - 1) and not switch_flag_down:
            frame_counter_down = 0
            switch_flag_down = True

        if (frame_counter_down == square_down_number_frames) and switch_flag_down:
            frame_counter_down = 0
            switch_flag_down = False

        # Original Code
#        if frame_counter_down == square_down_number_frames:
#            frame_counter_down = 0
#            switch_flag_down = not switch_flag_down
        # ==============================================================================================================

        if frame_counter_face == square_face_number_frames:
            frame_counter_face = 0
            switch_flag_face = not switch_flag_face

        # Check boolean flags: True is for ON stimulus, False is for OFF stimulus
        # Left Stimulus
        if switch_flag_left:
            square_left_ON.setAutoDraw(True)
            square_left_fixation.setAutoDraw(True)
            square_left_OFF.setAutoDraw(False)
        else:
            square_left_ON.setAutoDraw(False)
            square_left_fixation.setAutoDraw(False)
            square_left_OFF.setAutoDraw(True)

        # Right Stimulus
        if switch_flag_right:
            square_right_ON.setAutoDraw(True)
            square_right_fixation.setAutoDraw(True)
            square_right_OFF.setAutoDraw(False)
        else:
            square_right_ON.setAutoDraw(False)
            square_right_fixation.setAutoDraw(False)
            square_right_OFF.setAutoDraw(True)

        # Up Stimulus
        if switch_flag_up:
            square_up_ON.setAutoDraw(True)
            square_up_fixation.setAutoDraw(True)
            square_up_OFF.setAutoDraw(False)
        else:
            square_up_ON.setAutoDraw(False)
            square_up_fixation.setAutoDraw(False)
            square_up_OFF.setAutoDraw(True)

        # Down Stimulus
        if switch_flag_down:
            square_down_ON.setAutoDraw(True)
            square_down_fixation.setAutoDraw(True)
            square_down_OFF.setAutoDraw(False)
        else:
            square_down_ON.setAutoDraw(False)
            square_down_fixation.setAutoDraw(False)
            square_down_OFF.setAutoDraw(True)

        # Face Stimulus
        if switch_flag_face:
            square_face_ON.setAutoDraw(True)
        else:
            square_face_ON.setAutoDraw(False)

        ''' Based on current command from the sequence, display a pointing arrow '''

        # ---- If showing arrows is selected, choose arrow and draw it
        if arrow_display:

            # Disable all arrow images before choosing
            arrow_left.setAutoDraw(False)
            arrow_right.setAutoDraw(False)
            arrow_up.setAutoDraw(False)
            arrow_down.setAutoDraw(False)
            arrow_face.setAutoDraw(False)

            # Disable also the fixation mark
            focus_fixation.setAutoDraw(False)

            # Display left arrow if it is on sequence
            if current_command == "Left":
                arrow_left.setAutoDraw(True)

            # Display right arrow if it is on sequence
            if current_command == "Right":
                arrow_right.setAutoDraw(True)

            # Display left arrow if it is on sequence
            if current_command == "Up":
                arrow_up.setAutoDraw(True)

            # Display down arrow if it is on sequence
            if current_command == "Down":
                arrow_down.setAutoDraw(True)

            # Display face arrow if it is on sequence
            if current_command == "Face":
                arrow_face.setAutoDraw(True)

        else:
            # ----- If Fixation cross is activated, display it

            # Make arrows invisible
            arrow_left.setAutoDraw(False)
            arrow_right.setAutoDraw(False)
            arrow_up.setAutoDraw(False)
            arrow_down.setAutoDraw(False)
            arrow_face.setAutoDraw(False)

            # Make fixation visible
            focus_fixation.setAutoDraw(True)

        # ------------------------------- Time checking ------------------------------
        ''' Arrow OR Fixation has been displayed, check execution time if reached 5 seconds for another switch '''
        # Get the current time
        elapsed_time = clock_object.getTime()
        print(str(elapsed_time))

        # Check if the specified command execution time has occurred
        duration_elapsed = (elapsed_time > int(command_display_time * (command_time_counter - 1))) and \
                           (elapsed_time <= int(command_display_time * command_time_counter))

        if duration_elapsed:

            # The 5 seconds have passed, change to fixation mode and increase command time counter
            command_time_counter += 1
            arrow_display = not arrow_display
            time_flip_counter += 1

            # Check for arrow event or cross
            event_index += 1

            if arrow_display:
                if current_command == "Left":
                    LSL_send_command = current_command
                    event_matrix[0, event_index] = EVENT_LEFT
                    event_matrix[1, event_index] = time.clock()

                if current_command == "Right":
                    LSL_send_command = current_command
                    event_matrix[0, event_index] = EVENT_RIGHT
                    event_matrix[1, event_index] = time.clock()

                if current_command == "Up":
                    LSL_send_command = current_command
                    event_matrix[0, event_index] = EVENT_UP
                    event_matrix[1, event_index] = time.clock()

                if current_command == "Down":
                    LSL_send_command = current_command
                    event_matrix[0, event_index] = EVENT_DOWN
                    event_matrix[1, event_index] = time.clock()

                if current_command == "Face":
                    LSL_send_command = current_command
                    event_matrix[0, event_index] = EVENT_FACE
                    event_matrix[1, event_index] = time.clock()
            else:
                LSL_send_command = 'Cross'
                event_matrix[0, event_index] = EVENT_CROSS
                event_matrix[1, event_index] = time.clock()

            # After the event has been recorded also transmit it through the LSL inlet
            outlet.push_sample([LSL_send_command])

            # Detect when a command has been completed
            if time_flip_counter == 2:
                time_flip_counter = 0
                executed_command += 1

    # Count a trial that has finished
    trial_done += 1

    # ----------------------------------------------------------------------------------------------------------------------
    ''' At this point current trial has finished: stop flickering and pause for the specified time'''

    # Refresh screen
    window_handle.flip()

    # Make invisible all stimulus
    arrow_left.setAutoDraw(False)
    arrow_right.setAutoDraw(False)
    arrow_up.setAutoDraw(False)
    arrow_down.setAutoDraw(False)
    arrow_face.setAutoDraw(False)
    focus_fixation.setAutoDraw(False)
    square_face_ON.setAutoDraw(False)
    square_left_ON.setAutoDraw(False)
    square_left_OFF.setAutoDraw(False)
    square_left_fixation.setAutoDraw(False)
    square_right_ON.setAutoDraw(False)
    square_right_OFF.setAutoDraw(False)
    square_right_fixation.setAutoDraw(False)
    square_up_ON.setAutoDraw(False)
    square_up_OFF.setAutoDraw(False)
    square_up_fixation.setAutoDraw(False)
    square_down_ON.setAutoDraw(False)
    square_down_OFF.setAutoDraw(False)
    square_down_fixation.setAutoDraw(False)

    # Make visible the text stimulus for end-of-trial message
    trial_text = 'Trial '+str(trial_done+1)+' has ended!. You will have '+str(after_trial_pause)+' seconds to rest'
    trial_indicator_text_stimulus.setAutoDraw(True)
    trial_indicator_text_stimulus.setText(trial_text)

    # Send 'End trial' command through the LSL inlet
    outlet.push_sample(['End_of_Trial'])

    # Reset timer and wait the specified time
    countdown_time = core.CountdownTimer(after_trial_pause)
    event_index += 1
    event_matrix[0, event_index] = EVENT_REST
    event_matrix[1, event_index] = time.clock()

    while countdown_time.getTime() > 0:
        elapsed_time = clock_object.getTime()
        window_handle.flip()

    # Reset frame counters and rise running program flag
    frame_counter_left = 0
    frame_counter_right = 0
    frame_counter_up = 0
    frame_counter_down = 0
    frame_counter_face = 0

    # Reset command sequence and time variables
    executed_command = 0
    elapsed_time = 0
    clock_object.reset()
    command_time_counter = 1
    time_flip_counter = 0

# ----------------------------------------------------------------------------------------------------------------------
''' At this point all the scheduled trials for this session have finished. Display message and end'''
# Make invisible all stimulus
arrow_left.setAutoDraw(False)
arrow_right.setAutoDraw(False)
arrow_up.setAutoDraw(False)
arrow_down.setAutoDraw(False)
arrow_face.setAutoDraw(False)
focus_fixation.setAutoDraw(False)
square_face_ON.setAutoDraw(False)
square_left_ON.setAutoDraw(False)
square_left_OFF.setAutoDraw(False)
square_left_fixation.setAutoDraw(False)
square_right_ON.setAutoDraw(False)
square_right_OFF.setAutoDraw(False)
square_right_fixation.setAutoDraw(False)
square_up_ON.setAutoDraw(False)
square_up_OFF.setAutoDraw(False)
square_up_fixation.setAutoDraw(False)
square_down_ON.setAutoDraw(False)
square_down_OFF.setAutoDraw(False)
square_down_fixation.setAutoDraw(False)

window_handle.flip()
# Update and display text
trial_text = 'SSVEP Session has ended, all trials completed successfully. Closing..'
trial_indicator_text_stimulus.setText(trial_text)
window_handle.flip()

# Send 'End trial' command through the LSL inlet
outlet.push_sample(['End_of_Experiment'])

# Stop program and close OpenGL window
window_handle.flip()          # Flip screen one last time
core.wait(1)                  # Waiting half second improves stability
window_handle.close()

# Register the 'End-of-Session' event as a PAUSE event
event_index += 1
event_matrix[0, event_index] = EVENT_PAUSE
event_matrix[1, event_index] = time.clock()

# ----------------------------------------------------------------------------------------------------------------------
# Save event log and time reference
time_reference_filename = "Log_reference_time_"+str(reference_time[0])+"_"+str(reference_time[1])+"_" + \
                          str(reference_time[2])+"_"+str(reference_time[3])+"_"+str(reference_time[4]) + \
                          "_"+str(reference_time[5])+".txt"

reference_time_text = ['Year: ', 'Month: ', 'Day: ', 'Hour: ', 'Minute: ', 'Second: ', 'Microsecond: ']

time_reference_file_handle = open(time_reference_filename, 'w')
for list_item in range(len(reference_time)):
    time_reference_file_handle.write(str(reference_time_text[int(list_item)])+str(reference_time[int(list_item)])+'\n')
time_reference_file_handle.close()

event_log_filename = "Event_log"+str(reference_time[0])+"_"+str(reference_time[1])+"_" + \
                     str(reference_time[2])+"_"+str(reference_time[3])+"_"+str(reference_time[4]) + \
                     "_"+str(reference_time[5])+".csv"

np.savetxt(event_log_filename, event_matrix, delimiter=",")