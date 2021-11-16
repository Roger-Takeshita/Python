# https://stackoverflow.com/questions/30331944/finding-red-color-in-image-using-python-opencv

import cv2
import numpy as np

image_path = "/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/002.png"

# blurring and smoothin
img1 = cv2.imread(image_path, 1)

hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

# lower red
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])


# upper red
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(img1, img1, mask=mask)


mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
res2 = cv2.bitwise_and(img1, img1, mask=mask2)

img3 = res + res2
img4 = cv2.add(res, res2)
img5 = cv2.addWeighted(res, 0.5, res2, 0.5, 0)


kernel = np.ones((15, 15), np.float32) / 225
smoothed = cv2.filter2D(res, -1, kernel)
smoothed2 = cv2.filter2D(img3, -1, kernel)


cv2.imshow("Original", img1)
cv2.imshow("Averaging", smoothed)
cv2.imshow("mask", mask)
cv2.imshow("res", res)
cv2.imshow("mask2", mask2)
cv2.imshow("res2", res2)
cv2.imshow("res3", img3)
cv2.imshow("res4", img4)
cv2.imshow("res5", img5)
cv2.imshow("smooth2", smoothed2)


cv2.waitKey(0)
cv2.destroyAllWindows()
