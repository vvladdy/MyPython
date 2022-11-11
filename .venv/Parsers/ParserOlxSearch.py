import time
from queue import Queue

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class ParserOlx():

    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    TIMEOUT = 10
    pools = 2

    def __init__(self, searchprod, region):
        self.url = f"https://www.olx.ua/d/{region}/q-" + str('-'.join(
            searchprod.split(' ')))
        self.region = region
        self.queue_links = Queue()
        self.queue_single = Queue()
        self.worker = 1

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
                        # try:
                        #     price = soup.select('.css-1q7gvpp-Text')[i].text
                        # except Exception as error:
                        #     print('Цена не определена', error)
                        # print(title)
                        # print(link)

                        # print(price)

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
        urls = self.queue_single
        while urls.qsize() > 0:
            url = urls.get()
            # print(url, urls.qsize())
            with ThreadPoolExecutor(max_workers=self.worker) as tread:
                tread.submit(self._pars, url)

    def _pars(self, url):
        time.sleep(2)
        print(f'WORKING ON {url}. Remain {self.queue_single.qsize()} links')
        time.sleep(2)
        with requests.Session() as session:
            response = session.get(url,
                                   timeout=self.TIMEOUT)
            if response.status_code == 200:
                print(response.status_code)
                soup = BeautifulSoup(response.content, 'html.parser')
                try:
                    title = soup.select('.css-r9zjja-Text')[0].text
                    print(title)
                    price = soup.select('.css-okktvh-Text')[0].text
                    print(price)
                except Exception as error:
                    price = 'Договорная'
                    print('ОШИБКА', error)
                    price = 'Договорная'
                description = soup.select('.css-g5mtbi-Text')[0].text.split('\n')[
                            0].strip()
                print(description)
                user_id = soup.select('.css-sddt1v-Text')[0].text.replace(
                    'ID:', '').strip()
                print(user_id)

                url_api = f'https://www.olx.ua/api/v1/offers' \
                       f'/{user_id}/limited-phones/'

                print(url_api)
                headers = {
                    'Authorization': 'Bearer d7ef6400520b639c2faf02a3d6a15003240eb351'}
                time.sleep(5)
                phone_number = requests.get(url_api, headers=headers)
                print(phone_number.json()['data']['phones'][0])
                time.sleep(3)

    def main(self):
        self.pagination()
        self.find_links()
        self.parsing()


# задаем что ищем (часы apple) и где (область)
cat = ParserOlx('часы apple', 'ko')
cat.main()
# 'ko' - Киевская область. Все расширения в файле end_reg_olx.json

# для телефона
# 'https://www.olx.ua/api/v1/offers/770485169/limited-phones/'
# Autorization -  Bearer Token 84c0b04ccac52283bd66332dfc01fba1b18d2c9c