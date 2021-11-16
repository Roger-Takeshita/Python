# https://www.youtube.com/watch?v=FbR9Xr0TVdY

import cv2

img = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/002.png")
imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(imggray, 127, 255, 0)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print("Number of contours = {}".format(len(contours)))
print(contours[0])

cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
# original image, contours found, contour indexes, color, line thickness

cv2.imshow("Image", img)
cv2.imshow("Image Gray", imggray)
cv2.waitKey(0)
cv2.destroyAllWindows()
