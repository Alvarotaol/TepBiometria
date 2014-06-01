import cv2
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

s = '101_3'

# imgrgb = cv2.imread(s + '_skel.bmp', 1)
img = cv2.imread(s + '_skel.bmp', 0)
height, width = img.shape
size = np.size(img)

ctrl1 = np.zeros(img.shape,np.uint8)
ctrl2 = np.zeros(img.shape,np.uint8)

for i in range(1, height-1):
	for j in range(1, width-1):
		if neibPoint(img, i, j, 3):
			ctrl1[i, j] = 255
			# imgrgb[i-1, j-1] = [0, 0, 255]
			# imgrgb[i-1, j] = [0, 0, 255]
			# imgrgb[i-1, j+1] = [0, 0, 255]
			# imgrgb[i, j-1] = [0, 0, 255]
			# imgrgb[i, j+1] = [0, 0, 255]
			# imgrgb[i+1, j-1] = [0, 0, 255]
			# imgrgb[i+1, j] = [0, 0, 255]
			# imgrgb[i+1, j+1] = [0, 0, 255]
	
for i in range(1, height-1):
	for j in range(1, width-1):
		if neibPoint(img, i, j, -1):
			ctrl2[i, j] = 255
			# imgrgb[i-1, j-1] = [0, 255, 0]
			# imgrgb[i-1, j] = [0, 255, 0]
			# imgrgb[i-1, j+1] = [0, 255, 0]
			# imgrgb[i, j-1] = [0, 255, 0]
			# imgrgb[i, j+1] = [0, 255, 0]
			# imgrgb[i+1, j-1] = [0, 255, 0]
			# imgrgb[i+1, j] = [0, 255, 0]
			# imgrgb[i+1, j+1] = [0, 255, 0]

# Minutiaes 1: bifurcacoes, ou seja, pontos que possuem 3 pontos adjacentes
# Minutiaes 2: finais de linha, ou seja, que possuem apenas 1 ponto adjacente
# cv2.imwrite(s + "_mn_1_2.bmp", imgrgb)
cv2.imwrite(s + "_mn_1_only.bmp", ctrl1)
cv2.imwrite(s + "_mn_2_only.bmp", ctrl2)

# Borda falsa - para evitar falha de segmentacao e variantes
for i in range(0, height):
	img[i, 0] = 0
	img[i, width-1] = 0
for i in range(0, width):
	img[0, i] = 0
	img[height-1, i] = 0

ctrl3 = ctrl1.copy()

# Retiradas de "bifurcacoes" unidas
for i in range(1, height-1):
	for j in range(1, width-1):
		if ctrl3[i][j] == 255:
			for k in range(-30, 31):
				for l in range(-30, 31):
					if i+k < height and j+l < width:
						ctrl3[i+k][j+l] = 0
			ctrl3[i][j] = 255

# cv2.imwrite(s + "_mn_1_clean.bmp", ctrl3)

# # Remocao de bifurcacoes falsas
# for i in range(1, height-1):
#	for j in range(1, width-1):
#	if ctrl1[i, j] == 255:
#		count = 0
#	    for a in range(-1, 2):
#		for b in range(-1, 2):
#		    if img[i+a, j+b] == 255:
#			ctrl4 = ctrl1.copy()
#			ctrl4[i, j] = 200
#			if searchPath(img, ctrl4, i+a, j+b) == False:
#			    count += 1
#	    if count < 2:
#		ctrl3[i, j] = 0

# Minutiaes escolhidas
cv2.imwrite(s + "_mn_1_selection.bmp", ctrl3)

for i in range(0, height):
	for j in range(0, width):
		if img[i, j] == 255:
			if ctrl3[i, j] == 0:
				ctrl3[i, j] = 40

# Minutiaes com a digital no fundo
# cv2.imwrite(s + "_mn_1_selection2.bmp", ctrl3)

ctrl3 = ctrl2.copy()

# Inicios e terminos de linha
for i in range(1, height-1):
	for j in range(1, width-1):
		if ctrl2[i, j] == 255:
			count = 0
			for a in range(-1, 2):
				for b in range(-1, 2):
					if img[i+a, j+b] == 255:
						ctrl4 = ctrl2.copy()
						ctrl4[i, j] = 200
						if not searchPath(img, ctrl4, i+a, j+b, 50):
							count += 1
			if count >= 1:
				ctrl3[i, j] = 0

# Retiradas de terminais unidos
for i in range(1, height-1):
	for j in range(1, width-1):
		if ctrl3[i][j] == 255:
			for k in range(-20, 21):
				for l in range(-20, 21):
					if i+k < height and j+l < width:
						ctrl3[i+k][j+l] = 0
			ctrl3[i][j] = 255

# Minutiaes escolhidas
cv2.imwrite(s + "_mn_2_selection.bmp", ctrl3)

for i in range(0, height):
	for j in range(0, width):
		if img[i, j] == 255:
			if ctrl3[i, j] == 0:
				ctrl3[i, j] = 40

# Minutiaes com a digital no fundo
# cv2.imwrite(s + "_mn_2_selection2.bmp", ctrl3)

# Calculo do core
img = cv2.imread(s + "_mn_1_selection.bmp", 0)
tX = 0
tY = 0
qt = 0
for i in range(0, height):
	for j in range(0, width):
		if img[i, j] == 255:
			tX += i
			tY += j
			qt += 1

img = np.zeros(img.shape,np.uint8)
tX /= qt
tY /= qt

# for i in range(-1, 2):
#   for j in range(-1, 2):
# 	img[tX+i, tY+j] = 255
img[tX, tY] = 255

cv2.imwrite(s + "_core.bmp", img)

# Escolha entre todas as minutiae

img = cv2.imread(s + "_mn_1_selection.bmp", 0)
img2 = cv2.imread(s + "_mn_2_selection.bmp", 0)
img3 = img
img3 = np.zeros(img.shape,np.uint8)

for i in range(0, height):
	for j in range(0, width):
		if img[i][j] == 255 or img2[i][j] == 255:
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

cv2.imwrite(s + "_minutiae.bmp", img3)
