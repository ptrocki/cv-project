
import numpy as np
import cv2

img = cv2.imread('test.jpg',0)
blurred = cv2.GaussianBlur(img, (3, 3), 0)
edges = cv2.Canny(blurred,100,200)
cv2.imshow('edges',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()