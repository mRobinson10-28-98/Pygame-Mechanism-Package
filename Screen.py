import pygame as py

import Variables as v
import Keys as ks
from Point import Point
from Button import Button


class Screen:
    def __init__(self, screen_dimension_pixels, screen_dimension_inches):
        py.init()

        self.dimension_pixels = screen_dimension_pixels
        self.dimension_inches = screen_dimension_inches
        self.origin_x = self.dimension_inches / 2
        self.origin_y = self.dimension_inches / 2

        # Creates the window and defines its dimensions
        self.window = py.display.set_mode((self.dimension_pixels, self.dimension_pixels))

        # Title
        self.caption = ''
        py.display.set_caption(self.caption)


        self.points = []
        self.linkages = []
        self.deleted_points = []
        self.buttons = []
        self.key_commanders = []

        self.point_index = 0
        self.current_point = 0

        self.xy = True
        self.planar_path = True
        self.xy_modifier = Button(self, 10, 25, "XY SCREEN", True, v.green)
        self.planar_path_modifier = Button(self, 50, 25, "Keep Path Planar", True, v.green)

    # Converts length from pixels to inches (usually for kinematic analysis)
    def pixels_to_inches(self, pixels):
        return (pixels * self.dimension_inches) / self.dimension_pixels

    # Converts length from inches to pixels (usually for display purposes)
    def inches_to_pixels(self, inches):
        return (inches * self.dimension_pixels) / self.dimension_inches

    def initialize(self):
        py.time.delay(v.time_delay)
        self.window.fill((255, 255, 255))

        self.linkages = []
        self.current_point = self.points[self.point_index]
        self.xy = self.xy_modifier.boolean
        self.planar_path = self.planar_path_modifier.boolean

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

    def draw(self, additional_renders = []):
        py.draw.line(self.window, v.gray,
                     (self.inches_to_pixels(self.origin_x - self.dimension_inches), self.inches_to_pixels(self.origin_y)),
                     (self.inches_to_pixels(self.origin_x + self.dimension_inches), self.inches_to_pixels(self.origin_y)))
        py.draw.line(self.window, v.gray,
                     (self.inches_to_pixels(self.origin_x), self.inches_to_pixels(self.origin_y - self.dimension_inches)),
                     (self.inches_to_pixels(self.origin_x), self.inches_to_pixels(self.origin_y + self.dimension_inches)))
        axisFont = py.font.Font('freesansbold.ttf', 20)

        if self.xy:
            self.window.blit(axisFont.render("X", True, v.black),
                             (self.dimension_pixels - 20, self.inches_to_pixels(self.origin_y)))
            self.window.blit(axisFont.render("Y", True, v.black),
                             (self.inches_to_pixels(self.origin_x), self.dimension_pixels - 20))

        else:
            self.window.blit(axisFont.render("Z", True, v.black),
                             (self.dimension_pixels - 20, self.inches_to_pixels(self.origin_y)))
            self.window.blit(axisFont.render("Y", True, v.black),
                             (self.inches_to_pixels(self.origin_x), self.dimension_pixels - 20))

        for point in self.points:
            point.render()
        for linkage in self.linkages:
            linkage.render()
        for button in self.buttons:
            button.render()

        for render in additional_renders:
            for object in render:
                object.render()

        py.display.update()

    def check_key_commands(self, input_array):
        # If "z" is pressed, delete previous point, and add it to deleted points list
        if ks.z_click.clicked(input_array) and len(self.points) > 1:
            self.points.pop(-1)
            Point(self, self.points[-1].x, self.points[-1].y, self.points[-1].z, self.deleted_points)
            ks.z_click.refresh()

        # If "r" is pressed, redraw point most previously deleted (redo)
        if ks.r_click.clicked(input_array) and len(self.deleted_points) > 0:
            self.points.append(self.deleted_points[-1])
            self.deleted_points.pop(-1)
            ks.r_click.refresh()

        # If "l" is pressed, go to next point in list
        if ks.l_click.clicked(input_array):
            if self.point_index < len(self.points) - 1:
                self.point_index += 1
            else:
                self.point_index = 0
            ks.l_click.refresh()

        # If "j" is pressed, go to previous point in list
        if ks.j_click.clicked(input_array):
            if self.point_index > 0:
                self.point_index -= 1
            else:
                self.point_index = len(self.points) - 1
            ks.j_click.refresh()

        if ks.a_click.clicked(input_array):
            if self.xy:
                self.current_point.x -= 1
            else:
                self.current_point.z -= 1
            ks.a_click.refresh()

        if ks.d_click.clicked(input_array):
            if self.xy:
                self.current_point.x += 1
            else:
                self.current_point.z += 1
            ks.d_click.refresh()

        if ks.w_click.clicked(input_array):
            self.current_point.y -= 1
            ks.w_click.refresh()

        if ks.s_click.clicked(input_array):
            self.current_point.y += 1
            ks.s_click.refresh()

        self.current_point.x_inches = self.pixels_to_inches(self.current_point.x) - self.origin_x
        self.current_point.y_inches = self.pixels_to_inches(self.current_point.y) - self.origin_y
        self.current_point.z_inches = self.pixels_to_inches(self.current_point.z) - self.origin_x

        for key_commander in self.key_commanders:
            key_commander.check_key_commands(input_array)

