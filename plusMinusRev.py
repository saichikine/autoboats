import serial
import time
import sys
import tty
import os

#Reverse/Forward command for left motor (pin3)
#pin2=1, pin4=0 == Forward
#pin2=0, pin4=1 == Reverse
#pin2=1, pin4=1 == Brake

def reverseLeft():
    revLeft = '00rv00010000;'
    ser.write(revLeft.encode())
    print('Left Motor in Reverse')

def forwardLeft():
    forLeft = '00fw00010000;'
    ser.write(forLeft.encode())
    print('Left Motor in Forward')

#Reverse command for right motor (pin9)
#pin7=0, pin8=1 == Forward
#pin7=1, pin8=0 == Reverse
#pin7=1, pin4=8 == Brake

def reverseRight():
    revRight = '00rv00020000;'
    ser.write(revRight.encode())
    print('Right Motor in Reverse')

def forwardRight():
    forRight = '00fw00020000;'
    ser.write(forRight.encode())
    print('Right Motor in Forward')

ser = serial.Serial(
    port='/dev/cu.usbserial-A700eSou', #check this with "ls /dev/{tty,cu}.*"
    baudrate=57600
)


forwardRight()
time.sleep(0.010)
forwardLeft()

#Spin both motors at startup (startup chime)
# ser.write('00br010001000500;'.encode())
# time.sleep(0.5)
# ser.write('00br000000000500;'.encode())
# time.sleep(0.010)
#
# #Test reversal
# reverseLeft()
# time.sleep(0.005)
# reverseRight()
# time.sleep(0.010)
#
# #Spin both motors (in reverse) at startup (startup chime)
# ser.write('00br010001000500;'.encode())
# time.sleep(0.5)
# ser.write('00br000000000500;'.encode())
# time.sleep(0.010)
#
# forwardLeft()
# time.sleep(0.005)
# forwardRight()

threshold = '10' #threshold pwm value for motor spin

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

f = open("logControl.csv", "w+")

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
        if leftPWM >= 0:
            forwardLeft()
            #If PWM signal below 100, add extra leading zero to format string properly
            if leftPWM < 100:
                serialString = start+'0'+str(round(leftPWM))+'0'+'300'+rampTime+close
            else:
                serialString = start+str(round(leftPWM))+'0'+'300'+rampTime+close
            ser.write(serialString.encode())
        elif leftPWM < 0:
            reverseLeft()
            #If PWM signal below 100, add extra leading zero to format string properly
            if leftPWM > -100:
                serialString = start+'0'+str(round(-leftPWM))+'0'+'300'+rampTime+close
            else:
                serialString = start+str(round(-leftPWM))+'0'+'300'+rampTime+close
            ser.write(serialString.encode())

    #Decrement left motor speed (-)
    elif key==122: #122 is z key
        if (leftPWM - delta) >= -250:
            leftPWM -= delta
        if leftPWM >= 0:
            forwardLeft()
            #If PWM signal below 100, add extra leading zero to format string properly
            if leftPWM < 100:
                serialString = start+'0'+str(round(leftPWM))+'0'+'300'+rampTime+close
            else:
                serialString = start+str(round(leftPWM))+'0'+'300'+rampTime+close
            ser.write(serialString.encode())
        elif leftPWM < 0:
            reverseLeft()
            if leftPWM > -100:
                serialString = start+'0'+str(round(-leftPWM))+'0'+'300'+rampTime+close
            else:
                serialString = start+str(round(-leftPWM))+'0'+'300'+rampTime+close
            ser.write(serialString.encode())

    #Increment right motor speed (+)
    elif key==100: #100 is d key
        if (rightPWM + delta) <= 250:
            rightPWM += delta
        if rightPWM >= 0:
            forwardRight()
            #If PWM signal below 100, add extra leading zero to format string properly
            if rightPWM < 100:
                serialString = start+'300'+'0'+'0'+str(round(rightPWM))+rampTime+close
            else:
                serialString = start+'300'+'0'+str(round(rightPWM))+rampTime+close
            ser.write(serialString.encode())
        elif rightPWM <0:
            reverseRight()
            if rightPWM > -100:
                serialString = start+'300'+'0'+'0'+str(round(-rightPWM))+rampTime+close
            else:
                serialString = start+'300'+'0'+str(round(-rightPWM))+rampTime+close
            ser.write(serialString.encode())

    #Decrement right motor speed (-)
    elif key==99: #100 is c key
        if (rightPWM - delta) >= -250:
            rightPWM -= delta
        if rightPWM >= 0:
            forwardRight()
            #If PWM signal below 100, add extra leading zero to format string properly
            if rightPWM < 100:
                serialString = start+'300'+'0'+'0'+str(round(rightPWM))+rampTime+close
            else:
                serialString = start+'300'+'0'+str(round(rightPWM))+rampTime+close
            ser.write(serialString.encode())
        elif rightPWM < 0:
            reverseRight()
            if rightPWM > -100:
                serialString = start+'300'+'0'+'0'+str(round(-rightPWM))+rampTime+close
            else:
                serialString = start+'300'+'0'+str(round(-rightPWM))+rampTime+close
            ser.write(serialString.encode())

    #Increment both motors (+)
    elif key==119: #119 is w key
        if (leftPWM + delta) <= 250:
            leftPWM += delta
        if (rightPWM + delta) <= 250:
            rightPWM += delta
        if (leftPWM >=0 and rightPWM >=0):
            forwardLeft()
            time.sleep(0.010)
            forwardRight()
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
        elif (leftPWM >= 0 and rightPWM < 0):
            forwardLeft()
            time.sleep(0.010)
            reverseRight()
            if (leftPWM < 100 and rightPWM <= -100):
                serialString = start+'0'+str(round(leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            elif (rightPWM > -100 and leftPWM >= 100):
                serialString = start+str(round(leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            elif (leftPWM < 100 and rightPWM > -100):
                serialString = start+'0'+str(round(leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            else:
                serialString = start+str(round(leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            ser.write(serialString.encode())
        elif (leftPWM < 0 and rightPWM >= 0):
            reverseLeft()
            time.sleep(0.010)
            forwardRight()
            if (leftPWM > -100 and rightPWM >= 100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+str(round(rightPWM))+rampTime+close
            elif (rightPWM < 100 and leftPWM <= -100):
                serialString = start+str(round(-leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
            elif (leftPWM > -100 and rightPWM < 100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
            else:
                serialString = start+str(round(-leftPWM))+'0'+str(round(rightPWM))+rampTime+close
            ser.write(serialString.encode())
        elif (leftPWM < 0 and rightPWM < 0):
            reverseLeft()
            time.sleep(0.010)
            reverseRight()
            if (leftPWM > -100 and rightPWM <= -100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            elif (rightPWM > -100 and leftPWM <= -100):
                serialString = start+str(round(-leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            elif (leftPWM > -100 and rightPWM > -100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            else:
                serialString = start+str(round(-leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            ser.write(serialString.encode())

    #Decrement both motors (-)
    elif key==115: #115 is s key
        if (leftPWM - delta) >= -250:
            leftPWM -= delta
        if (rightPWM - delta) >= -250:
            rightPWM -= delta
        if (leftPWM >=0 and rightPWM >=0):
            forwardLeft()
            time.sleep(0.010)
            forwardRight()
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
        elif (leftPWM >= 0 and rightPWM < 0):
            forwardLeft()
            time.sleep(0.010)
            reverseRight()
            if (leftPWM < 100 and rightPWM <= -100):
                serialString = start+'0'+str(round(leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            elif (rightPWM > -100 and leftPWM >= 100):
                serialString = start+str(round(leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            elif (leftPWM < 100 and rightPWM > -100):
                serialString = start+'0'+str(round(leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            else:
                serialString = start+str(round(leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            ser.write(serialString.encode())
        elif (leftPWM < 0 and rightPWM >= 0):
            reverseLeft()
            time.sleep(0.010)
            forwardRight()
            if (leftPWM > -100 and rightPWM >= 100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+str(round(rightPWM))+rampTime+close
            elif (rightPWM < 100 and leftPWM <= -100):
                serialString = start+str(round(leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
            elif (leftPWM > -100 and rightPWM < 100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+'0'+str(round(rightPWM))+rampTime+close
            else:
                serialString = start+str(round(-leftPWM))+'0'+str(round(rightPWM))+rampTime+close
            ser.write(serialString.encode())
        elif (leftPWM < 0 and rightPWM < 0):
            reverseLeft()
            time.sleep(0.010)
            reverseRight()
            if (leftPWM > -100 and rightPWM <= -100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            elif (rightPWM > -100 and leftPWM <= -100):
                serialString = start+str(round(-leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            elif (leftPWM > -100 and rightPWM > -100):
                serialString = start+'0'+str(round(-leftPWM))+'0'+'0'+str(round(-rightPWM))+rampTime+close
            else:
                serialString = start+str(round(-leftPWM))+'0'+str(round(-rightPWM))+rampTime+close
            ser.write(serialString.encode())

    elif key==113: #113 is q key
        break

    #Shut off motors if any other key is pressed
    else:
        ser.write('00br000000000500;'.encode()) #shut off motors if any other keys are pressed

    print('leftPWM= '+str(leftPWM)+', rightPWM= '+str(rightPWM))

    #print(time.time())

    f.write("%f,%f,%f\n" %(leftPWM, rightPWM, time.time()))

#reset terminal, otherwise can't see what you're typing
os.system('stty sane')
sys.exit(0)
