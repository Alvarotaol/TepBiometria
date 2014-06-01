import cv2
import numpy as np
from sklearn import svm

# Funcao de calculo das coordenadas polares
def pol(x, y, a, b):
    dist = np.sqrt((a-x)**2 + (b-y)**2)
    ang = np.pi
    if a-x != 0:
	ang = np.arctan((b-y)/(a-x))
    return [dist, ang]


# Codigo das digitais
s1 = '101_1'
s2 = '101_2'
s3 = '102_1'
s4 = '101_3'

# Leitura das minutiaes e cores
# PS.: Trocar por leitura de arquivos .txt
img_min1 = cv2.imread(s1 + '_minutiae.bmp', 0)
img_core1 = cv2.imread(s1 + '_core.bmp', 0)
img_min2 = cv2.imread(s2 + '_minutiae.bmp', 0)
img_core2 = cv2.imread(s2 + '_core.bmp', 0)
img_min3 = cv2.imread(s3 + '_minutiae.bmp', 0)
img_core3 = cv2.imread(s3 + '_core.bmp', 0)
img_min4 = cv2.imread(s4 + '_minutiae.bmp', 0)
img_core4 = cv2.imread(s4 + '_core.bmp', 0)
height, width = img_min1.shape
size = np.size(img_min1)

# Listas (vazias) das coordenadas polares
coord1 = []
coord2 = []
coord3 = []
coord4 = []
coord5 = []
coord6 = []
matchList = []
predictList = []
matchClass = []
matchScore = 0
matchQt = 0
listLen = 0
radDist = 0.0
radAngle = 0.0
tresh = 20

# Comparacao 1 e 2
# Primeira digital
# Extracao do core
for i in range (0, height):
	for j in range(0, width):
		if img_core1[i, j] == 255:
		    cX,cY = i,j

# Extracao das minutiaes, conversao para coordenadas polares
for i in range (0, height):
    for j in range(0, width):
		if img_min1[i, j] == 255:
			coord1.append(pol(cX, cY, i, j))

# Segunda digital
# Extracao do core
for i in range (0, height):
	for j in range(0, width):
		if img_core2[i, j] == 255:
		    cX,cY = i,j

# Extracao das minutiaes, conversao para coordenadas polares
for i in range (0, height):
    for j in range(0, width):
		if img_min2[i, j] == 255:
			coord2.append(pol(cX, cY, i, j))

# Calculo dos pontos de matching
coord1Size = len(coord1)
coord2Size = len(coord2)
if coord1Size < coord2Size:
	listLen = coord1Size
else:
	listLen = coord2Size

matchQt = 0
for i in range(0, listLen/2):
	radDist = abs((coord1.pop()).pop(0) - (coord2.pop()).pop(0))/2
	radAngle = abs((coord1.pop()).pop() - (coord2.pop()).pop())/2
	if radDist + radAngle <	tresh:
		matchQt = matchQt + 1

matchScore = pow(matchQt, 2)/float(((coord1Size/2)*(coord2Size/2)))
matchList.append([matchScore, matchQt])
matchClass.append(1)

# Comparacao 3 e 4
# Terceira digital
# Extracao do core
for i in range (0, height):
	for j in range(0, width):
		if img_core2[i, j] == 255:
		    cX,cY = i,j

# Extracao das minutiaes, conversao para coordenadas polares
for i in range (0, height):
    for j in range(0, width):
		if img_min2[i, j] == 255:
			coord3.append(pol(cX, cY, i, j))

# Quarta digital
# Extracao do core
for i in range (0, height):
	for j in range(0, width):
		if img_core3[i, j] == 255:
		    cX,cY = i,j

# Extracao das minutiaes, conversao para coordenadas polares
for i in range (0, height):
    for j in range(0, width):
		if img_min3[i, j] == 255:
			coord4.append(pol(cX, cY, i, j))

# Calculo dos pontos de matching
coord3Size = len(coord3)
coord4Size = len(coord4)
if coord3Size < coord4Size:
	listLen = coord3Size
else:
	listLen = coord4Size

matchQt = 0
for i in range(0, listLen/2):
	radDist = abs((coord3.pop()).pop(0) - (coord4.pop()).pop(0))/2
	radAngle = abs((coord3.pop()).pop() - (coord4.pop()).pop())/2
	if radDist + radAngle <	tresh:
		matchQt = matchQt + 1

matchScore = pow(matchQt, 2)/float(((coord3Size/2)*(coord4Size/2)))
matchList.append([matchScore, matchQt])
matchClass.append(0)

# Comparacao 5 e 6
# Extracao do core
for i in range (0, height):
	for j in range(0, width):
		if img_core1[i, j] == 255:
		    cX,cY = i,j

# Extracao das minutiaes, conversao para coordenadas polares
for i in range (0, height):
    for j in range(0, width):
		if img_min1[i, j] == 255:
			coord5.append(pol(cX, cY, i, j))

# Extracao do core
for i in range (0, height):
	for j in range(0, width):
		if img_core4[i, j] == 255:
		    cX,cY = i,j

# Extracao das minutiaes, conversao para coordenadas polares
for i in range (0, height):
    for j in range(0, width):
		if img_min4[i, j] == 255:
			coord6.append(pol(cX, cY, i, j))

# Calculo dos pontos de matching
coord5Size = len(coord5)
coord6Size = len(coord6)
if coord5Size < coord6Size:
	listLen = coord5Size
else:
	listLen = coord6Size

matchQt = 0
for i in range(0, listLen/2):
	radDist = abs((coord5.pop()).pop(0) - (coord6.pop()).pop(0))/2
	radAngle = abs((coord5.pop()).pop() - (coord6.pop()).pop())/2
	if radDist + radAngle <	tresh:
		matchQt = matchQt + 1

matchScore = pow(matchQt, 2)/float(((coord5Size/2)*(coord6Size/2)))
predictList.append([matchScore, matchQt])

# Aprendizado e verificacao
print(matchList)
print(matchClass)
print(predictList)

clf = svm.SVC(kernel='linear')
clf.fit(matchList, matchClass)

print(clf.predict(predictList))
