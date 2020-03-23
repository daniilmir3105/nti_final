import cv2
from Objects_detector import ObjectsDetector

vs = cv2.VideoCapture(0)
# vs = VideoStream(src=0).start()
# time.sleep(0.5)

detector = ObjectsDetector(debug_mode=True)

while True:
    frame = vs.read()[1]
    # print(detector.is_rotated(frame))

    objects = detector.get_objects(frame)

vs.release()
cv2.destroyAllWindows()
