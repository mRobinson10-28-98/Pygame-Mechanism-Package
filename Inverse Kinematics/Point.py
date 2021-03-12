import pygame as py
import math as m

import Variables as v
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels


# Point class defines the position of a point for inverse kinematics
class Point:
    def __init__(self, x, y, z, set):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.set = set
        self.color = v.red
        self.radius = 3
        self.x_inches = pixels_to_inches(self.x) - v.origin_x
        self.y_inches = pixels_to_inches(self.y) - v.origin_y
        self.z_inches = pixels_to_inches(self.z) - v.origin_x
        self.set.append(self)

    def render(self, window, xyScreen):
        if xyScreen:
            py.draw.circle(window, self.color, (self.x, self.y), self.radius)
        else:
            py.draw.circle(window, self.color, (self.z, self.y), self.radius)