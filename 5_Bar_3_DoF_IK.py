import pygame as py
import math as m
import csv


fileWriteName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
fileReadName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
 
# Initiated pygame
py.init()
 
# Time delay sets delay in each loop in millis
time_delay = 100
 
# Sets screen width and height in pixels
screen_dimension = 800
 
# Screen width and height in inches for math
screen_dimension_inches = 24
 
# Defines window
win = py.display.set_mode((screen_dimension, screen_dimension))
 
# Title
py.display.set_caption('Inverse Kinematics')
 
# Screen multiplier
multiplier = 2
 
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
 
# Mechanism origin in screen (for visuals only)
origin_x = screen_dimension_inches / 2
origin_y = screen_dimension_inches / 4
 
# Colors
red = (255, 10, 92)
orange = (255, 95, 10)
yellow = (255, 180, 0)
green = (25, 100, 25)
blue = (0, 200, 250)
purple = (100, 10, 100)
gray = (50, 50, 50)
white = (255, 255, 255)
black = (10, 10, 10)
 
# Converts length from pixels to inches (usually for kinematic analysis)
def pixels_to_inches(pixels):
    return (pixels * screen_dimension_inches) / screen_dimension
 
# Converts length from inches to pixels (usually for display purposes)
def inches_to_pixels(inches):
    return (inches * screen_dimension) / screen_dimension_inches
 
# Created grid for reference
 
 
def draw_screen():
    py.draw.line(win, gray, (inches_to_pixels(origin_x-screen_dimension_inches/2), inches_to_pixels(origin_y)),
                 (inches_to_pixels(origin_x+screen_dimension_inches/2), inches_to_pixels(origin_y)))
    py.draw.line(win, gray, (inches_to_pixels(origin_x), inches_to_pixels(origin_y-screen_dimension_inches/2)),
                 (inches_to_pixels(origin_x), inches_to_pixels(origin_y+screen_dimension_inches)))
    axisFont = py.font.Font('freesansbold.ttf', 20)
 
    if xyScreen:
        win.blit(axisFont.render("X", True, black),
                 (screen_dimension - 20, inches_to_pixels(origin_y)))
        win.blit(axisFont.render("Y", True, black),
                 (inches_to_pixels(origin_x), screen_dimension - 20))
 
    else:
        win.blit(axisFont.render("Z", True, black),
                 (screen_dimension - 20, inches_to_pixels(origin_y)))
        win.blit(axisFont.render("Y", True, black),
                 (inches_to_pixels(origin_x), screen_dimension - 20))
        
    for linkage in linkages:
        linkage.render()
    for button in buttons:
        button.render()
    for point in points:
        point.render()
        
    leg1.render()
    py.display.update()
        
        
def create_leg1():
    linkage1 = Linkage(leg1.l1, leg1.origin_x,
                   leg1.origin_y, (m.pi/2)-leg1.theta1, red, leg1)
    linkage2 = Linkage(leg1.l2, leg1.origin_x,
                   leg1.origin_y, (m.pi/2)-leg1.theta2, orange, leg1)
    linkage3 = Linkage(leg1.l3, leg1.joint2_x,
                   leg1.joint2_y, (m.pi/2)-leg1.theta3, yellow, leg1)
    linkage4 = Linkage(leg1.l4 + leg1.l5, leg1.joint3_x,
                   leg1.joint3_y, (m.pi/2)-leg1.theta4, blue, leg1)
    linkage_hipz = Linkage(leg1.lhipz, leg1.origin_x,
                       leg1.origin_y, -leg1.thetahip, blue, leg1, xy=False)
    linkage_hipy = Linkage(leg1.lhipy, leg1.jointhip_z,
                       leg1.jointhip_y, -leg1.thetahip + m.pi/2, blue, leg1, xy=False)
    
def initialize_screen():
    py.time.delay(time_delay)
    win.fill((255, 255, 255))
 
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
            

# Point class defines the position of a point for inverse kinematics
class Point:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.color = red
        self.radius = 3
        self.x_inches = pixels_to_inches(self.x) - origin_x
        self.y_inches = pixels_to_inches(self.y) - origin_y
        self.z_inches = pixels_to_inches(self.z) - origin_x
        points.append(self)
 
    def render(self):
        if xyScreen:
            py.draw.circle(win, self.color, (self.x, self.y), self.radius)
        else:
            py.draw.circle(win, self.color, (self.z, self.y), self.radius)
 
# x,y are coordinate points that are determined by clicking mouse
# x,y coordinates are converted to inches in Point class before defined in Leg class
# All Leg parameters in inches
# All Angles referenced from y-axis +CCW
 
 
class Leg:
    def __init__(self, l1, l2, l3, l4, l5, lhipz):
        self.origin_x = origin_x
        self.origin_y = origin_y
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
            py.draw.circle(win, black, (int(inches_to_pixels(self.joint2_x)), int(
                inches_to_pixels(self.joint2_y))), 8)
            py.draw.circle(win, black, (int(inches_to_pixels(self.joint3_x)), int(
                inches_to_pixels(self.joint3_y))), 8)
            py.draw.circle(win, black, (int(inches_to_pixels(self.joint4_x)), int(
                inches_to_pixels(self.joint4_y))), 8)
            py.draw.circle(win, purple, (int(inches_to_pixels(self.origin_x)), int(
                inches_to_pixels(self.origin_y))), 10)
        else:
            py.draw.circle(win, black, (int(inches_to_pixels(self.jointhip_z)), int(
                inches_to_pixels(self.jointhip_y))), 8)
            py.draw.circle(win, purple, (int(inches_to_pixels(self.origin_x)), int(
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
                               str(inches_to_pixels(self.x + origin_x)), str(inches_to_pixels(self.y + origin_y)), str(inches_to_pixels(self.z + origin_x))])
        
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
         
 
# All Linkage parameters input in iches, then converted in __init__ to pixels
class Linkage:
    def __init__(self, length, x1, y1, theta, color, leg, xy=True):
        self.x1 = inches_to_pixels(x1)
        self.y1 = inches_to_pixels(y1)
        self.length = inches_to_pixels(length)
        self.theta = theta
        self.x2 = self.x1 + self.length * m.cos((self.theta))
        self.y2 = self.y1 + self.length * m.sin((self.theta))
        self.color = color
        self.xyPlane = True
        self.xy = xy
        linkages.append(self)
 
    def render(self):
        if self.xy == xyScreen:
            py.draw.line(win, self.color, (self.x1, self.y1),
                         (self.x2, self.y2), 12)
 
 
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
        self.x = screen_dimension - self.width - 10
        self.color = red
        self.buttonFont = py.font.Font('freesansbold.ttf', self.fontSize)
        buttons.append(self)
 
    def render(self):
        py.draw.rect(win, black, (self.x, self.y, self.width, self.height))
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
 
leg1 = Leg(linkLength1, linkLength2, linkLength3,
           linkLength4, linkLength5, linkLengthhip)
 
mouse = Mouse(0, 0)

#Left click is for adding points for the foot
left_click = Key(mouse_left_click, 250)
right_click = Key(mouse_right_click)
k_click = Key(keys[py.K_k])
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
planarPath.color = green
editMode = Button(90, 25, 'Edit Mode')
 
point_index = 0
Point(inches_to_pixels(origin_x - 4),
                    screen_dimension - inches_to_pixels(origin_y + 4), inches_to_pixels(origin_x - 4))
 
run = True
test = False
while run:
    initialize_screen()
    
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
                            points.insert(indexClosest, Point(mouse.x, mouse.y, inches_to_pixels(origin_x + leg1.lhipz)))
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
                        mouse.point = Point(mouse.x, mouse.y, mouse.x)
                        x = mouse.x
                        y = mouse.y
                        previousPointIndex = point_index
                        xyScreen = False
                    else:
                        Point(mouse.x, mouse.y, inches_to_pixels(origin_x + leg1.lhipz))
                
                # If you've already clicked a point in the xy plane and are not in yx plane, create a point
                elif not xyScreen and mouse.holdingPoint:
                    points.pop(-1)
                    Point(x, y, mouse.x)
                    mouse.holdingPoint = False
                    mouse.point = 0
                    point_index = previousPointIndex
                    xyScreen = True
 
    if mouse.holdingPoint and not editModeBoolean:
        mouse.point.z = mouse.x
        mouse.point.z_inches = pixels_to_inches(mouse.point.z) - origin_x
        point_index = points.index(mouse.point)
        mouse.render()
 
    # If "k" is pressed, delete all points other than original
    if k_click.clicked():
        if not planarPathBoolean:
            points = []
            point_index = 0
            mouse.holdingPoint = True
            mouse.point = Point(mouse.x, mouse.y, mouse.x)
            x = mouse.x
            y = mouse.y
            previousPointIndex = point_index
            xyScreen = False
            k_click.refresh()
        else:
            points = []
            point_index = 0
            Point(mouse.x, mouse.y, inches_to_pixels(origin_x + leg1.lhipz))
            k_click.refresh()
 
    # If "z" is pressed, delete previous point, and add it to deleted points list
    if z_click.clicked():
        points.pop(-1)
        deleted_points.append(Point(points[-1].x, points[-1].y, points[-1].z))
        points.pop(-1)
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
                    points.append(Point(int(float(line[3])), int(float(line[4])), int(float(line[5]))))
                
            shift_click.refresh()
        space_click.refresh()
   
 
    # If the flip screen button is clicked, flip the screen from xy to yz or yz to xy
    if flipScreen.isclick(mouse_pos[0], mouse_pos[1], mouse_left_click) and left_click.passed() >= 250:
        xyScreen = bool(m.fmod(int(xyScreen)+1, 2))
        left_click.refresh()
    
    # Switch path from planar to non planar or vv
    if planarPath.isclick(mouse_pos[0], mouse_pos[1], mouse_left_click) and left_click.passed() >= 250:
        planarPathBoolean = bool(m.fmod(int(planarPathBoolean)+1, 2))
        planarPath.color = green if planarPathBoolean else red
        left_click.refresh()
        
    # Switch to edit mode or vv
    if editMode.isclick(mouse_pos[0], mouse_pos[1], mouse_left_click) and left_click.passed() >= 250:
        editModeBoolean = bool(m.fmod(int(editModeBoolean)+1, 2))
        editMode.color = green if editModeBoolean else red
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


