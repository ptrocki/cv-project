
import cv2
import numpy as np


#img = cv2.imread('test2.jpg',0)
#blurred = cv2.GaussianBlur(img, (3, 3), 0)

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


mser = cv2.MSER_create()
mser.setMinArea(100)
mser.setMaxArea(800)

coordinates, bboxes = mser.detectRegions(gray)

## Filter the coordinates
# vis = img.copy()
# coords = []
# bb = []
# for coord in coordinates:
#     bbox = cv2.boundingRect(coord)
#     x,y,w,h = bbox
#     if w< 10 or h < 10 or w/h > 5 or h/w > 5:
#         continue
#     coords.append(coord)
#     bb.append(bbox)

## colors
colors = [[43, 43, 200], [43, 75, 200], [43, 106, 200], [43, 137, 200], [43, 169, 200], [43, 200, 195], [43, 200, 163], [43, 200, 132], [43, 200, 101], [43, 200, 69], [54, 200, 43], [85, 200, 43], [116, 200, 43], [148, 200, 43], [179, 200, 43], [200, 184, 43], [200, 153, 43], [200, 122, 43], [200, 90, 43], [200, 59, 43], [200, 43, 64], [200, 43, 95], [200, 43, 127], [200, 43, 158], [200, 43, 190], [174, 43, 200], [142, 43, 200], [111, 43, 200], [80, 43, 200], [43, 43, 200]]

## Fill with random colors
np.random.seed(0)
canvas1 = img.copy()
# canvas2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
# canvas3 = np.zeros_like(img)

# for cnt in coords:
#     xx = cnt[:,0]
#     yy = cnt[:,1]
#     color = colors[np.random.choice(len(colors))]
#     canvas1[yy, xx] = color
#     canvas2[yy, xx] = color
#     canvas3[yy, xx] = color

xmin = bboxes[:, 0]
ymin = bboxes[:, 1]
xmax = bboxes[:, 2]
ymax = bboxes[:, 3]

xmax += xmin[:] - 1
ymax += ymin[:] - 1

expansionAmount = 0.02
xmin = (1-expansionAmount) * xmin
ymin = (1-expansionAmount) * ymin
xmax = (1+expansionAmount) * xmax
ymax = (1+expansionAmount) * ymax

smallestx = int(round(min(xmin), 0))
smallesty = int(round(min(ymin), 0))
biggestx = int(round(max(xmax), 0))
biggesty = int(round(max(ymax), 0))

cv2.rectangle(canvas1, (smallestx, smallesty), (biggestx, biggesty), (0, 0, 0), 2)
cv2.imwrite("result1.png", canvas1)
