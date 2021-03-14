import pygame as py

class Clock:
    def __init__(self, time=0):
        self.time = time
        self.previous = False
        self.current = False

    def refresh(self):
        self.time = py.time.get_ticks()

    def passed(self):
        return py.time.get_ticks() - self.time