CV-static
=========

# Contents
- [File and Folder Descriptions](#file-and-folder-descriptions)
- [Requirements](#requirements)


# File and Folder Descriptions:
####auto_canny.py
Script that loops through all of the .jpg's in the input-photos folder, performs Canny edge detection using automatically generated parameters, then runs findContours to hopefully find the buoys in the image, draws the contours on the image and saves it in output-photos-canny folder.
Stands for automatically defined parameters, canny edge detection.

####auto_canny_cntr.py
Script that is currently set to print out an 8x8 matrix filled with the number of contour centers found in each block of the image divided in an 8x8 grid. Currently set to operate on input-photos/left0002.jpg from 02/24/16 pool test. Image is outputted to output-photos-grid.
Stands for automatically defined parameters, canny edge detection, contour centers.

####blob.py
Idk? Blob detection algorithm maybe?

####circles.py
Idk? Hough circle transform attempt maybe?

####input-photos
Folder containing images to be input to algorithm. Currently contains the left images 1-100 from the 02/24/16 pool test.

####output-photos-canny
Folder containing the images from input-photos passed through auto_canny.py, on which are drawn the contours with areas>200.

####output-photos-grid
Folder containing the image output from auto_canny_cntr.py on which is drawn the grid used for the printed matrix as well as the contour and the minimum circles around the center of the contours

# Requirements:
* Python 2.7
* OpenCV 3.0

# To Do:
- [ ] Parametrize auto_canny_cntr.py so that file to be processed is inputted as a cmd line arg
- [ ] Actually return the matrix from auto_canny_cntr.py (needs to eventually integrate into ROS)
- [ ] Clean up both auto_canny scripts. Break up into functions, return objects, add main... the whole shebang