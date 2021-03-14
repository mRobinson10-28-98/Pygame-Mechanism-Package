import pygame as py
import math as m

import Variables as v
from Basic_Functions import pixels_to_inches
from Basic_Functions import inches_to_pixels

# x,y  are coordinate points that are determined by clicking mouse
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
            (self.x ** 2 + self.y ** 2 - self.l1 ** 2 - self.l5 ** 2) / (2 * self.l1 * self.l5))
        beta = m.atan2(self.l5 * m.sin(self.thetaRef),
                       (self.l1 + self.l5 * m.cos(self.thetaRef)))
        gamma = m.atan2(self.x, self.y)

        self.theta1 = gamma - beta
        self.theta4 = self.theta1 + self.thetaRef

        RHS = self.l3 ** 2 + self.l4 ** 2 + self.l1 ** 2 - self.l2 ** 2 - (2 * self.l4 * self.l1 * m.cos(
            self.theta4) * m.cos(self.theta1)) - (2 * self.l4 * self.l1 * m.sin(self.theta4) * m.sin(self.theta1))
        a = RHS + 2 * self.l3 * self.l1 * \
            m.cos(self.theta1) - 2 * self.l3 * self.l4 * m.cos(self.theta4)
        b = 4 * self.l3 * self.l4 * \
            m.sin(self.theta4) - 4 * self.l3 * self.l1 * m.sin(self.theta1)
        c = RHS + 2 * self.l3 * self.l4 * \
            m.cos(self.theta4) - 2 * self.l3 * self.l1 * m.cos(self.theta1)

        u1 = (-b + m.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

        self.theta3 = 2 * m.atan(u1)
        if self.theta3 <= 0:
            self.theta3 += (2 * m.pi)

        self.theta2 = m.asin((-self.l3 * m.sin(self.theta3) - self.l4 *
                              m.sin(self.theta4) + self.l1 * m.sin(self.theta1)) / self.l2)

        if (-self.l3 * m.cos(self.theta3) - self.l4 * m.cos(self.theta4) + self.l1 * m.cos(self.theta1)) / self.l2 <= 0:
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

        self.lhipy = m.sqrt(self.z ** 2 + self.y ** 2 - self.lhipz ** 2)
        self.thetahip = m.atan2(-self.y, self.z) + \
                        m.atan2(self.lhipy, self.lhipz)

    def servo_angles(self):
        if self.theta1 <= 0:
            self.theta1 = (self.theta1 + (2 * m.pi))
        elif self.theta1 >= 360:
            self.theta1 = (self.theta1 - 2 * m.pi)

        if self.theta2 <= 0:
            self.theta2 = (self.theta2 + (2 * m.pi))
        elif self.theta2 >= 360:
            self.theta2 = (self.theta2 - 2 * m.pi)

        if self.theta3 <= 0:
            self.theta3 = (self.theta3 + (2 * m.pi))
        elif self.theta3 >= 360:
            self.theta3 = (self.theta3 - 2 * m.pi)

        if self.theta4 <= 0:
            self.theta4 = (self.theta4 + (2 * m.pi))
        elif self.theta4 >= 360:
            self.theta4 = (self.theta4 - 2 * m.pi)

    def render(self, window, xyScreen):
        if xyScreen:
            py.draw.circle(window, v.black, (int(inches_to_pixels(self.joint2_x)), int(
                inches_to_pixels(self.joint2_y))), 8)
            py.draw.circle(window, v.black, (int(inches_to_pixels(self.joint3_x)), int(
                inches_to_pixels(self.joint3_y))), 8)
            py.draw.circle(window, v.black, (int(inches_to_pixels(self.joint4_x)), int(
                inches_to_pixels(self.joint4_y))), 8)
            py.draw.circle(window, v.purple, (int(inches_to_pixels(self.origin_x)), int(
                inches_to_pixels(self.origin_y))), 10)
        else:
            py.draw.circle(window, v.black, (int(inches_to_pixels(self.jointhip_z)), int(
                inches_to_pixels(self.jointhip_y))), 8)
            py.draw.circle(window, v.purple, (int(inches_to_pixels(self.origin_x)), int(
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

    def reassign_values(self, point):
        self.x = point.x_inches
        self.y = point.y_inches
        self.z = point.z_inches


    def return_for_csv(self):
        t1Csv = self.theta1
        t2Csv = self.theta2 - self.theta1
        if t2Csv <= 0:
            t2Csv += 2 * m.pi
        thCsv = self.thetahip
        return [str(m.degrees(t1Csv)), str(m.degrees(t2Csv)), str(m.degrees(thCsv)),
                               str(inches_to_pixels(self.x + v.origin_x)),
                               str(inches_to_pixels(self.y + v.origin_y)),
                               str(inches_to_pixels(self.z + v.origin_x))]

'''
    def append_for_csv(self):
        t1Csv = self.theta1
        t2Csv = self.theta2 - self.theta1
        if t2Csv <= 0:
            t2Csv += 2 * m.pi
        thCsv = self.thetahip
        print([str(m.degrees(t1Csv)), str(m.degrees(t2Csv)), str(m.degrees(thCsv))])
        self.csvThetas.append([str(m.degrees(t1Csv)), str(m.degrees(t2Csv)), str(m.degrees(thCsv)),
                               str(inches_to_pixels(self.x + v.origin_x)),
                               str(inches_to_pixels(self.y + v.origin_y)),
                               str(inches_to_pixels(self.z + v.origin_x))])

    def write_csv(self):
        print(' -   -   -   -   -   -   -   -   -   -   -   -  ')
        print(self.csvThetas)
        with open(fileWriteName, 'w', newline='') as new_file:
            thetaWriter = csv.writer(new_file, delimiter=',')
            for column in self.csvThetas:
                thetaWriter.writerow(
                    [str(column[0]), str(column[1]), str(column[2]), str(column[3]), str(column[4]),
                     str(column[5])])

    def append_and_write_csv(self):
        self.csvThetas = []
        for point in range(0, len(points)):
            bf.initialize_screen(win)
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
'''