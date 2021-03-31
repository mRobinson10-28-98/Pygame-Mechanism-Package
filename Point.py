import pygame as py
import math as m

import Variables as v

# Point class defines the position of a point for inverse kinematics
# Must give an x,y,z position, as well as the screen object
# Also must give specific set from that screen object (usually screen.points)
class Point:
    def __init__(self, screen, x, y, z, set):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.screen = screen
        self.set = set

        self.color = v.red
        self.radius = 3
        self.x_inches = self.screen.pixels_to_inches(self.x) - self.screen.origin_x
        self.y_inches = self.screen.pixels_to_inches(self.y) - self.screen.origin_y
        self.z_inches = self.screen.pixels_to_inches(self.z) - self.screen.origin_x
        self.set.append(self)

    def render(self):
        if self.screen.xy:
            py.draw.circle(self.screen.window, self.color, (self.x, self.y), self.radius)
        else:
            py.draw.circle(self.screen.window, self.color, (self.z, self.y), self.radius)