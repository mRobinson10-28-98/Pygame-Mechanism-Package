import csv

import Keys as ks

from Point import Point

class CsvReader:
    def __init__(self, screen, filename):
        self.filename = filename
        self.screen = screen
        self.csvList = []
        self.screen.key_commanders.append(self)

    def read_and_append_csv(self):
        self.screen.points = []
        with open(self.filename, 'r') as csv_read_file:
            csv_reader = csv.reader(csv_read_file)
            for line in csv_reader:
                self.screen.points.append(
                    Point(self.screen, int(float(line[0])), int(float(line[1])), int(float(line[2])), self.screen.points))

    def check_key_commands(self, input_array):
        if ks.space_click.clicked(input_array):
            if ks.shift_click.clicked(input_array):
                self.read_and_append_csv()
                ks.shift_click.refresh()
                ks.space_click.refresh()