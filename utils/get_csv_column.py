import csv


def get_csv_column(csv_file, column_name):
    data = []
    for row in csv.DictReader(csv_file):
        data.append(row[column_name])
    return data
