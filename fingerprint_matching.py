import cv2
import numpy as np

def pol(x, y, a, b):
	dist = np.sqrt((a-x)**2 + (b-y)**2)
	ang = np.pi
	if a-x != 0:
		ang = np.arctan((b-y)/(a-x))
	return dist, ang

img_min = cv2.imread(s + '_minutiae.bmp', 0)
img_core = cv2.imread(s + '_core.bmp', 0)
height, width = img.shape
size = np.size(img)

for i in range (0, height):
    for j in range(0, width):
	if img_core[i, j] == 255:
	    cX = i
	    cY = j

for i in range (0, height):
    for j in range(0, width):
	if img[i, j] == 255:
	    #ALGO pol(i, j, cX, cY)
