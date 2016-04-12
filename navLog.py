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
    
    # convert the 4th row into 8 bit binary to determine precise local of buoys
    m= '{0:08b}'.format(int_values[3])

    # input argument is currently just the row of the matrix (start at 5th one)
    # starting at middle, check to find where 2 spots are open and determine
    # the relative command that should be sent
    if m[2] and m[3] and m[4] and m[5]:
        command="forward"
    elif m[1] and m[2] and m[3] and m[4]:
        command= "moderate left"
    elif m[3] and m[4] and m[5] and m[6]:
        command="moderate right"
    elif m[0] and m[1] and m[2] and m[3]:
        command="left"
    elif m[4] and m[5] and m[6] and m[7]:
        command="right"
    else:
        command="stop"
    print (command)
    return command

# then publish the command to the topic
    
if __name__=="__main__":
    main()








