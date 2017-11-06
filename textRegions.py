
import cv2
import math
import numpy as np


def apprendRectangle(box, rectangle):
    if box[0] < rectangle[0]:
        rectangle[0] = box[0]

    if box[1] < rectangle[1]:
        rectangle[1] = box[1]

    x = box[0] + box[2]
    y = box[1] + box[3]
    if x > rectangle[2]:
        rectangle[2] = x

    if y > rectangle[3]:
        rectangle[3] = y

    return rectangle


def mergeBoxes(bboxes, avgHeight):
    rectangles = []
    unusedBoxes = list(bboxes)
    i = 0

    while i < len(unusedBoxes):
        box = unusedBoxes[i]
        rectangle = [box[0], box[1], box[0] + box[2], box[1] + box[3]]
        unused2 = unusedBoxes[:]
        toRemove = []

        for j in range(len(unused2)):
            bb = unused2[j]
            middlex = bb[0] + bb[2] / 2
            middley = bb[1] + bb[3] / 2
            corner1 = math.sqrt(pow(middlex - rectangle[0], 2) + pow(middley - rectangle[1], 2)) < avgHeight
            corner2 = math.sqrt(pow(middlex - rectangle[2], 2) + pow(middley - rectangle[1], 2)) < avgHeight
            corner3 = math.sqrt(pow(middlex - rectangle[2], 2) + pow(middley - rectangle[3], 2)) < avgHeight
            corner4 = math.sqrt(pow(middlex - rectangle[0], 2) + pow(middley - rectangle[3], 2)) < avgHeight

            if corner1 or corner2 or corner3 or corner4:
                rectangle = apprendRectangle(bb, rectangle)
                toRemove.append(j)

        for j in sorted(toRemove, reverse=True):
            unusedBoxes.pop(j)

            if j < i:
                i -= 1

        rectangles.append(rectangle)

        if len(unusedBoxes) == 0:
            break

        i += 1

    return rectangles

def convertToXYWH(toConvert):
    result = []

    for bb in toConvert:
        single = [bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1]]
        result.append(single)

    return result

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

mser = cv2.MSER_create()
# mser.setMinArea(100)
# mser.setMaxArea(800)

coordinates, bboxes = mser.detectRegions(gray)
bboxes2 = bboxes.copy()

imgcopy = img.copy()

xmin = bboxes[:, 0]
ymin = bboxes[:, 1]
xmax = bboxes[:, 2]
ymax = bboxes[:, 3]

avgHeight = sum(ymax) / len(ymax) + 15

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

cv2.rectangle(imgcopy, (smallestx, smallesty), (biggestx, biggesty), (0, 0, 0), 2)

cv2.imwrite("result1.png", imgcopy)

rectangles = mergeBoxes(bboxes2, avgHeight)
rectangles = convertToXYWH(rectangles)
rectangles = mergeBoxes(rectangles, avgHeight)


# needa work out smth better, bbox aren't sorted, so this doesn't work
# rectangle = [smallestx, smallesty, smallestx, smallesty]
# for bb in bboxes2:
#     if (rectangle[3] - bb[1]) > avgHeight:
#         rectangles.append(rectangle)
#         rectangle = [bb[0], bb[1], bb[0] + bb[2], bb[1] + bb[3]]
#     else:
#         rectangle[0] = int(round(min([rectangle[0], bb[0]])))
#         rectangle[1] = int(round(min([rectangle[1], bb[1]])))
#         rectangle[2] = int(round(max([rectangle[2], bb[0] + bb[2]])))
#         rectangle[3] = int(round(max([rectangle[3], bb[1] + bb[3]])))

for rect in rectangles:
    cv2.rectangle(imgcopy, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 0), 1)

cv2.imwrite("result3.png", imgcopy)


