"""
Conversion Notes from Spherical to Cartesian System
Refer to image on conversion information
"""

"""
# Conversion information: http://tutorial.math.lamar.edu/Classes/CalcIII/SphericalCoords.aspx
R - radial distance from the origin
theta - Angle between X axis and point
phi - Angle between Z axis and point
"""
import numpy as np
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


# This simulates one plane of a LIDAR Scan
R = np.ones(16)*2
phi = np.pi*np.ones(16)/6
theta = np.arange(0,np.pi/2,0.1)

X = R*np.sin(phi)*np.cos(theta)
Y = R*np.sin(phi)*np.sin(theta)
Z = R*np.cos(phi)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface.
ax.scatter3D(X, Y, Z, cmap='Greens')

# Tweak the limits and add latex math labels.
ax.set_zlim(0, 2.5)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)


plt.show()
