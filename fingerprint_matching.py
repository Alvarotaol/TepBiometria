import numpy as np
from sklearn import svm


def dist(t1, t2):
	return np.sqrt((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2)	 


# Funcao de calculo das coordenadas polares
def pol(y, x):
	xVar = x - 148
	yVar = y - 280
	
	dist = np.sqrt((xVar)**2 + (yVar)**2)	

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
	return [dist, ang]

#le as coordenadas cartesianas e as converte para polares
def lerArquivo(s):
	coord = []
	file = open(s + '_coord.txt', 'r')
	line = file.readline().strip()
	lineList = line.split(',')
	coord.append([int(lineList[0]), int(lineList[1])])
	
	line = file.readline().strip()
	lineList = line.split(',')
	coord.append([int(lineList[0]), int(lineList[1])])
	
	line = file.readline().strip()
	while line != '':
		lineList = line.split(',')
		coord.append(pol(int(lineList[0]), int(lineList[1])))
		line = file.readline().strip()
	file.close()
	return coord

# Funcao de calculo de matching
def matchCalc(s1, s2, matchList, matchClass, classValue):
	coord1 = []
	coord2 = []
	matchScore = 0
	listLen = 0
	radDist = 0.0
	radAngle = 0.0
	angCor1 = 0
	angCor2 = 0
	tresh = 20

	coord1 = lerArquivo(s1)
	coord2 = lerArquivo(s2)

	minQt = [0, 0, 0, 0, 0, 0, 0, 0]
	matchQt1 = 0
	matchQt2 = 0
	
	for i in range(2, len(coord1)):
		minQt[coord1[i][1]] += 1;
	for i in range(2, len(coord2)):
		minQt[coord2[i][1]] -= 1;
	for i in range(0, 8):
		matchQt1 += abs(minQt[i]);
		
	for i in range(2, min(len(coord1), len(coord2))):
		if abs(coord1[i][0] - coord2[i][0]) < tresh:
			matchQt2 += 1	
				
	# Calculo final
	matchList.append([(float)(matchQt2)/(float)(len(coord1)+len(coord2))])
	matchClass.append(classValue)
	#print s1, s2, (float)(matchQt2)/(float)(len(coord1)+len(coord2)), classValue

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
teste = []
prob = []

tsist = [[1,1],[1,2],[2,2],[2,7],[3,1],[3,2],[4,1],[4,2],[4,3],[4,4],[5,1],[5,2],[5,3],[5,7],[5,8],[6,2],[6,3],[6,8],[8,5],[8,6],[8,7],[9,2],[9,3],[9,6],[10,1],[10,2],[10,3]]

# Calculo de matching
matchCalc(esse(1, 1), esse(1, 2), matchList, matchClass, 1)
matchCalc(esse(3, 1), esse(3, 2), matchList, matchClass, 1)
matchCalc(esse(1, 1), esse(2, 1), matchList, matchClass, 0)
matchCalc(esse(1, 1), esse(8, 7), matchList, matchClass, 0)

for i in range(0, len(tsist)):
	for j in range(i, len(tsist)):
		teste.append([tsist[i], tsist[j]])
		if tsist[i][0] == tsist[j][0]:
			matchCalc(esse(tsist[i][0], tsist[i][1]), esse(tsist[j][0], tsist[j][1]), predictList, predictClass, 1)
		else:
			matchCalc(esse(tsist[i][0], tsist[i][1]), esse(tsist[j][0], tsist[j][1]), predictList, predictClass, 0)

# Treinamento do SVM
clf = svm.SVC(kernel = 'linear')
clf.fit(matchList, matchClass)

# Teste do SVM
result = clf.predict(predictList)

# Visualizacao de resultados

matching = 0
fnmr = 0
fmr = 0
for i in range(0, len(result)):
	if result[i] == predictClass[i]:
		matching += 1
		print 'X'
	else:
		print teste[i], result[i]
		if(result[i] == 0):
			fnmr += 1
		else:
			fmr += 1

print "Quantidade de acertos: ", matching
print "Quantidade de resultados: ", len(result)
print "Taxa de acertos: ", float(matching)/len(result)
print "Falsos negativos: ", fnmr
print "FNMR: ", float(fnmr)/len(result)
print "Falsos positivos: ", fmr
print "FMR: ", float(fmr)/len(result)

