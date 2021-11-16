import cv2
import numpy as np

lower = np.array([237, 97, 71], np.uint8)
upper = np.array([237, 97, 71], np.uint8)

image = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/002.png")
copy = image.copy()

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hue = img_hsv[:, :, 0]
thresh = cv2.inRange(img_hsv, lower, upper)

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0]

ROI_number = 0
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    ROI = image[y : y + h, x : x + w]
    cv2.imwrite(
        "/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/extracted/ROI_005_{}.png".format(
            ROI_number
        ),
        ROI,
    )
    cv2.rectangle(copy, (x, y), (x + w, y + h), (237, 97, 71), 2)
    ROI_number += 1

cv2.imshow("thresh", thresh)
cv2.imshow("copy", copy)
cv2.waitKey()
