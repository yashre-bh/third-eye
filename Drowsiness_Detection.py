from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import numpy as np
import mss
import time
import matplotlib.pyplot as plt
import keyboard
import os
from PyQt5 import QtWidgets
import sys


def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear


thresh = 0.25
frame_check = 20

detect = dlib.get_frontal_face_detector()
# Dat file is the crux of the code
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

print("Model Initialization Complete")


MyApp = QtWidgets.QApplication(sys.argv)
Screen = MyApp.desktop().screenGeometry()
monitor_height = Screen.height()
monitor_width = Screen.width()

monitor = {"top": 0, "left": 0, "width": monitor_width, "height": monitor_height}


print("Taking Screen Shots in 5 seconds")

now = time.time()

while 1 :

    right_now = time.time()

    delta_time = right_now - now

    if delta_time > 5 :

        print("Taking Screen shot")

        break
    
img_initial_nump = np.array(mss.mss().grab(monitor))

print("Initial Screen Shot Taken")


def horizontalChecker ( i ) :

    for j in range ( monitor["width"] ) :

        if [ img_initial_nump[i][j][0] , img_initial_nump[i][j][1] , img_initial_nump[i][j][2] , img_initial_nump[i][j][3] ] != [ 36 , 33 , 32 , 255 ] :

            return 0

    return 1

def verticalChecker ( j , i1 , i2 ) :

    for i in range ( i1 , i2+1 ) :

        if [ img_initial_nump[i][j][0] , img_initial_nump[i][j][1] , img_initial_nump[i][j][2] , img_initial_nump[i][j][3] ] != [ 36 , 33 , 32 , 255 ] :

            return 0

    return 1




horizontal_cuts = []

black_row = [0] * len(img_initial_nump)

for i in range ( len(img_initial_nump) ) :

    if not horizontalChecker ( i ) :

        continue

    black_row[ i ] = 1

    if black_row[i-1] == 1 :

        continue

    horizontal_cuts += [ i ]

horizontal_cuts = horizontal_cuts[:-1]

all_vertical_cuts = []

for i in range ( len(horizontal_cuts) - 1 ) :

    vertical_cuts = []

    black_column = [0] * monitor["width"]

    for j in range ( monitor["width"] ) :

        if not verticalChecker ( j , horizontal_cuts[i] , horizontal_cuts[i+1] ) :

            continue

        black_column[ j ] = 1

        if black_column[j-1] == 1 :

            continue

        vertical_cuts += [ j ]

    all_vertical_cuts += [vertical_cuts]


no_of_boxes = 0
boxes_in_a_row = []
for i in all_vertical_cuts :

    no_of_boxes += len(i)-1

    boxes_in_a_row += [ len(i) - 1 ]

flag = [0] * no_of_boxes

penalty = [0] * no_of_boxes

negligence = []

total_time = 0

boxes_before_a_row = [0]

for i in range( len(boxes_in_a_row) - 1 ) :

        boxes_before_a_row += [ boxes_before_a_row[-1] + boxes_in_a_row[i] ]


print("Preprocessing Done")


while True:

    total_time += 1
    
    img_nump = np.array(mss.mss().grab(monitor))


    for row_no in range ( len(horizontal_cuts) - 1 ) :

        for column_no in range ( len(all_vertical_cuts[row_no]) - 1 ) :
            
            
            user_no = boxes_before_a_row[row_no] + column_no
            
            user_img_nump = [ img_nump[iii][all_vertical_cuts[row_no][column_no] : all_vertical_cuts[row_no][column_no + 1]] for iii in range ( horizontal_cuts[row_no] , horizontal_cuts[row_no +1] ) ]

            user_img_nump = np.array(user_img_nump)

            user_img_nump = imutils.resize(user_img_nump, width=450)
            
            gray = cv2.cvtColor(user_img_nump, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            if not subjects: 
                flag[user_no] += 1
                #print(flag)
                
                if flag[user_no] >= frame_check:
                    penalty[user_no] +=1
            for subject in subjects:

                shape = predict(gray, subject)
                shape = face_utils.shape_to_np(shape)#converting to NumPy Array
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(user_img_nump, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(user_img_nump, [rightEyeHull], -1, (0, 255, 0), 1)
                if ear < thresh:
                    flag[user_no] += 1
                    #print(flag)
                    if flag[user_no] >= frame_check:
                        penalty[user_no] +=1
                else:
                    flag[user_no] = 0

    total_negligence_now = 0
    for i in flag:
        if i >= frame_check :
            total_negligence_now += 1 
    negligence += [ total_negligence_now ]

                
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if keyboard.is_pressed("ctrl+alt+l"):
        break

#print(negligence)
for i in range ( len(negligence) ) :
    negligence[i] = no_of_boxes - negligence[i]


penalty_percent = [ ( total_time - penalty[i] )/total_time for i in range ( len(penalty) ) ]
user_nos = [ i+1 for i in range(len(penalty)) ]

plt.bar( user_nos , penalty_percent )
plt.xlabel("Attendees")
plt.ylabel("Attention Given")
if os.path.isfile('analysis1.png'):
   os.remove('./static/analysis1.png')
plt.savefig('./static/analysis1.png')

plt.clf()

plt.plot(negligence)
plt.xlabel("time")
plt.ylabel("People Attending")
if os.path.isfile('analysis2.png'):
   os.remove('./static/analysis2.png')
plt.savefig('./static/analysis2.png')


#cv2.destroyAllWindows()
