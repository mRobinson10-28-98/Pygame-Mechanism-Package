import csv
import Basic_Functions as bf
import Keys as ks

class CsvWriter:
    def __init__(self, filename, object, screen):
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
            lengthWriter = csv.writer(new_file, delimiter=',')
            for column in self.csvList:
                lengthWriter.writerow(column)

    def append_and_write_csv(self):
        self.csvList = []
        for point in self.screen.points:
            self.iterate_function(point)
            self.append_for_csv(self.object.return_for_csv())

        self.write_csv()

    def iterate_function(self, point):
        self.screen.initialize()
        self.object.inv_kinematics(point)
        self.object.create()
        self.screen.draw()

    def check_key_commands(self, input_array):
        if ks.space_click.clicked(input_array):
            if ks.ctrl_click.clicked(input_array):
                self.append_and_write_csv()
                ks.ctrl_click.refresh()
                ks.space_click.refresh()