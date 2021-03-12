import pygame as py

poop = 'poop'

class Clock:
    def __init__(self, time=0):
        self.time = time
        self.previous = False
        self.current = False

    def update(self):
        self.time = py.time.get_ticks()

    def passed(self):
        return py.time.get_ticks() - self.time

left_click = Clock()
right_click = Clock()
k_click = Clock()
z_click = Clock()
r_click = Clock()
l_click = Clock()
j_click = Clock()
p_click = Clock()
d_click = Clock()
a_click = Clock()
space_click = Clock()

keys = py.key.get_pressed()
mouse_pos = py.mouse.get_pos()
mouse_press = py.mouse.get_pressed()
mouse_left_click = mouse_press[0]
mouse_right_click = mouse_press[2]

def r_press():
    if keys[py.K_r] and r_click.passed() > 200:
        return True
