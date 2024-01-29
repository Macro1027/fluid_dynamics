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


def distance(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def create_cylinder(Ny, Nx, radius):
    cylinder = np.full((Ny, Nx), False)
    for y in range(Ny):
        for x in range(Nx):
            # Loci of cylinder
            if distance(x, y, Nx//4, Ny//2) < radius: 
                cylinder[y][x] = True
    return cylinder

def create_from_img(img, Ny, Nx, y, x, radius):
    base = np.full((Ny, Nx), False)
    image = cv2.imread(img)

    # Resize the image to fit into the region
    resized_image = cv2.resize(image, (radius, radius))

    base[y:y+radius, x:x+radius] = img_to_bool(resized_image)
    
    return base