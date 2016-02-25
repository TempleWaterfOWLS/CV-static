#!/usr/local/bin/python

import os
import cv2
import math
import numpy as np
import argparse
import glob

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

# Set some parameters
sigma=0.33
med = np.median(img)
lower = int(max(0, (1.0 - sigma) * med))
upper = int(min(255, (1.0 + sigma) * med))
edged = cv2.Canny(img, lower, upper)

## Make image single stream black and white
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
can = cv2.Canny(gray, 25, 75)

filteredContour = []

im2, contour,hier = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for iteration in range(0,len(contour)):

    areaOfContour = cv2.contourArea(contour[iteration])
    if areaOfContour >= 500:
        print "Contour %d of size %d" %(iteration,areaOfContour)
        filteredContour.append(contour[iteration])
        cv2.drawContours(img, filteredContour, -1, (0,255,0), 2)

    
#blank = cv2.dilate(blank,kernel, iterations=1)
cv2.imshow("canny", can)
cv2.imshow("colorCanny", edged)

## Show Images
cv2.imshow("gray", gray)
cv2.imshow("img",img)


while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
