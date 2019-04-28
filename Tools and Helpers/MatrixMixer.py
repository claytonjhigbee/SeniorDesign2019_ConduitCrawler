import numpy as np
import sys, serial, argparse
rows = 5
columns = 30
b = np.zeros(shape = (rows,columns))
i = 0

while i <= 4:
    x = np.random.randint(300, size=10)
    difference = columns - len(x)
    storezero = np.zeros(shape = (1,difference))
    test = np.append(x,storezero)
    b[i] = test
    i = i + 1


print(b)