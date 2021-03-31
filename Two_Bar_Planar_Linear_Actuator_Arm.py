import pygame as py
import math as m

import Keys as ks
import Variables as v
from Linkage import Linkage

class Arm:
    def __init__(self, screen, l1, l2, actuator1_ground, actuator2_ground, actuator1_connection, linkage2_connection):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.z = 0

        self.origin_x = self.screen.origin_x
        self.origin_y = self.screen.origin_y
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
        self.max_range = self.l1 + self.l3
        self.min_range = abs(self.l1 - self.l3)

        self.m1 = 20 / v.g
        self.m2 = 20 / v.g
        self.theta1 = 0
        self.theta2 =0
        self.thetaRef = 0
        self.phi1 = 0
        self.actuator1_length = 0
        self.actuator2_length = 0
        self.phi2 = 0

        self.linkage_joint = [0, 0]
        self.actuator1_joint = [0, 0]
        self.actuator2_joint = [0, 0]

        self.actuator2_force = 0
        self.linkage_joint_Ry = 0
        self.linkage_joint_Rx = 0
        self.actuator1_force = 0
        self.origin_Ry = 0
        self.origin_Rx = 0
        self.load = 0
        self.load_angle = 0

    def inv_kinematics(self):
        self.x = self.screen.current_point.x_inches
        self.y = self.screen.current_point.y_inches
        self.z = 0

        self.origin_x = self.screen.origin_x
        self.origin_y = self.screen.origin_y

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
        self.actuator2_joint[1] = self.linkage_joint[1] + self.linkage2_connection * m.sin(self.theta2)

        actuator1_xLength = self.actuator1_joint[0] - self.actuator1_ground[0]
        actuator1_yLength = -((self.actuator1_joint[1]) - self.actuator1_ground[1])
        self.phi1 = m.atan2(actuator1_yLength,
                               actuator1_xLength)
        self.actuator1_length = m.sqrt(actuator1_xLength ** 2 + actuator1_yLength ** 2)

        actuator2_xLength = self.actuator2_joint[0] - self.actuator2_ground[0]
        actuator2_yLength = -((self.actuator2_joint[1]) - self.actuator2_ground[1])
        self.actuator2_length = m.sqrt(actuator2_xLength ** 2 + actuator2_yLength ** 2)
        self.phi2 = m.atan2(actuator2_yLength, actuator2_xLength)

    def kinetics(self, load, angle):
        self.load = load
        self.load_angle = angle
        self.actuator2_force = (self.l3 * self.load * m.sin( self.load_angle - self.theta2)) /(self.linkage2_connection * m.sin(self.phi2 - self.theta2))
        self.linkage_joint_Ry = -self.load * m.sin(self.load_angle) - self.actuator2_force * m.sin(self.phi2) + self.m1 * v.g
        self.linkage_joint_Rx = -self.load * m.cos(self.load_angle) - self.actuator2_force * m.cos(self.phi2)
        self.actuator1_force = (self.linkage_joint_Rx * self.l1 * m.sin(self.theta2) + self.m2 * v.g * (self.l1/2) * m.cos(self.theta1) - self.linkage_joint_Ry * self.l1 * m.cos(self.theta1)) / (self.actuator1_connection * m.sin(self.phi1 - self.theta1))
        self.origin_Rx = - self.actuator1_force * m.cos(self.phi1) - self.linkage_joint_Rx
        self.origin_Ry = self.m1 * v.g - self.actuator1_force * m.sin(self.phi1) - self.linkage_joint_Ry
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
            py.draw.circle(self.screen.window, v.black, (int(self.screen.inches_to_pixels(self.actuator1_joint[0])), int(
                self.screen.inches_to_pixels(self.actuator1_joint[1]))), 8)
            py.draw.circle(self.screen.window, v.black, (int(self.screen.inches_to_pixels(self.actuator2_joint[0])), int(
                self.screen.inches_to_pixels(self.actuator2_joint[1]))), 8)
            py.draw.circle(self.screen.window, v.black, (int(self.screen.inches_to_pixels(self.linkage_joint[0])), int(
                self.screen.inches_to_pixels(self.linkage_joint[1]))), 8)
            py.draw.circle(self.screen.window, v.purple, (int(self.screen.inches_to_pixels(self.origin_x)), int(
                self.screen.inches_to_pixels(self.origin_y))), 10)
            py.draw.circle(self.screen.window, v.purple, (int(self.screen.inches_to_pixels(self.actuator1_ground[0])), int(
                self.screen.inches_to_pixels(self.actuator1_ground[1]))), 10)
            py.draw.circle(self.screen.window, v.purple, (int(self.screen.inches_to_pixels(self.actuator2_ground[0])), int(
                self.screen.inches_to_pixels(self.actuator2_ground[1]))), 10)
            py.draw.circle(self.screen.window, v.red, (int(self.screen.inches_to_pixels(self.origin_x)), int(
                self.screen.inches_to_pixels(self.origin_y))), self.screen.inches_to_pixels(self.max_range), 2)
            py.draw.circle(self.screen.window, v.red, (int(self.screen.inches_to_pixels(self.origin_x)), int(
                self.screen.inches_to_pixels(self.origin_y))), self.screen.inches_to_pixels(self.min_range), 2)

    def print_system(self):
        print('- - - - - - - - ')
        print('x: ' + str(self.x), ', y: ' + str(self.y))
        print('theta 1: ' + str(self.theta1), ', theta 2: ' + str(self.theta2))
        print('Load Force: ' + str(self.load), ', Load Angle: ' + str(self.load_angle))
        print('Rx: ' + str(self.origin_Rx), ', Ry: ' + str(self.origin_Ry))
        print('RLx: ' + str(self.linkage_joint_Rx), ', RLy: ' + str(self.linkage_joint_Ry))
        print('Actuator 1 force: ' + str(self.actuator1_force), ', Actuator 1 length: ' + str(self.actuator1_length), ', Actuator 1 angle: ' + str(self.phi1))
        print('Actuator 2 force: ' + str(self.actuator2_force), ', Actuator 2 length: ' + str(self.actuator2_length), ', Actuator 2 angle: ' + str(self.phi2))
        print('- - - - - - - - ')

    def return_for_csv(self):
        l1 = self.actuator1_length
        l2 = self.actuator2_length
        f1 = self.actuator1_force
        f2 = self.actuator2_force

        return [str(int(self.screen.inches_to_pixels(self.x + v.origin_x))),
                str(int(self.screen.inches_to_pixels(self.y + v.origin_y))),
                str(int(self.screen.inches_to_pixels(self.z + v.origin_x))),
                str(l1), str(l2), str(f1), str(f2)]

    def check_key_commands(self, input_array):
        # If "p" is clicked, print values
        if ks.p_click.clicked(input_array):
            self.print_system()
            ks.p_click.refresh()