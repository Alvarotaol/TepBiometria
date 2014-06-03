import cv2
import numpy as np
from sklearn import svm

matchList = [[0,1],[2,2],[3,4],[6,5],[2,5]]
matchClass = [0,0,1,1,0]
predictList = [[1,7],[5,3],[2,10000]]
clf = svm.SVC(kernel='linear')
clf.fit(matchList, matchClass)

result = clf.predict(predictList)
print(result)
matching = 0
