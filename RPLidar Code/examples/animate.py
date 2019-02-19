#!/usr/bin/env python3
'''Animates distances and measurement quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits import mplot3d

PORT_NAME = '/dev/ttyUSB1'
DMAX = 2000
IMIN = 0
IMAX = 50

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run(): # Added ax1 to change grid setup to 3d., remove ax1
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax1 = plt.axes(projection = '3d')
    #ax = plt.subplot(111, projection='polar')  #
    line = ax1.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    #ax1.set_rmax(DMAX)
    ax1.grid(True)

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    lidar.stop_motor()

if __name__ == '__main__':
    run()
