import cv2
import numpy as np
from sklearn import svm


# Funcao de calculo das coordenadas polares
def pol(x, y, a, b, c):
	dist = np.sqrt((a-x)**2 + (b-y)**2)
	
	xVar = a - x
	yVar = b - y
	ang = 0
	if yVar >= 0:
		if xVar >= 0:
			ang = 1
		else:
			ang = 3
	else:
		if xVar < 0:
			ang = 5
		else:
			ang = 7
	
	if ((ang % 4 == 1 and abs(xVar) > abs(yVar)) or (ang % 4 == 3 and abs(xVar) <= abs(yVar))):
		ang -= 1
	
	#ang = np.arctan()
	return [dist, ang, c]

#le as coordenadas cartesianas e as converte para polares
def lerArquivo(s):
	coord = []
	file = open(s + '_coord.txt', 'r')
	line = file.readline().strip()
	lineList = line.split(',')
	coord.append([int(lineList[0]), int(lineList[1]), -1])
	line = file.readline().strip()
	lineList = line.split(',')
	coord.append([int(lineList[0]), int(lineList[1]), -1])
	line = file.readline().strip()
	while line != '':
		lineList = line.split(',')
		coord.append(pol(coord[0][0], coord[0][1], int(lineList[0]), int(lineList[1]), coord[0][2]))
		line = file.readline().strip()
	file.close()
	return coord

# Calculo de matching
def matchCalc(s1, s2, matchList, matchClass, classValue):
	coord1 = []
	coord2 = []
	matchScore = 0
	matchQt = 0
	listLen = 0
	radDist = 0.0
	radAngle = 0.0
	angCor1 = 0
	angCor2 = 0
	tresh = 20

	coord1 = lerArquivo(s1)
	coord2 = lerArquivo(s2)
		
	# Comparacao de minutiaes
	coord1Size = len(coord1)
	coord2Size = len(coord2)
	if coord1Size < coord2Size:
		listLen = coord1Size/2
	else:
		listLen = coord2Size/2
	matchQt = 0 
	for i in range(2, min(coord1Size,coord2Size) -1):
		if coord1[i][2] == coord2[i][2]:
			radDist = abs(coord1[i][0] - coord2[i][0])
			radAngle = abs(coord1[i][1] - coord2[i][1])
			# Correcao do 8 com 1
			if radAngle == 7:
				radAngle = 1
			# Caso nao sejam adjacentes, punicao. Caso sejam, adiciona peso
			if radAngle > 1:
				radAngle = tresh
			else:
				radAngle * 160
			if radDist  < tresh:
				matchQt = matchQt + 1
			
	# Calculo final
	matchScore = pow(matchQt, 2)/(float(((coord1Size)*(coord2Size)))+1)
	matchList.append([matchScore, matchQt])
	matchClass.append(classValue)


# Listas (vazias) das coordenadas polares
matchList = []
matchClass = []
predictList = []
predictClass = []

# Calculo de matching
s = "img/10%i_%i"

matchCalc(s%(1, 1), s%(1, 1), matchList, matchClass, 1)
matchCalc(s%(1, 1), s%(1, 3), matchList, matchClass, 1)
matchCalc(s%(2, 1), s%(1, 1), matchList, matchClass, 0)

matchCalc(s%(1, 1), s%(1, 4), predictList, predictClass, 1)
matchCalc(s%(1, 1), s%(2, 2), predictList, predictClass, 0)

clf = svm.SVC(kernel='linear')
clf.fit(matchList, matchClass)

result = clf.predict(predictList)
print predictList
print matchList
matching = 0
for i in range(0, len(result)):
	if result[i] == predictClass[i]:
		matching += 1
print matching
