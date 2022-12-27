import requests
import json
from pprint import pprint

def pars(url):

    with requests.session() as session:
        response = session.get(url)

        print(response.status_code)

        json_text = response.json()
        data = json_text.get('data')
        info = data.get('otherColorsProducts')
        # pprint(info)
        for el in range(len(info)):
            name = str(info[el].get('name')).strip()
            description = str(info[el].get('description')).replace('\n', '').strip()
            price = info[el].get('price')
            saleprice = info[el].get('salePrice')
            forlink = info[el].get('unique')
            link = f'https://megasport.ua/ua/product/{forlink}'

            print(name, price, saleprice, link)
            print(description)

        with open('Files/megasport.json', 'w', encoding='utf-8') as file:
            json.dump(json_text, file, indent=4, ensure_ascii=False)

def parsownrequest(url):
    headers = {
        'sections%5B%5D': 'kurtka-puhovik',
        'genders%5B%5D': 'male',
        'sizes%5B%5D': 'M'
    }
    with requests.session() as session:
        response = session.get(url, params=headers)

        print(response.status_code)

        json_text = response.json()
        data = json_text.get('data')
        info = data.get('otherColorsProducts')
        # pprint(info)
        for el in range(len(info)):
            try:
                competitorPrices = info[el].get('competitorPrices')
            except Exception as err:
                competitorPrices = 'Null'

            pprint(competitorPrices)
            compPr = []
            for i in competitorPrices:
                if i != []:
                    compPr.append(competitorPrices)
                    # print(competitorPrices)
            for el in compPr:
                for k, v in el.items():
                    print(k, v['price'])

def main():
    url = 'https://megasport.ua/api/filters/?sections%5B%5D=kurtka-puhovik&genders%5B%5D=male&catalog=catalog&outlet=1&offset=0&limit=60&language=ua'
    # pars(url)
    url_base = 'https://megasport.ua/api/filters/?sections%5B%5D=kurtka' \
               '-puhovik&genders%5B%5D=male&catalog=catalog&outlet=1&offset=0' \
               '&limit=60&language=ua'
    parsownrequest(url_base)

if __name__ == '__main__':
    main()
