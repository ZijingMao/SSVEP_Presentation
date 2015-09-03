# Modified from
# https://github.com/psychopy/psychopy/blob/master/psychopy/demos/coder/stimuli/starField.py

from psychopy import visual, event
from psychopy.tools.coordinatetools import pol2cart
import numpy

# ---- Create a full-screen window with invisible mouse, collect real monitor refresh rate ----
window_handle = visual.Window([1920, 1080], fullscr=False, winType='pyglet', monitor='testMonitor',
                              units='norm', screen=1, color=[-1, -1, -1], colorSpace='rgb')

monitor_frame_rate = int(window_handle.getActualFrameRate())
window_handle.setMouseVisible(False)


# The number of dots
nDots = 500
# The maximum speed of the dots
maxSpeed = 10
# The size of the field. Note that you also need to modify the `fieldSize`
# keyword that is passed to `ElementArrayStim` below, due to (apparently) a bug
# in PsychoPy
fieldSize = 200
# The size of the dots
dotSize = 2
# The number of frames
nFrames = 1000

# Initial parameters
dotsTheta = numpy.random.rand(nDots)*360
dotsRadius = (numpy.random.rand(nDots)**0.5)*200
speed = numpy.random.rand(nDots)*maxSpeed

# Create the stimulus array
dots = visual.ElementArrayStim(window_handle, elementTex=None, fieldShape='circle',
                               elementMask='circle', nElements=nDots, sizes=dotSize,
                               units='pix', fieldSize=10000)

# Walk through each frame, update the dot positions and draw it
for frameN in range(100):
    # update radius
    dotsRadius = (dotsRadius+speed)
    # random radius where radius too large
    outFieldDots = (dotsRadius>=fieldSize)
    dotsRadius[outFieldDots] = numpy.random.rand(sum(outFieldDots))*fieldSize
    dotsX, dotsY = pol2cart(dotsTheta,dotsRadius)
    dots.setXYs(numpy.array([dotsX, dotsY]).transpose())
    dots.draw() 
    window_handle.flip()