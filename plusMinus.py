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

#Spin both motors at startup
ser.write('00aw00090120;'.encode())
time.sleep(0.010)
ser.write('00aw00030120;'.encode())
time.sleep(1)
ser.write('00aw00030000;'.encode())
time.sleep(0.010)
ser.write('00aw00090000;'.encode())

threshold = '100' #threshold pwm value for motor spin

leftMotorF = '00aw00030'
rightMotorF = '00aw0090'
close = ';'

#initalize both motors to threshold pwm
initLeft = leftMotorF + threshold + close
initRight = rightMotorF + threshold + close

ser.write(initLeft.encode())
ser.write(initRight.encode())

leftPWM = 0
rightPWM = 0

#speed increment
delta = (250-100)/15

#a, d increment left, right motors by delta, respectively
#z, c decrement left, right motors by delta, respectively
#w, s increment/decrement both motors by delta, respectively

while(True):

    tty.setcbreak(sys.stdin)
    key = ord(sys.stdin.read(1))  # key captures the key-code

    time.sleep(0.050)

    #Increment left motor speed (+)
    if key==97: #97 is a key
        if leftPWM <= 250:
            leftPWM += delta
        ser.write((leftMotorF + str(leftPWM) + close).encode())

    #Decrement left motor speed (-)
    if key==122: #122 is z key
        if leftPWM >= 100:
            leftPWM -= delta
        ser.write((leftMotorF + str(leftPWM) + close).encode())

    #Increment right motor speed (+)
    elif key==100: #100 is d key
        if rightPWM <= 250:
            rightPWM += delta
        ser.write((rightMotorF + str(rightPWM) + close).encode())

    #Decrement right motor speed (-)
    elif key==99: #100 is c key
        if rightPWM >= 100:
            rightPWM -= delta
        ser.write((rightMotorF + str(rightPWM) + close).encode())

    #Increment both motors (+)
    elif key==119: #119 is w key
        if leftPWM <= 250:
            leftPWM += delta
        if rightPWM <= 250:
            rightPWM += delta
        ser.write((leftMotorF + str(leftPWM) + close).encode())
        time.sleep(0.010)
        ser.write((rightMotorF + str(rightPWM) + close).encode())

    #Decrement both motors (-)
    elif key==119: #119 is w key
        if leftPWM >= 100:
            leftPWM -= delta
        if rightPWM >= 100:
            rightPWM -= delta
        ser.write((rightMotorF + str(rightPWM) + close).encode())
        time.sleep(0.010)
        ser.write((leftMotorF + str(leftPWM) + close).encode())

    elif key==113: #113 is q key
        break

    else:
        ser.write('00aw00030000;'.encode())
        time.sleep(0.010)
        ser.write('00aw00090000;'.encode())

os.system('stty sane')
sys.exit(0)
