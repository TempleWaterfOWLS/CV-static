CV-static
=========

# Contents
- [File and Folder Descriptions](#file-and-folder-descriptions)
- [Requirements](#requirements)
- [To Do](#to-do)


# File and Folder Descriptions:
####blob.py
Script that loops through all of the .jpg's in the input-photos folder to implement the Blob Detection algorithm on the bottom half of each picture (below the horizon line) in order to find buoys. The script should generate and print a matrix with values in the grid cells where the center of a buoy was found. It draws the 8x8 grid on the bottom half of the picture, as well as all of the detected keypoints. Image is outputted to output-photos-blob.

####blob_single.py
Script that contains the function `blob_single(image)` which should be called with the input of the name of the .jpg in input-photos.

####canny.py
Script that loops through all of the .jpg's in the input-photos folder to implement the Canny Edge Detection algorithm. It is currently set to print out an 8x8 matrix filled with the number of contour centers found in each block of the image divided in an 8x8 grid. It draws the 8x8 grid as well as the contours of the detected buoys on the image outputted to output-photos-canny. NOTE: This is the algorithm we decided to continue with as it worked more efficiently than Blob Detect.

####canny_single.py
Script that contains the function `canny_single(image)` which should be called with the input of the name of the .jpg in input-photos.

####circles.py
Idk? Hough circle transform attempt maybe?

####input-photos
Folder containing images to be input to algorithm. Currently contains the left images 1-100 from the 02/24/16 pool test.

![Input photo](/input-photos/left0002.jpg)

####output-photos-blob
Folder containing the images from input-photos passed through blob.py, on which are drawn the keypoints found (including those in the top half of the photo, not included in the generated matrix).

![Output Blob](/output-photos-blob/left0002.jpg)

####output-photos-canny
Folder containing the image output from canny.py on which is drawn the grid used for the printed matrix as well as the contour and the minimum circles around the center of the contours. Note that the contours should have an area>200 and the radius for their estimated minimum circle should be <75px (arbitrarily chosen to remove the false positives from reflections of the water)

![Output Canny](/output-photos-canny/left0002.jpg)

# Requirements:
* Python 2.7
* OpenCV 3.0

# To Do:
- [ ] Parametrize canny.py so that file to be processed is inputted as a cmd line arg
- [ ] Actually return the matrix from canny.py (needs to eventually integrate into ROS)
- [ ] Clean up both auto_canny scripts. Refactor code.
- [X] Remove the top half of the grid from the matrix (useless above water information, wastes processing time and creates false positives)