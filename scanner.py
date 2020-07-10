import numpy as np
import cv2
from fpt import four_point_transform
import imutils
import matplotlib.pyplot as plt

image=cv2.imread("page.jpg")
ratio=image.shape[0]/500.0
orig=image.copy()
image=imutils.resize(image,height=500)

#Step1: Edge Detection
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray=cv2.GaussianBlur(gray,(5,5),0)
edged=cv2.Canny(gray,75,200)

#Step2: Find contour representing the paper being scanned
img,contours,hierarchies = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

for c in cnts:
    
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*peri,True)
    
    if(len(approx)==4):
        page=approx
        break
    
#Step 3: Apply a Perspective Transform & Threshold    
warped = four_point_transform(orig, page.reshape(4, 2) * ratio)
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
th1=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,8)
th2=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,8)
warped =cv2.addWeighted(src1=th1,alpha=0.7,src2=th2,beta=0.3,gamma=0)

cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)
