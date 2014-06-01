import cv2
import numpy as np
from sklearn import svm


# Funcao de calculo das coordenadas polares
def pol(x, y, a, b, c):
	dist = np.sqrt((a-x)**2 + (b-y)**2)
	
	xVar = a - x
	yVar = b - y
	ang = 0
	if xVar >= 0:
		if yVar >= 0:
			ang = 2
		elif yVar < 0:
			ang = 4
	elif xVar < 0:
		if yVar < 0:
			ang = 6
		elif xVar >= 0:
			ang = 8
	
	if abs(xVar) > abs(yVar):
		ang -= 1
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
		coord.append(pol(int(lineList[0]), int(lineList[1]), coord[0][0], coord[0][1], coord[0][2]))
		line = file.readline().strip()
	file.close()
	return coord

# Calculo de matching
def matchCalc(s1, s2, matchList, matchClass, classValue):
	print s1
	print s2
	coord1 = []
	coord2 = []
	matchScore = 0
	matchQt = 0
	listLen = 0
	radDist = 0.0
	radAngle = 0.0
	angCor1 = 0
	angCor2 = 0
	tresh = 40

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
	for i in range(2, coord1Size-1):
		for j in range(i+1, coord2Size-1):
			if coord1[i][2] == coord2[j][2]:
				radDist = abs(coord1[i][0] - coord2[i][0])
				radAngle = abs(coord1[i][1] - coord2[i][1])
				# Correcao do 8 com 1
				if radAngle == 7:
					radAngle = 1
				# Caso nao sejam adjacentes, punicao. Caso sejam, adiciona peso
				if radAngle > 1:
					radAngle = tresh
				else:
					radAngle * 20
				if radDist + radAngle <	tresh:
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
for i in range(1, 6):
	for j in range(1, 9):
		for k in range(i, 6):
			for l in range(j+1, 9):
				if j <= 5:
					if i == k:
						matchCalc(s%(i, j), s%(k, l), matchList, matchClass, 1)
					else:
						matchCalc(s%(i, j), s%(k, l), matchList, matchClass, 0)
				else:
					if i == k:
						matchCalc(s%(i, j), s%(k, l), predictList, predictClass, 1)
					else:
						matchCalc(s%(i, j), s%(k, l), predictList, predictClass, 0)

print("Primeira parte")
clf = svm.SVC(kernel='linear')
clf.fit(matchList, matchClass)

result = clf.predict(predictList)
print(result)
matching = 0
for i in range(0, len(result)):
	if result[i] == predictClass[i]:
		matching += 1
print matching
print len(result)
print(result)
