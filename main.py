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
    script = '''
    display dialog "Cases {} -> {}" with title "NU COVID-19" buttons {{"Open Site", "Dismiss"}} 
    set the button_pressed to the button returned of the result
    if the button_pressed is "Open Site" then
        open location "https://www.northwestern.edu/coronavirus-covid-19-updates/developments/confirmed-cases.html"
    end if
    '''.format(last_cases, new_cases)
    os.system("osascript -e '{}'".format(script))


if __name__ == "__main__":
    last_cases = None
    while True:
        new_cases = cases()
        print(new_cases)
        if last_cases and last_cases != new_cases:
            notify(last_cases, new_cases)

        last_cases = new_cases
        time.sleep(60 * 10)
