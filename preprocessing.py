import cv2
import numpy as np

def img_to_bool(img):
    # Convert the image to grayscale
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold, all pixel values in the grayscale image above 127 will be set to 255 (white), all pixel values below 127 will be set to 0 (black)
    _, im_bw = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)

    
    # Convert the binary image to a boolean array, where True represents white pixels (255) and False represents black pixels (0)
    im_bool = im_bw == 255  
    return np.logical_not(im_bool == 1)

# print(img_to_bool(cv2.imread("cow.png"), 30))