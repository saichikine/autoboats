
import numpy as np
import cv2
import cv2.aruco as aruco
import argparse
from collections import deque
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	cap = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    cap = cv2.VideoCapture(args["video"])

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

#CROP TO XMIN, YMIN, WIDTH, HEIGHT = [270, 80, 565, 570]
frame_rate = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print("Frame Rate: ", frame_rate)
print("Height: ", height)
print("Width: ", width)

f = open("logCamTracking.csv", "w+")

display = 0;

while(True):
    #Timer
    start = time.time()
    # Capture frame-by-frame
    ret, frame = cap.read()
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #might be faster to convert to greyscale here
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    #print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    #Top left is (0,0)
    pos = [0,0]
    ang = 0

    if corners:
        [one, two, three, four] = corners[0][0]
		#Position of center is average of coordinates of opposite corners
        pos = [(one[0]+three[0])/2, (one[1]+three[1])/2]
        ang = -np.degrees(np.arctan2(two[1]-one[1],two[0]-one[0]))
        print("angle {0}".format(ang))
        print("position {0}".format(pos))
		#print(one)
		#print('corners: {0}'.format(corners[0][0]))
		#print(ids)

    frame = aruco.drawDetectedMarkers(frame, corners, ids, borderColor=(255,0,0))
    #gray = aruco.drawDetectedMarkers(gray,corners)
    #print(rejectedImgPoints)

    # Display the resulting frame
    # Much faster without drawing

    if display:
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # End timer and print
    end = time.time()
    elapsedTime = end-start
    print(elapsedTime)

    #Write x, y, angle, dt to csv file (comma delineated)
    f.write("%d,%d,%d,%f\n" %(pos[0], pos[1], ang, elapsedTime))

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
