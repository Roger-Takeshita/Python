# https://gist.github.com/siphomateke/78cc10a5c0a978f9399098e92754c1ce

import numpy as np
import cv2

# The hsv color of the rectangle (0, 255, 255)
# If the hsv color will not be exactly pure you can change lower and upper accordingly
lower = np.array([237, 97, 71], np.uint8)
upper = np.array([237, 97, 71], np.uint8)

img = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/002.png", cv2.IMREAD_COLOR)
# if image was loaded correctly
if img is not None:
    # convert to hsv
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Extract the hue value
    hue = img_hsv[:, :, 0]
    # Threshold to extract only color we want
    thresh = cv2.inRange(img_hsv, lower, upper)

    # Detect contours with tree hierachy
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # For each contour extract the child idxs
    # This is so that the inside of the rectangle is extracted
    # otherwise we would get the rectangle in our extracted images
    idxs = []
    for i in range(len(contours)):
        # more info on contour hierachy: http://docs.opencv.org/trunk/d9/d8b/tutorial_py_contours_hierarchy.html
        child = hierarchy[0][i][2]
        if child > 0:
            idxs.append(child)

    # convert to numpy array and get only child contours
    contours = np.array(contours)
    contours = contours[idxs]

    # get the bounding rectangles for each contour
    rects = [cv2.boundingRect(c) for c in contours]

    # add some inwards padding to the ROI to allow for error
    padding = 2

    extracted_imgs = []
    for r in rects:
        x = r[0] + padding
        y = r[1] + padding
        w = r[2] - (padding * 2)
        h = r[3] - (padding * 2)
        roi = img[y : y + h, x : x + w]
        extracted_imgs.append(roi)

    # Display the extracted images
    for i in range(len(extracted_imgs)):
        img = extracted_imgs[i]
        cv2.imshow("Image {}".format(i), img)
    cv2.waitKey(0)
