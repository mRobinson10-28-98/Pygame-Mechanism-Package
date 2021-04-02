import sys
import pygame as py
import math as m
import Variables as v
from Point import Point
from CsvWriter import CsvWriter
from CsvReader import CsvReader
from Five_Bar_3DoF_Leg import Leg
from Screen import Screen
from Button import Button
from Mouse import Mouse

'''
*********************************How to use*******************************
Left click: Add a point
Right click: Clear all points
Z: delete last point
R: redo last deletion
L: Move to next point
J: Move to previous point
A: Move current point left
D: Move current point right
W: Move current point up
S: Move current point down
Ctrl+Space: Iterate through all points and write point positions and specified values to csv file
Shift+Space: Grab points from designated csv file and add them to screen

*********************************How to create*******************************
NOTE: This code will not run without specifying a fileRead and fileWrite name for the csv objects.

IMPORTING: This file IS in the Pygame-Mechanism_Mechanism directory, but if it were not, import sys, 
and above importing any of this package, run sys.insert(0, "path"), where path would be the path to the directory.

SCREEN: To create a script, first create a screen object, specifying the screen dimension in pixels,
and the screen dimension in inches. This code's screen object is named "screen". The screen object keeps track of all 
linkages, points, and many basic key commands. Most object that are created, including the mechanisms, csvReader/Writer, 
mouse, and points, must have the screen specified as the first argument.

INPUTS: The pygame while loop must calculate the key inputs, mouse button inputs, and mouse position
specified in this file as keys, mouse_press, and mouse_pos respectively. The mouse_pos and mouse_press must the input 
into mouse.function(), optionally with the z-offset for any points created in the planar configuration. 

NEW PACKAGES: Any new classes, including new mechanisms, that will have any keyboard inputs related to that class,
should be put in a method called check_key_commands, and in the __init__ method, 
the object should be appended to the screens key_commanders list by typing self.screen.key_commanders.append(self).
For new mechanisms, have a method called inv_kinematics, and a method called create, which runs inv_kinematics and 
draws the mechanism on the screen using linkage class. See Four_Bar_3DoF_Leg.py for reference

CSV: To create a csv reader object, specify the screen and file path. the writer object also needs a mechanism or any 
object that has a method called return_for_csv(), which returns a row of values to be written into a row of the 
specified csv file. 
**************************************************************************
'''


fileWriteName = 'specify path here'
fileReadName = 'specify path here'

screen_dim_pix = 800
screen_dim_inch = 24

# Screen multiplier
multiplier = 1

# Link Lengths in inches (Thigh, crank, coupler, follower, calf, hip)
linkLength1 = 4.5
linkLength2 = 1.5
linkLength3 = 4.5
linkLength4 = 1.5
linkLength5 = 6.5 - linkLength4
linkLengthhip = 2

linkLength1 *= multiplier
linkLength2 *= multiplier
linkLength3 *= multiplier
linkLength4 *= multiplier
linkLength5 *= multiplier
linkLengthhip *= multiplier

screen = Screen(screen_dim_pix, screen_dim_inch)

leg1 = Leg(screen, linkLength1, linkLength2, linkLength3,
           linkLength4, linkLength5, linkLengthhip)

csvWriter = CsvWriter(screen, fileWriteName, leg1)
csvReader = CsvReader(screen, fileReadName)

mouse = Mouse(screen)

Point(screen, screen.inches_to_pixels(screen.origin_x), screen.inches_to_pixels(screen.origin_y + 3), 0, screen.points)

run = True
test = False
while run:
    screen.initialize()

    # Mouse Position
    keys = py.key.get_pressed()
    mouse_press = py.mouse.get_pressed()
    mouse_pos = py.mouse.get_pos()
    mouse.function(mouse_pos, mouse_press, leg1.lhipz)

    screen.check_key_commands(keys)

    # Calculate all position and force variables based on current point
    leg1.create()

    screen.draw([[leg1]])

py.quit()


