
"""
Import necessary libraries and folders
"""
#  Imports from Arduino Related files
import sys, serial, argparse
from collections import deque
import re
#  Imports Related to RPLidar files
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits import mplot3d
from statistics import mode

#  Declarations/Variables
PORT_NAME = '/dev/ttyUSB1' #  RPLidar Port Name
strPort = '/dev/ttyUSB0' # MCU Port Name

#####################

    # Define point updater object
def update_line(num, iterator,ax,Aport,lidar,Xs,Ys,Zs,i=[0]):
    checkbit = 0
    iterbit = 0
    checkbit = str(num)
    checkbit = checkbit[-1]
    checkbit = int(checkbit)
    if (checkbit == 0):
        iterbit = 0
    if (checkbit == 1):
        iterbit = 1
    if (checkbit == 2):
        iterbit = 2
    if (checkbit == 3):
        iterbit = 3
    if (checkbit == 4 ):
        iterbit = 4
    if (checkbit == 5 ):
        iterbit = 5
    if (checkbit == 6 ):
        iterbit = 6
    if (checkbit == 7 ):
        iterbit = 7
    if (checkbit == 8 ):
        iterbit = 8
    if (checkbit == 9 ):
        iterbit = 9

    try:
        scan = next(iterator)
    except:
        print("Second attempt for a Lidar Scan")
        lidar = RPLidar(PORT_NAME)  # Connect to the RPLidar Port
        iterator = lidar.iter_scans()  # Object to pull scans from the RPLidar
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
    Aport = serial.Serial(strPort, 115200)
    try:
        # First Attempt to read an angle value from the MCU Serial Port
        line = Aport.readline()
        #Aport.write(b'value received')
        line = str(line,"utf-8")
        angle = int(re.sub("[^0-9]","",line))
    # If a misread occurs, try again
    except:
        # Second attempt to read an angle value from the MCU Serial Port
        # print("Angle misread, second attempt")
        line = Aport.readline()
        # Aport.write(b'value received')
        line = str(line, "utf-8")
        angle = int(re.sub("[^0-9]", "", line))
    angle = (angle) * 0.3515625
    # Affine Transform:
    angle = np.deg2rad(angle)
    # print(angle)
    theta  = np.array([(np.radians(meas[1])) for meas in scan])
    R = np.array([meas[2] for meas in scan])
    phi = np.pi/2

    newtheta = []
    newR = []
    for i in range(len(theta)):
        if (theta[i] >= 0) & (theta[i] <= np.pi):
            newtheta.append(theta[i])
            newR.append(R[i])

    newtheta = np.array(newtheta)
    newR = np.array(newR)

    # Perform Spherical to Cartesian Conversion
    X = newR * np.sin(phi) * np.cos(newtheta)
    Y = newR * np.sin(phi) * np.sin(newtheta)
    Z = newR * np.cos(phi)

    Rotate = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
    V = np.array([[X], [Y], [Z]])

    Xnew = np.take(Rotate, 0) * X + np.take(Rotate, 1) * Y + np.take(Rotate, 2) * Z
    Ynew = np.take(Rotate, 3) * X + np.take(Rotate, 4) * Y + np.take(Rotate, 5) * Z
    Znew = np.take(Rotate, 6) * X + np.take(Rotate, 7) * Y + np.take(Rotate, 8) * Z

    rows = 2
    columns = 500
    differenceX = columns - len(Xnew)
    storezeroX = np.zeros(shape=(1, differenceX))
    appendX = np.append(Xnew, storezeroX)
    differenceY = columns - len(Ynew)
    storezeroY = np.zeros(shape=(1, differenceY))
    appendY = np.append(Ynew, storezeroY)
    differenceZ = columns - len(Znew)
    storezeroZ = np.zeros(shape=(1, differenceZ))
    appendZ = np.append(Znew, storezeroZ)


    Xs[iterbit] = appendX
    Ys[iterbit] = appendY
    Zs[iterbit] = appendZ
    print(angle)
    ax.clear()
    myn = 500
    ax.set_zlim(-1*myn, myn)
    ax.set_xlim(-1*myn, myn)
    ax.set_ylim(-1*myn, myn)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.scatter3D(Xs, Ys, Zs, c='r',s = 1)
    return  Xs, Ys, Zs

# Setup Main run object
def run():
    print('MCU read from serial port %s...' % strPort)
    Aport = serial.Serial(strPort, 115200)
    print('RPLidar read from serial port %s...' % PORT_NAME)
    lidar = RPLidar(PORT_NAME) # Connect to the RPLidar Port
    iterator = lidar.iter_scans() # Object to pull scans from the RPLidar
    # An object to collect arduino readings must go here when thats complete!

    # Declare empty Cartesien Coordinates
    rows = 10
    columns = 500
    Xs = np.zeros(shape = (rows,columns))
    Ys = np.zeros(shape = (rows,columns))
    Zs = np.zeros(shape = (rows,columns))

    fig = plt.figure() # Create a figure object
    ax = fig.add_subplot(111, projection='3d') # Create plot axes object, 3D
    ax.scatter3D(0, 0, 0)  # 3D Scatter Plot, This needs to be assigned to an object?

    # Begin matplotlib animation function
    # Save up to 50 samples and update interval is every 100ms
    ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, ax, Aport,lidar,Xs,Ys,Zs), interval=5)
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
    print('I am here once')
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