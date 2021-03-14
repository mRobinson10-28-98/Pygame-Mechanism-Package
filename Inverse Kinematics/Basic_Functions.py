import Variables as v
import pygame as py

# Converts length from pixels to inches (usually for kinematic analysis)
def pixels_to_inches(pixels):
    return (pixels * v.screen_dimension_inches) / v.screen_dimension


# Converts length from inches to pixels (usually for display purposes)
def inches_to_pixels(inches):
    return (inches * v.screen_dimension) / v.screen_dimension_inches

def initialize_screen(window):
    py.time.delay(v.time_delay)
    window.fill((255, 255, 255))

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False