import os

data = {"file": "Book2.csv",
            "error": "Invalid JSON input."}

import os
import csv
#
# # Construct the relative path to Book1.csv from app.py
# relative_path = os.path.join(os.path.dirname(__file__), '..', 'Book1.csv')
#
# # Resolve to an absolute path (optional, but often useful)
# absolute_path = os.path.abspath(relative_path)
#
# print(absolute_path)
#
file = "hello.txt"
if os.path.exists(file):
    print("hello")
else:
    print("it doesn't exist")

try:
    with open(file) as csvfile:
        # start = csvfile.read(4096)
        #
        # if not any(char in start for char in [',', ';', '\t']):
        #     print("Not CSV")
        #
        # csvfile.seek(0)


        reader = csv.reader(csvfile, delimiter=',')

        # header = next(reader)
        # row_count = sum(1 for row in reader)
        #
        # if row_count > 0:

        # sum1 = 0
        sum = 0

        output = ""



        for row in reader:
            if row[0] == "wheat":
                sum += int(row[1])
            output += row

        print(sum)
        # else:
        #     print("Not CSV")
except Exception as e:
    print("Not CSV" + e)

    # for row in csv_reader:
    #     if row[0] == product:
    #         sum += int(row[1])
    #     with open(filename) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=',')
    #         sum = 0
    #
    #         for row in csv_reader:
    #             if row[0] == product:
    #                 sum += int(row[1])
