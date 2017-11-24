import cv2
import numpy as np

import detector


class AnswersRegion:

    # def remove_similar(self,bboxes, delta = 4):
    #     unique = []
    #     unique.append(bboxes[0])
    #     bboxes.remove(bboxes[0])
    #     for t in bboxes:
    #         if t[3] < 69:
    #             continue
    #         uni = unique[-1]
    #         diff = abs(uni[1]-t[1])
    #         if diff > delta:
    #             unique.append(t)
    #         else:
    #             continue
    #     return unique

    @staticmethod
    def is_marked(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh2 = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY)
        # thresh2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,21,2)
        kernel = np.ones((2, 2), np.uint8)
        erosion = cv2.erode(thresh2, kernel, iterations=1)

        cut = detector.Detector.cutAnsSquare(erosion)
        # cv2.imwrite("asd.png", cut)

        allPixels = []
        foundPixels = []
        rows, cols = cut.shape

        for i in range(rows):
            for j in range(cols):
                pixel = cut[i, j]
                if pixel < 150:
                    foundPixels.append(pixel)
                allPixels.append(pixel)

        ratio = float(len(foundPixels)) / float(len(allPixels))
        print("Ratio:", ratio)

        if ratio > 0.40:
            return True
        else:
            return False



    # def test(self, img):
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     ret,thresh2 = cv2.threshold(gray,220,255,cv2.THRESH_BINARY_INV)
    #     kernel = np.ones((5,5),np.uint8)
    #     erosion = cv2.erode(thresh2,kernel,iterations = 1)
    #     mser = cv2.MSER_create()
    #     vis = img.copy()
    #     regions, bboxes = mser.detectRegions(erosion)
    #
    #     uniqueasd = self.remove_similar(sorted(bboxes, key = lambda x: x[1]))
    #     for uni in uniqueasd:
    #         cv2.rectangle(vis, (uni[0], uni[1]), (uni[0]+uni[2], uni[1]+uni[3]), (0, 255, 0), 2)
    #
    #     self.is_marked(uniqueasd,img)
    #     cv2.imwrite("answ2_result.png", erosion)