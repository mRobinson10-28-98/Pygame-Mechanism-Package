import pygame as py
import math as m
import csv

import Variables as v
import Basic_Functions as bf
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels
from Point import Point
from Linkage import Linkage
from CsvWriter import CsvWriter
from CsvReader import CsvReader
from Five_Bar_3DoF_Leg import Leg
from Key import Key
from Screen import Screen
from Button import Button
from Mouse import Mouse
import Keys as ks


'''
fileWriteName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
fileReadName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
 '''
fileWriteName = 'C:/Users/drunk/PycharmProjects/pythonProject/Sean/5 Bar 3 Dof Quadruped/Normal Walking Gaits/03132021.csv'
fileReadName = 'C:/Users/drunk/PycharmProjects/pythonProject/Sean/5 Bar 3 Dof Quadruped/Normal Walking Gaits/03132021.csv'

# Initiated pygame
py.init()
 
# Defines window
win = py.display.set_mode((v.screen_dimension, v.screen_dimension))
 
# Title
py.display.set_caption('Inverse Kinematics')

screen = Screen(win)
leg1 = Leg(v.linkLength1, v.linkLength2, v.linkLength3,
           v.linkLength4, v.linkLength5, v.linkLengthhip, screen)

csvWriter = CsvWriter(fileWriteName, leg1, screen)
csvReader = CsvReader(fileReadName, screen)

mouse = Mouse(0, 0, screen)

xy_screen_button = Button(10, 25, "XY SCREEN", True, screen)
xy_screen_button.color = v.green
planar_path_button = Button(50, 25, "Keep Path Planar", True, screen)
planar_path_button.color = v.green
edit_mode_button = Button(90, 25, 'Edit Mode', False, screen)

screen.xy_modifier = xy_screen_button
screen.planar_path_modifier = planar_path_button
screen.edit_mode_modifier = edit_mode_button

Point(inches_to_pixels(v.origin_x - 4),
                    v.screen_dimension - inches_to_pixels(v.origin_y + 4), inches_to_pixels(v.origin_x - 4), screen, screen.points)

run = True
test = False
while run:
    screen.initialize()

    # Mouse Position
    keys = py.key.get_pressed()
    mouse_press = py.mouse.get_pressed()
    mouse_pos = py.mouse.get_pos()
    mouse.update(mouse_pos)

    mouse.function(mouse_press, leg1.lhipz)

    screen.check_key_commands(keys)

    # Calculate all position and force variables based on current point
    leg1.inv_kinematics(screen.current_point)
    leg1.create()
    screen.draw()
 
py.quit()


