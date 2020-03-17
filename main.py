from bs4 import BeautifulSoup
import requests
import time
import os


def cases() -> int:
    url = 'https://www.northwestern.edu/coronavirus-covid-19-updates/developments/confirmed-cases.html'
    request = requests.get(url, headers={'Cache-Control': 'no-cache'})

    soup = BeautifulSoup(request.text, features="html.parser")
    table_body = soup.find_all("table")[0].find('tbody')
    row_text = table_body.find_all('tr')[-1].text.strip()

    return int(row_text.replace('Total cases\n', ''))


def notify(last_cases: int, new_cases: int):
    os.system("""
              osascript -e 'display dialog "{}" with title "{}" buttons {{"Ok"}}'
              """.format('Cases {} -> {}'.format(last_cases, new_cases), 'NU COVID-19'))


if __name__ == "__main__":
    last_cases = None
    while True:
        new_cases = cases()
        print(new_cases)
        if last_cases and last_cases != new_cases:
            notify(last_cases, new_cases)

        last_cases = new_cases
        time.sleep(60 * 10)
