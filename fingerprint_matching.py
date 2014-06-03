import cv2
import numpy as np
from sklearn import svm
import random as rd


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

	matchQt = 0
	for i in range(2, coord1Size):
		for j in range(2, coord2Size):
			radDist = abs(coord1[i][0] - coord2[j][0])
			radAngle = abs(coord1[i][1] - coord2[j][1])
		
			if radDist < tresh and radAngle == 0:
					matchQt = matchQt + 1
			
	# Calculo final
	matchScore = pow(matchQt, 2)/(float(((coord1Size)*(coord2Size)))+1)
	matchList.append([matchScore, matchQt])
	matchClass.append(classValue)

def esse(i, j):
	s1 = "img/1"
	s2 = "%i_%i"
	if(i < 10):
		return s1 + '0' + s2%(i,j)
	else:
		return s1 + s2%(i,j)

# Listas (vazias) das coordenadas polares
matchList = []
matchClass = []
predictList = []
predictClass = []

trist = [[1,1],[1,2],[1,4],[1,5],[1,6],[2,2],[2,7],[3,1],[3,2],[4,1],[4,2],[4,3],[4,4],[5,1],[5,2],[5,3],[5,7],[5,8],[6,2],[6,3],[6,8]]
tsist = [[8,5],[8,6],[8,7],[9,2],[9,3],[9,6],[10,1],[10,2],[10,3],[10,7]]

def coment():
	for i in range(0, len(trist)):
		for j in range(i + 1, len(trist)):
			if trist[i][0] == trist[j][0]:
				if trist[i][0] < 10:
					matchCalc(esse(trist[i][0], trist[i][1]), esse(trist[j][0], trist[j][1]), matchList, matchClass, 1)
				else:
					matchCalc(esse(trist[i][0], trist[i][1]), esse(trist[j][0], trist[j][1]), matchList, matchClass, 1)
			else:
				if trist[i][0] < 10:
					matchCalc(esse(trist[i][0], trist[i][1]), esse(trist[j][0], trist[j][1]), matchList, matchClass, 0)
				else:
					matchCalc(esse(trist[i][0], trist[i][1]), esse(trist[j][0], trist[j][1]), matchList, matchClass, 0)

	for i in range(0, len(tsist)):
		for j in range(i + 1, len(tsist)):
			if tsist[i][0] == tsist[j][0]:
				if tsist[i][0] < 10:
					matchCalc(esse(tsist[i][0], tsist[i][1]), esse(tsist[j][0], tsist[j][1]), predictList, predictClass, 1)
				else:
					matchCalc(esse(tsist[i][0], tsist[i][1]), esse(tsist[j][0], tsist[j][1]), predictList, predictClass, 1)
			else:
				if tsist[i][0] < 10:
					matchCalc(esse(tsist[i][0], tsist[i][1]), esse(tsist[j][0], tsist[j][1]), predictList, predictClass, 0)
				else:
					matchCalc(esse(tsist[i][0], tsist[i][1]), esse(tsist[j][0], tsist[j][1]), predictList, predictClass, 0)
				
# Calculo de matching
def comentado():
	for i in range(1, 4):
		for j in range(1, 9):
			for k in range(i, 4):
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


for i in range(2,3):
	matchCalc(esse(1, 1), esse(1, i), matchList, matchClass, 1)
matchCalc(esse(1, 1), esse(2, 1), matchList, matchClass, 0)
matchCalc(esse(1, 1), esse(1, 3), predictList, predictClass, 1)
matchCalc(esse(1, 1), esse(2, 2), predictList, predictClass, 0)
matchCalc(esse(1, 1), esse(3, 3), predictList, predictClass, 0)
print("Primeira parte")
clf = svm.SVC(kernel='linear')
clf.fit(matchList, matchClass)

result = clf.predict(predictList)
#result[0:10] = [1,1,1,1,1,1,1,1,1,1]
#rd.shuffle(result)
print str(result)
print predictClass
matching = 0
ferro = 0
facerto = 0
for i in range(0, len(result)):
	if result[i] == predictClass[i]:
		matching += 1
	else:
		if(result[i] == 0):
			ferro += 1
		else:
			facerto += 1

print "Taxa de acertos: ", float(matching)/len(result)
print "Falsos erros: ", ferro
print "Falsos acertos: ", facerto

