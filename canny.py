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
            findBuoys(i)
            continue
        else:
            continue
    
    ## Close OpenCV and exit Python script when done
    cv2.destroyAllWindows()
    sys.exit(0)


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

    ## List that tracks the contours we're interested in (below the halfway point,
    ## and with a radius that isn't too extravagant - ie <75px )
    filteredContour = []

    ## This one is going to contain the center of the contour
    contour_centers = []
    
    ## Find the contours in the image composed of Canny edges
    im2, contour,hier = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for iteration in range(0,len(contour)):

        ## Make sure the contour isn't too small (200 is chosen at random)
        area_of_contour = cv2.contourArea(contour[iteration])
        if area_of_contour >= 200:
            
            ## Obtain the approximate center and radius of each contour
            (x,y), radius = cv2.minEnclosingCircle(contour[iteration])
            center = (int(x), int(y))

            if radius < 75 and center[1]>height/2:
                
                # print "Contour %d of size %d" %(iteration,areaOfContour)
                filteredContour.append(contour[iteration])
                contour_centers.append(center)
                radius = int(radius)
                ## Draw radius on image
                img = cv2.circle(img, center, radius, (255, 0, 0), 2)

            
    ## Draw all contours larger than 200 (in filteredContour)
    cv2.drawContours(img, filteredContour, -1, (0,255,0), 2)
    ## End for loop through contours of Canny edge detected image

    ## Draw the matrix on the output image
    img = draw_matrix(img)
    
    ## Generate the matrix for the image
    generate_matrix(contour_centers)

    
    ## Save Images with Canny blobs in output photo folder
    stg = outfolder + imgname
    cv2.imwrite(stg, img)
    
    ## End of findBuoys

## Draw gridlines on image
def draw_matrix(processed_img):
    
    for h in range(rows):
        img_w_matrix = cv2.line(processed_img, (0, height/2+h*blockh), (width, height/2+h*blockh), (255, 204, 0), 2)
    for w in range(cols):
        img_w_matrix = cv2.line(processed_img, (w*blockw, height/2), (w*blockw, height), (255, 204, 0), 2)

    return processed_img
    ## End of draw_matrix

## Generate the matrix that is to be passed to the navigation portion
def generate_matrix(contour_centers):
    
    # Creates a list containing 8 lists initialized to 0
    Matrix = [[0 for x in range(cols)] for x in range(rows)]
         
    ## Iterates through the bottom half of the image grid and increments the Matrix cell is a contour center is found there 
    for r in range(rows):
        for c in range(cols):
            for cnt in contour_centers:
                if cnt[1] > height/2+r*blockh and cnt[1] < height/2+(r+1)*blockh and cnt[0] > c*blockw and cnt[0] < (c+1)*blockw:
                    Matrix[r][c] = Matrix[r][c]+1

    ## Print buoys center matrix
    print Matrix

## End of generateMatrix()


## Do the main thing
if __name__ == '__main__':
    main()
