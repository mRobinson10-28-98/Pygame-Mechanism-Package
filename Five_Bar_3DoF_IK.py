import sys
sys.path.insert(0, 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame-Mechanism-Module/Inverse Kinematics')

import pygame as py
import math as m

import Variables as v
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels
from Point import Point
from CsvWriter import CsvWriter
from CsvReader import CsvReader
from Five_Bar_3DoF_Leg import Leg
from Screen import Screen
from Button import Button
from Mouse import Mouse


'''
fileWriteName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
fileReadName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
 '''
fileWriteName = 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame-Mechanism-Module/Normal Walking Gaits/03132021.csv'
fileReadName = 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame-Mechanism-Module/Normal Walking Gaits/03132021.csv'

screen = Screen()


leg1 = Leg(screen, v.linkLength1, v.linkLength2, v.linkLength3,
           v.linkLength4, v.linkLength5, v.linkLengthhip)

csvWriter = CsvWriter(screen, fileWriteName, leg1)
csvReader = CsvReader(screen, fileReadName)

mouse = Mouse(0, 0, screen)

Point(inches_to_pixels(v.origin_x), inches_to_pixels(v.origin_y + 12), 0, screen, screen.points)

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
    leg1.create()

    screen.draw()
 
py.quit()


