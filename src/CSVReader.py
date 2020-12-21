import csv

from PathProvider import PathProvider


class CSVReader:

    def __init__(self):
        pass

    # returns list of file names
    @staticmethod
    def read_group(x):
        file = ''
        if x == 1:
            file = PathProvider.group1_csv
        elif x == 2:
            file = PathProvider.group2_csv
        elif x == 3:
            file = PathProvider.group3_csv

        column1, column2 = [], []
        with open(file, newline='') as csv_file:
            data = csv.reader(csv_file)
            header = True
            for row in data:
                if header:
                    header = False
                    continue

                column1.append(row[0])
                column2.append(row[1])

        return column1
