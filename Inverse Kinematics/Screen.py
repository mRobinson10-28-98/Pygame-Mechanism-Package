from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels
import Variables as v
import pygame as py

class Screen:
    def __init__(self, window):
        self.window = window
        self.xy = True
        self.renders = []

        self.points = []
        self.linkages = []
        self.deleted_points = []
        self.buttons = []

        self.point_index = 0

    def initialize(self):
        py.time.delay(v.time_delay)
        self.window.fill((255, 255, 255))

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

    def draw(self, additional_renders = []):
        py.draw.line(self.window, v.gray,
                     (inches_to_pixels(v.origin_x - v.screen_dimension_inches / 2), inches_to_pixels(v.origin_y)),
                     (inches_to_pixels(v.origin_x + v.screen_dimension_inches / 2), inches_to_pixels(v.origin_y)))
        py.draw.line(self.window, v.gray,
                     (inches_to_pixels(v.origin_x), inches_to_pixels(v.origin_y - v.screen_dimension_inches / 2)),
                     (inches_to_pixels(v.origin_x), inches_to_pixels(v.origin_y + v.screen_dimension_inches)))
        axisFont = py.font.Font('freesansbold.ttf', 20)

        if self.xy:
            self.window.blit(axisFont.render("X", True, v.black),
                               (v.screen_dimension - 20, inches_to_pixels(v.origin_y)))
            self.window.blit(axisFont.render("Y", True, v.black),
                               (inches_to_pixels(v.origin_x), v.screen_dimension - 20))

        else:
            self.window.blit(axisFont.render("Z", True, v.black),
                               (v.screen_dimension - 20, inches_to_pixels(v.origin_y)))
            self.window.blit(axisFont.render("Y", True, v.black),
                               (inches_to_pixels(v.origin_x), v.screen_dimension - 20))

        for render in self.renders:
            for object in render:
                object.render()

        for render in additional_renders:
            for object in render:
                object.render()

        py.display.update()

    def update(self, additional_renders = []):
        self.renders = []
        self.renders.append(self.points)
        self.renders.append(self.linkages)
        self.renders.append(self.buttons)

        self.draw(additional_renders)
