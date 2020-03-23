import cv2
import imutils
import numpy as np
from imutils.video import VideoStream
import time
import math

#vs = VideoStream(src=1).start()
time.sleep(0.5)
MIN = 200

DELTA = 7

OFFSET = 0.07

def get_cube_coords(vs):
    frame = vs.read()
    frame = imutils.resize(frame, width=640, height=360)

    if frame is None:
        return

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (19, 19), 0)
    gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 1)
    thresh = cv2.bitwise_not(thresh)
    cv2.imshow("thresh", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = []
    circles_coords = []

    circles = cv2.HoughCircles(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.HOUGH_GRADIENT, 1.5, 20)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
        circles_coords.append([x, y])

    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < MIN:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        if not circles_coords:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center.append([int(x + w / 2), int(y + h / 2)])
        for circle in circles_coords:
            if max((np.array([x, y]) - np.array(circle))) > DELTA:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center.append([int(x + w/2), int(y + h/2)])
        #print(center)
    cv2.imshow("result", frame)
    key = cv2.waitKey(1) & 0xFF
    return center

def check_existance(obj, coord):
    eps = 0.05
    for o in obj:
        if math.sqrt((o[0] - coord[0])**2 + (o[1] - coord[1])**2) <= 0.05:
            return obj.index(o)
    return False

if __name__ == "__main__":
    vs = VideoStream(src=0).start()
    time.sleep(0.5)
    velocity = 0.2
    x, y = 0, 0
    dt = 0.05
    obj = []
    h = 0.1
    f = lambda x: -1100000/9991*x + 938212/9991
    while True:
        coords = get_cube_coords()
        for coord in coords:
            coord[0] -= 320
            coord[1] -= 180
            pic = f(h)
            coord[0] /= (100*pic)
            coord[1] = coord[1]/(100*pic) - OFFSET
            i = check_existance(obj, coord)
            if not i:
                obj.append(coord)
            else:
                obj[i][0] += coord[0]
                obj[i][1] += coord[1]
                obj[i][0] /= 2
                obj[i][1] /= 2
        x += velocity*dt
    print(obj)
