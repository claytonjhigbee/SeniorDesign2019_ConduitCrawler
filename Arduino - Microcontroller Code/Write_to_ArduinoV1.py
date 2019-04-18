# /*
# This code is used to write to the arduino/Atmega328P serial port
#
# */

import serial # Import Serial library, our code is already doing this
import time
ser = serial.Serial('/dev/ttyUSB0', 115200) # Setup serial connection object at a specified port and baudrate
time.sleep(10)
# Syncing with the MCU should be done ONLY when the Arduino Viewport is closed. Not sure why it doesnt work?
ser.write(b'S') # Send a binary encoded word to the port, this is done symbol by symbol

# A phrase like Hello serial world! would equate to:
# 72 101 108 108 111 32 115 101 114 105 97 108 32 119 111 114 108 100 33
# This includes the upper and lower cases, spaces, and symobols IE --> !