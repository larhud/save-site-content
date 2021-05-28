import argparse
import csv
import os
import requests

rows_valid = []


def write_csv(path):
    directory, extension = os.path.splitext(path)
    directory = directory + '_checked' + extension
    with open(directory, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows_valid)


def verify_url(url):
    try:
        response = requests.get(url)
        if response.ok:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


def read_csv(csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')

        # add header
        header = reader.fieldnames or []
        header.append('Validate')
        rows_valid.append(header)

        for row in reader:
            is_valid = verify_url(row['URL'])
            if is_valid:
                row['Validate'] = 'OK'
            else:
                row['Validate'] = 'ERROR'
            row_list = list(row.values())
            rows_valid.append(row_list)

    write_csv(csv_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    args = parser.parse_args()
    read_csv(args.path)
