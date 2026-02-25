import cv2
import numpy as np

gray = cv2.imread("BM-M4.jpg", 0)
print(gray.shape)
cv2.imshow("Gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Stack grayscale image into 3 channels
three_channel = np.dstack((gray, gray, gray))

cv2.imshow("3 Channel", three_channel)
cv2.waitKey(0)
cv2.destroyAllWindows()