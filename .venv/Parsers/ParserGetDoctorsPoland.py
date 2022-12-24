import time
from pprint import pprint

import openpyxl
import requests
import json


def pars_quant_pages():
    API = 'https://znajdzfizjoterapeute.pl/api/search/getadvancedsearchresult'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }

    raw = {
        "SelectedDiseases": [],
        "SelectedTherapies": [],
        "CriteriaInputValue": "",
        "PlaceInputValue":
            {
                "name": "Warszawa",
                "administrativeArea": "mazowieckie",
                "id": "VwBhAHIAcwB6AGEAdwBhAA==",
                "useOnlyViewportForSearch": 'false',
                "location":
                    {"lat": 52.2296756, "lng": 21.0122287},
                "viewport":
                    {"northeast":
                         {"lat": 52.3679992, "lng": 21.2710984},
                     "southwest":
                         {"lat": 52.0978767, "lng": 20.8512898}
                     }
            },
        "CurrentPage": 1,
        "SortOrder": -1
    }

    response_text = requests.post(API, json=raw, headers=headers,
                                  timeout=10)
    print(response_text.status_code)

    response_json = response_text.json()

    pages = response_json['Value']['TotalPageCount']

    return pages


def pars_post(url):
    info = []
    if url.split('/')[-1] == 'warszawa':
        print('OK')
    API = 'https://znajdzfizjoterapeute.pl/api/search/getadvancedsearchresult'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }

    pages = pars_quant_pages()
    print(pages)
    # pages = 2
    for j in range(1, pages):
        print(f'WORKING ON........ PAGE: {j}')
        raw = {
            "SelectedDiseases": [],
            "SelectedTherapies": [],
            "CriteriaInputValue": "",
            "PlaceInputValue":
                {
                    "name":"Warszawa",
                    "administrativeArea":"mazowieckie",
                    "id":"VwBhAHIAcwB6AGEAdwBhAA==",
                    "useOnlyViewportForSearch":'false',
                "location":
                    {"lat": 52.2296756, "lng": 21.0122287},
                "viewport":
                    {"northeast":
                         {"lat": 52.3679992, "lng": 21.2710984},
                    "southwest":
                         {"lat": 52.0978767, "lng": 20.8512898}
                    }
                },
            "CurrentPage": f'{j}',
            "SortOrder": -1
        }
        # requests.post(url, data={key: value}, json={key: value}, args)
        # data - dictionary, json - json objects
        response_text = requests.post(API, json=raw, headers=headers, timeout=10)
        print(response_text.status_code)

        response_json = response_text.json()

        all_info = response_json['Value']['Result']
        # pprint(all_info)

        for i in range(len(all_info)):
            first_name = response_json['Value']['Result'][i]['BasicInfo'][
                'FirstName']
            last_name = response_json['Value']['Result'][i]['BasicInfo'][
                'LastName']
            id = response_json['Value']['Result'][i]['BasicInfo'][
                'Id']
            specialization = response_json['Value']['Result'][i]['BasicInfo'][
                'Specialization']
            time.sleep(0.3)
            clinics = all_info[i]['Clinics']
            clinic_addres = []
            for i in range(len(clinics)):
                address = clinics[i]['FullAddress']
                if address:
                    clinic_addres.append(address)
                    print('CLINIC ADRESS', address)
            print('DOCTOR', first_name, last_name, specialization, id)

            time.sleep(1)
            contact = phone_number(id)
            print('CONTACT_INFO', contact)
            link = f'https://znajdzfizjoterapeute.pl/fizjoterapeuta/{id}'
            print('LINK', link)
            print('-'*50)
            time.sleep(0.5)

            info.append(
                {
                    'name': (first_name, last_name),
                    'clinic adress': clinic_addres,
                    'specialization': specialization,
                    'contact': contact,
                    'link': link
                })
    print('RARSING GOOD!!! Write to file')
    write_json(info)

def phone_number(id):
    # id = 6747
    url = f'https://znajdzfizjoterapeute.pl/api/physiotherapist' \
          f'/getphysiotherapistsprofile?physiotherapistId={id}'
    response_text = requests.get(url, timeout=10)
    json_text = response_text.json()
    # print(response_text.status_code)
    # pprint(json_text['Value'])
    phone = []
    for i in range(len(json_text['Value']['Clinics'])):
        phone.append(str(json_text['Value']['Clinics'][i]['Phone']).replace(' ',''))
    try:
        email = json_text['Value']['PhysiotherapistInfo']['Email']
    except Exception:
        email = 'Null'
    return (', '.join(phone).strip(', '), email)


def write_json(info):
    with open('D:/MyPythonFolder/MyPython/.venv/Parsers/Files'
              '/Doc_znajdzfizjoterapeute.json', 'w', encoding='utf-8') as file:
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
        book.save('D:/MyPythonFolder/MyPython/.venv/Parsers/Files/Doc_znajdzfizjoterapeute.xlsx')
        book.close()

def main():
    url = 'https://znajdzfizjoterapeute.pl/szukaj/warszawa'
    path = 'D:/MyPythonFolder/MyPython/.venv/Parsers/Files/Doc_znajdzfizjoterapeute.json'
    # pars_quant_pages()
    # pars_post(url)
    # print(phone_number(6747))
    write_excel(path)
if __name__ == '__main__':
    main()
