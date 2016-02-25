#!/usr/local/bin/python

import os
import cv2
#import cv2.cv as cv
import math
import numpy as np

blank = np.zeros((480, 640), np.uint8)
blank[:,:] = (255)


## Resize with resize command
def resizeImage(img):
    
    # mapping from destination to source
    dst = cv2.resize(img,None,fx=0.25,fy=0.25,interpolation=cv2.INTER_LINEAR)
    return dst

## Load image
#img = cv2.imread("./buoy_red_1.jpeg")
img = cv2.imread("./pool.jpg")

#img = cv2.bilateralFilter(img, 9, 75, 75)

## Make image single stream black and white
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.medianBlur(gray, 5)
can = cv2.Canny(gray, 25, 75)

filteredContour = []

im2, contour,hier = cv2.findContours(can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for iteration in range(0,len(contour)):

    areaOfContour = cv2.contourArea(contour[iteration])
    if areaOfContour >= 1000:
        print "Contour %d of size %d" %(iteration,areaOfContour)
        filteredContour.append(contour[iteration])
        cv2.drawContours(img, filteredContour, -1, (0,255,0), 2)


#kernel = np.ones((3,3),np.uint8)
#can = cv2.erode(can, kernel, iterations=1)        
#blank = cv2.dilate(blank,kernel, iterations=1)
cv2.imshow("canny", can)
#cv2.imshow("blank", blank)
"""
## Use Hough circles to determine the center of the circle (using fake dp and minDist args)
circles = cv2.HoughCircles(blank, cv2.HOUGH_GRADIENT,1,10)

#circles = np.uint16(np.around(circles))
print circles

for i in circles[0,:]:
    #draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    #draw the centre of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
"""
## Show Images
cv2.imshow("gray", gray)
cv2.imshow("img",img)


'''
## End of program
cv2.waitKey(0)
'''

while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
