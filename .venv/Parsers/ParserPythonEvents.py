import sys
import requests
from bs4 import BeautifulSoup

with requests.Session() as session:
    temp = sys.stdout
    sys.stdout = open('log.txt', 'w')
    responce = session.get('https://www.python.org/', timeout=10)
    assert responce.status_code == 200, 'BAD RESPONSE'

    soup = BeautifulSoup(responce.content, 'html.parser')

    page_event = soup.select('.shrubbery')
    for i in range(1, len(page_event)+2):
        date = soup.select('.medium-widget')[1].select('time')[i-1].text
        link_event = soup.select('.medium-widget')[1].select('a')[i].get('href')
        name = soup.select('.medium-widget')[1].select('a')[i].text
        print(date)
        print(name)
        print('https://www.python.org'+ link_event)
        print()
    sys.stdout = temp
    sys.stdout.close()
