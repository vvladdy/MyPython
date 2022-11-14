import re
import time
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import pickle
from fake_useragent import FakeUserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



#url = 'https://www.olx.ua/d/obyavlenie/shnekoviy-pogruzchik-133-159
# -transportergvintoviy-konver-shnek-zerna-IDMfJdo.html'
url = 'https://www.olx.ua/d/obyavlenie/besplatnoe-zhile-pitanie-i-zarplata-IDPGoun.html'
fake = FakeUserAgent()

user_agent = fake.random

print(user_agent)

headers = {
    'user-agent': f'{user_agent}'
}

options = webdriver.ChromeOptions()
options.headless = True

driver_service = Service(
    executable_path='c:/Users/User/PycharmProjects/chromedriver.exe'
)

driver = webdriver.Chrome(options=options, service=driver_service,
            executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')

driver.implicitly_wait(4)
token_new_variant = []

try:
    driver.get(url)
    print(driver.title)

    pickle.dump(driver.get_cookies(), open('cookies_new.txt', 'wb'))

    # cookies_str = driver.get_cookies()
    # pprint(cookies_str)
    # # # "'value': '214d82308a67dc3e3ac13acc4b0b7b9f998e5a04'}"
    # for i in range(5):
    #     token_new_variant.append(cookies_str[i]['value'])
    #
    # print("TOKEN from str", token_new_variant[1])

except Exception as erro:
    print(erro)
finally:
    driver.close()
    driver.quit()


with open('cookies_new.txt', 'rb') as file:
    d_new = file.read()
    # print(d)
    regex_all_new = re.findall(r'[a-z0-9]{40}', str(d_new))
    token_new = regex_all_new[0]
    print('Bearer', token_new)


    #'471799559fbe258d00db00a432dfc88994365222'
    #'20f0c4cdb34d5c73fe44d10a58d4ac2835f76f2a'
    # '20973d53de6c85517b19cc636f0e9e942385481e'

Bearer = token_new
# Bearer = token_new_variant[1]
headers = {
    'Authorization':f'Bearer {Bearer}'
}

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
print(url)

user_id = soup.select('.css-ogllc8 a')[0].get('href')
user = re.search(r'\d{3,}',str(user_id))
user_id_for_req = user[0]
print(user_id)
print('USER',user[0])


responce = requests.get(f'https://www.olx.ua/api/v1/targeting/data/?page=ad'
                        f'&params%5Bad_id%5D={user_id_for_req}',
                        headers=headers)

responce_tel = requests.get(f'https://www.olx.ua/api/v1/offers'
                        f'/{user_id_for_req}/limited-phones/', headers=headers)
time.sleep(5)
json_info = responce.json()
tel_numb = responce_tel.json()
ad_id = json_info['data']['targeting']['ad_id']
ad_title = json_info['data']['targeting']['ad_title']
ad_price = json_info['data']['targeting']['ad_price']
ad_currency = json_info['data']['targeting']['currency']
phone_numb = tel_numb['data']['phones'][0]
city = json_info['data']['targeting']['city']


# pprint(json_info)
print(str(ad_title).title(), ad_price, ad_currency)
print(ad_id, phone_numb, city)




#
# resp = requests.get(url)
# soup = BeautifulSoup(resp.text, 'html.parser')
# print(url)
#
# user_id = soup.select('.css-ogllc8 a')[0].get('href')
# user = re.search(r'\d{3,}',str(user_id))
# print(user_id)
# print('USER',user[0])