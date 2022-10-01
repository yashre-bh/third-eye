from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import numpy as np
import mss



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
# cap = cv2.VideoCapture(0)
flag = 0
print(1)

def horizontal_checker ( i ) :

    for j in range ( 450 ) :

        if [ img_short[i][j][0] , img_short[i][j][1] , img_short[i][j][2] , img_short[i][j][3] ] != [ 36 , 33 , 32 , 255 ] :

            return 0

    return 1

def vertical_checker ( j , i1 , i2 ) :

    for i in range ( i1 , i2+1 ) :

        if [ img_short[i][j][0] , img_short[i][j][1] , img_short[i][j][2] , img_short[i][j][3] ] != [ 36 , 33 , 32 , 255 ] :

            return 0

    return 1


monitor = {"top": 0, "left": 0, "width": 1366, "height": 768}

for i in range(100) :
    
    img_np = np.array(mss.mss().grab(monitor))

    img_short = imutils.resize ( img_np , width = 450 )
    
    #cv2.imshow("OpenCV/Numpy normal", img_short )

Vals = []

for i in range ( len(img_short) ) :

    if not horizontal_checker ( i ) :

        continue

    Vals += [ i ]

    break

for i in range ( Vals[0] + 20 , len(img_short) ) :

    if not horizontal_checker ( i ) :

        continue

    Vals += [ i ]

    break

if len(Vals) == 2 :

    while 1 :

        a = Vals[-1]

        a += Vals[1] - Vals[0]

        if a < len(img_short) and horizontal_checker ( a ) :

            Vals += [a]

            continue

        break


Vals22 = []

for i in range ( len(Vals) - 1 ) :

    Vals2 = []

    for j in range ( monitor["width"] ) :

        if vertical_checker ( j , Vals[i] , Vals[i+1] ) :

            continue

        Vals2 += [ j-1 ]

        break

    for j in range ( Vals2[0]+1 , monitor["width"] ) :

        if not vertical_checker ( j , Vals[i] , Vals[i+1] ) :

            continue

        Vals2 += [ j ]

        break

    if len(Vals2) == 2 :

        while 1 :

            a = Vals2[-1]

            a += Vals2[1] - Vals2[0]

            if a < 450 and vertical_checker ( a , Vals[i] , Vals[i+1] ) :

                Vals2 += [a]

                continue

            break

    Vals22 += [Vals2]

'''
WIP
boxes = 0
for i in Vals22 :

    boxes += len(i)-1

flag = [0] * boxes
'''

while True:
    img_size= {"top": 40, "left": 0, "width": 800, "height": 640}
    img_np = np.array(mss.mss().grab(img_size))

    # ret, frame = cap.read()
    # frame = imutils.resize(frame, width=450);
    
    img_np_full = imutils.resize(img_np, width=450)

    


    for height_i in range ( len(Vals) - 1 ) :

        for position_j in range ( len(Vals22[height_i]) - 1 ) :

            
            img_np = [ img_np_full[iii][Vals22[height_i][position_j] : Vals22[height_i][position_j + 1]+1] for iii in range ( Vals[height_i] , Vals[height_i +1] + 1 ) ]

            img_np = np.array(img_np)
            
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            if not subjects: 
                flag += 1
                print(flag)
                if flag >= frame_check:
                    cv2.putText(img_np, "****************ALERT!****************", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(img_np, "****************ALERT!****************", (10, 325),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
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
                cv2.drawContours(img_np, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(img_np, [rightEyeHull], -1, (0, 255, 0), 1)
                if ear < thresh:
                    flag += 1
                    print (flag)
                    if flag >= frame_check:
                        cv2.putText(img_np, "****************ALERT!****************", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(img_np, "****************ALERT!****************", (10,325),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                                        # print ("Drowsy")
                    else:
                        flag = 0
            
    #cv2.imshow("Frame", img_np)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
# cap.release() 
