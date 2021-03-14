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
 
    if xyScreen:
        win.blit(axisFont.render("X", True, v.black),
                 (v.screen_dimension - 20, inches_to_pixels(v.origin_y)))
        win.blit(axisFont.render("Y", True, v.black),
                 (inches_to_pixels(v.origin_x), v.screen_dimension - 20))
 
    else:
        win.blit(axisFont.render("Z", True, v.black),
                 (v.screen_dimension - 20, inches_to_pixels(v.origin_y)))
        win.blit(axisFont.render("Y", True, v.black),
                 (inches_to_pixels(v.origin_x), v.screen_dimension - 20))
        
    for linkage in linkages:
        linkage.render(win, xyScreen)
    for button in buttons:
        button.render(win)
    for point in points:
        point.render(win, xyScreen)
        
    leg1.render(win, xyScreen)
    py.display.update()
        
        
def create_leg1():
    linkage1 = Linkage(leg1.l1, leg1.origin_x,
                   leg1.origin_y, (m.pi/2)-leg1.theta1, v.red, linkages)
    linkage2 = Linkage(leg1.l2, leg1.origin_x,
                   leg1.origin_y, (m.pi/2)-leg1.theta2, v.orange, linkages)
    linkage3 = Linkage(leg1.l3, leg1.joint2_x,
                   leg1.joint2_y, (m.pi/2)-leg1.theta3, v.yellow, linkages)
    linkage4 = Linkage(leg1.l4 + leg1.l5, leg1.joint3_x,
                   leg1.joint3_y, (m.pi/2)-leg1.theta4, v.blue, linkages)
    linkage_hipz = Linkage(leg1.lhipz, leg1.origin_x,
                       leg1.origin_y, -leg1.thetahip, v.blue, linkages, xy=False)
    linkage_hipy = Linkage(leg1.lhipy, leg1.jointhip_z,
                       leg1.jointhip_y, -leg1.thetahip + m.pi/2, v.blue, linkages, xy=False)

def csv_writer_iterate_function(point):
    leg1.reassign_values(point)
    leg1.inv_kinematics()
    leg1.servo_angles()

 
class Button:
    def __init__(self, y, height, name):
        self.y = y
        self.name = str(name)
        self.height = height
        self.fontSize = int(2 * self.height / 3)
        self.width = 2*(len(self.name) * self.fontSize)/3
        self.x = v.screen_dimension - self.width - 10
        self.color = v.red
        self.buttonFont = py.font.Font('freesansbold.ttf', self.fontSize)
        buttons.append(self)
 
    def render(self, window):
        py.draw.rect(window, v.black, (self.x, self.y, self.width, self.height))
        win.blit(self.buttonFont.render(self.name, True, self.color),
                 (self.x + self.fontSize/2, self.y + self.fontSize/3))
 
    def clicked(self, x, y, click):
        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.height:
                if click:
                    return True
 
 
class Mouse:
    def __init__(self, x, y, point=0, holdingPoint=False):
        self.x = x
        self.y = y
        self.holdingPoint = holdingPoint
        self.point = point
 
    def modify_point(self):
        self.point.x = self.x
        self.point.y = self.y
        self.point.z = self.x
 
    def render(self):
        self.point.render(win, xyScreen)
 
 
# List of Point elements
points = []
deleted_points = []
 
# Buttons!
buttons = []
 
leg1 = Leg(v.linkLength1, v.linkLength2, v.linkLength3,
           v.linkLength4, v.linkLength5, v.linkLengthhip)

csvWriter = CsvWriter(fileWriteName)

mouse = Mouse(0, 0)

#Left click is for adding points for the foot
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

 
xyScreen = True
planarPathBoolean = True
editModeBoolean = False
 
flipScreen = Button(10, 25, "FLIP SCREEN")
planarPath = Button(50, 25, "Keep Path Planar")
planarPath.color = v.green
editMode = Button(90, 25, 'Edit Mode')
 
point_index = 0
Point(inches_to_pixels(v.origin_x - 4),
                    v.screen_dimension - inches_to_pixels(v.origin_y + 4), inches_to_pixels(v.origin_x - 4), points)
 
run = True
test = False
while run:
    bf.initialize_screen(win)

    # List of Links
    linkages = []
 
    # Mouse Position
    keys = py.key.get_pressed()
    mouse_press = py.mouse.get_pressed()
    mouse_pos = py.mouse.get_pos()
    mouse.x = mouse_pos[0]
    mouse.y = mouse_pos[1]


    # First, check if any buttons are being clicked
    if left_click.clicked(mouse_press):
        buttonBool = False
        for button in buttons:
            if button.clicked(mouse_pos[0], mouse_pos[1], left_click.clicked(mouse_press)):
                buttonBool = True
                
        if not buttonBool:
            if editModeBoolean:
                if xyScreen:
                    if not mouse.holdingPoint:
                        indexClosest = 0
                        pointClosest = 0
                        rShortest = 10000
                        for point in points:
                            r = m.sqrt((mouse.x - point.x)**2 + (mouse.y - point.y)**2)
                            if r < rShortest:
                                rShortest = r
                                indexClosest = points.index(point)
                        points.pop(indexClosest)
                        mouse.holdingPoint = True
                        left_click.refresh()
                        
                    else:
                        if planarPathBoolean:
                            points.insert(indexClosest, Point(mouse.x, mouse.y, inches_to_pixels(v.origin_x + leg1.lhipz)))
                            mouse.holdingItem = False
                            left_click.refresh()
                        else:
                            mouse.holdingItem = False
                            x = mouse.x
                            y = mouse.y
                            xyScreen = False
                            
                else:
                    points.insert(indexClosest, Point(x, y, mouse.x))
                    left_click.refresh()
                        
                          
            else:
                # If no buttons are being clicked, check if on the xy screen
                # If planar mode is NOT on, attach the mouse to a point and switch screens
                # Once on the other screen, the point will be constrained to the xy plane and move only in the z
                if xyScreen and not buttonBool:
                    if not planarPathBoolean:
                        mouse.holdingPoint = True
                        mouse.point = Point(mouse.x, mouse.y, mouse.x, points)
                        x = mouse.x
                        y = mouse.y
                        previousPointIndex = point_index
                        xyScreen = False
                        left_click.refresh()
                    else:
                        Point(mouse.x, mouse.y, inches_to_pixels(v.origin_x + leg1.lhipz), points)
                        left_click.refresh()
                
                # If you've already clicked a point in the xy plane and are not in yx plane, create a point
                elif not xyScreen and mouse.holdingPoint:
                    points.pop(-1)
                    Point(x, y, mouse.x, points)
                    mouse.holdingPoint = False
                    mouse.point = 0
                    point_index = previousPointIndex
                    xyScreen = True
                    left_click.refresh()
 
    if mouse.holdingPoint and not editModeBoolean:
        mouse.point.z = mouse.x
        mouse.point.z_inches = pixels_to_inches(mouse.point.z) - v.origin_x
        point_index = points.index(mouse.point)
        mouse.render()
 
    # If "k" is pressed, delete all points other than original
    if k_click.clicked(keys):
        if not planarPathBoolean:
            points = []
            point_index = 0
            mouse.holdingPoint = True
            mouse.point = Point(mouse.x, mouse.y, mouse.x, points)
            x = mouse.x
            y = mouse.y
            previousPointIndex = point_index
            xyScreen = False

        else:
            points = []
            point_index = 0
            Point(mouse.x, mouse.y, inches_to_pixels(v.origin_x + leg1.lhipz), points)

        k_click.refresh()

 
    # If "z" is pressed, delete previous point, and add it to deleted points list
    if z_click.clicked(keys) and len(points) > 1:
        points.pop(-1)
        Point(points[-1].x, points[-1].y, points[-1].z, deleted_points)
        z_click.refresh()

 
    # If "r" is pressed, redraw point most previously deleted (redo)
    if r_click.clicked(keys) and len(deleted_points) > 0:
        points.append(deleted_points[-1])
        deleted_points.pop(-1)
    r_click.refresh()

 
    # If "l" is pressed, go to next point in list
    if l_click.clicked(keys):
        if point_index < len(points) - 1:
            point_index += 1
        else:
            point_index = 0
        l_click.refresh()

 
    # If "j" is pressed, go to previous point in list
    if j_click.clicked(keys):
        if point_index > 0:
            point_index = point_index - 1
        else:
            point_index = len(points) - 1
        j_click.refresh()

 
    # If "p" is clicked, print theta values
    if p_click.clicked(keys):
        leg1.print_system()
        p_click.refresh()

   
    if space_click.clicked(keys):
        if ctrl_click.clicked(keys):
            csvWriter.append_and_write_csv(win, points, leg1.return_for_csv, csv_writer_iterate_function)
            ctrl_click.refresh()
        
        if shift_click.clicked(keys):
            points = []
            with open(fileReadName, 'r') as csv_read_file:
                csv_reader = csv.reader(csv_read_file)
                for line in csv_reader:
                    points.append(Point(int(float(line[3])), int(float(line[4])), int(float(line[5])), points))

    # If the flip screen button is clicked, flip the screen from xy to yz or yz to xy
    if flipScreen.clicked(mouse.x, mouse.y, left_click.clicked(mouse_press)):
        xyScreen = not xyScreen
        left_click.refresh()
    
    # Switch path from planar to non planar or vv
    if planarPath.clicked(mouse.x, mouse.y,  left_click.clicked(mouse_press)):
        planarPathBoolean = not planarPathBoolean
        planarPath.color = v.green if planarPathBoolean else v.red
        left_click.refresh()
        
    # Switch to edit mode or vv
    if editMode.clicked(mouse.x, mouse.y,  left_click.clicked(mouse_press)):
        editModeBoolean = not editModeBoolean
        editMode.color = v.green if editModeBoolean else v.red
        left_click.refresh()
 
    # Calculate all position and force variables based on current point
    current_point = points[point_index]
    leg1.x = current_point.x_inches
    leg1.y = current_point.y_inches
    leg1.z = current_point.z_inches
    leg1.inv_kinematics()
    leg1.servo_angles()

    create_leg1()
    draw_screen()
 
py.quit()


