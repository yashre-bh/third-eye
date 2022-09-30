from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import numpy as np
from PIL import ImageGrab



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
while True:
    img = ImageGrab.grab(bbox=(0, 0, 1000, 1000))  # x,y,w,h
    img_np = np.array(img)
    # ret, frame = cap.read()
    # frame = imutils.resize(frame, width=450);
    img_np = imutils.resize(img_np, width=450)
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
	
        cv2.imshow("Frame", img_np)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

cv2.destroyAllWindows()
# cap.release() 
