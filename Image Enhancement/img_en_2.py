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

<<<<<<< HEAD
s = '..\\..\\digi\\102_6';
=======
def searchPath(img1, img2, x, y):
    a = x;
    b = y;
    img2[a, b] = 100
    for i in range (0, 10):
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

s = '102_1'
>>>>>>> 0a2994d32621b8c77ee6339e355360c60cd7ca75

# Image input
img = cv2.imread(s + '.tif',0)
cv2.imwrite(img, 'teste.bmp')
height, width = img.shape
size = np.size(img)

# Blur 5x5
kernel = np.ones((5,5),np.float32)/25
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite(s + "_blur.bmp", img)

# Sharpening 5x5
kernel = np.matrix('-1, -1, -1, -1, -1;\
	-1, -1, -1, -1, -1;\
	-1, -1, 25, -1, -1;\
	-1, -1, -1, -1, -1;\
	-1, -1, -1, -1, -1', np.float32)
img = cv2.filter2D(img, -1, kernel)
cv2.imwrite(s + "_sharp.bmp", img)

# Binarization
for i in range(0, height):
    for j in range(0, width):
	if img[i, j] < 80 :
	    img[i, j] = 0
	else:
	    img[i, j] = 255
cv2.imwrite(s + "_binary.bmp", img)

# REVERSAL
for i in range(0, height):
    for j in range(0, width):
	if img[i, j] == 255:
	    img[i, j] = 0
	else:
	    img[i, j] = 255
cv2.imwrite(s + "_inv_binary.bmp", img)

# Skeleton
img = morphology.skeletonize(img_as_float(img))
img = img_as_ubyte(img)
cv2.imwrite(s + "_skel.bmp", img)

imgrgb = cv2.imread(s + '_skel.bmp', 1)

ctrl1 = np.zeros(img.shape,np.uint8)
ctrl2 = np.zeros(img.shape,np.uint8)

for i in range(1, height-1):
    for j in range(1, width-1):
	if neibPoint(img, i, j, 3):
	    ctrl1[i, j] = 255
	    imgrgb[i-1, j-1] = [0, 0, 255]
	    imgrgb[i-1, j] = [0, 0, 255]
	    imgrgb[i-1, j+1] = [0, 0, 255]
	    imgrgb[i, j-1] = [0, 0, 255]
	    imgrgb[i, j+1] = [0, 0, 255]
	    imgrgb[i+1, j-1] = [0, 0, 255]
	    imgrgb[i+1, j] = [0, 0, 255]
	    imgrgb[i+1, j+1] = [0, 0, 255]

for i in range(1, height-1):
    for j in range(1, width-1):
	if neibPoint(img, i, j, -1):
	    ctrl2[i, j] = 255
	    imgrgb[i-1, j-1] = [0, 255, 0]
	    imgrgb[i-1, j] = [0, 255, 0]
	    imgrgb[i-1, j+1] = [0, 255, 0]
	    imgrgb[i, j-1] = [0, 255, 0]
	    imgrgb[i, j+1] = [0, 255, 0]
	    imgrgb[i+1, j-1] = [0, 255, 0]
	    imgrgb[i+1, j] = [0, 255, 0]
	    imgrgb[i+1, j+1] = [0, 255, 0]

# Minutiaes 1: bifurcacoes, ou seja, pontos que possuem 3 pontos adjacentes
# Minutiaes 2: finais de linha, ou seja, que possuem apenas 1 ponto adjacente
cv2.imwrite(s + "_mn_1_2.bmp", imgrgb)
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
	if ctrl3[i, j] == 255:
	    ctrl3[i-1, j-1] = 0
	    ctrl3[i-1, j] = 0
	    ctrl3[i-1, j+1] = 0
	    ctrl3[i, j-1] = 0
	    ctrl3[i, j+1] = 0
	    ctrl3[i+1, j-1] = 0
	    ctrl3[i+1, j] = 0
	    ctrl3[i+1, j+1] = 0

cv2.imwrite(s + "_mn_1_clean.bmp", ctrl3)

# Remocao de bifurcacoes falsas
for i in range(1, height-1):
    for j in range(1, width-1):
	if ctrl1[i, j] == 255:
	    count = 0
	    for a in range(-1, 2):
		for b in range(-1, 2):
		    if img[i+a, j+b] == 255:
			ctrl4 = ctrl1.copy()
			ctrl4[i, j] = 200
			if searchPath(img, ctrl4, i+a, j+b) == False:
			    count += 1
	    if count < 2:
		ctrl3[i, j] = 0

# Minutiaes escolhidas
cv2.imwrite(s + "_mn_1_selection.bmp", ctrl3)

for i in range(0, height):
    for j in range(0, width):
	if img[i, j] == 255:
	    if ctrl3[i, j] == 0:
		ctrl3[i, j] = 40

# Minutiaes com a digital no fundo
cv2.imwrite(s + "_mn_1_selection2.bmp", ctrl3)

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
			if searchPath(img, ctrl4, i+a, j+b) == False:
			    count += 1
	    if count >= 1:
		ctrl3[i, j] = 0

# Minutiaes escolhidas
cv2.imwrite(s + "_mn_2_selection.bmp", ctrl3)

for i in range(0, height):
    for j in range(0, width):
	if img[i, j] == 255:
	    if ctrl3[i, j] == 0:
		ctrl3[i, j] = 40

# Minutiaes com a digital no fundo
cv2.imwrite(s + "_mn_2_selection2.bmp", ctrl3)

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

for i in range(-1, 2):
    for j in range(-1, 2):
	img[tX+i, tY+j] = 255


cv2.imwrite(s + "_core.bmp", img)
