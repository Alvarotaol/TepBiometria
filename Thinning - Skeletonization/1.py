import numpy as np
from skimage import morphology
import cv2

im = cv2.imread("3_binary.jpg")
im = morphology.skeletonize(im)
cv2.imwrite("dst.png", im)