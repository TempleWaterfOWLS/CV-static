#!/usr/local/bin/python

import os
import cv2
import math
import numpy as np
import sys

blank = np.zeros((480, 640), np.uint8)
blank[:,:] = (255)

## Set folder of input and output images
infolder = "input-photos/"
outfolder = "output-photos-blob/"

## Set number image and matrix parameters
cols = rows = 8
width = 640
height = 480

## I divide the following height by two because the grid should only cover half of the image
blockw = width/cols
blockh = height/(rows*2)


## Main function
def main():
    ## Iterate through all of the input jpg photos in the directory under the working dir
    ## and run the findBuoys Canny function on them.
    for i in os.listdir(os.getcwd()+"/input-photos/"):
        if i.endswith(".jpg"):
            print i
            findBuoysBlob(i)
            # Whatever function I do here
            continue
        else:
            continue
    
    ## Close OpenCV and exit Python script when done
    cv2.destroyAllWindows()
    sys.exit(0)

## Resize with resize command
def resizeImage(img):
    
    # mapping from destination to source
    dst = cv2.resize(img,None,fx=0.25,fy=0.25,interpolation=cv2.INTER_LINEAR)
    return dst

def findBuoysBlob(imgname):

    centers = []
    
    ## Load image from input photo folder
    img = cv2.imread(infolder + imgname)
        
    ## Make image single stream black and white and find the keypoints for each blob detected
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = cv2.SimpleBlobDetector_create()
    keypts = detector.detect(gray)

    img = cv2.drawKeypoints(img, keypts, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    for k in keypts:
        print "x = %d; y = %d" %(k.pt[0], k.pt[1])

    centers = filter_buoys(keypts)
    generate_matrix(centers)
    img = draw_matrix(img)
    
    ## Save Images with Canny blobs in output photo folder
    stg = outfolder + imgname
    cv2.imwrite(stg, img)


def filter_buoys(unfiltered_buoys):

    ## Keep track of the centers that work
    filtered_centers = []
    
    for buoy in unfiltered_buoys:
        center = (int(buoy.pt[0]), int(buoy.pt[1]))
        if center[1] > height/2:
            filtered_centers.append(center)

    return filtered_centers

## End of filter_buoys

## Draw gridlines on image
def draw_matrix(processed_img):
    
    for h in range(rows):
        img_w_matrix = cv2.line(processed_img, (0, height/2+h*blockh), (width, height/2+h*blockh), (255, 204, 0), 2)
    for w in range(cols):
        img_w_matrix = cv2.line(processed_img, (w*blockw, height/2), (w*blockw, height), (255, 204, 0), 2)

    return processed_img
    ## End of draw_matrix


def generate_matrix(cCenters):
    
    # Creates a list containing 8 lists initialized to 0
    Matrix = [[0 for x in range(cols)] for x in range(rows)]

    ## Iterates through the image grid and increments the Matrix cell is a contour center is found there 
    for r in range(rows):
        for c in range(cols):
            for cnt in cCenters:
                if cnt[1] > height/2+r*blockh and cnt[1] < height/2+(r+1)*blockh and cnt[0] > c*blockw and cnt[0] < (c+1)*blockw:
                    Matrix[r][c] = Matrix[r][c]+1

    ## Print buoys center matrix
    print Matrix

## End of generateMatrix()


## Do the main thing
if __name__ == '__main__':
    main()
