import serial
#import string as str
import time
import sys
import tty
import os
#import round

ser = serial.Serial(
    port='/dev/tty.usbserial-A700eSou',
    baudrate=57600
)

#Spin both motors at startup
ser.write('00br012001200500;'.encode())
time.sleep(0.5)
ser.write('00br000000000500;'.encode())


threshold = '10' #threshold pwm value for motor spin

rampTime = '0010'
close = ';'
start = '00br0'

#initalize both motors to threshold pwm
initSerial = start+threshold+'0'+threshold+rampTime+close
ser.write(initSerial.encode())

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
        if (leftPWM + delta) <= 250:
            leftPWM += delta
        serialString = start+str(round(leftPWM))+'0'+'300'+rampTime+close
        ser.write(serialString.encode())

    #Decrement left motor speed (-)
    if key==122: #122 is z key
        if (leftPWM - delta) >= int(threshold):
            leftPWM -= delta
        serialString = start+str(round(leftPWM))+'0'+'300'+rampTime+close
        ser.write(serialString.encode())

    #Increment right motor speed (+)
    elif key==100: #100 is d key
        if (rightPWM + delta) <= 250:
            rightPWM += delta
        serialString = start+'300'+'0'+str(round(rightPWM))+rampTime+close
        ser.write(serialString.encode())

    #Decrement right motor speed (-)
    elif key==99: #100 is c key
        if (rightPWM - delta) >= int(threshold):
            rightPWM -= delta
        serialString = start+'300'+'0'+str(round(rightPWM))+rampTime+close
        ser.write(serialString.encode())

    #Increment both motors (+)
    elif key==119: #119 is w key
        if (leftPWM + delta) <= 250:
            leftPWM += delta
        if (rightPWM + delta) <= 250:
            rightPWM += delta
        serialString = start+str(round(leftPWM))+'0'+str(round(rightPWM))+rampTime+close
        ser.write(serialString.encode())

    #Decrement both motors (-)
    elif key==119: #119 is w key
        if (leftPWM - delta) >= int(threshold):
            leftPWM -= delta
        if (rightPWM - delta) >= int(threshold):
            rightPWM -= delta
        serialString = start+str(int(round(leftPWM)))+'0'+str(int(round(rightPWM)))+rampTime+close
        ser.write(serialString.encode())

    elif key==113: #113 is q key
        break

    else:
        ser.write('00br001000100010;'.encode())

os.system('stty sane')
sys.exit(0)
