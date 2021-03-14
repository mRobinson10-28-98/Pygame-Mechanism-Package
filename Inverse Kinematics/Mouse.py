import pygame as py
import Variables as v
from Point import Point
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels

class Mouse:
    def __init__(self, x, y, screen, point=0, holdingPoint=False):
        self.x = x
        self.y = y
        self.screen = screen
        self.holdingPoint = holdingPoint
        self.point = point
        self.onButton = False
        self.fixedx = 0
        self.fixedy = 0
        self.previous_point_index = 0

    def modify_point(self):
        self.point.x = self.x
        self.point.y = self.y
        self.point.z = self.x

    def render(self):
        self.point.render()

    def check_buttons(self, input_boolean):
        self.onButton = False
        for button in self.screen.buttons:
            if button.clicked(self.x, self.y, input_boolean):
                self.onButton = True

    def append_point(self, input_key, planar_path_boolean, planar_offset):
        if self.screen.xy:
            if not planar_path_boolean:
                self.holdingPoint = True
                self.point = Point(self.x, self.y, self.x, self.screen, self.screen.points)
                self.fixedx = self.x
                self.fixedy = self.y
                self.previous_point_index = self.screen.point_index
                self.screen.xy = False
                input_key.refresh()
            else:
                Point(self.x, self.y, inches_to_pixels(v.origin_x + planar_offset), self.screen, self.screen.points)
                input_key.refresh()

        # If you've already clicked a point in the xy plane and are now in zy plane, create a point
        elif not self.screen.xy and self.holdingPoint:
            self.screen.points.pop(-1)
            Point(self.fixedx, self.fixedy, self.x, self.screen, self.screen.points)
            self.holdingPoint = False
            self.point = 0
            self.screen.point_index = self.previous_point_index
            self.screen.xy = True
            input_key.refresh()

    def edit_point(self):
        pass
        '''
        if xyScreen:
            if not mouse.holdingPoint:
                indexClosest = 0
                pointClosest = 0
                rShortest = 10000
                for point in points:
                    r = m.sqrt((mouse.x - point.x) ** 2 + (mouse.y - point.y) ** 2)
                    if r < rShortest:
                        rShortest = r
                        indexClosest = points.index(point)
                points.pop(indexClosest)
                mouse.holdingPoint = True
                left_click.refresh()

            else:
                if planarPath.boolean:
                    points.insert(indexClosest, Point(mouse.x, mouse.y, inches_to_pixels(v.origin_x + leg1.lhipz)))
                    mouse.holdingItem = False
                    left_click.refresh()
                else:
                    mouse.holdingItem = False
                    x = mouse.x
                    y = mouse.y
                    screen.xy = False

        else:
            points.insert(indexClosest, Point(x, y, mouse.x))
            left_click.refresh()
        '''
