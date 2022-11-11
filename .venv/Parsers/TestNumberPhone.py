import json
from pprint import pprint

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

url = f'https://www.olx.ua/api/v1/offers/{756641483}/limited-phones/'

user_agent = UserAgent()

Bearer = 'f2ca5b11f5158675bbb7c77a0dde91b6f27bd46d'

# 'Bearer d7ef6400520b639c2faf02a3d6a15003240eb351'

# Токены нужно обновлять. Как это сделать в автомате не знаю

userag = user_agent.random
print(userag)

headers = {
    'Authorization':f'Bearer {Bearer}'
}

# phone_number = requests.get(url, headers=headers)
# print(phone_number.json()['data']['phones'][0])
#
# with requests.Session() as session:
#     work_url = 'https://www.olx.ua/d/obyavlenie/apple-watch-4-44mm-IDQbCq7.html'
#     response = requests.get(work_url)
#     if response.status_code == 200:
#         print(response.status_code)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         try:
#             title = soup.select('.css-r9zjja-Text')[0].text
#             price = soup.select('.css-okktvh-Text')[0].text
#         except Exception as error:
#             print('ОШИБКА')
#             price = 'Договорная'
#         description = soup.select('.css-g5mtbi-Text')[0].text.split('\n')[
#             0].strip()
#         # user_id = soup.select('.css-sddt1v-Text')[0].text.replace('ID:', '').strip()
#         # print(title, price)
#         # print(description)
#         # print(int(user_id))

##########################################################################
# # все объявления пользователя
# url = f'https://www.olx.ua/api/v1/users/{194637158}'
# headers = {
#     'Authorization':'Bearer f2ca5b11f5158675bbb7c77a0dde91b6f27bd46d'
# }
# info = requests.get(url, headers=headers)
# print(info.json())
##########################################################################

url_regions = 'https://www.olx.ua/api/v1/offers/metadata/search/?offset=0&limit=40&category_id=1944&filter_refiners=spell_checker&facets=%5B%7B%22field%22%3A%22region%22%2C%22fetchLabel%22%3Atrue%2C%22fetchUrl%22%3Atrue%2C%22limit%22%3A30%7D%5D'
headers = {
    'Authorization':f'Bearer {Bearer}'
}
info = requests.get(url_regions, headers=headers)
# pprint(info.json())
end_reg = info.json()['data']['facets']['region']
pprint(end_reg)
# print(len(end_reg))

for_json = []
for el in range(0, len(end_reg)):
    region = end_reg[el]
    end = end_reg[el]['url'].split('/')[-1]
    print(region['label'], end)
    for_json.append(
        {
            'name': region['label'],
            'end': end
         }
    )

with open('end_reg_olx.json', 'w', encoding='utf-8') as file:
    json.dump(for_json, file, indent=4, ensure_ascii=False)
