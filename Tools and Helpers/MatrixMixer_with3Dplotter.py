import numpy as np
import sys, serial, argparse
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
rows = 5
columns = 100
plotview = 700
randsize = columns
a = np.zeros(shape = (rows,columns))
b = np.zeros(shape = (rows,columns))
c = np.zeros(shape = (rows,columns))
i = 0

while i <= 4:
    x = np.random.randint(500, size=randsize)
    difference = columns - len(x)
    storezero = np.zeros(shape = (1,difference))
    test = np.append(x,storezero)
    a[i] = test
    i = i + 1

print(a)

i = 0
while i <= 4:
    x = np.random.randint(500, size=randsize)
    difference = columns - len(x)
    storezero = np.zeros(shape = (1,difference))
    test = np.append(x,storezero)
    b[i] = test
    i = i + 1

print(b)

i = 0
while i <= 4:
    x = np.random.randint(500, size=randsize)
    difference = columns - len(x)
    storezero = np.zeros(shape = (1,difference))
    test = np.append(x,storezero)
    c[i] = test
    i = i + 1

print(c)


fig = plt.figure() # Create a figure object
ax = fig.add_subplot(111, projection='3d') # Create plot axes object, 3D
ax.scatter3D(a, b, c)  # 3D Scatter Plot, This needs to be assigned to an object?
ax.set_zlim(-1*plotview, plotview)
ax.set_xlim(-1*plotview, plotview)
ax.set_ylim(-1*plotview, plotview)

plt.show()