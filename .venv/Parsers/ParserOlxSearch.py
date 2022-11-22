import time
from queue import Queue
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import FakeUserAgent
import MyInfo
import pickle
import re

class ParserOlx():

    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    TIMEOUT = 10
    pools = 2

    def __init__(self, region, searchprod=None, categor=None):
        if searchprod == None:
            self.url = f'https://www.olx.ua/d/{categor}/{region}'
            # self.url = f'https://www.olx.ua/d/detskiy-mir/{region}'
        else:
            self.url = f"https://www.olx.ua/d/{region}/q-" + str('-'.join(
                searchprod.split(' ')))
        self.region = region
        self.queue_links = Queue()
        self.queue_single = Queue()
        self.worker = 1

    def _authorization(self, user_id_for_req):
        print('START AUTORIZATION')
        # url = 'https://www.olx.ua/account/'
        # fake = FakeUserAgent()
        # user_ag = fake.random
        # print(user_ag)
        #
        # headers = {
        #     "user-agent": f'{user_ag}'
        #     #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        #     #"AppleWebKit/537.36 (KHTML, like Gecko)
        #     # Chrome/106.0.0.0 Safari/537.36"
        # }
        #
        # login = MyInfo.LOGIN_olx
        # pasword = MyInfo.PASSWORD_olx
        #
        # datas = {
        #     'login[email_phone]': login,
        #     'login[password]': pasword
        # }
        # session = requests.Session()
        # authorisation = session.post(url, headers=headers, data=datas)
        # print(authorisation.status_code)
        #
        #
        # pickle.dump(session.cookies,
        #             open('olx_auth.cookies', 'wb'))
        #
        #
        # cokies_dict = [
        #     {
        #         'domain': key.domain,
        #         'name': key.name,
        #         'path': key.path,
        #         'value': key.value
        #     }
        #     for key in session.cookies
        # ]
        #
        session2 = requests.Session()
        # for cookies in cokies_dict:
        #     session2.cookies.set(**cookies)

        # токен авторизации выдается раз в сутки
        Bearer = '9108cad153c019682289924dd23918db45bde654'
        headers = {
            'Authorization': f'Bearer {Bearer}'
        }
        time.sleep(1)

        responce_tel = session2.get(f'https://www.olx.ua/api/v1/offers'
                                    f'/{user_id_for_req}/limited-phones/',
                                    headers=headers)
        time.sleep(1)

        tel_numb = responce_tel.json()
        try:
            phone_numb = tel_numb['data']['phones'][0]
            return phone_numb
        except Exception as er:
            phone_numb = None
            print('NO Phone-Number', er)
            return phone_numb

    def find_links(self):
        urls = self.pagination()
        while urls.qsize() > 0:
            url = urls.get()
            # print(url, urls.qsize())
            with requests.Session() as session:
                response = session.get(url,
                                       timeout=self.TIMEOUT)
                if response.status_code == 200:
                    print(response.status_code)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    for i in range(len(soup.select('.css-rc5s2u'))):
                        try:
                            title = soup.select('.css-1pvd0aj-Text')[i].text
                        except Exception:
                            continue
                        link = 'https://www.olx.ua' + soup.select('.css-rc5s2u')[
                            i].get('href')
                        self.queue_single.put(link)

    def pagination(self):
        url = self.url
        print(self.url)
        with requests.Session() as session:
            response = session.get(url, timeout=self.TIMEOUT)
        assert response.status_code == 200, 'BAD RESPONSE'
        soup = BeautifulSoup(response.content, 'html.parser')
        pages = int(soup.select('.css-1mi714g')[-1].text.strip())
        print('Страниц', pages)
        pages = 2
        for i in range(1, pages+1):
            urls = self.url + f'/?page={i}'
            # print(urls)
            self.queue_links.put(urls)
        return self.queue_links

    def parsing(self):
        print(self.url)
        urls = self.queue_single
        while urls.qsize() > 0:
            url = urls.get()
            # print(url, urls.qsize())
            with ThreadPoolExecutor(max_workers=self.worker) as tread:
                for i in range(self.worker):
                    tread.submit(self._pars, url)

    def _pars(self, url):
        # time.sleep(2)
        print(f'WORKING ON {url}. Remain {self.queue_single.qsize()} links')

        options = webdriver.ChromeOptions()
        options.headless = True

        driver_service = Service(
            executable_path='c:/Users/User/PycharmProjects/chromedriver.exe'
        )

        driver = webdriver.Chrome(options=options, service=driver_service,
            executable_path='c:/Users/User/PycharmProjects/chromedriver.exe')

        token_new_variant = []
        driver.implicitly_wait(1)
        try:
            driver.get(url)
            print(driver.title)
            cookies_str = driver.get_cookies()
            for i in range(5):
                token_new_variant.append(cookies_str[i]['value'])
        except Exception as erro:
            print(erro)
        finally:
            driver.close()
            driver.quit()

        for i in token_new_variant:
            regex_all_new = re.search(r'[a-z0-9]{40}', str(i))
            if regex_all_new:
                self.token_new = regex_all_new.group(0)

        Bearer = self.token_new
        print(Bearer)
        headers = {
            'Authorization': f'Bearer {Bearer}'
        }

        #be9ba423c8272d23a267fd7f42169b99d0a31c6e
        #fbeedfd2fbc7d8742a099bc0918f7441d3fb5d7c
        #038269f4b8ac242df528cd989cec5848e48dc9e2

        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        try:
            user_id = soup.select('.css-ogllc8 a')[0].get('href')
            user = re.search(r'\d{3,}', str(user_id))
            user_id_for_req = user[0]
            # print(user_id)
            print('USER', user[0])
        except Exception as error:
            user_id_for_req = self._other_request_id(url)
            time.sleep(2)
            print('No ID', error)
        try:
            user_name = soup.select('.css-1fp4ipz h4')[0].text.strip()
        except Exception as error:
            user_name = 'Unknown'
            print('UnnameUser', error)
        time.sleep(3)
        responce = requests.get(
            f'https://www.olx.ua/api/v1/targeting/data/?page=ad'
            f'&params%5Bad_id%5D={user_id_for_req}',
            headers=headers)

        # time.sleep(3)
        responce_tel = requests.get(f'https://www.olx.ua/api/v1/offers'
                                    f'/{user_id_for_req}/limited-phones/',
                                    headers=headers)
        # time.sleep(5)
        json_info = responce.json()
        tel_numb = responce_tel.json()
        ad_id = json_info['data']['targeting']['ad_id']

        ad_title = json_info['data']['targeting']['ad_title']
        try:
            ad_price = json_info['data']['targeting']['ad_price']
            ad_currency = json_info['data']['targeting']['currency']
        except Exception as err:
            ad_price = None
            ad_currency = None
            print('NO PRICE', err)
        try:
            phone_numb = tel_numb['data']['phones'][0]
        except Exception as er:
            phone_numb = self._authorization(user_id_for_req)
            # phone_numb = None
            print('NO Phone-Number', er)

        city = json_info['data']['targeting']['city']
        # pprint(json_info)
        print(str(ad_title).title(), ad_price, ad_currency)
        print(ad_id, user_name, phone_numb, city)

    def _other_request_id(self, url):
        with requests.Session() as session:
            response = session.get(url,
                                   timeout=self.TIMEOUT)
            if response.status_code == 200:
                print(response.status_code)
                soup = BeautifulSoup(response.content, 'html.parser')
                time.sleep(1)
                user_id = soup.select('.css-sddt1v-Text')[0].text.replace(
                    'ID:', '').strip()
                print(user_id)
                return user_id

    def main(self):
        self.pagination()
        self.find_links()
        self.parsing()


# categor плохо работает, так есть подкатегории
# задаем: область, категорию categor и\или что ищем searchprod(часы apple)
cat = ParserOlx( 'ko', searchprod='детская обувь')
cat.main()
