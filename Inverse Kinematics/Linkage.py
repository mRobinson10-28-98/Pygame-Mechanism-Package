import pygame as py
import math as m

import Variables as v
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels

# All Linkage parameters input in iches, then converted in __init__ to pixels
class Linkage:
    def __init__(self, length, x1, y1, theta, color, set, xy=True):
        self.x1 = inches_to_pixels(x1)
        self.y1 = inches_to_pixels(y1)
        self.length = inches_to_pixels(length)
        self.theta = theta
        self.x2 = self.x1 + self.length * m.cos((self.theta))
        self.y2 = self.y1 + self.length * m.sin((self.theta))
        self.color = color
        self.set = set
        self.xyPlane = True
        self.xy = xy
        self.set.append(self)

    def render(self, window, xyScreen):
        if self.xy == xyScreen:
            py.draw.line(window, self.color, (self.x1, self.y1),
                         (self.x2, self.y2), 12)