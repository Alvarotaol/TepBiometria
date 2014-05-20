import numpy as np
import cv2

def  acharDir(img, x, y):
	m = np.matrix("1 1 0 -1 -1;1 1 0 -1 -1;0 0 0 0 0;-1 -1 0 1 1;-1 -1 0 1 1")
	soma = 0
	for i in range(5):
		for j in range(5):
			soma += img[x+i, y+j] * m[i,j]
	
	return soma

def orientar(img):
	x, y = img.shape
	for i in range(x/5):
		for j in range(y/5):
			#simples
			dir = acharDir(img, i * 5, j * 5)
			if dir < -50:
				for k in range(5):
					img[i*5 + k][j*5:j*5+5] = [255,255,255,255,255]
			elif dir > 300:
				for k in range(5):
					img[i*5 + k][j*5:j*5+5] = [128,128,128,128,128]
			else:
				for k in range(5):
					img[i*5 + k][j*5:j*5+5] = [0,0,0,0,0]

img = cv2.imread("fuc.bmp", 0)

orientar(img)
cv2.imwrite("1_quant.bmp", img)
img = cv2.filter2D(img, -1, np.matrix("0 1 0;1 1 1;0 1 0"))
cv2.imwrite("2_filt.bmp", img)