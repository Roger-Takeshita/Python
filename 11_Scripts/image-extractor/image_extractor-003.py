# https://www.py4u.net/discuss/18846

import cv2

# Load image, grayscale, Otsu's threshold
image = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/001.png")
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours, obtain bounding box, extract and save ROI
ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
    ROI = original[y : y + h, x : x + w]
    cv2.imwrite(
        "/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/extracted/ROI_003_{}.png".format(
            ROI_number
        ),
        ROI,
    )
    ROI_number += 1

cv2.imshow("image", image)
cv2.waitKey()
