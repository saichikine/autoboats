
import numpy as np
import cv2
import cv2.aruco as aruco
import argparse
#from collections import deque
import time
import serial
import sys
import tty
import os
import multiprocessing

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
# 	help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,
# 	help="max buffer size")
# args = vars(ap.parse_args())
#
# # if a video path was not supplied, grab the reference
# # to the webcam
# if not args.get("video", False):
# 	cap = cv2.VideoCapture(0)
#
# # otherwise, grab a reference to the video file
# else:
#     cap = cv2.VideoCapture(args["video"])
#
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# cap.set(cv2.CAP_PROP_FPS, 30)
#
# frame_rate = cap.get(cv2.CAP_PROP_FPS)
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#
# print("Frame Rate: ", frame_rate)
# print("Height: ", height)
# print("Width: ", width)

f = open("LogCombinedPy.csv", "w+")

#Boolean to display frames or not
#Set to 0 for faster code but no demo
display = 1;

#speed increment
delta = 5

threshold = '10' #threshold pwm value for motor spin

rampTime = '0010' #ramp time for each setpoint
close = ';'
start = '00br0'

#Initialize Serial Port
ser = serial.Serial(
    port='/dev/cu.usbserial-A700eSou', #check this with "ls /dev/{tty,cu}.*"
    baudrate=57600
)

#Spin both motors at startup (startup chime)
ser.write('00br010001000500;'.encode())
time.sleep(0.5)
ser.write('00br000000000500;'.encode())

#initalize both motors to threshold pwm
initSerial = start+threshold+'0'+threshold+rampTime+close
ser.write(initSerial.encode())

#init to threshold PWM
leftPWM = int(threshold)
rightPWM = int(threshold)

#Top left is (0,0)
pos = [0,0] #position
ang = 0 #angle

while(True):
    #Timer
    start = time.time()

    # ret, frame = cap.read()
    #
    # aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    # parameters = aruco.DetectorParameters_create()
    #
    # corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    #
    # if corners:
    #     [one, two, three, four] = corners[0][0]
	# 	#Position of center is average of coordinates of opposite corners
    #     pos = [(one[0]+three[0])/2, (one[1]+three[1])/2]
    #     #Check which corner is on top (check if marker is upright)
    #     if one[1] <= four[1]: #if upright
    #         ang = np.degrees(np.arctan((two[1]-one[1])/(one[0]-two[0])))
    #     elif one[1] > four[1]: #if flipped
    #         ang = np.degrees(np.arctan((one[0]-two[0])/(one[1]-two[1])))
    #         if ang>0:
    #             ang+=90
    #         elif ang<0:
    #             ang-=90
	# 		#Put in a case here for ang=0
    #     else:
    #         print("Error: angle")
    #     print("angle {0}".format(ang))
    #     print("position {0}".format(pos))
    #
    # frame = aruco.drawDetectedMarkers(frame, corners, ids, borderColor=(255,0,0))
    #
    # # Display the resulting frame
    # # Much faster without drawing
    # if display==1:
    #     cv2.imshow('frame',frame)
    #
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    ##################### CONTROL SECTION ######################
    tty.setcbreak(sys.stdin)
    key = ord(sys.stdin.read(1))  # key captures the key-code

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

    # End timer and print
    end = time.time()
    elapsedTime = end-start
    print(elapsedTime)

    #Write x, y, angle, dt to csv file (comma delineated)
    f.write("%d,%d,%d,%f\n" %(pos[0], pos[1], ang, elapsedTime))

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
os.system('stty sane')
sys.exit(0)
