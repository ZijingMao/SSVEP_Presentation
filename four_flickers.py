# Author: Mauricio Merino, BASED on the code by John Naulty. March of 2015
from psychopy import visual, event, core
import Image, time, pylab, cv, numpy


#----- Configure Window -----
mywin= visual.Window([1280, 800], fullscr=False, monitor='testMonitor',units='deg')
monitor_framerate = mywin.getActualFrameRate()
mywin.setMouseVisible(False)
clock_object = core.Clock()


#------ Create stimulus -----
# Left square
number_frames_1 = 3
square_left_ON = visual.GratingStim(win=mywin, name='pattern11', units='cm', tex=None,
                              mask=None, ori=0, pos = [-15, 0], size=4, sf=1,
                              phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-1.0)

square_left_OFF = visual.GratingStim(win=mywin, name='pattern12', units='cm', tex=None,
                              mask=None, ori=0, pos = [-15, 0], size=4, sf=1,
                              phase=0, color=[-1, -1, -1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-2.0)

square_left_fixation = visual.GratingStim(win=mywin, size = 0.3, pos=[-15,0], sf=0, rgb=-1)


# Right square
number_frames_2 = 5
square_right_ON = visual.GratingStim(win=mywin, name='pattern21', units='cm', tex=None,
                              mask=None, ori=0, pos = [15, 0], size=4, sf=1,
                              phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-1.0)

square_right_OFF = visual.GratingStim(win=mywin, name='pattern22', units='cm', tex=None,
                              mask=None, ori=0, pos = [15, 0], size=4, sf=1,
                              phase=0, color=[-1, -1, -1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-2.0)

square_right_fixation = visual.GratingStim(win=mywin, size = 0.3, pos=[15,0], sf=0, rgb=-1)


# Up square
number_frames_3 = 1
square_up_ON = visual.GratingStim(win=mywin, name='pattern31', units='cm', tex=None,
                              mask=None, ori=0, pos = [0, 8], size=4, sf=1,
                              phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-1.0)

square_up_OFF = visual.GratingStim(win=mywin, name='pattern32', units='cm', tex=None,
                              mask=None, ori=0, pos = [0, 8], size=4, sf=1,
                              phase=0, color=[-1, -1, -1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-2.0)

square_up_fixation = visual.GratingStim(win=mywin, size = 0.3, pos=[0,8], sf=0, rgb=-1)


# Down square
number_frames_4 = 2
square_down_ON = visual.GratingStim(win=mywin, name='pattern41', units='cm', tex=None,
                              mask=None, ori=0, pos = [0, -8], size=4, sf=1,
                              phase=0.0, color=[1, 1, 1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-1.0)

square_down_OFF = visual.GratingStim(win=mywin, name='pattern42', units='cm', tex=None,
                              mask=None, ori=0, pos = [0, -8], size=4, sf=1,
                              phase=0, color=[-1, -1, -1], colorSpace='rgb',
                              opacity=1, texRes=256, interpolate=True, depth=-2.0)

square_down_fixation = visual.GratingStim(win=mywin, size = 0.3, pos=[0,-8], sf=0, rgb=-1)



#------ Include an STATIC texts stimulus on the Center-top of the screen -----
# Compute flickers frequencies
frequency1 = monitor_framerate/ (2 * number_frames_1)
frequency2 = monitor_framerate/ (2 * number_frames_2)
frequency3 = monitor_framerate/ (2 * number_frames_3)
frequency4 = monitor_framerate/ (2 * number_frames_4)

# Generate text string
static_text = 'SSVEP Test. Frequencies (Hz). L: '\
              +str(int(frequency1))+', R: '\
              +str(int(frequency2))+', Up: '\
              +str(int(frequency3))+', Dn: '\
              +str(int(frequency4))

# Create stimulus
message1 = visual.TextStim(win=mywin, text=static_text, pos = [0, 3])
message1.size = 2
message1.setAutoDraw(True)

#------ Include an DYNAMIC text stimulus on the Center of the screen -----
message2 = visual.TextStim(win=mywin, text='Frame rate', pos = [0, -4])
message2.setAutoDraw(True)


#----- Run SSVEP simulation (loops forever until a key is pressed) -------

# Define counters and boolean flags
frame_lap = 0
frame_time = 0
frame_counter = 0
frame_counter_1 = 0
frame_counter_2 = 0
frame_counter_3 = 0
frame_counter_4 = 0

switch_stim1 = False
switch_stim2 = False
switch_stim3 = False
switch_stim4 = False


# Start frame loops
run_program = True
while run_program:

    # Increase frame counters
    frame_counter = frame_counter + 1
    frame_counter_1 = frame_counter_1 + 1
    frame_counter_2 = frame_counter_2 + 1
    frame_counter_3 = frame_counter_3 + 1
    frame_counter_4 = frame_counter_4 + 1

    # When number_frames is reached, switch stimulus (Stim 1)
    if frame_counter_1 == number_frames_1:
        frame_counter_1 = 0
        switch_stim1 = not(switch_stim1)


    # When number_frames is reached, switch stimulus (Stim 2)
    if frame_counter_2 == number_frames_2:
        frame_counter_2 = 0
        switch_stim2 = not(switch_stim2)


    # When number_frames is reached, switch stimulus (Stim 3)
    if frame_counter_3 == number_frames_3:
        frame_counter_3 = 0
        switch_stim3 = not(switch_stim3)


    # When number_frames is reached, switch stimulus (Stim 4)
    if frame_counter_4 == number_frames_4:
        frame_counter_4 = 0
        switch_stim4 = not(switch_stim4)


    # As long switch_stim1 is TRUE, show the ON, otherwise, show OFF (stimulus 1)
    if switch_stim1:
        square_left_ON.setAutoDraw(True)
        square_left_fixation.setAutoDraw(True)
        square_left_OFF.setAutoDraw(False)
    else:
        square_left_ON.setAutoDraw(False)
        square_left_fixation.setAutoDraw(True)
        square_left_OFF.setAutoDraw(True)


    # As long switch_stim2 is TRUE, show the ON, otherwise, show OFF (stimulus 2)
    if switch_stim2:
        square_right_ON.setAutoDraw(True)
        square_right_fixation.setAutoDraw(True)
        square_right_OFF.setAutoDraw(False)
    else:
        square_right_ON.setAutoDraw(False)
        square_right_fixation.setAutoDraw(True)
        square_right_OFF.setAutoDraw(True)


    # As long switch_stim3 is TRUE, show the ON, otherwise, show OFF (stimulus 3)
    if switch_stim3:
        square_up_ON.setAutoDraw(True)
        square_up_fixation.setAutoDraw(True)
        square_up_OFF.setAutoDraw(False)
    else:
        square_up_ON.setAutoDraw(False)
        square_up_fixation.setAutoDraw(True)
        square_up_OFF.setAutoDraw(True)


    # As long switch_stim4 is TRUE, show the ON, otherwise, show OFF (stimulus 4)
    if switch_stim4:
        square_down_ON.setAutoDraw(True)
        square_down_fixation.setAutoDraw(True)
        square_down_OFF.setAutoDraw(False)
    else:
        square_down_ON.setAutoDraw(False)
        square_down_fixation.setAutoDraw(True)
        square_down_OFF.setAutoDraw(True)


    # Reset monitor frame counter after ~ 1 second, capture time
    if frame_counter == int(monitor_framerate):
        frame_counter = 0
        frame_lap = frame_lap + 1
        frame_time = clock_object.getTime()

        # Update the Text stimulus with some information (frame couter)
        stim_text = str(frame_lap)+" Monitor refreshes in Apox. :"+str(frame_time)
        message2.setText(stim_text)


    # Flip the screen
    mywin.flip()


# Close window
mywin.flip()
core.wait(1.0)
mywin.close()
