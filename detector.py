import cv2
import numpy as np
import pytesseract
import textRegions as txt
from PIL import Image
from matplotlib.pyplot import imshow

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

    @staticmethod
    def readText(img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # kernel = np.ones((1, 1), np.uint8)
        # img = cv2.dilate(img, kernel, iterations=1)
        # img = cv2.erode(img, kernel, iterations=1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh2 = cv2.threshold(gray, 103, 255, cv2.THRESH_BINARY)
        # thresh2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        kernel = np.ones((2, 2), np.uint8)
        thresh2 = cv2.dilate(thresh2, kernel, iterations=1)
        img = cv2.erode(thresh2, kernel, iterations=1)

        imga = Image.fromarray(img)
        # imga.show()
        result = pytesseract.image_to_string(imga)

        return result