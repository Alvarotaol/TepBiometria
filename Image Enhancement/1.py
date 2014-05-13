from skimage import morphology
import cv2
import numpy as np
import math

i = 0;
j = 0;

# Image input
img = cv2.imread('105_7.tif',0)
height, width = img.shape
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
cv2.imwrite("0_original.bmp", img)

# Blur 5x5
kernel = np.ones((5,5),np.float32)/25
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite("1_blur.bmp", img)

# Sharpening 5x5
kernel = np.matrix('-1, -1, -1, -1, -1;\
					-1, -1, -1, -1, -1;\
					-1, -1, 25, -1, -1;\
					-1, -1, -1, -1, -1;\
					-1, -1, -1, -1, -1', np.float32)
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite("2_sharpening.bmp", img)

# Binarization
# Inicializacao de pobre
output = input 
for i in range(0, height):
	for j in range(0, width):
		if img[i, j] < 100:
			img[i, j] = 0
		else:
			img[i, j] = 255
cv2.imwrite("3_binary.bmp", img)

# REVERSAL
for i in range(0, height):
	for j in range(0, width):
		if img[i, j] == 255:
			img[i, j] = 0
		else:
			img[i, j] = 255
cv2.imwrite("4_REVERSAL.bmp", img)

# Sketonization
# Co piado e Co lado
ret,img = cv2.threshold(img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False
 
while( not done):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy()
 
    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        done = True
cv2.imwrite("5_skeletonization.bmp", skel)

img = morphology.skeletonize(img > 0)
cv2.imwrite("teste.bmp", img)

# # Laplacian
# output = cv2.Laplacian(output, cv2.CV_64F)
# cv2.imwrite("4_laplacian.jpg", output)

# # Binarization
# for i in range(0, height):
	# for j in range(0, width):
		# if output[i, j] < 128:
			# output[i, j] = 0
		# else:
			# output[i, j] = 255
# cv2.imwrite("5_binary.jpg", output)