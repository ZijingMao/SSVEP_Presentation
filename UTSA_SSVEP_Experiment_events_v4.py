__author__ = 'EEGLAB'
"""UTSA SSVEP experiment v1, using a procedural approach and everything exposed into a single file
Author: Mauricio Merino, Yufei Huang EEg Laboratory, University of Texas at San Antonio. April 2015
This code is BASED on the code by John Naulty. This version is hardcoded for a 24 inches monitor or bigger"""

# ---- Include required modules from Psychopy API ----
from psychopy import visual, core, logging
import time
from pylsl import StreamInfo, StreamOutlet
# ----------------------------------------------------------------------------------------------------------------------


# ---------------------------------- Configure the SSVEP Presentation Program ------------------------------------------
# Command sequence
base_sequence = ['Left', 'Face', 'Up', 'Extra', 'Right', 'Down']
number_sequence_cycles = 3
command_sequence = base_sequence * number_sequence_cycles

# Program duration (based on command sequence)
number_of_trials = 3
after_trial_pause = 90
command_display_time = 7
fixation_display_time = 3

# Flickering frequency for the Up-Down-Left-Right stimulus
monitor_to_use = 1
square_left_number_frames = 3    # 3 frames ON and 3 frames OFF to make 10 Hz
square_right_number_frames = 5   # 5 frames ON and 5 frames OFF to make 6 Hz
square_up_number_frames = 4      # 4 frames ON and 4 frames OFF to make 7.5 Hz
square_down_number_frames = 4    # 4 frames ON BUT 3 frames OFF to make 8.57 Hz

# Create LSL inlet and send the first event "Waiting..." during the pause everything is being set up
info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'Experiment01')
outlet = StreamOutlet(info)
outlet.push_sample(['Waiting...'])
time.sleep(1)

# Create an artificial pause to give time to prepare LSL recording externally
clock_object = core.Clock()
recording_pause = 10
countdown_time = core.CountdownTimer(recording_pause)
while countdown_time.getTime() > 0:
    elapsed_time = clock_object.getTime()
clock_object.reset()
elapsed_time = 0
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# ---- Create a full-screen window with invisible mouse, collect real monitor refresh rate ----
window_handle = visual.Window([1920, 1080], fullscr=True, winType='pyglet', monitor='testMonitor', units='deg',
                              screen=monitor_to_use, color=[-1, -1, -1], colorSpace='rgb')

# Enable frame monitoring and logging (to detect drop frames)
monitor_frame_rate = int(window_handle.getActualFrameRate())
window_handle.setMouseVisible(False)
window_handle.flip()
window_handle.setRecordFrameIntervals(True)
window_handle._refreshThreshold = (1/60.0) + 0.004  # 60Hz monitor and 4 ms of tolerance
logging.console.setLevel(logging.WARNING)
window_handle.flip()
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# ---- Create FLICKERING SQUARES, fixation, arrows and text stimulus (ALL in Invisible mode at first) -----
square_left_ON = visual.GratingStim(win=window_handle, name='leftON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[-25, 0], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
square_left_OFF = visual.GratingStim(win=window_handle, name='leftOFF', units='cm', tex=None, mask=None, ori=0,
                                     pos=[-25, 0], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                     opacity=0.93, texRes=256, interpolate=True, depth=-2.0)
square_right_ON = visual.GratingStim(win=window_handle, name='rightON', units='cm', tex=None, mask=None, ori=0,
                                     pos=[25, 0], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                     opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
square_right_OFF = visual.GratingStim(win=window_handle, name='rightOFF', units='cm', tex=None, mask=None, ori=0,
                                      pos=[25, 0], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                      opacity=0.93, texRes=256, interpolate=True, depth=-2.0)
square_up_ON = visual.GratingStim(win=window_handle, name='upON', units='cm', tex=None, mask=None, ori=0,
                                  pos=[0, 13], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                  opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
square_up_OFF = visual.GratingStim(win=window_handle, name='upOFF', units='cm', tex=None, mask=None, ori=0,
                                   pos=[0, 13], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                   opacity=0.94, texRes=256, interpolate=True, depth=-2.0)
square_down_ON = visual.GratingStim(win=window_handle, name='downON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[0, -13], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
square_down_OFF = visual.GratingStim(win=window_handle, name='downOFF', units='cm', tex=None, mask=None, ori=0,
                                     pos=[0, -13], size=3, sf=1, phase=0, color=[-1, -1, -1], colorSpace='rgb',
                                     opacity=0.93, texRes=256, interpolate=True, depth=-2.0)
square_face_ON = visual.GratingStim(win=window_handle, name='downON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[-25, 13], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
square_face_OFF = visual.GratingStim(win=window_handle, name='downON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[-25, 13], size=3, sf=1, phase=0.0, color=[-1, -1, -1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
square_extra_ON = visual.GratingStim(win=window_handle, name='downON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[25, 13], size=3, sf=1, phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
square_extra_OFF = visual.GratingStim(win=window_handle, name='downON', units='cm', tex=None, mask=None, ori=0,
                                    pos=[25, 13], size=3, sf=1, phase=0.0, color=[-1, -1, -1], colorSpace='rgb',
                                    opacity=0.93, texRes=256, interpolate=True, depth=-1.0)
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
arrow_extra = visual.ImageStim(win=window_handle, image='arrow_right.jpg', mask=None, units='', pos=[20, 13], size=None,
                              ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, opacity=1.0, depth=0,
                              interpolate=False, flipHoriz=False, flipVert=False, texRes=256, name=None,
                              autoLog=None, maskParams=None)

focus_fixation = visual.GratingStim(win=window_handle, mask='cross', name='bigFixation', size=1.2, pos=[0, 0], sf=0)
trial_indicator_text_stimulus = visual.TextStim(win=window_handle, text=' ', pos=[0, -3])
square_extra_fixation = visual.GratingStim(win=window_handle, size=0.2, pos=[25, 13], sf=0,
                                           color=[-1, -1, -1], colorSpace='rgb')

square_face_fixation = visual.GratingStim(win=window_handle, size=0.2, pos=[-25, 13], sf=0,
                                          color=[-1, -1, -1], colorSpace='rgb')

square_down_fixation = visual.GratingStim(win=window_handle, size=0.2, pos=[0, -13], sf=0,
                                          color=[-1, -1, -1], colorSpace='rgb')

square_up_fixation = visual.GratingStim(win=window_handle, size=0.2, pos=[0, 13], sf=0,
                                        color=[-1, -1, -1], colorSpace='rgb')

square_right_fixation = visual.GratingStim(win=window_handle, size=0.2, pos=[25, 0],
                                           sf=0, color=[-1, -1, -1], colorSpace='rgb')

square_left_fixation = visual.GratingStim(win=window_handle, size=0.2, pos=[-25, 0],
                                          sf=0, color=[-1, -1, -1], colorSpace='rgb')
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# ---- Configure the flickering frequencies of square stimulus and experiment commands and length ----

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
arrow_extra.setAutoDraw(False)
focus_fixation.setAutoDraw(False)
trial_indicator_text_stimulus.setAutoDraw(True)

# Boolean flags fro stimulus switching
switch_flag_left = False
switch_flag_right = False
switch_flag_up = False
switch_flag_down = False
arrow_display = False

# Counters for stimulus switching
switch_flag_face = 1
switch_flag_extra = 1
sequence_counter = 0
sequence_counter_extra = 0
frame_counter_down = 0
frame_counter_left = 0
frame_counter_up = 0
frame_counter_right = 0
command_time_counter = 1
time_flip_counter = 0
executed_command = 0
trial_done = 0
event_index = -1
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
'''       Main Loop of the SSVEP presentation program: Trials => Sequence => Time => Monitor frames     '''

# --- Loop through trials
for current_trial in range(number_of_trials):
    # For each trial complete a command sequence

    # Activate the fixation marks for the flicker squares (stimulus)
    square_left_fixation.setAutoDraw(True)
    square_right_fixation.setAutoDraw(True)
    square_up_fixation.setAutoDraw(True)
    square_down_fixation.setAutoDraw(True)
    square_extra_fixation.setAutoDraw(True)
    square_face_fixation.setAutoDraw(True)

    # An inner loop to navigate through the command sequence (current trial)
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

        # ======================== 10.9Hz (Top-Left Flicker) =========================
        if switch_flag_face == 1:
            sequence_counter += 1
            square_face_ON.draw()

            if sequence_counter == 3:
                switch_flag_face = 2
                sequence_counter = 0

        elif switch_flag_face == 2:
            sequence_counter += 1
            square_face_OFF.draw()

            if sequence_counter == 2:
                switch_flag_face = 3
                sequence_counter = 0

        elif switch_flag_face == 3:
            sequence_counter += 1
            square_face_ON.draw()

            if sequence_counter == 3:
                switch_flag_face = 4
                sequence_counter = 0

        elif switch_flag_face == 4:
            sequence_counter += 1
            square_face_OFF.draw()

            if sequence_counter == 3:
                switch_flag_face = 1
                sequence_counter = 0
        # ==============================================================================================================

        # ======================== 13.3Hz (Top-Right Flicker) =========================
        if switch_flag_extra == 1:
            sequence_counter_extra += 1
            square_extra_ON.draw()

            if sequence_counter_extra == 2:
                switch_flag_extra = 2
                sequence_counter_extra = 0

        elif switch_flag_extra == 2:
            sequence_counter_extra += 1
            square_extra_OFF.draw()

            if sequence_counter_extra == 2:
                switch_flag_extra = 3
                sequence_counter_extra = 0

        elif switch_flag_extra == 3:
            sequence_counter_extra += 1
            square_extra_ON.draw()

            if sequence_counter_extra == 3:
                switch_flag_extra = 4
                sequence_counter_extra = 0

        elif switch_flag_extra == 4:
            sequence_counter_extra += 1
            square_extra_OFF.draw()

            if sequence_counter_extra == 2:
                switch_flag_extra = 1
                sequence_counter_extra = 0
        # ==============================================================================================================

        # Check boolean flags: True is for ON stimulus, False is for OFF stimulus
        # Left Stimulus
        if switch_flag_left:
            square_left_ON.draw()
        else:
            square_left_OFF.draw()

        # Right Stimulus
        if switch_flag_right:
            square_right_ON.draw()
        else:
            square_right_OFF.draw()

        # Up Stimulus
        if switch_flag_up:
            square_up_ON.draw()
        else:
            square_up_OFF.draw()

        # Down Stimulus
        if switch_flag_down:
            square_down_ON.draw()
        else:
            square_down_OFF.draw()
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
        ''' Based on current command from the sequence, display a pointing arrow '''

        # ---- If showing arrows is selected, choose arrow and draw it
        if arrow_display:

            # Display left arrow if it is on sequence
            if current_command == "Left":
                arrow_left.draw()

            # Display right arrow if it is on sequence
            if current_command == "Right":
                arrow_right.draw()

            # Display left arrow if it is on sequence
            if current_command == "Up":
                arrow_up.draw()

            # Display down arrow if it is on sequence
            if current_command == "Down":
                arrow_down.draw()

            # Display face arrow if it is on sequence
            if current_command == "Face":
                arrow_face.draw()

            # Display EXTRA arrow if it is on sequence
            if current_command == "Extra":
                arrow_extra.draw()

        else:
            focus_fixation.draw()   # If Fixation cross is activated, display it, Make fixation visible
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
        ''' Arrow OR Fixation has been displayed, check execution time if reached 5 seconds for another switch '''

        # Check if the specified command execution time has occurred
        elapsed_time = clock_object.getTime()   # Get the current elapsed time
        duration_elapsed = (elapsed_time > int(command_display_time * (command_time_counter - 1))) and \
                           (elapsed_time <= int(command_display_time * command_time_counter))

        if duration_elapsed:

            # The 5 seconds have passed, change to fixation mode and increase command time counter
            command_time_counter += 1
            arrow_display = not arrow_display
            time_flip_counter += 1

            # Check for arrow event or cross and capture command to be send to LSL
            event_index += 1
            if arrow_display:
                LSL_send_command = current_command
            else:
                LSL_send_command = 'Cross'

            # After the event has been recorded also transmit it through the LSL inlet
            outlet.push_sample([LSL_send_command])

            # Detect when a command has been completed
            if time_flip_counter == 2:
                time_flip_counter = 0
                executed_command += 1

    # Count a trial that has finished
    trial_done += 1
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
    ''' At this point current trial has finished: stop flickering and pause for the specified time'''

    # Refresh screen
    window_handle.flip(clearBuffer=True)

    # Make invisible all stimulus
    # Arrows
    arrow_left.setAutoDraw(False)
    arrow_right.setAutoDraw(False)
    arrow_up.setAutoDraw(False)
    arrow_down.setAutoDraw(False)
    arrow_face.setAutoDraw(False)
    arrow_extra.setAutoDraw(False)

    # Fixation marks
    square_left_fixation.setAutoDraw(False)
    square_right_fixation.setAutoDraw(False)
    square_up_fixation.setAutoDraw(False)
    square_down_fixation.setAutoDraw(False)
    square_face_fixation.setAutoDraw(False)
    square_extra_fixation.setAutoDraw(False)
    focus_fixation.setAutoDraw(False)

    # Flickering squares (ON)
    square_up_ON.setAutoDraw(False)
    square_down_ON.setAutoDraw(False)
    square_left_ON.setAutoDraw(False)
    square_right_ON.setAutoDraw(False)
    square_face_ON.setAutoDraw(False)
    square_extra_ON.setAutoDraw(False)

    # Flickering squares (OFF)
    square_up_OFF.setAutoDraw(False)
    square_down_OFF.setAutoDraw(False)
    square_left_OFF.setAutoDraw(False)
    square_right_OFF.setAutoDraw(False)
    square_face_OFF.setAutoDraw(False)
    square_extra_OFF.setAutoDraw(False)

    # Make visible the text stimulus for end-of-trial message
    trial_indicator_text_stimulus.setAutoDraw(True)

    # Send 'End trial' command through the LSL inlet
    outlet.push_sample(['End_of_Trial'])

    # Reset timer and wait the specified time
    elapsed_time = 0
    clock_object.reset()
    countdown_time = core.CountdownTimer(after_trial_pause)
    while countdown_time.getTime() > 0:
        elapsed_time = clock_object.getTime()

        # Update count-down counter on the Screen
        remaining_time_str = "{0:.1f}".format(after_trial_pause - elapsed_time)
        trial_text = 'Trial '+str(trial_done)+' has ended!. You will have '+remaining_time_str+' seconds to rest'
        trial_indicator_text_stimulus.setText(trial_text)
        window_handle.flip()

    # Prepare to launch a new trial: reset time and counters
    frame_counter_left = 0
    frame_counter_right = 0
    frame_counter_up = 0
    frame_counter_down = 0
    executed_command = 0
    elapsed_time = 0
    command_time_counter = 1
    time_flip_counter = 0
    window_handle.flip()
    clock_object.reset()
# ----------------------------------------------------------------------------------------------------------------------


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

# Update and display text
window_handle.flip()
trial_text = 'SSVEP Session has ended, all trials completed successfully. Closing..'
trial_indicator_text_stimulus.setText(trial_text)
window_handle.flip()

# Send 'End trial' command through the LSL inlet
outlet.push_sample(['End_of_Experiment'])

# Stop program and close OpenGL window
window_handle.flip()          # Flip screen one last time
core.wait(1)                  # Waiting half second improves stability
window_handle.close()
# ----------------------------------------------------------------------------------------------------------------------
