from abc import ABC

"""
Objects for detection
"""


class Object(ABC):
    """
    # position – tuple of pixels!!!
    # x and y coordinates (e.g. (x,y) )
    #
    # color - String
    # Can be 'RED', 'YELLOW', 'GREEN', and 'BLUE'
    """
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.distance = 0

    def get_position(self):
        return self.position

    def calc_distance(self, coord):
        self.distance = ((self.position[0] - coord[0]) ** 2
                         + (self.position[1] - coord[1]) ** 2) ** 0.5

    def set_position(self, position):
        self.position = position

    def get_color(self):
        return self.color

    def __str__(self):
        return '{} {} at position {}'.format(self.color, self.__class__.__name__, self.position)


class Cube(Object):
    def __init__(self, position, color):
        super().__init__(position, color)


class Bucket(Object):
    # radius - int, pixels!
    def __init__(self, position, color, radius):
        super().__init__(position, color)
        self.radius = radius

    def get_radius(self):
        return self.radius
