
"""
Import necessary libraries and folders
"""
#  Imports from Arduino Related files
import time
import re
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
strPort = '/dev/ttyACM0' # MCU Port Name

#####################


# plot class
class AnalogPlot:
    # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(strPort, 115200)
        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.maxLen = maxLen
        line = self.ser.readline()

    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        assert (len(data) == 2)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])

    # update plot
    def update(self, frameNum, a0, a1):
        try:
            line = self.ser.readline()
            data = [float(val) for val in line.split()]
            print(data)
            # print data
            if (len(data) == 2):
                self.add(data)
                a0.set_data(range(self.maxLen), self.ax)
                a1.set_data(range(self.maxLen), self.ay)
        except KeyboardInterrupt:
            print('exiting')

        return a0,

        # clean up

    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()

    # Define point updater object
def update_line(num, iterator, ax,Aport,X,Y,Z):
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
    try:
        # First Attempt to read an angle value from the MCU Serial Port
        line = Aport.readline()
        Aport.write(b'value received')
        line = str(line,"utf-8")
        angle = int(re.sub("[^0-9]","",line))
    # If a misread occurs, try again
    except:
        # Second attempt to read an angle value from the MCU Serial Port
        print("Angle misread, second attempt")
        line = Aport.readline()
        # Aport.write(b'value received')
        line = str(line, "utf-8")
        angle = int(re.sub("[^0-9]", "", line))
    theta  = np.array([(np.radians(meas[1])) for meas in scan])
    R = np.array([meas[2] for meas in scan])
    phi = np.deg2rad(angle) # Test value in the phi angle, to be switched with Arduino object value
    
    # Perform Spherical to Cartesian Conversion and append overall lists
    X.append(R*np.sin(phi)*np.cos(theta))
    Y.append(R*np.sin(phi)*np.sin(theta))
    Z.append(R*np.cos(phi))
    # X = X[-20:]
    # Y = Y[-20:]
    # Z = Z[-20:]

    # Draw x and y lists
    offsets = np.array([X,Y,Z])
    ax.clear()
    ax.scatter3D(X, Y, Z)
    return X, Y, Z


# Setup Main run object
def run():
    print('MCU being reading from serial port %s...' % strPort)
    Aport = serial.Serial(strPort, 115200)
    print('RPlidar being reading from serial port %s...' % PORT_NAME)
    lidar = RPLidar(PORT_NAME) # Connect to the RPLidar Port
    iterator = lidar.iter_scans() # Object to pull scans from the RPLidar
    # An object to collect arduino readings must go here when thats complete!

    fig = plt.figure() # Create a figure object
    ax = fig.add_subplot(111, projection='3d') # Create plot axes object, 3D
    # Declare empty X,Y,Z
    X = []
    Y = []
    Z = []
    ax.scatter3D(X, Y, Z)  # initialize 3D Scatter Plot Object, does this need to be assigned to an object?
    ax.set_zlim(-2500, 2500)
    ax.set_xlim(-2500, 2500)
    ax.set_ylim(-2500, 2500)

    # Send Conduit Crawler Initialization Commands

    # Begin matplotlib animation function
    # Update Interval is every 10ms
    ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, ax,Aport,X,Y,Z), interval=100)
    """
    animation.FuncAnimation arguments:
    class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, **kwargs)
    
    fig -> figure object
    
    func -> The function to call at each frame. The first argument will be the next value in frames. 
    Any additional positional arguments can be supplied via the fargs parameter.
    
    fargs -> Additional arguments to pass to each call to func.
    
    interval -> Delay between frames in milliseconds. Defaults to 200.
    
    save_count -> int, optional The number of values from frames to cache.
    """

    # Show the developed plot, this is called and remains open until a keyboard interrupt or plot is closed
    plt.show()
    
    # After Keyboard Interrupt occurs....
    lidar.stop() # RPLidar Scanner Stops
    lidar.stop_motor() # Scanner Motor Stops
    lidar.disconnect() # Disconnect from RPLidar
    

    
if __name__ == '__main__':
    run()


'''
Simple file operations that could be used
open()
File_
remember to close the file after use
forces to write everything at the very end
Write a simple file on its own to operate the files like you want
append or delete previous data
Can make a new file every time
'''