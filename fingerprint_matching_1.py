import cv2
import numpy as np
from sklearn import svm


# Funcao de calculo das coordenadas polares
def pol(x, y, a, b, c):
    dist = np.sqrt((a-x)**2 + (b-y)**2)
    ang = np.pi
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
	tresh = 40

	file = open(s1 + '_coord.txt', 'r')
	line = file.readline().strip()
	lineList = line.split(',')
	coord1.append([int(lineList[0]), int(lineList[1]), 0])
	line = file.readline()
	while line != '':
		lineList = line.split(',')
		coord1.append(pol(int(lineList[0]), int(lineList[1]), coord1[0][0], coord1[0][1], coord1[0][2]))
		line = file.readline()
	file.close()
	
	file = open(s2 + '_coord.txt', 'r')
	line = file.readline().strip()
	lineList = line.split(',')
	coord2.append([int(lineList[0]), int(lineList[1]), 0])
	line = file.readline()
	while line != '':
		lineList = line.split(',')
		coord2.append(pol(int(lineList[0]), int(lineList[1]), coord2[0][0], coord2[0][1], coord2[0][2]))
		line = file.readline()
	file.close()
	
	# Comparacao de minutiaes
	coord1Size = len(coord1)
	coord2Size = len(coord2)
	if coord1Size < coord2Size:
		listLen = coord1Size/2
	else:
		listLen = coord2Size/2
	matchQt = 0
	for i in range(1, listLen-1):
		if coord1[i][2] == coord2[i][2]:
			radDist = abs(coord1[i][0] - coord2[i][0])
			radAngle = abs(coord1[i][1] - coord2[i][1])
			if radDist + radAngle <	tresh:
				matchQt = matchQt + 1
			
	# Calculo final
	matchScore = pow(matchQt, 2)/(float(((coord1Size/2)*(coord2Size/2)))+1)
	matchList.append([matchScore, matchQt])
	matchClass.append(classValue)


# Listas (vazias) das coordenadas polares
matchList = []
matchClass = []
predictList = []
predictClass = []

# Calculo de matching
matchCalc('101_1', '101_2', matchList, matchClass, 1)
matchCalc('102_1', '102_2', matchList, matchClass, 1)
matchCalc('101_3', '102_3', matchList, matchClass, 0)
matchCalc('101_4', '102_4', matchList, matchClass, 0)

matchCalc('101_5', '101_6', predictList, predictClass, 1)
matchCalc('101_1', '101_6', predictList, predictClass, 1)
matchCalc('101_1', '101_3', predictList, predictClass, 1)
matchCalc('101_5', '101_2', predictList, predictClass, 1)

matchCalc('102_1', '101_2', predictList, predictClass, 0)
matchCalc('102_3', '101_1', predictList, predictClass, 0)
matchCalc('102_4', '101_5', predictList, predictClass, 0)
matchCalc('102_2', '101_3', predictList, predictClass, 0)
	
# Aprendizado e verificacao
print(matchList)
#print(matchClass)
print(predictList)
#print(predictClass)

clf = svm.SVC(kernel='linear')
clf.fit(matchList, matchClass)

print(clf.predict(predictList))
