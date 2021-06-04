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
    if not url:
        print("URL NULA")
        return 'NULA'

    try:
        response = requests.get(url, timeout=10, allow_redirects=False)
        if response.status_code == 200:
            return 'OK'
        elif response.status_code == 302 or response.status_code == 301:
            return 'REDIRECT'
        else:
            return 'ERROR'
    except Exception as error:
        print(error)
        return 'ERROR'


def read_csv(csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')

        # add header
        header = reader.fieldnames or []
        header.append('Validate')
        rows_valid.append(header)

        for row in reader:
            url = row.get('URL')
            print(f"Verificando URL {url}...")
            status = verify_url(url)
            print(status)
            row['Validate'] = status

            row_list = list(row.values())
            rows_valid.append(row_list)

    write_csv(csv_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    args = parser.parse_args()
    read_csv(args.path)
