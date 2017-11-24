
import cv2
import math
import numpy as np


class TextRegions:

    @staticmethod
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

    @staticmethod
    def mergeTwoBoxes(box1, box2):
        if box1[0] <= box2[0] and box1[2] + box1[0] > box2[2] + box2[0]:
            x1 = box1[0]
            x2 = box1[2]
        elif box1[0] <= box2[0]:
            x1 = box1[0]
            x2 = box2[0] - box1[0] + box2[2]
        else:
            x1 = box2[0]
            x2 = box1[0] - box2[0] + box1[2]

        if box1[1] <= box2[1] and box1[3] + box1[1] > box2[3] + box2[1]:
            y1 = box1[1]
            y2 = box1[3]
        elif box1[1] <= box2[1]:
            y1 = box1[1]
            y2 = box2[1] - box1[1] + box2[3]
        else:
            y1 = box2[1]
            y2 = box1[1] - box2[1] + box1[3]

        bigBox = [x1, y1, x2, y2]

        return bigBox

    @staticmethod
    def mergeWithinHeight(bboxes):
        new = bboxes
        result = []

        i = 0
        while i < len(new):
            j = i + 1
            bb = new[i]
            toRemove = []

            while j < len(new):
                bb2 = new[j]
                isSimilar = bb[1] <= bb2[1] <= bb[1] + bb[3]
                isSimilar = isSimilar or bb2[1] <= bb[1] <= bb2[1] + bb2[3]

                if isSimilar:
                    bb = TextRegions.mergeTwoBoxes(bb, bb2)
                    toRemove.append(j)

                j += 1

            for j in sorted(toRemove, reverse=True):
                new = np.delete(new, j, axis=0)

                if j < i:
                    i -= 1

            result.append(bb)
            i += 1

        return result

    @staticmethod
    def mergeAmbiguous(bboxes, ambiguityThreshold = 4):
        new = bboxes
        result = []

        i = 0
        while i < len(new):
            j = i + 1
            bb = new[i]
            toRemove = []

            while j < len(new):
                bb2 = new[j]
                isSimilar = abs(bb[0] - bb2[0]) < ambiguityThreshold
                isSimilar = isSimilar and abs(bb[1] - bb2[1]) < ambiguityThreshold

                if isSimilar:
                    bb = TextRegions.mergeTwoBoxes(bb, bb2)
                    toRemove.append(j)

                j += 1

            for j in sorted(toRemove, reverse=True):
                new = np.delete(new, j, axis=0)

                if j < i:
                    i -= 1

            result.append(bb)
            i += 1

        return result

    @staticmethod
    def removeAmbiguous(bboxes, ambiguityThreshold = 3):
        new = list(bboxes)
        toRemove = []

        i = 0
        while i < len(new):
            j = i + 1
            bb = new[i]

            while j < len(new):
                bb2 = new[j]
                isSimilar = abs(bb[0] - bb2[0]) < ambiguityThreshold
                isSimilar = isSimilar and abs(bb[1] - bb2[1]) < ambiguityThreshold
                isSimilar = isSimilar and abs(bb[2] - bb2[2]) < ambiguityThreshold
                isSimilar = isSimilar and abs(bb[3] - bb2[3]) < ambiguityThreshold

                if isSimilar:
                    try:
                        toRemove.index(j)
                    except ValueError:
                        toRemove.append(j)

                j += 1

            i += 1

        for j in sorted(toRemove, reverse=True):
            new.pop(j)

        return new

    @staticmethod
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
                    rectangle = TextRegions.apprendRectangle(bb, rectangle)
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

    @staticmethod
    def convertToXYWH(toConvert):
        result = []

        for bb in toConvert:
            single = [bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1]]
            result.append(single)

        return result

    @staticmethod
    def findText(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        mser = cv2.MSER_create()

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

        wholeRegion = (smallestx, smallesty, biggestx, biggesty)

        cv2.imwrite("output/result1.png", imgcopy)

        # rectangles = mergeAmbiguous(bboxes2)
        # rectangles = sorted(rectangles)
        rectangles = TextRegions.mergeBoxes(bboxes2, avgHeight)
        rectangles = TextRegions.convertToXYWH(rectangles)
        rectangles = TextRegions.mergeWithinHeight(rectangles)
        # rectangles = mergeBoxes(rectangles, avgHeight)

        for rect in rectangles:
            # cv2.rectangle(imgcopy, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 0), 1)
            cv2.rectangle(imgcopy, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 0), 1)

        cv2.imwrite("output/result3.png", imgcopy)

        return wholeRegion, rectangles


