import cv2
import pickle
import numpy as np
 
# Video feed
cap = cv2.VideoCapture('carPark.mp4')
 
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)
 
width, height = 107, 48
 
 
def checkParkingSpace(imgPro):
    spaceCounter = 0
 
    for pos in posList:
        x, y = pos
 
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)
 
 
        if count < 900:
            color = (0, 255, 0)
            thickness = 2
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
 
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        org = (x, y + height - 3)
        # fontScale
        fontScale = 0.5
        # Blue color in BGR
        color = (255, 0, 0)
        # Line thickness of 2 px
        thickness = 1

        # Using cv2.putText() method
        cv2.putText(img, str(count), org, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.putText(img, f'Free: {spaceCounter}/{len(posList)}', (50, 50), font, 1, (255, 0, 0), 4, cv2.LINE_AA)


while True:
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
 
    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
