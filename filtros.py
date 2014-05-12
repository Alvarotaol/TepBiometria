import cv2
import numpy as np
import math


def trabalho(img, xu, xd):
	height, width = img.shape
	size = np.size(img)
	skel = np.zeros(img.shape,np.uint8)
	#cv2.imwrite("0_original.jpg", img)
	  
	# Blur 5x5
	#kernel = np.ones((5,5),np.float32)/25
	img = cv2.blur(img, (5,5))
	# cv2.imwrite("1_blur.jpg", img)

	# Sharpening 5x5 
	kernel = np.matrix('-1 -1 -1 -1 -1;\
						-1 -1 -1 -1 -1;\
						-1 -1 25 -1 -1;\
						-1 -1 -1 -1 -1;\
						-1 -1 -1 -1 -1'	, np.float32)
	img = cv2.filter2D(img, -1, kernel)
	# cv2.imwrite("2_sharpening.jpg", img)

	# Laplacian 
	# img = cv2.Laplacian(img, cv2.CV_64F) 
	# cv2.imwrite("2_laplacian.jpg", img) 

	# Binarization
	for i in range(0, height):
		for j in range(0, width):
			if img[i, j] < 100:
				img[i, j] = 0
			else:
				img[i, j] = 255
	# cv2.imwrite("3_binary.jpg", img)
	  
	# REVERSAL
	for i in range(0, height):
		for j in range(0, width):
			img[i, j] = 255 - img[i, j]

	# cv2.imwrite("4_REVERSALRUSSA.jpg", img)

	# Sketonization
	# Co piado e Co lado
	ret,img = cv2.threshold(img,127,255,0)
	element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	done = False

	while(not done):
		erotic = cv2.erode(img,element)
		temp = cv2.dilate(erotic,element)
		temp = cv2.subtract(img,temp)
		skel = cv2.bitwise_or(skel,temp)
		img = erotic.copy()

		zeros = size - cv2.countNonZero(img)
		if zeros==size:
			done = True
	# cv2.imwrite("5_skeletonizeixon.jpg", skel)
	
	#pode alterar o nome saidas e saida se quiser. mude cada nome de arquivo acima pra seguir o mesmo esquema
	
	cv2.imwrite("saidasteste\\saida10%d_%d.bmp" %(xu, xd), skel)

#Parte importante: substitua 'digi' pela pasta com as digitais. Te vire
str = 'digi\\10%d_%d.tif'
for i in range(1,11):
	print "ma oe"
	for j in range(1,2):
		img = cv2.imread(str % (i, j),0)
		trabalho(img, i, j)

# Image input
# img = cv2.imread('digi\\101_1.tif',0)
# trabalho(img, 1, 1)
