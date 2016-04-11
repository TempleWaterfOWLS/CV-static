#!/usr/bin/env python

import sys
import os
import os.path
import canny
import canny_single
import subprocess

def main():
    m=subprocess.Popen("canny_single.py",shell=True)

    #input argument is currently just the row of the matrix (start at 5th one)
    if m[3] and m[4]:
        command="forward"
    elif m[3] and m[2]:
        command= "slight left"
    elif m[4] and m[5]:
        command="slight right"
    elif m[2] and m[1]:
        command="moderate left"
    elif m[5] and m[6]:
        command="moderate right"
    elif m[1] and m[0]:
        command="hard left"
    elif m[6] and m[7]:
        command="hard right"
    else:
        command="stop"
    print (command)

#publish the command to the topic
    
if __name__=="__main__":
    main()








