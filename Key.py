import pygame as py
from Clock import Clock


class Key(Clock):
    def __init__(self, key_code, debounceTime=150):
        super(Key, self).__init__()
        self.key_code = key_code
        self.set = set
        self.debounceTime = debounceTime

    def clicked(self, set):
        if set[self.key_code] and self.passed() >= self.debounceTime:
            return True
        else:
            return False
