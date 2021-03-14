import Basic_Functions as bf
import Variables as v

class Screen:
    def __init__(self, window):
        self.window = window
        self.xy = True
        self.points = []
        self.linkages = []
        self.deleted_points = []
        self.buttons = []
        self.point_index = 0