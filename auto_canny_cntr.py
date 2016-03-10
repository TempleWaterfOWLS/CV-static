#!/usr/local/bin/python

# lol do I even still use all of these imports?
import os
import cv2
import math
import numpy as np
import argparse
import glob
import sys


## Set folder of input and output images
infolder = "input-photos/"
outfolder = "output-photos-grid/"

## Set number image and matrix parameters
cols = rows = 8
width = 640
height = 480
blockw = width/cols
blockh = height/rows


### findBuoys(input_image_name)
## Function to use Canny Edge Detection + findContours methods to find buoys in every image in the
## input photo folder, then save the images with the detected contours in the output photo folder.
## It uses weird statistics magic that I stole from the internet to set the parameter for Canny ED. 
def findBuoys(imgname):
    
    ## Load image from input photo folder
    img = cv2.imread(infolder + imgname)

    # Set some parameters automatically (based on statistics magic that I stole from the internet)
    sigma=0.33
    med = np.median(img)
    lower = int(max(0, (1.0 - sigma) * med))
    upper = int(min(255, (1.0 + sigma) * med))
    edged = cv2.Canny(img, lower, upper)

    ## Make image single stream black and white
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## Not gonna lie, I don't super remember what this does
    filteredContour = []

    ## This one is going to contain the center of the contour
    cntCntrs = []

    ## Find the contours in the image composed of Canny edges
    im2, contour,hier = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for iteration in range(0,len(contour)):

        ## Make sure the contour isn't too small (200 is chosen at random)
        areaOfContour = cv2.contourArea(contour[iteration])
        if areaOfContour >= 200:
            print "Contour %d of size %d" %(iteration,areaOfContour)
            filteredContour.append(contour[iteration])

            ## Obtain more location information for each contour
            (x,y), radius = cv2.minEnclosingCircle(contour[iteration])
            center = (int(x), int(y))
            cntCntrs.append(center)
            radius = int(radius)
            ## Draw radius on image
            img = cv2.circle(img, center, radius, (255, 0, 0), 2)
                             
    ## Draw the contours bigger than 200
    cv2.drawContours(img, filteredContour, -1, (0,255,0), 2)
    print cntCntrs
    ## End for loop through contours of Canny edge detected image

    ## Draw gridlines on image
    for h in range(rows):
        img = cv2.line(img, (0, h*blockh), (width, h*blockh), (0, 0, 255), 1)
    for w in range(cols):
        img = cv2.line(img, (w*blockw, 0), (w*blockw, height), (0, 0, 255), 1)

    ## Generate the matrix for the image
    generateMatrix(cntCntrs)
    
    ## Save Images with Canny blobs in output photo folder
    stg = outfolder + imgname
    cv2.imwrite(stg, img)

    ## End of findBuoys

    
def generateMatrix(cCenters):

    
    # Creates a list containing 8 lists initialized to 0
    Matrix = [[0 for x in range(cols)] for x in range(rows)]

    ## Matrix initialized with 0's
    print Matrix

    ## Iterates through the image grid and increments the Matrix cell is a contour center is found there 
    for r in range(rows):
        for c in range(cols):
            #print str(r) + ", " + str(c)
            for cnt in cCenters:
                if cnt[1] > r*blockh and cnt[1] < (r+1)*blockh and cnt[0] > c*blockw and cnt[0] < (c+1)*blockw:
                    Matrix[r][c] = Matrix[r][c]+1

    ## Print buoys center matrix
    print Matrix

## End of generateMatrix()


## Actual main function that I would write cleanly if I wasn't terrible:

#generateMatrix()
findBuoys("left0002.jpg")

"""
## Iterate through all of the input jpg photos in the directory under the working dir
## and run the findBuoys Canny function on them.
for i in os.listdir(os.getcwd()+"/input-photos/"):
    if i.endswith(".jpg"):
        print i
        findBuoys(i)
        continue
    else:
        continue
"""

## Close OpenCV and exit Python script when done
cv2.destroyAllWindows()
sys.exit(0)
