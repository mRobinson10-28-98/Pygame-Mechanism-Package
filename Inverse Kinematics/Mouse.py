import pygame as py
import Variables as v
from Point import Point
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels
import Keys as ks

class Mouse:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

        self.holding_point = False
        self.point = 0
        self.onButton = False
        self.fixedx = 0
        self.fixedy = 0
        self.fixedz = 0
        self.previous_point_index = 0

    def update(self, input_array):
        self.x = input_array[0]
        self.y = input_array[1]

    def modify_point(self):
        self.point.x = self.x
        self.point.y = self.y
        self.point.z = self.x

    def render(self):
        self.point.render()

    def check_buttons(self, input_set):
        self.onButton = False
        for button in self.screen.buttons:
            if button.clicked(self.x, self.y, ks.left_click.clicked(input_set)):
                self.onButton = True
                button.boolean = not button.boolean
                if button.boolean:
                    button.color = v.green
                else:
                    button.color = v.red
                ks.left_click.refresh()

    def append_point_planar(self, planar_offset):
        Point(self.x, self.y, inches_to_pixels(v.origin_x + planar_offset), self.screen, self.screen.points)

    def fix_point_xy(self):
        self.holding_point = True
        self.point = Point(self.x, self.y, self.x, self.screen, self.screen.points)
        self.fixedx = self.x
        self.fixedy = self.y
        self.previous_point_index = self.screen.point_index
        self.screen.xy_modifier.boolean = False

    def fix_point_zy(self):
        self.holding_point = True
        self.point = Point(self.x, self.y, self.x, self.screen, self.screen.points)
        self.fixedz = self.x
        self.fixedy = self.y
        self.previous_point_index = self.screen.point_index
        self.screen.xy_modifier.boolean = True

        # If you've already clicked a point in the xy plane and are now in zy plane, create a point
    def append_point_xy(self):
        self.screen.points.pop(-1)
        Point(self.x, self.fixedy, self.fixedz, self.screen, self.screen.points)
        self.holding_point = False
        self.point = 0
        self.screen.point_index = self.previous_point_index
        self.xy = False

    def append_point_zy(self):
        self.screen.points.pop(-1)
        Point(self.fixedx, self.fixedy, self.x, self.screen, self.screen.points)
        self.holding_point = False
        self.point = 0
        self.screen.point_index = self.previous_point_index
        self.xy = True

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

    def function(self, input_set, planar_offset):
        self.check_buttons(input_set)
        # First, check if any buttons are being clicked
        if ks.left_click.clicked(input_set) and not self.onButton:

            if self.screen.edit_mode:
                self.edit_point()

            else:
                # If no buttons are being clicked, and edit mode is not on...
                # Check if in planar path mode, and if so, add point to plane specifying xy plane offset in z direction
                # If not planar path, fix a point to the screen and change screens to append a final point
                # Once on the other screen, the point will be constrained to the previous plane and move only along the 3rd axis
                if self.screen.xy and self.screen.planar_path:
                    self.append_point_planar(planar_offset)

                elif not self.screen.planar_path:
                    if not self.holding_point:
                        if self.screen.xy:
                            self.fix_point_xy()
                        else:
                            self.fix_point_zy()

                    else:
                        if self.screen.xy:
                            self.append_point_xy()
                        else:
                            self.append_point_zy()

            ks.left_click.refresh()

        if ks.right_click.clicked(input_set) and not self.onButton:
            self.screen.points = []
            if self.screen.xy and self.screen.planar_path:
                self.append_point_planar(planar_offset)

            ks.right_click.refresh()

        if self.holding_point and not self.screen.edit_mode:
            if not self.screen.xy:
                self.point.z = self.x
                self.point.z_inches = pixels_to_inches(self.point.z) - v.origin_x
                self.screen.point_index = self.screen.points.index(self.point)
                self.render()
            else:
                self.point.x = self.x
                self.point.x_inches = pixels_to_inches(self.point.x) - v.origin_x
                self.screen.point_index = self.screen.points.index(self.point)
                self.render()
