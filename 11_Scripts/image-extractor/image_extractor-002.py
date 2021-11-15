# https://www.py4u.net/discuss/18846

import cv2

im = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/001.png")
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
idx = 0
for cnt in contours:
    idx += 1
    x, y, w, h = cv2.boundingRect(cnt)
    roi = im[y : y + h, x : x + w]
    cv2.imwrite(
        "/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/extracted/ROI_002_" + str(idx) + ".jpg",
        roi,
    )
    # cv2.rectangle(im,(x,y),(x+w,y+h),(200,0,0),2)
cv2.imshow("img", im)
cv2.waitKey(0)
