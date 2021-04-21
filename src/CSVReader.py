import csv

'''
CSV reader class. 
'''
class CSVReader:

    def __init__(self):
        pass

    """
    Returns list of file names.
    Reads from csv file with name combined with 'group' and <x> placed in <directory>.
    """
    @staticmethod
    def read_group(directory, x):
        file = directory + 'group' + str(x) + '.csv'

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
