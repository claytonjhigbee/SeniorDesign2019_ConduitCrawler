# Serial Reader for Python
import sys, serial, argparse
import re
strPort = '/dev/ttyUSB0' # MCU Port Name
Aport = serial.Serial(strPort, 115200)
while 1 < 2:
    try:
        # First Attempt to read an angle value from the MCU Serial Port
        line = Aport.readline()
        line = str(line, "utf-8")
        print(line)
        angle = int(re.sub("[^0-9]", "", line))
        print(angle)
    # If a misread occurs, try again
    except:
        # Second attempt to read an angle value from the MCU Serial Port
        # print("Angle misread, second attempt")
        line = Aport.readline()
        line = str(line, "utf-8")
        print(line)
        # angle = int(re.sub("[^0-9]", "", line))