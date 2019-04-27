import numpy as np
import matplotlib.pyplot as plt


def X_Rotate(X, Y, Z, Angle):
    Xnew = np.take(Rotate, 0) * X + np.take(Rotate, 1) * Y + np.take(Rotate, 2) * Z
    Ynew = np.take(Rotate, 3) * X + np.take(Rotate, 4) * Y + np.take(Rotate, 5) * Z
    Znew = np.take(Rotate, 6) * X + np.take(Rotate, 7) * Y + np.take(Rotate, 8) * Z
    # Pass measurements to related variables
    Rotate = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])

    # Perform Spherical to Cartesian Conversion
    X = R * np.sin(phi) * np.cos(theta)
    Y = R * np.sin(phi) * np.sin(theta)
    Z = R * np.cos(phi)

    offsets = np.array([X, Y, Z])
    scatter = ax.scatter3D(X, Y, Z)
    # I don't really understand the set_offsets call. Is this a general matplotlib function that passes arguments?
    # See this: https://matplotlib.org/api/collections_api.html and the small section on set_offsets()
    # intens = np.array([meas[0] for meas in scan]) - I dont think we need this argument passed
    # scatter.set_array(intens) - Or this one
    return scatter, X, Y, Z

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

# This simulates one plane of a LIDAR Scan
R = np.ones(63)
phi = np.pi*np.ones(63)/2
theta = np.arange(0,2*np.pi,0.1)
angle = np.deg2rad(45)
X = R*np.sin(phi)*np.cos(theta)
Y = R*np.sin(phi)*np.sin(theta)
Z = R*np.cos(phi)


Rotate = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)],[0, np.sin(angle), np.cos(angle)]])
V = np.array([[X],[Y],[Z]])

Xnew = np.take(Rotate,0)*X + np.take(Rotate,1)*Y + np.take(Rotate,2)*Z
Ynew = np.take(Rotate,3)*X + np.take(Rotate,4)*Y + np.take(Rotate,5)*Z
Znew = np.take(Rotate,6)*X + np.take(Rotate,7)*Y + np.take(Rotate,8)*Z

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface.
ax.scatter3D(Xnew, Ynew, Znew, cmap='Greens')

# Tweak the limits and add latex math labels.
ax.set_zlim(-2, 2)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)


plt.show()