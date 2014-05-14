import numpy as np
import cv2

img = cv2.imread("101_1.tif", 0)

img = cv2.filter2D(img, -1,  np.matrix("-1 -1 -1 -1 0 1 1 1 1;\
										-1 -1 -1 -1 0 1 1 1 1;\
										-1 -1 -1 -1 0 1 1 1 1;\
										-1 -1 -1 -1 0 1 1 1 1;\
										0  0  0  0  0 0 0 0 0;\
										1 1 1 1 0 -1 -1 -1 -1;\
										1 1 1 1 0 -1 -1 -1 -1;\
										1 1 1 1 0 -1 -1 -1 -1;\
										1 1 1 1 0 -1 -1 -1 -1"))
cv2.imwrite("filt.bmp", img)