import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = cv2.imread("/Users/roger-that/Documents/Codes/Python/11_Scripts/image-extractor/002.png")

# Convert the image to grayscale
image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("Number of shapes {0}".format(len(contours)))

for cnt in contours:
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    img = cv2.drawContours(img, [box], 0, (0, 255, 0), 3)

plt.figure("Example 1")
plt.imshow(img)
plt.title("Binary contours in an image")
