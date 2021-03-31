import csv

import Keys as ks

class CsvWriter:
    def __init__(self, screen, filename, object):
        self.filename = filename
        self.screen = screen
        self.object = object
        self.csvList = []
        self.screen.key_commanders.append(self)

    def append_for_csv(self, append_list):
        self.csvList.append(append_list)

    def write_csv(self):
        print(' -   -   -   -   -   -   -   -   -   -   -   -  ')
        print(self.csvList)
        with open(self.filename, 'w', newline='') as new_file:
            writer = csv.writer(new_file, delimiter=',')
            for row in self.csvList:
                writer.writerow(row)

    def append_and_write_csv(self):
        self.csvList = []
        for index in range(0, len(self.screen.points)):
            self.screen.point_index = index
            self.iterate_function()
            self.append_for_csv(self.object.return_for_csv())

        self.write_csv()

    def iterate_function(self):
        self.screen.initialize()
        self.object.inv_kinematics()
        self.object.create()
        self.screen.draw()

    def check_key_commands(self, input_array):
        if ks.space_click.clicked(input_array):
            if ks.ctrl_click.clicked(input_array):
                self.append_and_write_csv()
                ks.ctrl_click.refresh()
                ks.space_click.refresh()