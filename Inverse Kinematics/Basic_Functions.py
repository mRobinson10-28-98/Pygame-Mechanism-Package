import Variables as v
import pygame as py

# Converts length from pixels to inches (usually for kinematic analysis)
def pixels_to_inches(pixels):
    return (pixels * v.screen_dimension_inches) / v.screen_dimension

# Converts length from inches to pixels (usually for display purposes)
def inches_to_pixels(inches):
    return (inches * v.screen_dimension) / v.screen_dimension_inches


