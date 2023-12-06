import cv2
import pickle
import numpy as np
 
# cap = cv2.VideoCapture('parking.mp4')

# USING WEBCAME
cap = cv2.VideoCapture(0)

width, height = 40, 18
#width, height = 103, 43
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)
 
 
def empty(a):
    pass
 
 
cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 160)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)
 
 
def checkSpaces():
    spaces = 0
    for pos in posList:
        x, y = pos
        w, h = width, height
 
        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)
 
        if count < 100:
            color = (0, 255, 0)
            thic = 1
            spaces += 1
 
        else:
            color = (0, 0, 255)
            thic = 1
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

    cv2.putText(img, f'Available: {spaces}/{len(posList)}', (200, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4, cv2.LINE_AA)
 
while True:
 
    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

 
    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)
 
    checkSpaces()
    # Display Output
    cv2.imshow("Paking Control", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
