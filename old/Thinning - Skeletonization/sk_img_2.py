import numpy as np
import cv2

def casou(img, x, y):
	#tipo 1
	#teste branco
	if img[x-1,y-1] > 1:
		#teste horizontal
		if img[x-1,y] > 1 and img[x-1,y+1] > 1:
			if img[x+1,y-1] + img[x+1,y] + img[x+1,y+1] == 0:
				return True
		#teste vertical
		
		if img[x,y-1] > 1 and img[x+1,y-1] > 1:
			if img[x-1,y+1] + img[x,y+1] + img[x+1,y+1] == 0:
				return True
	#teste preto
	else:
		#teste horizontal
		if img[x-1,y] == 0 and img[x-1,y+1] == 0:
			if img[x+1,y-1] * img[x+1,y] * img[x+1,y+1] > 0:
				return True
		#teste vertical
		if img[x,y-1] == 0 and img[x+1,y-1] == 0:
			if img[x-1,y+1] * img[x,y+1] * img[x+1,y+1] > 0:
				return True
	return False

def marcar(img):
	x, y = img.shape
	for i in range(1,x-1):
		for j in range(1, y-1):
			if img[i,j] == 255 and casou(img, i, j):
				img[i,j] = 127

img = cv2.imread("4_REVERSAL.bmp", 0)
print "uhuuu"
marcar(img)
cv2.imwrite("skel.bmp", img)
