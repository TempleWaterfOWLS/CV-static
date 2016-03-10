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
outfolder = "output-photos-canny/"

"""
findBuoys(input_image_name)
Function to use Canny Edge Detection + findContours methods to find buoys in every image in the
input photo folder, then save the images with the detected contours in the output photo folder.
It uses weird statistics magic that I stole from the internet to set the parameter for Canny ED.
""" 
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

    ## Find the contours in the image composed of Canny edges
    im2, contour,hier = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for iteration in range(0,len(contour)):
        areaOfContour = cv2.contourArea(contour[iteration])
        if areaOfContour >= 200:
            print "Contour %d of size %d" %(iteration,areaOfContour)
            filteredContour.append(contour[iteration])
            cv2.drawContours(img, filteredContour, -1, (0,255,0), 2)

    ## Save Images with Canny blobs in output photo folder
    stg = outfolder + imgname
    cv2.imwrite(stg, img)

    ## End of findBuoys


## Actual main function that I would write cleanly if I wasn't terrible:
    
## Iterate through all of the input jpg photos in the directory under the working dir
## and run the findBuoys Canny function on them.
for i in os.listdir(os.getcwd()+"/input-photos/"):
    if i.endswith(".jpg"):
        print i
        findBuoys(i)
        continue
    else:
        continue


## Close OpenCV and exit Python script when done
cv2.destroyAllWindows()
sys.exit(0)
