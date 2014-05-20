import cv2
import numpy as np
import math

#Conta quantas linhas saem de um quadrado 5x5 en volta do ponto (x,y)
def contarLinhas(img, x, y, tipo):
	pontos3 = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1]]#9
	pontos5 = [[x-2,y-2],[x-2,y-1],[x-2,y],[x-2,y+1],[x-2,y+2],[x-1,y+2],[x,y+2],[x+1,y+2],[x+2,y+2],[x+2,y+1],[x+2,y],[x+2,y-1],[x+2,y-2],[x+1,y-2],[x,y-2],[x-1,y-2]]#25
	i = 0
	linhas = 0
	if tipo == 3:
		tam = 8
		pontos = pontos3
	else:
		tam = 16
		pontos = pontos5
	while i < tam:
		if img[pontos[i][0]][pontos[i][1]] == 255:
			while i < tam and img[pontos[i][0]][pontos[i][1]] == 255:
				i += 1
			linhas += 1
		i += 1
	
	return linhas

#ideia: marcar 5x5 se o 3x3 der certo
def marcarMin(img, x, y):
	#pontos3 = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1]]
	pontos = [[x-2,y-2],[x-2,y-1],[x-2,y],[x-2,y+1],[x-2,y+2],[x-1,y+2],[x,y+2],[x+1,y+2],[x+2,y+2],[x+2,y+1],[x+2,y],[x+2,y-1],[x+2,y-2],[x+1,y-2],[x,y-2],[x-1,y-2]]#25
	if img[x,y] == 255 and contarLinhas(img, x, y, 3) > 3 and contarLinhas(img, x, y, 5) == 3:
		for pt in pontos:
			img[pt[0], pt[1]] = 127

def extrmin(img, z):
	x, y = img.shape
	for i in range(2, x - 2):
		for j in range(2, y - 2):
			marcarMin(img, i, j)
	cv2.imwrite("testeMin%s.bmp"%(z), img)

#Faz nada ainda
def acharCentro(img):
	dir = np.matrix("5 5", np.int32)
	pos = np.matrix("0 0", np.int32)
	while(True):
		pos = pos + dir

str = '5_skeletonization.bmp'
for i in range(1,2):
	for j in range(1,2):
		img = cv2.imread(str, 0)
		extrmin(img, i)