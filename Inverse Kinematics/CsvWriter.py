import csv
import Basic_Functions as bf

class CsvWriter:
    def __init__(self, filename):
        self.filename = filename
        self.csvList = []

    def append_for_csv(self, append_list):
        self.csvList.append(append_list)

    def write_csv(self):
        print(' -   -   -   -   -   -   -   -   -   -   -   -  ')
        print(self.csvList)
        with open(self.filename, 'w', newline='') as new_file:
            lengthWriter = csv.writer(new_file, delimiter=',')
            for column in self.csvList:
                lengthWriter.writerow(column)

    def append_and_write_csv(self, window, iterate_list, append_list, iterate_function):
        self.csvList = []
        for object in iterate_list:
            bf.initialize_screen(window)
            iterate_function(object)
            self.append_for_csv(append_list())

        self.write_csv()