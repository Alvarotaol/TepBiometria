import cv2, sys
import numpy as np
import math
from skimage import morphology, img_as_float, img_as_ubyte


def neibPoint(img, x, y, qt):
	i = -1;
	j = -1;
	neibQt = -1
	if img[x, y] == 255:
		for i in range(-1, 2):
			for j in range(-1, 2):
				if img[(x + i), (y + j)] == 255:
					neibQt += 1
	if neibQt == qt and qt > 0:
		return True
	elif neibQt == -qt and qt < 0:
		return True
	else:
		return False


def searchPath(img1, img2, x, y, distance):
	a = x;
	b = y;
	img2[a, b] = 100
	for i in range (0, distance):
		for m in range(-1, 2):
			for n in range(-1, 2):
				if img1[a+m, b+n] == 255:
					if img2[a+m, b+n] == 0:
						a = a+m
						b = b+n
						img2[a, b] = 100
					elif img2[a+m, b+n] == 255:
						return False
	return True


def minutiaeExtraction(s):
	print s
	file = open(s + '_coord.txt', 'w')

	img = cv2.imread(s + '_skel.bmp', 0)
	height, width = img.shape
	size = np.size(img)

	img1 = np.zeros(img.shape,np.uint8)
	img2 = np.zeros(img.shape,np.uint8)

	for i in range(1, height-1):
		for j in range(1, width-1):
			if neibPoint(img, i, j, 3):
				img1[i, j] = 255
	
	for i in range(1, height-1):
		for j in range(1, width-1):
			if neibPoint(img, i, j, -1):
				img2[i, j] = 255

	# Borda falsa - para evitar falha de segmentacao e variantes
	for i in range(0, height):
		img[i, 0] = 0
		img[i, width-1] = 0
	for i in range(0, width):
		img[0, i] = 0
		img[height-1, i] = 0
	
	# Minutiaes escolhidas
	cv2.imwrite(s + "_mn_1_selection.bmp", img1)

	img3 = img2.copy()
	# Inicios e terminos de linha
	for i in range(1, height-1):
		for j in range(1, width-1):
			if img2[i, j] == 255:
				count = 0
				for a in range(-1, 2):
					for b in range(-1, 2):
						if img[i+a, j+b] == 255:
							img4 = img2.copy()
							img4[i, j] = 200
							if not searchPath(img, img4, i+a, j+b, 50):
								count += 1
				if count >= 1:
					img3[i, j] = 0

	# Retiradas de terminais unidos
	for i in range(1, height-1):
		for j in range(1, width-1):
			if img3[i][j] == 255:
				for k in range(-20, 21):
					for l in range(-20, 21):
						if i+k < height and j+l < width:
							img3[i+k][j+l] = 0
				img3[i][j] = 255
				
	img2 = img3.copy()
	img3 = np.zeros(img1.shape,np.uint8)
	
	# Core 1
	tX = 0
	tY = 0
	qt = 0
	for i in range(0, height):
		for j in range(0, width):
			if img1[i, j] == 255:
				tX += i
				tY += j
				qt += 1

	tX /= qt
	tY /= qt
	file.write(str(tX)+','+str(tY)+'\n')
	
	# Core 2
	tX = 0
	tY = 0
	qt = 0
	for i in range(0, height):
		for j in range(0, width):
			if img2[i, j] == 255:
				tX += i
				tY += j
				qt += 1

	tX /= qt
	tY /= qt
	file.write(str(tX)+','+str(tY)+'\n')

	# Escolha entre todas as minutiae

	img1 = cv2.imread(s + "_mn_1_selection.bmp", 0)
#	img2 = cv2.imread(s + "_mn_2_selection.bmp", 0)
	img3 = img1
	img3 = np.zeros(img1.shape,np.uint8)

	for i in range(0, height):
		for j in range(0, width):
			if img1[i][j] == 255: #or img2[i][j] == 255:
				if math.sqrt( math.pow(abs(i - tX), 2) + math.pow(abs(j - tY), 2)) < 170:
					img3[i][j] = 255

	# Retiradas de minutiaes unidos
	for i in range(1, height-1):
		for j in range(1, width-1):
			if img3[i][j] == 255:
				for k in range(-20, 21):
					for l in range(-20, 21):
						if i+k < height and j+l < width:
							img3[i+k][j+l] = 0
				img3[i][j] = 255
				if img1[i][j] == 255:
					file.write(str(i)+','+str(j)+',1\n')
				else:
					file.write(str(i)+','+str(j)+',0\n')

	cv2.imwrite(s + "_minutiae.bmp", img3)
	file.close()
	
s = "img/10%i_%i"
for i in range(1, 6):
	for j in range(1, 9):
		minutiaeExtraction(s%(i, j))
#for i in range(1, 9):
#	minutiaeExtraction("img/110_%i"%i)
