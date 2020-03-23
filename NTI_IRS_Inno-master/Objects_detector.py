from typing import List, Optional, Union

import cv2
import imutils
import numpy as np

from objects.Object import Bucket, Cube
#from dominant_color import DominantColorDetector


class ObjectsDetector:

    def stupid_detection(self, frame):
        hsv, thresh = self.__prepare_frame(frame, height=self._height, width=self._width)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            if cv2.contourArea(c) < self._min_area:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            
            return x + w / 2, y + h / 2

    """
    Constants
    #
    # @param width
    # @param height
    #
    # @param circles_pool_length length of pool with previous circles to prevent fluctuations of contours
    # @param min_area_to_detect min area to detect contours
    #
    # @param circle_factor coefficient to prevent fluctuations of contours with circles
    # @param debug_mode if true call cv2.imshow() to take a look at result
    # @param rotation_factor coefficient for is_rotated. The smaller it is, the more precise would be algorithm.
    # @param daytime preset for day or night light. Should be customize for your environment.
    """

    def __init__(self,
                 # TODO determine this factor
                 rotation_factor=22,
                 width=640,
                 height=360,
                 circles_pool_length=5,
                 min_area_to_detect=400,
                 circle_factor=1.25,
                 debug_mode=False,
                 # TODO change min are
                 min_area_to_compute_mean_colors=100000,
                 daytime="DAY"):

        self._width = width
        self._height = height
        self._pool_size = circles_pool_length
        self._min_area = min_area_to_detect
        self._circle_factor = circle_factor
        self._circles_coords_pool = list()
        self._debug_mode = debug_mode
        self._min_area_for_dominant = min_area_to_compute_mean_colors
        self._daytime = 100 if daytime == "DAY" else 125
        self._rotation_factor = rotation_factor
        #self._dominant_detector = DominantColorDetector(n_clusters=7)

    # crop image
    def _get_subimage_by_pxs(self, image, start, shift):
        cropped_image = []

        for i in range(shift[1]):
            cropped_image.append([])
            for j in range(shift[0]):
                cropped_image[i].append([])
                cropped_image[i][j] = image[start[1] + i][start[0] + j]

        return np.array(cropped_image)

    # Can detect that cube is rotated relatively to the camera
    def is_rotated(self, frame):
        hsv, thresh = self.__prepare_frame(frame, height=self._height, width=self._width)

        cv2.imshow("thresh", thresh)
        # find cube
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) < self._min_area:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            # take a small image of it
            area = self._get_subimage_by_pxs(thresh, start=(x, y), shift=(w, h))
            print(area.shape)
            # cv2.imshow('result', area)
            # compute a factor
            factor = self.__get_difference(area)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                return None

            if factor >= self._rotation_factor:
                return True
            else:
                return False

    # using absdiff to get all pixels that deviate from reference
    def __get_difference(self, frame_thresh):
        reference = cv2.imread('./src/reference.png')
        shape = min(min((frame_thresh.shape, reference.shape[:-1])))
        frame = cv2.resize(reference, (shape, shape))
        hsv, reference_thresh = self.__prepare_frame(reference, width=shape, height=shape)
        frame_thresh = cv2.resize(frame_thresh, (shape, shape))

        frame_delta = cv2.absdiff(frame_thresh, reference_thresh)
        frame_delta = cv2.dilate(frame_delta, None, iterations=2)

        # count pixels
        counter = 0
        for row in frame_delta:
            for pixel in row:
                if pixel == 255:
                    counter += 1
        # devide by shape to get relation with size of the cropped image
        return counter / shape

    # function that resize and make hsv and thresh copy of a frame
    def __prepare_frame(self, frame, width, height):

        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        blur = cv2.GaussianBlur(hsv, (19, 19), 0)

        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, self._daytime, 255, 1)
        thresh = cv2.bitwise_not(thresh)
        return hsv, thresh

    # Check if this object is circle and we shouldn't detect it
    # iterate though pool with circles and check a distance between coordinates and circles
    def _circle_check(self, pool, coords):
        if pool:
            for circles in pool:
                for circle in circles:
                    if max(abs(np.array(circle.get_position()) - np.array(coords))) < \
                            self._circle_factor * circle.get_radius():
                        return False

        return True

    """
    # @brief Color detection by hue, check HSV wiki for details. Take a 20x20 px square and count mean H component
    # then translate it to 360 points scale. Then just compare it with table (wiki) 
    # @note if a color cannot be detected return 'no_color'
    # @param image just image where needed to detect color 
    
    # @param x coordinate of a dot where to detect color
    # @param y 
    
    """

    def _get_color(self, image, x, y):
        # if contour nearby edge use square with smaller side
        if x == self._width:
            x -= 1
        if y == self._height:
            y -= 1

        area = 0
        for i in range(10):
            if x - i < 0 or x + i >= self._width:
                break
            elif y - i < 0 or y + i >= self._height:
                break
            else:
                area = i

        avg_color = 0
        # Count mean
        for i in range(x - area, x + area):
            for j in range(y - area, y + area):
                avg_color += image[j, i, 0]

        # translate result
        avg_color = avg_color / area ** 2 if area != 0 else image[y, x, 0]
        hsv_color = 255 / 360 * avg_color
        # compare
        if 0 < hsv_color <= 13 or 330 <= hsv_color:
            return 'RED'
        elif 13 <= hsv_color < 35:
            return 'BLUE'
        elif 35 <= hsv_color < 70:
            return 'ORANGE'
        elif 70 <= hsv_color < 180:
            return 'GREEN'
        elif 180 <= hsv_color < 300:
            return 'YELLOW'
        else:
            return 'no_color'


    """
    # @brief Detect objects(bucket or cube) in image
    # @param frame take an image (RGB) were need to detect objects(bucket or cube). 
    """

    def get_objects(self, frame) -> Optional[List[Union[Bucket, Cube]]]:
        if frame is None:
            raise ValueError('Frame is none')

        frame = cv2.resize(frame, (self._width, self._height))

        # Font
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        fontColor = (255, 255, 255)

        hsv, thresh = self.__prepare_frame(frame, height=self._height, width=self._width)

        # Store here all objects
        objects_in_frame = []

        """
        # First detect only buckets. It's more simple to detect circle in frame then 
        # we iterate each contour and check if it is circle or not.
        # We conclude a contour a circle if it has the center nearby a center of already detected circles.
        # `get_color` - function that make a verification for contour
        """

        #  Pool must not be bigger than max size
        if self._circles_coords_pool is not None and len(self._circles_coords_pool) >= self._pool_size:
            self._circles_coords_pool.pop()

        # Get circles
        circles = cv2.HoughCircles(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.HOUGH_GRADIENT, dp=1.5, minDist=1000,
                                   param1=65, param2=90)
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                circles = list()
                bucket = Bucket(position=(x, y), radius=r, color=self._get_color(hsv, x, y))
                cv2.putText(img=frame, text=str(bucket),
                            org=(x, y),
                            fontFace=font,
                            fontScale=fontScale,
                            color=fontColor)
                circles.append(bucket)
                objects_in_frame.append(bucket)
            self._circles_coords_pool.append(circles)

        cv2.imshow('thresh', thresh)
        # Check all contours
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            # if the contour is too small, ignore it
            (x, y, w, h) = cv2.boundingRect(c)
            if cv2.contourArea(c) < self._min_area:
                continue
            elif cv2.contourArea(c) > self._min_area_for_dominant:
                # TODO find dominant color
                #self._reveal_clusters(frame, position=(x, y), shift=(w, h))
                pass
                # area = self._get_image_by_px(frame, [x, y], [x + w, y + h])
                # cv2.imshow("cropped", area)

            # area = self._get_image_by_px(frame, [x, y], [x + w, y + h])
            # Validation with circle_check
            if self._circle_check(self._circles_coords_pool, [x, y]):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center_x = int(x + w / 2)
                center_y = int(y + h / 2)
                cube = Cube(position=(center_x, center_y), color=self._get_color(hsv, x=center_x, y=center_y))
                cv2.putText(img=frame, text=str(cube),
                            org=(x, y),
                            fontFace=font,
                            fontScale=fontScale,
                            color=fontColor)
                objects_in_frame.append(cube)

        cv2.imshow('result', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            return None

        return objects_in_frame
