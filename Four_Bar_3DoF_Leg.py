import pygame as py
import math as m

import Keys as ks
import Variables as v
from Linkage import Linkage


# x,y  are coordinate points that are determined by clicking mouse
# x,y coordinates are converted to inches in Point class before defined in Leg class
# All Leg parameters in inches
# All Angles referenced from y-axis +CCW

class Leg:
    def __init__(self, screen, l1, l2, l3, l4, l5, lhipz):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        self.l5 = l5
        self.lhipz = lhipz

        self.screen = screen
        self.screen.key_commanders.append(self)

        self.max_range = self.l1 + self.l5
        self.min_range = abs(self.l1 - self.l5)

        self.origin_x = self.screen.origin_x
        self.origin_y = self.screen.origin_y

        self.x = 0
        self.y = 0
        self.z = 0

        self.lhipy = 0
        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0
        self.theta4 = 0
        self.thetahip = 0

        self.thetaRef = 0
        self.angles = [self.theta1, self.theta2, self.theta3, self.theta4]

        self.joint2 = [self.origin_x + self.l2 * m.sin(self.theta2), self.origin_y + self.l2 * m.cos(self.theta2)]

        self.joint3 = [self.origin_x + self.l2 * m.sin(self.theta2) + self.l3 * m.sin(self.theta3),
                       self.origin_y + self.l2 * m.cos(self.theta2) + self.l3 * m.cos(self.theta3)]

        self.joint4 = [self.origin_x + self.l1 * m.sin(self.theta1), self.origin_y + self.l1 * m.cos(self.theta1)]

        self.jointhip = [self.origin_x + self.lhipz * m.cos(self.thetahip),
                         self.origin_y - self.lhipz * m.sin(self.thetahip)]

        self.linkage1 = Linkage(self.screen, self.l1, self.origin_x,
                                self.origin_y, (m.pi / 2) - self.theta1, v.red)
        self.linkage2 = Linkage(self.screen, self.l2, self.origin_x,
                                self.origin_y, (m.pi / 2) - self.theta2, v.orange)
        self.linkage3 = Linkage(self.screen, self.l3, self.joint2[0],
                                self.joint2[1], (m.pi / 2) - self.theta3, v.yellow)
        self.linkage4 = Linkage(self.screen, self.l4 + self.l5, self.joint3[0],
                                self.joint3[1], (m.pi / 2) - self.theta4, v.blue)
        self.linkage_hipz = Linkage(self.screen, self.lhipz, self.origin_x,
                                    self.origin_y, -self.thetahip, v.blue, xy=False)
        self.linkage_hipy = Linkage(self.screen, self.lhipy, self.jointhip[0],
                                    self.jointhip[1], -self.thetahip + m.pi / 2, v.blue, xy=False)

    def inv_kinematics(self):
        self.x = self.screen.current_point.x_inches
        self.y = self.screen.current_point.y_inches
        self.z = self.screen.current_point.z_inches
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

        self.joint2[0] = self.origin_x + self.l2 * m.sin(self.theta2)
        self.joint2[1] = self.origin_y + self.l2 * m.cos(self.theta2)

        self.joint3[0] = self.origin_x + self.l2 * \
                        m.sin(self.theta2) + self.l3 * m.sin(self.theta3)
        self.joint3[1] = self.origin_y + self.l2 * \
                        m.cos(self.theta2) + self.l3 * m.cos(self.theta3)

        self.joint4[0] = self.origin_x + self.l1 * m.sin(self.theta1)
        self.joint4[1]= self.origin_y + self.l1 * m.cos(self.theta1)

        self.jointhip[0] = self.origin_x + self.lhipz * m.cos(self.thetahip)
        self.jointhip[1]= self.origin_y - self.lhipz * m.sin(self.thetahip)

        self.lhipy = m.sqrt(self.z ** 2 + self.y ** 2 - self.lhipz ** 2)
        self.thetahip = m.atan2(-self.y, self.z) + \
                        m.atan2(self.lhipy, self.lhipz)

    def create(self):
        self.inv_kinematics()
        self.linkage1 = Linkage(self.screen, self.l1, self.origin_x,
                                self.origin_y, (m.pi / 2) - self.theta1, v.red)
        self.linkage2 = Linkage(self.screen, self.l2, self.origin_x,
                                self.origin_y, (m.pi / 2) - self.theta2, v.orange)
        self.linkage3 = Linkage(self.screen, self.l3, self.joint2[0],
                                self.joint2[1], (m.pi / 2) - self.theta3, v.yellow)
        self.linkage4 = Linkage(self.screen, self.l4 + self.l5, self.joint3[0],
                                self.joint3[1], (m.pi / 2) - self.theta4, v.blue)
        self.linkage_hipz = Linkage(self.screen, self.lhipz, self.origin_x,
                                    self.origin_y, -self.thetahip, v.blue, xy=False)
        self.linkage_hipy = Linkage(self.screen, self.lhipy, self.jointhip[0],
                                    self.jointhip[1], -self.thetahip + m.pi / 2, v.blue, xy=False)

    def render(self):
        if self.screen.xy:
            py.draw.circle(self.screen.window, v.black, (int(self.screen.inches_to_pixels(self.joint2[0])), int(
                self.screen.inches_to_pixels(self.joint2[1]))), 8)
            py.draw.circle(self.screen.window, v.black, (int(self.screen.inches_to_pixels(self.joint3[0])), int(
                self.screen.inches_to_pixels(self.joint3[1]))), 8)
            py.draw.circle(self.screen.window, v.black, (int(self.screen.inches_to_pixels(self.joint4[0])), int(
                self.screen.inches_to_pixels(self.joint4[1]))), 8)
            py.draw.circle(self.screen.window, v.purple, (int(self.screen.inches_to_pixels(self.origin_x)), int(
                self.screen.inches_to_pixels(self.origin_y))), 10)
            py.draw.circle(self.screen.window, v.red, (int(self.screen.inches_to_pixels(self.origin_x)), int(
                self.screen.inches_to_pixels(self.origin_y))), int(self.screen.inches_to_pixels(self.max_range)), 2)
            py.draw.circle(self.screen.window, v.red, (int(self.screen.inches_to_pixels(self.origin_x)), int(
                self.screen.inches_to_pixels(self.origin_y))), int(self.screen.inches_to_pixels(self.min_range)), 2)
        else:
            py.draw.circle(self.screen.window, v.black, (int(self.screen.inches_to_pixels(self.jointhip[0])), int(
                self.screen.inches_to_pixels(self.jointhip[1]))), 8)
            py.draw.circle(self.screen.window, v.purple, (int(self.screen.inches_to_pixels(self.origin_x)), int(
                self.screen.inches_to_pixels(self.origin_y))), 10)

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


    def return_for_csv(self):
        t1Csv = m.degrees(self.theta1)
        t2Csv = m.degrees(self.theta2 - self.theta1)
        thCsv = m.degrees(self.thetahip) +1

        if t1Csv <= 0:
            t1Csv += 360
        elif t1Csv >= 360:
            t1Csv -= 360

        if t2Csv <= 0:
            t2Csv += 360
        elif t2Csv >= 360:
            t2Csv -= 360

        if thCsv <= -180:
            thCsv += 360
        elif thCsv >= 180:
            thCsv -= 360

        return [str(int(self.screen.inches_to_pixels(self.x + self.origin_x))),
                               str(int(self.screen.inches_to_pixels(self.y + self.origin_y))),
                               str(int(self.screen.inches_to_pixels(self.z + self.origin_x))),
                str(int(t1Csv)), str(int(t2Csv)), str(int(thCsv))]

    def check_key_commands(self, input_array):
        # If "p" is clicked, print theta values
        if ks.p_click.clicked(input_array):
            self.print_system()
            ks.p_click.refresh()
