import pygame as py
import math as m

import Keys as ks
import Variables as v

from Basic_Functions import inches_to_pixels
from Basic_Functions import pixels_to_inches
from Linkage import Linkage

class Arm:
    def __init__(self, screen, l1, l2, actuator1_ground, actuator2_ground, actuator1_connection, linkage2_connection):
        self.x = 0
        self.y = 0
        self.z = 0

        self.origin_x = v.origin_x
        self.origin_y = v.origin_y
        self.screen = screen
        self.screen.key_commanders.append(self)

        self.l1 = l1
        self.l2 = l2

        self.actuator1_ground = actuator1_ground
        self.actuator1_ground[0] += self.origin_x
        self.actuator1_ground[1] = self.origin_y - self.actuator1_ground[1]

        self.actuator2_ground = actuator2_ground
        self.actuator2_ground[0] += self.origin_x
        self.actuator2_ground[1] = self.origin_y - self.actuator2_ground[1]

        self.actuator1_connection = actuator1_connection
        self.linkage2_connection = linkage2_connection
        self.l3 = self.l2 - self.linkage2_connection

        self.theta1 = 0
        self.theta2 =0
        self.thetaRef = 0
        self.phi1 = 0
        self.actuator1_length = 0
        self.actuator2_xlength = 0
        self.actuator2_ylength =  0
        self.actuator2_length = 0
        self.phi2 = 0

        self.linkage_joint = [0, 0]
        self.actuator1_joint = [0, 0]
        self.actuator2_joint = [0, 0]

    def inv_kinematics(self):
        self.x = self.screen.current_point.x_inches
        self.y = self.screen.current_point.y_inches
        self.z = 0

        u = (self.x ** 2 + self.y ** 2 - self.l1 ** 2 - self.l3 ** 2) / (2 * self.l1 * self.l3)

        self.thetaRef = m.atan2(m.sqrt(1 - u**2), u)
        beta = m.atan2(self.l3 * m.sin(self.thetaRef),
                       (self.l1 + self.l3 * m.cos(self.thetaRef)))
        gamma = m.atan2(self.x, self.y)

        self.theta1 = gamma - beta - (m.pi / 2)
        self.theta2 = self.theta1 + self.thetaRef

        self.linkage_joint[0] = self.origin_x + self.l1 * m.cos(self.theta1)
        self.linkage_joint[1] = self.origin_y - self.l1 * m.sin(self.theta1)

        self.actuator1_joint[0] = self.origin_x + self.actuator1_connection * m.cos(self.theta1)
        self.actuator1_joint[1] = self.origin_y - self.actuator1_connection * m.sin(self.theta1)

        self.actuator2_joint[0] = self.linkage_joint[0] - self.linkage2_connection * m.cos(self.theta2)
        self.actuator2_joint[1] =(self.linkage_joint[1] + self.linkage2_connection * m.sin(self.theta2))

        actuator1_xLength = (self.actuator1_joint[0]) - self.actuator1_ground[0]
        actuator1_yLength = -((self.actuator1_joint[1]) - self.actuator1_ground[1])
        self.phi1 = m.atan2(actuator1_yLength,
                               actuator1_xLength)
        self.actuator1_length = m.sqrt(actuator1_xLength ** 2 + actuator1_yLength ** 2)

        actuator2_xLength = self.actuator2_joint[0] - self.actuator1_ground[0]
        actuator2_yLength = -((self.actuator2_joint[1]) - self.actuator2_ground[1])
        self.actuator2_length = m.sqrt(actuator2_xLength ** 2 + actuator2_yLength ** 2)
        self.phi2 = m.atan2(self.actuator2_ylength, self.actuator2_xlength)


    def kinetics(self):
        pass

    def create(self):
        self.inv_kinematics()
        self.linkage1 = Linkage(self.screen, self.l1, self.origin_x,
                                self.origin_y, -self.theta1, v.red)
        self.linkage2 = Linkage(self.screen, self.l2, self.actuator2_joint[0],
                                self.actuator2_joint[1], - self.theta2, v.yellow)
        self.actuator1 = Linkage(self.screen, self.actuator1_length, self.actuator1_ground[0],
                                self.actuator1_ground[1], - self.phi1, v.blue)
        self.actuator2 = Linkage(self.screen, self.actuator2_length, self.actuator2_ground[0],
                                self.actuator2_ground[1], - self.phi2, v.blue)


    def render(self):
        pass

    def print_system(self):
        pass

    def return_for_csv(self):
        pass

    def check_key_commands(self, input_array):
        pass