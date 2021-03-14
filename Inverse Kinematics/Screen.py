from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels
import Variables as v
import pygame as py
import Keys as ks
from Point import Point

class Screen:
    def __init__(self, window):
        self.window = window
        self.xy_modifier = 0
        self.planar_path_modifier = 0
        self.edit_mode_modifier = 0

        self.xy = True
        self.planar_path = True
        self.edit_mode = False

        self.points = []
        self.linkages = []
        self.deleted_points = []
        self.buttons = []
        self.key_commanders = []

        self.point_index = 0
        self.current_point = 0

    def initialize(self):
        py.time.delay(v.time_delay)
        self.window.fill((255, 255, 255))

        self.current_point = self.points[self.point_index]
        self.xy = self.xy_modifier.boolean
        self.planar_path = self.planar_path_modifier.boolean
        self.edit_mode = self.edit_mode_modifier.boolean

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
            Point(self.points[-1].x, self.points[-1].y, self.points[-1].z, self, self.deleted_points)
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

        for key_commander in self.key_commanders:
            key_commander.check_key_commands(input_array)

