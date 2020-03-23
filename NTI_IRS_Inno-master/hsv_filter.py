import cv2
import imutils
import numpy as np
import time


def nothing(*arg):
    pass


cv2.namedWindow("result")  # создаем главное окно
cv2.namedWindow("settings")  # создаем окно настроек

# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0, 0, 0, 0, 0, 0]

vs = cv2.VideoCapture("./camera/WIN_20200321_13_34_37_Pro.mp4")
now = time.time()

while abs(now - time.time()) <= 1:
    img = vs.read()[1]

img = vs.read()[1]
while True:
    frame = imutils.resize(img, width=640, height=360)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('result', thresh)

    ch = cv2.waitKey(5)
    if ch == 27:
        break

print(h1)
print(s1)
print(v1)
print(h2)
print(s2)
print(v2)
cv2.destroyAllWindows()
