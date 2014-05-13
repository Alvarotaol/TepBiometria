import cv2
import numpy as np
import math

i = 0;
j = 0;

# Image input
img = cv2.imread('101_1.tif',0)
height, width = img.shape
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
cv2.imwrite("0_original.jpg", img)

# Blur 5x5
kernel = np.ones((5,5),np.float32)/25
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite("1_blur.jpg", img)

# Sharpening 3x3
kernel = np.matrix('-1, -1, -1;\
					-1, 9, -1;\
					-1, -1, -1', np.float32)
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite("2_sharpening.jpg", img)

# Binarization
for i in range(0, height):
	for j in range(0, width):
		if img[i, j] < 120:
			img[i, j] = 0
		else:
			img[i, j] = 255
cv2.imwrite("3_binary.jpg", img)

# Laplacian
img = cv2.Laplacian(img, cv2.CV_64F)
cv2.imwrite("4_laplacian.jpg", img)


# # Binarization
# for i in range(0, height):
	# for j in range(0, width):
		# if output[i, j] < 128:
			# output[i, j] = 0
		# else:
			# output[i, j] = 255
# cv2.imwrite("5_binary.jpg", output)