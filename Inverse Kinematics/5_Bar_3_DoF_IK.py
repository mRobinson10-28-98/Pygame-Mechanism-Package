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
from Leg import Leg
from Key import Key
from Screen import Screen
from Button import Button
from Mouse import Mouse


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

# Created grid for reference
def draw_screen():
    py.draw.line(win, v.gray, (inches_to_pixels(v.origin_x-v.screen_dimension_inches/2), inches_to_pixels(v.origin_y)),
                 (inches_to_pixels(v.origin_x+v.screen_dimension_inches/2), inches_to_pixels(v.origin_y)))
    py.draw.line(win, v.gray, (inches_to_pixels(v.origin_x), inches_to_pixels(v.origin_y-v.screen_dimension_inches/2)),
                 (inches_to_pixels(v.origin_x), inches_to_pixels(v.origin_y+v.screen_dimension_inches)))
    axisFont = py.font.Font('freesansbold.ttf', 20)
 
    if screen.xy:
        screen.window.blit(axisFont.render("X", True, v.black),
                 (v.screen_dimension - 20, inches_to_pixels(v.origin_y)))
        screen.window.blit(axisFont.render("Y", True, v.black),
                 (inches_to_pixels(v.origin_x), v.screen_dimension - 20))
 
    else:
        screen.window.blit(axisFont.render("Z", True, v.black),
                 (v.screen_dimension - 20, inches_to_pixels(v.origin_y)))
        screen.window.blit(axisFont.render("Y", True, v.black),
                 (inches_to_pixels(v.origin_x), v.screen_dimension - 20))
        
    for linkage in screen.linkages:
        linkage.render()
    for button in screen.buttons:
        button.render()
    for point in screen.points:
        point.render()
        
    leg1.render()
    py.display.update()
        
        
def create_leg1():
    linkage1 = Linkage(leg1.l1, leg1.origin_x,
                   leg1.origin_y, (m.pi/2)-leg1.theta1, v.red, screen)
    linkage2 = Linkage(leg1.l2, leg1.origin_x,
                   leg1.origin_y, (m.pi/2)-leg1.theta2, v.orange, screen)
    linkage3 = Linkage(leg1.l3, leg1.joint2_x,
                   leg1.joint2_y, (m.pi/2)-leg1.theta3, v.yellow, screen)
    linkage4 = Linkage(leg1.l4 + leg1.l5, leg1.joint3_x,
                   leg1.joint3_y, (m.pi/2)-leg1.theta4, v.blue, screen)
    linkage_hipz = Linkage(leg1.lhipz, leg1.origin_x,
                       leg1.origin_y, -leg1.thetahip, v.blue, screen, xy=False)
    linkage_hipy = Linkage(leg1.lhipy, leg1.jointhip_z,
                       leg1.jointhip_y, -leg1.thetahip + m.pi/2, v.blue, screen, xy=False)

def csv_writer_iterate_function(point):
    leg1.reassign_values(point)
    leg1.inv_kinematics()
    leg1.servo_angles()
    create_leg1()
    draw_screen()


screen = Screen(win)
leg1 = Leg(v.linkLength1, v.linkLength2, v.linkLength3,
           v.linkLength4, v.linkLength5, v.linkLengthhip, screen)

csvWriter = CsvWriter(fileWriteName, screen)

mouse = Mouse(0, 0, screen)

# Left click is for adding points for the foot
keys = py.key.get_pressed()
mouse_press = py.mouse.get_pressed()
mouse_pos = py.mouse.get_pos()

left_click = Key(0)
right_click = Key(2)
k_click = Key(py.K_k, debounceTime=10)
z_click = Key(py.K_z)
r_click = Key(py.K_r)
l_click = Key(py.K_l)
j_click = Key(py.K_j)
p_click = Key(py.K_p)
space_click = Key(py.K_SPACE)
ctrl_click = Key(py.K_LCTRL)
shift_click = Key(py.K_LSHIFT)

flip_screen = Button(10, 25, "FLIP SCREEN", True, screen)
planar_path = Button(50, 25, "Keep Path Planar", True, screen)
planar_path.color = v.green
edit_mode = Button(90, 25, 'Edit Mode', False, screen)

Point(inches_to_pixels(v.origin_x - 4),
                    v.screen_dimension - inches_to_pixels(v.origin_y + 4), inches_to_pixels(v.origin_x - 4), screen, screen.points)

run = True
test = False
while run:
    bf.initialize_screen(screen.window)

    # List of Links
    screen.linkages = []
 
    # Mouse Position
    keys = py.key.get_pressed()
    mouse_press = py.mouse.get_pressed()
    mouse_pos = py.mouse.get_pos()
    mouse.x = mouse_pos[0]
    mouse.y = mouse_pos[1]


    # First, check if any buttons are being clicked
    if left_click.clicked(mouse_press):
        mouse.check_buttons(left_click.clicked(mouse_press))
        if not mouse.onButton:
            if edit_mode.boolean:
                mouse.edit_point()
                          
            else:
                # If no buttons are being clicked, check if on the xy screen
                # If planar mode is NOT on, attach the mouse to a point and switch screens
                # Once on the other screen, the point will be constrained to the xy plane and move only in the z
                mouse.append_point(left_click, planar_path.boolean, leg1.lhipz)
 
    if mouse.holdingPoint and not edit_mode.boolean:
        mouse.point.z = mouse.x
        mouse.point.z_inches = pixels_to_inches(mouse.point.z) - v.origin_x
        screen.point_index = screen.points.index(mouse.point)
        mouse.render()
 
    # If "k" is pressed, delete all points other than original
    if k_click.clicked(keys):
        if not planar_path.boolean:
            screen.xy = not screen.xy
            screen.points = []
            screen.point_index = 0
            mouse.holdingPoint = True
            mouse.point = Point(mouse.x, mouse.y, mouse.x, screen, screen.points)
            x = mouse.x
            y = mouse.y
            mouse.previous_point_index = screen.point_index

        else:
            screen.points = []
            screen.point_index = 0
            Point(mouse.x, mouse.y, inches_to_pixels(v.origin_x + leg1.lhipz), screen, screen.points)

        k_click.refresh()

 
    # If "z" is pressed, delete previous point, and add it to deleted points list
    if z_click.clicked(keys) and len(screen.points) > 1:
        screen.points.pop(-1)
        Point(screen.points[-1].x, screen.points[-1].y, screen.points[-1].z, screen, screen.deleted_points)
        z_click.refresh()

 
    # If "r" is pressed, redraw point most previously deleted (redo)
    if r_click.clicked(keys) and len(screen.deleted_points) > 0:
        screen.points.append(screen.deleted_points[-1])
        screen.deleted_points.pop(-1)
        r_click.refresh()

 
    # If "l" is pressed, go to next point in list
    if l_click.clicked(keys):
        if screen.point_index < len(screen.points) - 1:
            screen.point_index += 1
        else:
            screen.point_index = 0
        l_click.refresh()

 
    # If "j" is pressed, go to previous point in list
    if j_click.clicked(keys):
        if screen.point_index > 0:
            screen.point_index -= 1
        else:
            screen.point_index = len(screen.points) - 1
        j_click.refresh()

 
    # If "p" is clicked, print theta values
    if p_click.clicked(keys):
        leg1.print_system()
        p_click.refresh()

   
    if space_click.clicked(keys):
        if ctrl_click.clicked(keys):
            csvWriter.append_and_write_csv(win, screen.points, leg1.return_for_csv, csv_writer_iterate_function)
            ctrl_click.refresh()
        
        if shift_click.clicked(keys):
            screen.points = []
            with open(fileReadName, 'r') as csv_read_file:
                csv_reader = csv.reader(csv_read_file)
                for line in csv_reader:
                    screen.points.append(Point(int(float(line[3])), int(float(line[4])), int(float(line[5])), screen, screen.points))

    # If the flip screen button is clicked, flip the screen from xy to yz or yz to xy
    if flip_screen.clicked(mouse.x, mouse.y, left_click.clicked(mouse_press)):
        screen.xy = not screen.xy
        left_click.refresh()
    
    # Switch path from planar to non planar or vv
    if planar_path.clicked(mouse.x, mouse.y, left_click.clicked(mouse_press)):
        planar_path.boolean = not planar_path.boolean
        planar_path.color = v.green if planar_path.boolean else v.red
        left_click.refresh()
        
    # Switch to edit mode or vv
    if edit_mode.clicked(mouse.x, mouse.y, left_click.clicked(mouse_press)):
        edit_mode.boolean = not edit_mode.boolean
        edit_mode.color = v.green if edit_mode.boolean else v.red
        left_click.refresh()
 
    # Calculate all position and force variables based on current point
    current_point = screen.points[screen.point_index]
    leg1.reassign_values(current_point)
    leg1.inv_kinematics()
    leg1.servo_angles()

    create_leg1()
    draw_screen()
 
py.quit()


