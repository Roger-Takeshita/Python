# https://stackoverflow.com/questions/13887863/extract-bounding-box-and-save-it-as-an-image

import cv2

# Load image, grayscale, Otsu's threshold
image = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/1.png")
copy = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

ROI_number = 0
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    ROI = image[y : y + h, x : x + w]
    cv2.imwrite("ROI_{}.png".format(ROI_number), ROI)
    cv2.rectangle(copy, (x, y), (x + w, y + h), (36, 255, 12), 2)
    ROI_number += 1

cv2.imshow("thresh", thresh)
cv2.imshow("copy", copy)
cv2.waitKey()
