import json
import re
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import openpyxl

# pip install xlrd библиотека для работы с excel

info = []
translator = Translator()

searchtext = 'KOVAR'

# request = 'газовая-горелка-туристическая'
request = searchtext.replace(' ', '-')

oblast = 'ko' # url = f'https://www.olx.ua/d/{ko}/q-{request}/?page={j}'

for_filename = request.replace('-',' ')
print(for_filename)
filename = translator.translate(for_filename, dest='en').\
    text.title().replace(' ', '')
print(filename)

for j in range(1, 2):
    print('PROCESSING... page:', j)
    if j == 1:
        url = f'https://www.olx.ua/d/q-{request}'
    else:
        url = f'https://www.olx.ua/d/q-{request}/?page={j}'
    with requests.Session() as session:
        responce = session.get(url)
    assert responce.status_code == 200, 'BAD RESPONCE'

    soup = BeautifulSoup(responce.text, 'html.parser')

    for i in range(len(soup.select('.css-rc5s2u'))):
        title = soup.select('.css-ervak4-TextStyled')[i].text
        try:
            price = soup.select('.css-1667irc-TextStyled')[i].text.replace(' ', '')
            price_dig = int(re.search(r'\d*', price).group(0))
            print('PRICE.....', price_dig, price)
        except Exception as error:
            price_dig = 0
            print('No price')
        link = 'https://www.olx.ua' + soup.select('.css-rc5s2u')[
            i].get('href')
        location = soup.select('.css-1rsg3ca-TextStyled')[i].text
        # print(title, price, location)
        # print('LINK metod find_links', link)

        info.append({
            'title': title,
            'price': price_dig,
            'currency': 'uah',
            'link': link,
            'location': location
        })

with open(fr'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\{filename}.json',
          'w', encoding='utf-8') as file:
    json.dump(info, file, indent=4, ensure_ascii=False)

with open (fr'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\{filename}.json',
          'rb') as file:
    datas = json.load(file)
    filecontent = openpyxl.Workbook()

    sheet = filecontent.active

    sheet['A1'] = 'title'.upper()
    sheet['B1'] = 'Price'.upper()
    sheet['C1'] = 'currency'.upper()
    sheet['D1'] = 'location'.upper()
    sheet['E1'] = 'link'.upper()

    row = 2
    for info in datas:
        sheet[row][0].value = info['title']
        sheet[row][1].value = info['price']
        sheet[row][2].value = info['currency']
        sheet[row][3].value = info['location']
        sheet[row][4].value = info['link']
        row += 1
    filecontent.save(fr'D:\MyPythonFolder\MyPython\.venv\Parsers\Files\{filename}.xlsx')
    filecontent.close()
