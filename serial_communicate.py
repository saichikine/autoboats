import serial
import string as str
import time
import sys
import tty
import os

ser = serial.Serial(
    port='/dev/tty.usbserial-A700eSou',
    baudrate=57600
)

#test on
ser.write('00aw00090120;'.encode())
time.sleep(0.010)
ser.write('00aw00030120;'.encode())
time.sleep(1)
ser.write('00aw00030000;'.encode())
time.sleep(0.010)
ser.write('00aw00090000;'.encode())


#loop for detecting keypress
#waits 10ms at beginning of loop
#motor is on for 10-20ms and then stops until next loop
#key held down will move boat
#can't rotate and move forward at same time
#can't go backwards
#pin 9 is right, pin 3 is left

while(True):

    tty.setcbreak(sys.stdin)
    key = ord(sys.stdin.read(1))  # key captures the key-code

    time.sleep(0.050)

    #rotate right if d is pressed
    if key==100: #27 is d key
        ser.write('00aw00030255;'.encode())
        time.sleep(0.010)
        ser.write('00aw00030000;'.encode())

    #rotate left is a is pressed
    elif key==97: #97 is a key
        ser.write('00aw00090255;'.encode())
        time.sleep(0.010)
        ser.write('00aw00090000;'.encode())

    #go forward if w is pressed.
    elif key==119: #119 is w key
        ser.write('00aw00030255;'.encode())
        time.sleep(0.010)
        ser.write('00aw00090255;'.encode())
        time.sleep(0.010)
        ser.write('00aw00030000;'.encode())
        time.sleep(0.010)
        ser.write('00aw00090000;'.encode())

    elif key==113: #113 is q key
        break

    else:
        ser.write('00aw00030000;'.encode())
        time.sleep(0.010)
        ser.write('00aw00090000;'.encode())

    # ser.write('00aw00030000;'.encode())
    # time.sleep(0.010)
    # ser.write('00aw00090000;'.encode())

os.system('stty sane')
sys.exit(0)

#ser.write(arduinotypepinpwm;)
# ser.write('00aw00090255;'.encode())
# time.sleep(0.010)
# ser.write('00aw00030255;'.encode())
# time.sleep(4)
# ser.write('00aw00030000;'.encode())
# time.sleep(0.010)
# ser.write('00aw00090000;'.encode())
