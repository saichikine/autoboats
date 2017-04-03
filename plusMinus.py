import serial
import time
import sys
import tty
import os

ser = serial.Serial(
    port='/dev/cu.usbserial-A700eSou', #check this with "ls /dev/{tty,cu}.*"
    baudrate=57600
)

#Spin both motors at startup (startup chime)
ser.write('00br010001000500;'.encode())
time.sleep(0.5)
ser.write('00br000000000500;'.encode())


threshold = '85' #threshold pwm value for motor spin

rampTime = '0010' #ramp time for each setpoint
close = ';'
start = '00br0'

#initalize both motors to threshold pwm
initSerial = start+threshold+'0'+threshold+rampTime+close
ser.write(initSerial.encode())

#init to threshold PWM
leftPWM = int(threshold)
rightPWM = int(threshold)

#speed increment
delta = 5

#a, d increment left, right motors by delta, respectively
#z, c decrement left, right motors by delta, respectively
#w, s increment/decrement both motors by delta, respectively

while(True):

    tty.setcbreak(sys.stdin)
    key = ord(sys.stdin.read(1))  # key captures the key-code

    #Longest possible ramp with 10ms ramp is ~10ms (slightly more)
    #Arduino code sends incremented PWMs with 1ms delay
    #FIGURE THIS OUT

    time.sleep(0.010)

    #Increment left motor speed (+)
    if key==97: #97 is a key
        if (leftPWM + delta) <= 250:
            leftPWM += delta
        #If PWM signal below 100, add extra leading zero to format string properly
        if leftPWM < 100:
            serialString = start+'0'+str(round(leftPWM))+'0'+'300'+rampTime+close
        else:
            serialString = start+str(round(leftPWM))+'0'+'300'+rampTime+close
        ser.write(serialString.encode())

    #Decrement left motor speed (-)
    elif key==122: #122 is z key
        if (leftPWM - delta) >= int(threshold):
            leftPWM -= delta
        #If PWM signal below 100, add extra leading zero to format string properly
        if leftPWM < 100:
            serialString = start+'0'+str(round(leftPWM))+'0'+'300'+rampTime+close
        else:
            serialString = start+str(round(leftPWM))+'0'+'300'+rampTime+close
        ser.write(serialString.encode())

    #Increment right motor speed (+)
    elif key==100: #100 is d key
        if (rightPWM + delta) <= 250:
            rightPWM += delta
        #If PWM signal below 100, add extra leading zero to format string properly
        if rightPWM < 100:
            serialString = start+'300'+'0'+'0'+str(round(rightPWM))+rampTime+close
        else:
            serialString = start+'300'+'0'+str(round(rightPWM))+rampTime+close
        ser.write(serialString.encode())

    #Decrement right motor speed (-)
    elif key==99: #100 is c key
        if (rightPWM - delta) >= int(threshold):
            rightPWM -= delta
        #If PWM signal below 100, add extra leading zero to format string properly
        if rightPWM < 100:
            serialString = start+'300'+'0'+'0'+str(round(rightPWM))+rampTime+close
        else:
            serialString = start+'300'+'0'+str(round(rightPWM))+rampTime+close
        ser.write(serialString.encode())

    #Increment both motors (+)
    elif key==119: #119 is w key
        if (leftPWM + delta) <= 250:
            leftPWM += delta
        if (rightPWM + delta) <= 250:
            rightPWM += delta

        #If either (or both) PWM signal is below 100, add extra leading zero to format string
        if (leftPWM < 100 and rightPWM >= 100):
            serialString = start+'0'+str(round(leftPWM))+'0'+str(round(rightPWM))+rampTime+close
        elif (rightPWM < 100 and leftPWM >= 100):
            serialString = start+str(round(leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
        elif (leftPWM < 100 and rightPWM < 100):
            serialString = start+'0'+str(round(leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
        else:
            serialString = start+str(round(leftPWM))+'0'+str(round(rightPWM))+rampTime+close
        ser.write(serialString.encode())

    #Decrement both motors (-)
    elif key==115: #115 is s key
        if (leftPWM - delta) >= int(threshold):
            leftPWM -= delta
        if (rightPWM - delta) >= int(threshold):
            rightPWM -= delta

        #If either (or both) PWM signal is below 100, add extra leading zero to format string
        if (leftPWM < 100 and rightPWM >= 100):
            serialString = start+'0'+str(round(leftPWM))+'0'+str(round(rightPWM))+rampTime+close
        elif (rightPWM < 100 and leftPWM >= 100):
            serialString = start+str(round(leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
        elif (leftPWM < 100 and rightPWM < 100):
            serialString = start+'0'+str(round(leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
        else:
            serialString = start+str(round(leftPWM))+'0'+str(round(rightPWM))+rampTime+close
        ser.write(serialString.encode())

    elif key==113: #113 is q key
        break

    #Shut off motors if any other key is pressed
    else:
        ser.write('00br000000000500;'.encode()) #shut off motors if any other keys are pressed

    print('leftPWM= '+str(leftPWM)+', rightPWM= '+str(rightPWM))

#reset terminal, otherwise can't see what you're typing
os.system('stty sane')
sys.exit(0)
