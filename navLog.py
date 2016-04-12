#!/usr/bin/env python

import sys
import os
import os.path
import canny
import canny_single
import numpy

def main():
    # read in the integer values which represent the binary of where the buoys
    # are in the matrix through the use of canny_single and providing the
    # image to be checked
    int_values=canny_single.canny_single("left0002.jpg")
    #int_values= [2,4,8,16,32,64,80,0]
    # convert the 4th row into 8 bit binary to determine precise local of buoys
    M= '{0:08b}'.format(int_values[2])
    print("M " + M)
    m=[0]*8

    # Initialize output array
    m = [0]*len(M)
    
    # M is read in as a string, but we need to access the bits as binary
    for i in range(len(M)):
        m[i]= str2oppbool(M[i])
    
    # input argument is currently just the row of the matrix (start at 5th one)
    # starting at middle, check to find where 2 spots are open and determine
    # the relative command that should be sent
    if m[2] and m[3] and m[4] and m[5]:
        command="forward" # R= 0.6 L= 0.6
    elif m[1] and m[2] and m[3] and m[4]:
        command= "moderate left" # R= 0.6 L=0.45
    elif m[3] and m[4] and m[5] and m[6]:
        command="moderate right" # R=0.45 L=0.6
    elif m[0] and m[1] and m[2] and m[3]:
        command="left" # R= 0.6 L=0.3
    elif m[4] and m[5] and m[6] and m[7]:
        command="right" # R=0.3 L=0.6
    else:
        command="run awayyyy" # R= 0 L=0.6, maybe even higher
        ## really cant stop, prolly should pick a default side and make a
        ## hard turn to attempt to avoid all, maybe default left?
    print (command)
    return command

# then publish the command to the topic

# Stolen from the interet for our convenience
# switched it to be for the false values since we want the path to 
# be clear, which is represented by a 0, or boolean false
def str2oppbool(v):
    return v.lower() in ("no", "false", "f", "0")


if __name__=="__main__":
    main()








