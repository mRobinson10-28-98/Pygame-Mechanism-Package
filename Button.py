import pygame as py

import Variables as v

class Button:
    def __init__(self, screen, y, height, name, boolean, color):
        py.font.init()
        self.y = y
        self.name = str(name)
        self.height = height
        self.boolean = boolean
        self.screen = screen
        self.fontSize = int(2 * self.height / 3)
        self.width = 2 * (len(self.name) * self.fontSize) / 3
        self.x = v.screen_dimension - self.width - 10
        self.color = color
        self.buttonFont = py.font.Font('freesansbold.ttf', self.fontSize)
        self.screen.buttons.append(self)

    def render(self):
        py.draw.rect(self.screen.window, v.black, (self.x, self.y, self.width, self.height))
        self.screen.window.blit(self.buttonFont.render(self.name, True, self.color),
                 (self.x + self.fontSize / 2, self.y + self.fontSize / 3))

    def clicked(self, x, y, click):
        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.height:
                if click:
                    return True
