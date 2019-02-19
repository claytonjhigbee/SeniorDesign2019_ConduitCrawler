
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
Z = 0

#####################

# Define point updater object
def update_line(num, iterator, scatter,ax):
    scan = next(iterator)
    """
    Iterator returns 3 arguments:
    meas(0) -> quality : int
            Reflected laser pulse strength
    Meas(1) -> angle : float
            The measurement heading angle in degree unit [0, 360)
    meas(2) -> distance : float
            Measured object distance related to the sensor's rotation center.
            In millimeter unit. Set to 0 when measurement is invalid. 
    """
    # Pass measurements to related variables
    theta  = np.array([(np.radians(meas[1])) for meas in scan])
    R = np.array([meas[2] for meas in scan])
    phi = np.pi/2 # Test value in the phi angle, to be switched with Arduino object value
    
    # Perform Spherical to Cartesian Conversion
    X = R*np.sin(phi)*np.cos(theta)
    Y = R*np.sin(phi)*np.sin(theta)
    Z = R*np.cos(phi)
    
    offsets = np.array([X,Y,Z])
    scatter = ax.scatter3D(X, Y, Z)
    # I don't really understand the set_offsets call. Is this a general matplotlib function that passes arguments?
    # See this: https://matplotlib.org/api/collections_api.html and the small section on set_offsets()
    # intens = np.array([meas[0] for meas in scan]) - I dont think we need this argument passed
    # scatter.set_array(intens) - Or this one
    return scatter, X, Y, Z


# Setup Main run object
def run():
    lidar = RPLidar(PORT_NAME) # Connect to the RPLidar Port
    iterator = lidar.iter_scans() # Object to pull scans from the RPLidar
    # An object to collect arduino readings must go here when thats complete!

    fig = plt.figure() # Create a figure object
    ax = fig.add_subplot(111, projection='3d') # Create plot axes object, 3D
    scatter = ax.scatter3D(0, 0, 0)  # Define 3D Scatter Plot Object, This needs to be assigned to an object?
    ax.set_zlim(-2500, 2500)
    ax.set_xlim(-2500, 2500)
    ax.set_ylim(-2500, 2500)

    
    # matplotlib animation function
    ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, scatter, ax), interval=50)
    """
    animation.FuncAnimation arguments:
    class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, **kwargs)
    
    fig -> figure object
    
    func -> The function to call at each frame. The first argument will be the next value in frames. 
    Any additional positional arguments can be supplied via the fargs parameter.
    
    fargs -> Additional arguments to pass to each call to func.
    
    interval -> Delay between frames in milliseconds. Defaults to 200.
    """

        
    plt.show()
    
    # After Keyboard Interrupt occurs....
    lidar.stop() # RPLidar Scanner Stops
    lidar.stop_motor() # Scanner Motor Stops
    lidar.disconnect() # Disconnect from RPLidar
    

    
if __name__ == '__main__':
    run()



