import cv2

image = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/002.png")
im = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

ROI_number = 0

for c in contours:
    rect = cv2.boundingRect(c)
    if rect[2] < 100 or rect[3] < 100:
        continue
    print(cv2.contourArea(c))
    x, y, w, h = rect
    ROI = image[y : y + h, x : x + w]
    cv2.imwrite(
        "/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/extracted/ROI_001_{}.png".format(
            ROI_number
        ),
        ROI,
    )
    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
    ROI_number += 1
    # cv2.putText(im, "Moth Detected", (x + w + 10, y + h), 0, 0.3, (0, 255, 0))
# cv2.imshow("Show", im)
# cv2.waitKey()
# cv2.destroyAllWindows()
