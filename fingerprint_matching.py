import cv2
import numpy as np
from sklearn import svm


# Funcao de calculo das coordenadas polares
def pol(x, y, a, b, c):
	dist = np.sqrt((a-x)**2 + (b-y)**2)
	ang = 0
	if a-x != 0:
		ang = np.arctan((b-y)/(a-x))
	return [dist, ang, c]


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

	file = open(s1 + '_coord.txt', 'r')
	line = file.readline().strip()
	lineList = line.split(',')
	coord1.append([int(lineList[0]), int(lineList[1]), -1])
	line = file.readline().strip()
	lineList = line.split(',')
	coord1.append([int(lineList[0]), int(lineList[1]), -1])
	line = file.readline().strip()
	while line != '':
		lineList = line.split(',')
		coord1.append(pol(int(lineList[0]), int(lineList[1]), coord1[0][0], coord1[0][1], coord1[0][2]))
		line = file.readline().strip()
	file.close()
	
	file = open(s2 + '_coord.txt', 'r')
	line = file.readline().strip()
	lineList = line.split(',')
	coord2.append([int(lineList[0]), int(lineList[1]), -1])
	line = file.readline().strip()
	lineList = line.split(',')
	coord2.append([int(lineList[0]), int(lineList[1]), -1])
	line = file.readline().strip()
	while line != '':
		lineList = line.split(',')
		coord2.append(pol(int(lineList[0]), int(lineList[1]), coord2[0][0], coord2[0][1], coord2[0][2]))
		line = file.readline().strip()
	file.close()
	
	angCor = np.arctan((coord1[1][1] - coord1[0][1])/(coord1[1][0] - coord1[0][0])) - np.arctan((coord2[1][1]-coord2[0][1])/(coord2[1][0]-coord2[0][0]))
	
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
				radAngle = abs(coord1[i][1] - coord2[i][1] + angCor)
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
for i in range(1, 10):
	for j in range(1, 9):
		for k in range(i, 10):
			for l in range(j+1, 9):
				if j <= 5:
					if i == k:
						matchCalc(s%(i, j), s%(k, l), matchList, matchClass, 1)
					else:
						matchCalc(s%(i, j), s%(k, l), matchList, matchClass, 0)
				else:
					if i == k:
						matchCalc(s%(i, j), s%(k, l), matchList, matchClass, 1)
					else:
						matchCalc(s%(i, j), s%(k, l), matchList, matchClass, 0)
	
# Aprendizado e verificacao
print("Match List:\n");
print(matchList)
#print(matchClass)
print("Pred List\n");
print(predictList)
#print(predictClass)

clf = svm.SVC(kernel='linear')
clf.fit(matchList, matchClass)
print("E eu que sei?\n")
print(clf.predict(predictList))
