import cv2
import numpy as np
import math
from skimage import morphology, img_as_float, img_as_ubyte


def imageEnhancement(s):
	# Image input
	img = cv2.imread(s + '.tif',0)
	height, width = img.shape
	size = np.size(img)

	# Blur 5x5
	kernel = np.ones((5,5),np.float32)/25
	img = cv2.filter2D(img, -1, kernel)
	# //cv2.imwrite(s + "_blur.bmp", img)

	# Sharpening 5x5
	kernel = np.matrix('-1, -1, -1, -1, -1;\
		-1, -1, -1, -1, -1;\
		-1, -1, 25, -1, -1;\
		-1, -1, -1, -1, -1;\
		-1, -1, -1, -1, -1', np.float32)
	img = cv2.filter2D(img, -1, kernel)
	# cv2.imwrite(s + "_sharp.bmp", img)

	# Binarization
	for i in range(0, height):
		for j in range(0, width):
			if img[i, j] < 80 :
				img[i, j] = 0
			else:
				img[i, j] = 255
	# cv2.imwrite(s + "_binary.bmp", img)

	# REVERSAL
	for i in range(0, height):
		for j in range(0, width):
			if img[i, j] == 255:
				img[i, j] = 0
			else:
				img[i, j] = 255
	# cv2.imwrite(s + "_inv_binary.bmp", img)

	# Skeleton
	img = morphology.skeletonize(img_as_float(img))
	img = img_as_ubyte(img)
	cv2.imwrite(s + "_skel.bmp", img)
	

imageEnhancement('101_1')
imageEnhancement('101_2')
imageEnhancement('101_3')
imageEnhancement('101_4')
imageEnhancement('101_5')
imageEnhancement('101_6')
imageEnhancement('102_1')
imageEnhancement('102_2')
imageEnhancement('102_3')
imageEnhancement('102_4')
