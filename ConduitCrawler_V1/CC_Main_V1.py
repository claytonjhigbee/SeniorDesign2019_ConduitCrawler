
"""
Import necessary libraries and folders
"""
#  Imports from Arduino Related files
import time
start_time = time.time()
import sys, serial, argparse
from time import sleep
from collections import deque
import matplotlib.animation as animation

#  Imports Related to RPLidar files
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits import mplot3d

#  Declarations/Variables
PORT_NAME = '/dev/ttyUSB0' #  RPLidar Port Name
DMAX = 500 #  ?
IMIN = 0 #  ?
IMAX = 50 #  ?

"""
Class and Object Definitions
"""

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure() #
    ax = plt.axes(projection = 'polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()



"""
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import



# Fixing random state for reproducibility
np.random.seed(19680801)


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()


#####################

# Define point updater object
def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,


# Setup Main run object
def run():
    lidar = RPLidar(PORT_NAME) # Connect to the RPLidar Port
    fig = plt.figure() # Create a figure object
    
    ax = fig.add_subplot(111, projection='3d') # Create plot axes object , 3D
    
    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
        
    ax.scatter3D(X, Y, Z, c=c, marker=m) # Define 3D Scatter Plot Object, This needs to be assigned to an object?    
        
        
    plt.show()
    
    # After Keyboard Interrupt occurs....
    lidar.stop() # RPLidar Scanner Stops
    lidar.stop_motor() # Scanner Motor Stops
    lidar.disconnect() # Disconnect from RPLidar
    
    
    
    # Tweak the limits and add latex math labels.
    ax.set_zlim(0, 2.5)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    
if __name__ == '__main__':
    run()

"""

"""
Main Program Seat
Current code is only for the RPLIDAR polar animation plot
# Feb 4th, 2019 - Beginning to code in the 3D plot system, 
"""
if __name__ == '__main__':
    run()
