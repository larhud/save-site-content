import argparse
import json
import csv
import os
import time

from selenium import webdriver

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdf')

os.makedirs(BASE_DIR, exist_ok=True)


def configure_driver():
    chrome_options = webdriver.ChromeOptions()

    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
             'savefile.default_directory': BASE_DIR,
             }

    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(executable_path='webdrive/chromedriver', chrome_options=chrome_options)
    driver.set_page_load_timeout(10)

    return driver


def print_page(driver, **kwargs):
    if kwargs.get('url') and kwargs.get('id'):
        print(f"Abrindo página da URL: {kwargs.get('url')}...")
        driver.get(kwargs.get('url'))
        print('Salvando PDF...')
        driver.execute_script(f"document.title ='{kwargs.get('id')}'")
        driver.execute_script('window.print();')
        print('PDF salvo com sucesso.')


def read_csv(path):
    driver = configure_driver()

    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if row['Validate'] == 'OK':
                print_page(driver, url=row['URL'], id=row['ID'])
                time.sleep(5)

    driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    args = parser.parse_args()
    read_csv(args.path)
