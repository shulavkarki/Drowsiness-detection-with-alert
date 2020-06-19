#importing necessary packages
from scipy.spatial import distance
from imutils import face_utils
import imutils
import playsound
from argparse import ArgumentParser
from threading import Thread
import dlib
import queue
import cv2

def eye_aspect_ratio(eye):
    # compute the euclidean distance between the vertical eye landmark (x, y)-coordinates
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
    # compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
	C = distance.euclidean(eye[0], eye[3])
    #compute eye aspect ratio
	ear = (A + B) / (2.0 * C)
	return ear

def sound_alarm():
	# play an alarm sound
	playsound.playsound("./alarm.wav")

thresh = 0.25
frame_check = 20
TOTAL = 0
ALARM_ON = False
#Returns the default face detector
detect = dlib.get_frontal_face_detector()
#shape_predictor_68_face_landmarks is our pre-trained model for facial landmarks detector
predict = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap=cv2.VideoCapture(0)
flag=0
while True:
    #Getting out image by webcam
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=450)
    #Converting the image to gray scale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the grayscale frame
	subjects = detect(gray, 0)
    #Loop over the face detections
	for subject in subjects:
        #determine the facial landmarks for the face region, 
		shape = predict(gray, subject)
        #then, converting the facial landmark(x, y) coordinates to NumPy Array
		shape = face_utils.shape_to_np(shape)
        #extract the left and right eye coordinates, then 
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
        #use the coordinates to compute the eye aspect ratio for both eyes
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
        #compute the average of EAR for both eyes
		ear = (leftEAR + rightEAR) / 2.0
        # compute the convex hull for the left and right eye, then
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		# visualize each of the eyes
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        # check to see if the eye aspect ratio is below the blink threshold, 
		if ear < thresh:
			#and if so, increment the blink frame counter
			flag += 1
			print (flag)
			if flag >= frame_check:
				
				if not ALARM_ON:
					ALARM_ON = True
					t = Thread(target=sound_alarm)
					t.deamon = True
					t.start()
					
				#draw on the frame
				cv2.putText(frame, "!!!!!!!!!!!!****ALERT****!!!!!!!!!!!!", (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "!!!!!!!!!!!!****ALERT****!!!!!!!!!!!!", (10,325),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
					
				
				
		else:
			#reset the flag
			flag = 0
			ALARM_ON = False
			
	#show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	#if the 'q' key was pressed, break from the loop
	if key == ord("q"):
		break
#do a bit of cleanup
cap.release()
cv2.destroyAllWindows()
