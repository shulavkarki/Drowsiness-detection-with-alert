# Drowsiness Detection Alert System

 > Drowsiness is the biggest problem for road accidents.
       
## Description  
```This is a computer-vision system which detect drowsiness in real-time and plays an alarm when someone appears to be drowsy.```

## Application
 - Transporation where almost daily accidents occur due to driver fatigue.

## Code Requirements
 - Python (version greater than 2.7)
 
 ### Import dependencies
  - opencv(cv2)
  - dlib
  - imutils
  - scipy
  - playsound

## Algorithm
<p align="center">
  <img src="images/sample1.png" width="300" title="Facial Landmarks">
</p>
Here, pre-trained facial landmarks model is used in which we extract the 6 (x, y)- coordinates of detected eye and then find eye aspect ratio(EAR).

### Eye Aspect Ratio (EAR)
<p align="center">
  <img src="images/1.png" width="300" title="EAR">
  <img src="images/sample2.png" width="300" title="EAR">
</p>

It checks for 20 consecutive frames and if the EAR gets below 0.25, we set the alarm ON.
<p align="center">
  <img src="images/sample3.png" width="300" title="EAR">
</p>
## Samples

<p align="center">
  <img src="images/samples.gif" width="300" title="Sample 1">
 
</p>
