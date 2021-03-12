import pygame as py
import math as m
import csv

import Variables as v
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels
from Point import Point
from Linkage import Linkage



fileWriteName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
fileReadName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
 
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
        button.render()
    for point in points:
        point.render(win, xyScreen)
        
    leg1.render()
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
    
def initialize_screen():
    py.time.delay(v.time_delay)
    win.fill((255, 255, 255))
 
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
 
# x,y are coordinate points that are determined by clicking mouse
# x,y coordinates are converted to inches in Point class before defined in Leg class
# All Leg parameters in inches
# All Angles referenced from y-axis +CCW
 
 
class Leg:
    def __init__(self, l1, l2, l3, l4, l5, lhipz):
        self.origin_x = v.origin_x
        self.origin_y = v.origin_y
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        self.l5 = l5
        self.lhipz = lhipz
        
        self.x = 0
        self.y = 0
        self.z = 0
        self.csvCoord = []
        
        self.lhipy = 0
        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0
        self.theta4 = 0
        self.thetahip = 0
        self.csvThetas = []
        
        self.thetaRef = 0
        self.angles = [self.theta1, self.theta2, self.theta3, self.theta4]
 
        self.joint2_x = self.origin_x + self.l2 * m.sin(self.theta2)
        self.joint2_y = self.origin_y + self.l2 * m.cos(self.theta2)
 
        self.joint3_x = self.origin_x + self.l2 * \
            m.sin(self.theta2) + self.l3 * m.sin(self.theta3)
        self.joint3_y = self.origin_y + self.l2 * \
            m.cos(self.theta2) + self.l3 * m.cos(self.theta3)
 
        self.joint4_x = self.origin_x + self.l1 * m.sin(self.theta1)
        self.joint4_y = self.origin_y + self.l1 * m.cos(self.theta1)
 
        self.jointhip_z = self.origin_x + self.lhipz * m.cos(self.thetahip)
        self.jointhip_y = self.origin_y - self.lhipz * m.sin(self.thetahip)
 
    def inv_kinematics(self):
        self.thetaRef = m.acos(
            (self.x**2 + self.y**2 - self.l1**2 - self.l5**2) / (2 * self.l1 * self.l5))
        beta = m.atan2(self.l5 * m.sin(self.thetaRef),
                       (self.l1 + self.l5 * m.cos(self.thetaRef)))
        gamma = m.atan2(self.x, self.y)
 
        self.theta1 = gamma - beta
        self.theta4 = self.theta1 + self.thetaRef
 
        RHS = self.l3**2 + self.l4**2 + self.l1**2 - self.l2**2 - (2 * self.l4 * self.l1 * m.cos(
            self.theta4) * m.cos(self.theta1)) - (2 * self.l4 * self.l1 * m.sin(self.theta4) * m.sin(self.theta1))
        a = RHS + 2 * self.l3 * self.l1 * \
            m.cos(self.theta1) - 2 * self.l3 * self.l4 * m.cos(self.theta4)
        b = 4 * self.l3 * self.l4 *\
            m.sin(self.theta4) - 4 * self.l3 * self.l1 * m.sin(self.theta1)
        c = RHS + 2 * self.l3 * self.l4 *\
            m.cos(self.theta4) - 2 * self.l3 * self.l1 * m.cos(self.theta1)
 
        u1 = (-b + m.sqrt(b**2 - 4 * a * c)) / (2 * a)
 
        self.theta3 = 2 * m.atan(u1)
        if self.theta3 <= 0:
            self.theta3 += (2*m.pi)
 
        self.theta2 = m.asin((-self.l3 * m.sin(self.theta3) - self.l4 *
                              m.sin(self.theta4) + self.l1 * m.sin(self.theta1))/self.l2)
 
        if (-self.l3 * m.cos(self.theta3) - self.l4 * m.cos(self.theta4) + self.l1 * m.cos(self.theta1))/self.l2 <= 0:
            self.theta2 = m.pi - self.theta2
 
        self.joint2_x = self.origin_x + self.l2 * m.sin(self.theta2)
        self.joint2_y = self.origin_y + self.l2 * m.cos(self.theta2)
 
        self.joint3_x = self.origin_x + self.l2 * \
            m.sin(self.theta2) + self.l3 * m.sin(self.theta3)
        self.joint3_y = self.origin_y + self.l2 * \
            m.cos(self.theta2) + self.l3 * m.cos(self.theta3)
 
        self.joint4_x = self.origin_x + self.l1 * m.sin(self.theta1)
        self.joint4_y = self.origin_y + self.l1 * m.cos(self.theta1)
 
        self.jointhip_z = self.origin_x + self.lhipz * m.cos(self.thetahip)
        self.jointhip_y = self.origin_y - self.lhipz * m.sin(self.thetahip)
 
        self.lhipy = m.sqrt(self.z**2 + self.y**2 - self.lhipz**2)
        self.thetahip = m.atan2(-self.y, self.z) + \
            m.atan2(self.lhipy, self.lhipz)
 
 
    def servo_angles(self):
        if self.theta1 <= 0:
            self.theta1 = (self.theta1+(2*m.pi))
        elif self.theta1 >= 360:
            self.theta1 = (self.theta1 - 2*m.pi)
 
        if self.theta2 <= 0:
            self.theta2 = (self.theta2+(2*m.pi))
        elif self.theta2 >= 360:
            self.theta2 = (self.theta2 - 2*m.pi)
 
        if self.theta3 <= 0:
            self.theta3 = (self.theta3+(2*m.pi))
        elif self.theta3 >= 360:
            self.theta3 = (self.theta3 - 2*m.pi)
 
        if self.theta4 <= 0:
            self.theta4 = (self.theta4+(2*m.pi))
        elif self.theta4 >= 360:
            self.theta4 = (self.theta4 - 2*m.pi)
 
    def render(self):
        if xyScreen:
            py.draw.circle(win, v.black, (int(inches_to_pixels(self.joint2_x)), int(
                inches_to_pixels(self.joint2_y))), 8)
            py.draw.circle(win, v.black, (int(inches_to_pixels(self.joint3_x)), int(
                inches_to_pixels(self.joint3_y))), 8)
            py.draw.circle(win, v.black, (int(inches_to_pixels(self.joint4_x)), int(
                inches_to_pixels(self.joint4_y))), 8)
            py.draw.circle(win, v.purple, (int(inches_to_pixels(self.origin_x)), int(
                inches_to_pixels(self.origin_y))), 10)
        else:
            py.draw.circle(win, v.black, (int(inches_to_pixels(self.jointhip_z)), int(
                inches_to_pixels(self.jointhip_y))), 8)
            py.draw.circle(win, v.purple, (int(inches_to_pixels(self.origin_x)), int(
                inches_to_pixels(self.origin_y))), 10)
 
    def print_system(self):
        print('Theta1: ' + str(m.degrees(self.theta1)))
        print('Theta2: ' + str(m.degrees(self.theta1 - self.theta2)))
        print('ThetaHip: ' + str(m.degrees(self.thetahip)))

#         if self.theta1 - self.theta2 <= 0:
#             print(m.degrees(
#                 2*m.pi + self.theta1-self.theta2))
#         else:
#             print(m.degrees(self.theta1-self.theta2))
        print('                             ')
    
    def append_for_csv(self):
        t1Csv = self.theta1
        t2Csv = self.theta2 - self.theta1
        if t2Csv <= 0:
            t2Csv += 2*m.pi 
        thCsv = self.thetahip
        print([str(m.degrees(t1Csv)), str(m.degrees(t2Csv)), str(m.degrees(thCsv))])
        self.csvThetas.append([str(m.degrees(t1Csv)), str(m.degrees(t2Csv)), str(m.degrees(thCsv)),
                               str(inches_to_pixels(self.x + v.origin_x)), str(inches_to_pixels(self.y + v.origin_y)), str(inches_to_pixels(self.z + v.origin_x))])
        
    def write_csv(self):
        print(' -   -   -   -   -   -   -   -   -   -   -   -  ')
        print(self.csvThetas)
        with open(fileWriteName, 'w', newline = '') as new_file:
            thetaWriter = csv.writer(new_file, delimiter = ',')
            for column in self.csvThetas:
                thetaWriter.writerow([str(column[0]), str(column[1]), str(column[2]), str(column[3]), str(column[4]), str(column[5])])
                
    def append_and_write_csv(self):
        self.csvThetas = []
        for point in range(0, len(points)):
            initialize_screen()
            linkages = []
            current_point = points[point]
            self.x = current_point.x_inches
            self.y = current_point.y_inches
            self.inv_kinematics()
            self.servo_angles()
            self.append_for_csv()
            create_leg1()
            draw_screen()
            
        self.write_csv()
 
 
class Clock:
    def __init__(self, time=0):
        self.time = time
        self.previous = False
        self.current = False
 
    def refresh(self):
        self.time = py.time.get_ticks()
 
    def passed(self):
        return py.time.get_ticks() - self.time
 
 
class Key(Clock):
    def __init__(self, input, debounceTime = 150):
        super(Key, self).__init__()
        self.input = input
        self.debounceTime = debounceTime
 
    def update(self, bttn):
        self.input = bttn
 
    def clicked(self):
        if self.input and self.passed() >= self.debounceTime:
            return True
 
 
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
 
    def render(self):
        py.draw.rect(win, v.black, (self.x, self.y, self.width, self.height))
        win.blit(self.buttonFont.render(self.name, True, self.color),
                 (self.x + self.fontSize/2, self.y + self.fontSize/3))
 
    def isclick(self, x, y, click):
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
        self.point.render()
 
 
# List of Point elements
points = []
deleted_points = []
 
# Buttons!
buttons = []
 
 
keys = py.key.get_pressed()
mouse_pos = py.mouse.get_pos()
mouse_press = py.mouse.get_pressed()
mouse_left_click = 0
mouse_right_click = 0
 
leg1 = Leg(v.linkLength1, v.linkLength2, v.linkLength3,
           v.linkLength4, v.linkLength5, v.linkLengthhip)
 
mouse = Mouse(0, 0)

#Left click is for adding points for the foot
left_click = Key(mouse_left_click, 250)
right_click = Key(mouse_right_click)
k_click = Key(keys[py.K_k])
k_click.debounceTime = 10
z_click = Key(keys[py.K_z])
r_click = Key(keys[py.K_r])
l_click = Key(keys[py.K_l])
j_click = Key(keys[py.K_j])
p_click = Key(keys[py.K_p])
space_click = Key(keys[py.K_SPACE])
ctrl_click = Key(keys[py.K_LCTRL])
shift_click = Key(keys[py.K_LSHIFT])

 
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
    initialize_screen()
    print(py.time.get_ticks())
    # List of Links
    linkages = []
 
    # User inputs for pygame
    keys = py.key.get_pressed()
    mouse_pos = py.mouse.get_pos()
    mouse_press = py.mouse.get_pressed()
    mouse_left_click = mouse_press[0]
    mouse_right_click = mouse_press[2]
 
    mouse.x = mouse_pos[0]
    mouse.y = mouse_pos[1]
    left_click.input = mouse_left_click
    right_click.input = mouse_right_click
    k_click.input = keys[py.K_k]
    z_click.input = keys[py.K_z]
    r_click.input = keys[py.K_r]
    l_click.input = keys[py.K_l]
    j_click.input = keys[py.K_j]
    p_click.input = keys[py.K_p]
    space_click.input = keys[py.K_SPACE]
    ctrl_click.input = keys[py.K_LCTRL]
    shift_click.input = keys[py.K_LSHIFT]
    
    # First, check if any buttons are being clicked
    if left_click.clicked():
        buttonBool = False
        for button in buttons:
            if button.isclick(mouse_pos[0], mouse_pos[1], mouse_left_click):
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
                    else:
                        Point(mouse.x, mouse.y, inches_to_pixels(v.origin_x + leg1.lhipz), points)
                
                # If you've already clicked a point in the xy plane and are not in yx plane, create a point
                elif not xyScreen and mouse.holdingPoint:
                    points.pop(-1)
                    Point(x, y, mouse.x, points)
                    mouse.holdingPoint = False
                    mouse.point = 0
                    point_index = previousPointIndex
                    xyScreen = True
 
    if mouse.holdingPoint and not editModeBoolean:
        mouse.point.z = mouse.x
        mouse.point.z_inches = pixels_to_inches(mouse.point.z) - v.origin_x
        point_index = points.index(mouse.point)
        mouse.render()
 
    # If "k" is pressed, delete all points other than original
    if k_click.clicked():
        if not planarPathBoolean:
            points = []
            point_index = 0
            mouse.holdingPoint = True
            mouse.point = Point(mouse.x, mouse.y, mouse.x, points)
            x = mouse.x
            y = mouse.y
            previousPointIndex = point_index
            xyScreen = False
            k_click.refresh()
        else:
            points = []
            point_index = 0
            Point(mouse.x, mouse.y, inches_to_pixels(v.origin_x + leg1.lhipz), points)
            k_click.refresh()
 
    # If "z" is pressed, delete previous point, and add it to deleted points list
    if z_click.clicked():
        points.pop(-1)
        Point(points[-1].x, points[-1].y, points[-1].z, deleted_points)
        z_click.refresh()
 
    # If "r" is pressed, redraw point most previously deleted (redo)
    if r_click.clicked():
        if len(deleted_points) > 0:
            points.append(deleted_points[-1])
            deleted_points.pop(-1)
        r_click.refresh()
 
    # If "l" is pressed, go to next point in list
    if l_click.clicked():
        if point_index < len(points) - 1:
            point_index += 1
        else:
            point_index = 0
        l_click.refresh()
 
    # If "j" is pressed, go to previous point in list
    if j_click.clicked():
        if point_index > 0:
            point_index = point_index - 1
        else:
            point_index = len(points) - 1
        j_click.refresh()
 
    # If "p" is clicked, print theta values
    if p_click.clicked():
        leg1.print_system()
        p_click.refresh()
   
    if space_click.clicked():
        if ctrl_click.clicked():
            leg1.append_and_write_csv()
            ctrl_click.refresh()
        
        if shift_click.clicked():
            points = []
            with open(fileReadName, 'r') as csv_read_file:
                csv_reader = csv.reader(csv_read_file)
                for line in csv_reader:
                    points.append(Point(int(float(line[3])), int(float(line[4])), int(float(line[5])), points))
                
            shift_click.refresh()
        space_click.refresh()
   
 
    # If the flip screen button is clicked, flip the screen from xy to yz or yz to xy
    if flipScreen.isclick(mouse_pos[0], mouse_pos[1], mouse_left_click) and left_click.passed() >= 250:
        xyScreen = bool(m.fmod(int(xyScreen)+1, 2))
        left_click.refresh()
    
    # Switch path from planar to non planar or vv
    if planarPath.isclick(mouse_pos[0], mouse_pos[1], mouse_left_click) and left_click.passed() >= 250:
        planarPathBoolean = bool(m.fmod(int(planarPathBoolean)+1, 2))
        planarPath.color = v.green if planarPathBoolean else v.red
        left_click.refresh()
        
    # Switch to edit mode or vv
    if editMode.isclick(mouse_pos[0], mouse_pos[1], mouse_left_click) and left_click.passed() >= 250:
        editModeBoolean = bool(m.fmod(int(editModeBoolean)+1, 2))
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


