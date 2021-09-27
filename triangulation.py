import sys
import cv2
import numpy as np
import time

# funtion
def find_coordination(sort, Lx, Ly, Rx, Ry,  frame_right, frame_left, baseline,f, alpha):

    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    #if width_right == width_left:
    f_pixel = (1280 * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
    
    # CALCULATE THE DISPARITY:
    disparity = Lx - Rx      #Displacement between left and right frames [pixels]

    # CALCULATE DEPTH x, y, z:
    if sort != 'None':
        X = round(float(Lx *0.0198)) # [cm]
        Y = round(float(Ly *0.028),2)
        #Z = round(float((baseline * f_pixel) / disparity), 2)             #Depth in [cm]
        Z = 0 
    else:
        X =0
        Y = 0
        Z = 0
    #print(X, Y, Z)
    return X, Y, Z

