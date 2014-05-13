import cv2
import numpy as np
import math
from skimage import morphology, img_as_float, img_as_ubyte

i = 0;
j = 0;

s = '102_6';

# Image input
img = cv2.imread(s + '.tif',0)
height, width = img.shape
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
cv2.imwrite(s + "_0.bmp", img)

# Blur 5x5
kernel = np.ones((5,5),np.float32)/25
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite(s + "_1.bmp", img)

# Sharpening 5x5
kernel = np.matrix('-1, -1, -1, -1, -1;\
					-1, -1, -1, -1, -1;\
					-1, -1, 25, -1, -1;\
					-1, -1, -1, -1, -1;\
					-1, -1, -1, -1, -1', np.float32)
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite(s + "_2.bmp", img)

# Binarization
for i in range(0, height):
	for j in range(0, width):
		if img[i, j] < 100:
			img[i, j] = 0
		else:
			img[i, j] = 255
cv2.imwrite(s + "_3.bmp", img)

# REVERSAL
for i in range(0, height):
	for j in range(0, width):
		if img[i, j] == 255:
			img[i, j] = 0
		else:
			img[i, j] = 255
cv2.imwrite(s + "_4.bmp", img)

img = morphology.skeletonize(img_as_float(img))
cv2.imwrite(s + "_5.bmp", img_as_ubyte(img))
