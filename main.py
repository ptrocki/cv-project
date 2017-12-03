
import numpy as np
import cv2
import textRegions as txt
import detector
import answersRegion

answersCount = 3

def cutImage(img, rectangle, delta = 3):
    x0 = rectangle[0] - delta
    y0 = rectangle[1] - delta
    x1 = rectangle[0]+rectangle[2] + delta
    y1 = rectangle[1]+rectangle[3] + delta

    if x0 < 0:
        x0 = rectangle[0]

    if y0 < 0:
        y0 = rectangle[1]

    return img[y0:y1, x0:x1]


img = cv2.imread('input/all_sheet_ans2.jpg')
wholeRegion, rectangles = txt.TextRegions.findText(img)
imgCpy = img.copy()

rectangles = sorted(rectangles, key=lambda l:l[1])

i = 0
checkedAnswers = []
questions = []

while i < len(rectangles):
    answers = []
    checked = []

    rect = rectangles[i]
    qimg = cutImage(img, rect)
    question = detector.Detector.readText(qimg)
    questions.append(question)
    print "\n" + question
    print "Checked answers: "

    j = i + 1
    i += answersCount + 1
    while j < i:
        rect = rectangles[j]
        answers.append(rect)
        smallImg = cutImage(img, rect)
        marked = answersRegion.AnswersRegion.isMarked(smallImg)
        checked.append(marked)

        if marked:
            print str(j + answersCount - i + 1) + ", "
            cv2.rectangle(imgCpy, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (200, 10, 10), 3)
            cv2.imwrite("output/marked.png", imgCpy)

        j += 1

    checkedAnswers.append(checked)

# THIS DOESNT WORK WELL:
# answers = []
# ratios = []
#
# while i < len(rectangles):
#     checked = []
#     question = rectangles[i]
#
#     j = i + 1
#     i += answersCount + 1
#     while j < i:
#         rect = rectangles[j]
#         answers.append(rect)
#         smallImg = cutImage(img, rect)
#         ratio = answersRegion.AnswersRegion.computeRatio(smallImg)
#         ratios.append(ratio)
#
#         j += 1
#
# markedThreshold = answersRegion.AnswersRegion.computeMarkedThreshold(ratios)
#
# i = 0
# for ratio in ratios:
#     marked = answersRegion.AnswersRegion.isMarked(ratio, markedThreshold)
#     rect = answers[i]
#
#     if marked:
#         cv2.rectangle(imgCpy, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (200, 10, 10), 3)
#         cv2.imwrite("output/marked.png", imgCpy)
#
#     i += 1

# for rectangle in rectangles:
#     x0 = rectangle[0]
#     x1 = rectangle[0] + rectangle[2]
#     y0 = rectangle[1]
#     y1 = rectangle[1] + rectangle[3]
#
#     isAns = detector.Detector.isAnswer(img[y0:y1, x0:x1])

# answersRegion.AnswersRegion.test(img=img)