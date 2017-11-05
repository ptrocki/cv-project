import cv2
import numpy as np

def remove_similar(bboxes, delta = 4):
    unique = []
    unique.append(bboxes[0])
    bboxes.remove(bboxes[0])
    for t in bboxes:
        uni = unique[-1]
        diff = abs(uni[1]-t[1])
        if diff > delta:
            unique.append(t)
        else:
            continue
    return unique


def test():
    img = cv2.imread('answ2.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh2 = cv2.threshold(gray,220,255,cv2.THRESH_BINARY_INV)
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(thresh2,kernel,iterations = 1)
    mser = cv2.MSER_create()
    vis = img.copy()
    regions, bboxes = mser.detectRegions(erosion)

    uniqueasd = remove_similar(sorted(bboxes, key = lambda x: x[1]))
    for uni in uniqueasd:
        cv2.rectangle(vis, (uni[0], uni[1]), (uni[0]+uni[2], uni[1]+uni[3]), (0, 255, 0), 2)

    cv2.imwrite("answ2_result.png", vis)