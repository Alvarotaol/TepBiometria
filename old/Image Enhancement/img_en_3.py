import cv2
import numpy as np
import math
from skimage import morphology, img_as_float, img_as_ubyte

def neibPoint(img, x, y, qt):
    i = -1;
    j = -1;
    neibQt = -1
    if img[x, y] == 255:
	for i in range(-1, 2):
	    for j in range(-1, 2):
		if img[(x + i), (y + j)] == 255:
		    neibQt += 1
    if neibQt == qt and qt > 0:
	return True
    elif neibQt == -qt and qt < 0:
	return True
    else:
	return False

s = '102_6'

# Image input
img = cv2.imread(s + '.tif',0)
height, width = img.shape
size = np.size(img)

# Laplacian
kernel = np.matrix('0, 1, 0;\
	            1 -4, 1;\
	            0, 1, 0', np.float32)*10
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite(s + "_1_lap.bmp", img)

# Blur 5x5 duplo
kernel = np.ones((5,5),np.float32)/25
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite(s + "_2_blur.bmp", img)

# Binarization
for i in range(0, height):
    for j in range(0, width):
	if img[i, j] < 110 :
	    img[i, j] = 0
	else:
	    img[i, j] = 255
cv2.imwrite(s + "_4_binary.bmp", img)

# Skeleton
img = morphology.skeletonize(img_as_float(img))
img = img_as_ubyte(img)
cv2.imwrite(s + "_5_skel.bmp", img)

imgrgb = cv2.imread(s + '_5_skel.bmp', 1)

ctrl1 = np.zeros(img.shape,np.uint8)
ctrl2 = np.zeros(img.shape,np.uint8)

for i in range(1, height-1):
    for j in range(1, width-1):
	if neibPoint(img, i, j, 3):
	    ctrl1[i, j] = 255
	    imgrgb[i-1, j-1] = [0, 0, 255]
	    imgrgb[i-1, j] = [0, 0, 255]
	    imgrgb[i-1, j+1] = [0, 0, 255]
	    imgrgb[i, j-1] = [0, 0, 255]
	    imgrgb[i, j+1] = [0, 0, 255]
	    imgrgb[i+1, j-1] = [0, 0, 255]
	    imgrgb[i+1, j] = [0, 0, 255]
	    imgrgb[i+1, j+1] = [0, 0, 255]

for i in range(1, height-1):
    for j in range(1, width-1):
	if neibPoint(img, i, j, -1):
	    ctrl2[i, j] = 255
	    imgrgb[i-1, j-1] = [0, 255, 0]
	    imgrgb[i-1, j] = [0, 255, 0]
	    imgrgb[i-1, j+1] = [0, 255, 0]
	    imgrgb[i, j-1] = [0, 255, 0]
	    imgrgb[i, j+1] = [0, 255, 0]
	    imgrgb[i+1, j-1] = [0, 255, 0]
	    imgrgb[i+1, j] = [0, 255, 0]
	    imgrgb[i+1, j+1] = [0, 255, 0]

cv2.imwrite(s + "_6_mn_1_2.bmp", imgrgb)
cv2.imwrite(s + "_7_mn_1_only.bmp", ctrl1)
cv2.imwrite(s + "_8_mn_2_only.bmp", ctrl2)
