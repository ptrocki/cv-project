import cv2
import numpy as np

class AnswersRegion:

    def remove_similar(self,bboxes, delta = 4):
        unique = []
        unique.append(bboxes[0])
        bboxes.remove(bboxes[0])
        for t in bboxes:
            if t[3] < 69:
                continue
            uni = unique[-1]
            diff = abs(uni[1]-t[1])
            if diff > delta:
                unique.append(t)
            else:
                continue
        return unique

    def is_marked(self, bboxes, img):
        for b in bboxes:
            delta = 10
            x0 = b[0] + delta
            y0 = b[1] + delta
            x1 = b[0]+b[2] + delta
            y1 = b[1]+b[3] + delta
            gray = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
            ret, thresh2 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
            kernel = np.ones((2, 2), np.uint8)
            erosion = cv2.erode(thresh2, kernel, iterations=1)
            #cv2.imwrite("answ2_result.png", erosion)
            allPixels = []
            foundPixels = []
            rows, cols = erosion.shape
            for i in range(rows):
                for j in range(cols):
                    pixel = erosion[i, j]
                    if pixel < 150:
                        foundPixels.append(pixel)
                    allPixels.append(pixel)
            print("Ratio:", float(len(foundPixels)) / float(len(allPixels)))





    def test(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,thresh2 = cv2.threshold(gray,220,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(thresh2,kernel,iterations = 1)
        mser = cv2.MSER_create()
        vis = img.copy()
        regions, bboxes = mser.detectRegions(erosion)

        uniqueasd = self.remove_similar(sorted(bboxes, key = lambda x: x[1]))
        for uni in uniqueasd:
            cv2.rectangle(vis, (uni[0], uni[1]), (uni[0]+uni[2], uni[1]+uni[3]), (0, 255, 0), 2)

        self.is_marked(uniqueasd,img)
        cv2.imwrite("answ2_result.png", erosion)