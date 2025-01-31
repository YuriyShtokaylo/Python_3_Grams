import csv
from typing import List
from constants import RESOURCE, RESULT
from functions import analyze, parse, generate_result


def export_to_csv(data: List, filename: str):
    """
    This procedure generate csv file
    args:
       data - data we want to export
       filename - filename of file where we want to store data
    """
    with open(filename, mode='w', newline='', encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "3-gram 1", "3-gram  2", "3-gram  3", "3-gram  4", "3-gram  5"])
        writer.writerow([])
        for row in data:
            writer.writerow(row)


def app(file_to_read: str = RESOURCE, file_to_write: str = RESULT):
    """
    This procedure prepare and run our code
    args:
       file_to_read - filename of our input file (if nothing is provided we take it from constants as default value)
       file_to_write - filename of our output file (if nothing is provided we take it from constants as default value)
    """
    data = generate_result(analyze(parse(file_to_read)))
    export_to_csv(data, file_to_write)
