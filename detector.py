import cv2
import numpy as np
import textRegions as txt

class Detector:

    @staticmethod
    def isAnswer(img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours > 0:
            return True

        return False

    @staticmethod
    def cutAnsSquare(img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # _, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mser = cv2.MSER_create()
        regions, contours = mser.detectRegions(img)

        # for rect in contours:
        #     cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 0), 1)
        #     cv2.imwrite("asd.png", img)

        # ONLY FOR 1 LINE ANSWERS (seeks for the tallest box)
        heights = contours[:,3]
        contour = contours[0]
        i = 0
        while i < (heights.size/4):
            i += 1
            if heights[i] > contour[3]:
                contour = contours[i]

        # cv2.rectangle(img, (contour[0], contour[1]), (contour[0] + contour[2], contour[1] + contour[3]), (200, 10, 10), 3)
        # cv2.imwrite("asd.png", img)

        return img[contour[1]:(contour[1] + contour[3]), contour[0]:(contour[0] + contour[2])]