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


class Key(Clock):
    def __init__(self, key_code, debounceTime=150):
        super(Key, self).__init__()
        self.key_code = key_code
        self.set = set
        self.debounceTime = debounceTime

    def clicked(self, set):
        if set[self.key_code] and self.passed() >= self.debounceTime:
            return True
