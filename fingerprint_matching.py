import cv2
import numpy as np

def pol(x, y, a, b):
	dist = np.sqrt((a-x)**2 + (b-y)**2)
	ang = np.pi
	if a-x != 0:
		ang = np.arctan((b-y)/(a-x))
	return [dist, ang]

s = '101_1'

img_min = cv2.imread(s + '_minutiae.bmp', 0)
img_core = cv2.imread(s + '_core.bmp', 0)
height, width = img_min.shape
size = np.size(img_min)

for i in range (0, height):
    for j in range(0, width):
	if img_core[i, j] == 255:
	    cX = i
	    cY = j

a = []

for i in range (0, height):
    for j in range(0, width):
	if img_min[i, j] == 255:
	    a.append(pol(i, j, cX, cY))

print('.2%f' % a)
