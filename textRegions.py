
import cv2

def trocki():
    img = cv2.imread('answ.jpeg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mser = cv2.MSER_create()
    vis = img.copy()
    regions, bboxes = mser.detectRegions(gray)

    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
    cv2.polylines(vis, hulls, 1, (0, 255, 0))

    # number = 0
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # for h in hulls:
    #     cv2.putText(vis, str(number), tuple(h[0][0]), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    #     number = number + 1

    bboxes_x = bboxes[:, 0]
    bboxes_y = bboxes[:, 1]
    bboxes_w = bboxes[:, 2]
    bboxes_h = bboxes[:, 3]
    smallestx = int(round(min(bboxes_x), 0))
    yy = int(round(max(bboxes_y), 0))
    height = int(round(max(bboxes_h), 0))

    cv2.line(vis, (smallestx, 0), (smallestx, yy+height), (255, 0, 0), 5)
    cv2.line(vis, (smallestx+200, 0), (smallestx + 200, yy+height), (255, 255, 0), 5)
    # cv2.contourArea(regions[0])
    # startx = int(round(min(xmin), 0))
    # starty = int(round(min(ymin), 0))
    # cv2.rectangle(vis, (smallestx, smallesty), (smallestx + 20, smallesty + 20), (0, 255, 0), 2)

    cv2.imwrite("answ.png", vis)

def barber():
    img = cv2.imread('sc.jpeg')
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

    avgHeight = sum(ymax) / len(ymax)

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

    rectangle = [smallestx, smallesty, smallestx, smallesty]
    rectangles = []

    #needa work out smth better, bbox aren't sorted, so this doesn't work
    for bb in bboxes2:
        if (rectangle[3] - bb[1]) > avgHeight:
            rectangles.append(rectangle)
            rectangle = [bb[0], bb[1], bb[0] + bb[2], bb[1] + bb[3]]
        else:
            rectangle[0] = int( round(min([rectangle[0], bb[0]])))
            rectangle[1] = int(round(min([rectangle[1], bb[1]])))
            rectangle[2] = int(round(max([rectangle[2], bb[0] + bb[2]])))
            rectangle[3] = int(round(max([rectangle[3], bb[1] + bb[3]])))

    for rect in bboxes:
        cv2.rectangle(imgcopy, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 0), 1)

    cv2.imwrite("result2.png", imgcopy)

trocki()