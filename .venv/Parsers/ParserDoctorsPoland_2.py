import time
import openpyxl

import requests
from bs4 import BeautifulSoup
import json

info = []

def pars_post(url):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }

    with requests.session() as session:
        responce = session.get(url, headers=headers, timeout=10)
        assert responce.status_code == 200, 'BAD RESPONCE'

        print(responce.status_code)

        soup = BeautifulSoup(responce.text, 'html.parser')

        quantity_page = soup.select('.card.card-shadow-1.mb-1')
        for i in range(len(quantity_page)):
            try:
                name = soup.select('.card.card-shadow-1.mb-1')[i].get(
                    'data-doctor-name')
                spesialisation = soup.select('.h5.font-weight-normal.mb-0.d-inline '
                                             'span')[i].text.strip()
                link = soup.select('.card.card-shadow-1.mb-1')[i].get(
                    'data-doctor-url')
            except Exception:
                name, spesialisation, link = 'Null', 'Null', 'Null'
            try:
                address = soup.select('.m-0.d-flex.align-items-center span')[
                    i].text.strip()
            except Exception:
                address = 'Null'
            try:
                clinica = soup.select('.m-0.text-truncate.text-muted.font-weight-bold'
                                      '.address-details')[i].text.strip()
            except Exception:
                clinica = 'Null'
            print(name)
            print(clinica, '/', address)
            print(link)
            # print(data_id)
            # print(data_res_id)
            print(spesialisation)

            contact = phone_number(link)
            print(contact)
            print('-'*80)
            info.append(
                {
                    'name': name,
                    'clinic adress': clinica + '/' + address,
                    'specialization': spesialisation,
                    'contact': contact,
                    'link': link
                })
    print('PARSING GOOD!!!')
    return info

def phone_number(link):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }

    with requests.session() as session:
        responce = session.get(link, headers=headers, timeout=10)
        assert responce.status_code == 200, 'BAD RESPONCE'

        soup = BeautifulSoup(responce.text, 'html.parser')
        time.sleep(0.1)
        try:
            phone = int(soup.select('.text-muted.pl-2')[0].text.replace(' ',
                                                                '').strip())
        except Exception:
            phone = 'Null'
        return phone

def write_json(info):
    with open('D:/MyPythonFolder/MyPython/.venv/Parsers/Files'
              '/Doc_znanylekarz.json', 'a', encoding='utf-8') as file:
        json.dump(info, file, indent=4, ensure_ascii=False)

def write_excel(path):
    with open(path) as file:
        data = json.load(file)
        book = openpyxl.Workbook()

        sheet = book.active
        sheet['A1'] = 'name'.upper()
        sheet['B1'] = 'clinic adress'.upper()
        sheet['C1'] = 'specialization'.upper()
        sheet['D1'] = 'contact'.upper()
        sheet['E1'] = 'link'.upper()

        row = 2

        for info in data:
            sheet[row][0].value = info['name']
            sheet[row][1].value = info['clinic adress']
            sheet[row][2].value = info['specialization']
            sheet[row][3].value = info['contact']
            sheet[row][4].value = info['link']
            row += 1
        book.save('D:/MyPythonFolder/MyPython/.venv/Parsers/Files/Doc_znanylekarz.xlsx')
        book.close()


def main():
    tot_pages = 500
    # page = 5
    # for i in range(40, 50):
    #     print(f'WORKING ON PAGE {i}')
    #     url = f'https://www.znanylekarz.pl/szukaj?q=&loc=Warszawa&page={i}'
    #     pars_post(url)
    #     time.sleep(3)
    # print('WRITE TO FILE')
    # write_json(info)
    # time.sleep(1)
    path = 'D:/MyPythonFolder/MyPython/.venv/Parsers/Files/Doc_znanylekarz.json'
    write_excel(path)
if __name__ == '__main__':
    main()
