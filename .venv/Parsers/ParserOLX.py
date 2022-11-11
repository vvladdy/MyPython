import queue

import requests
from bs4 import BeautifulSoup
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

class ParserOlx():

    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    TIMEOUT = 10
    pools = 2

    def __init__(self, url):
        self.url = url
        self.queue = Queue()


    def _check_connection(self, url):
        with requests.Session() as session:
            response = session.get(url, headers=self.HEADERS,
                                   timeout=self.TIMEOUT)
            if response.status_code == 200:
                print(response.status_code)
                return response.text
            else:
                print('BAD RESPONSE')


    def parser_categories(self):
        context = self._check_connection(self.url)

        self.category = []

        soup = BeautifulSoup(context, 'html.parser')

        links_cat = soup.select('.item a')
        for i in range(len(links_cat)):
            link_cat = links_cat[i].get('href').replace('uk', 'd')
            cat_name = links_cat[i].text.strip()
            self.category.append((cat_name, link_cat))

        promo_url = 'https://categories.olxcdn.com/promo' \
                    '/categories/active?brand=olxua&lang=ru'
        promo_info = requests.get(promo_url).json()
        promo_cat_link = promo_info[0]['link']['url']
        promo_cat_name = promo_info[0]['name']

        self.category.append((promo_cat_name, promo_cat_link))
        print(self.category)
        return self.category

    def parser_subcategories(self):
        context = self._check_connection(self.url)

        self.sub_category = []

        soup = BeautifulSoup(context, 'html.parser')

        info_all = soup.select('.subcategories-list ul li a')
        for j in range(len(info_all)):
            name_cat_single = info_all[j].text.strip()
            links_cat_single = info_all[j].get('href')
            self.sub_category.append((name_cat_single, links_cat_single))
        print(self.sub_category)
        return self.sub_category

    def make_queue_single_url_category(self):
        urls_link = self.parser_categories()
        for link in urls_link:
            cat_link = link[1]
            # print(cat_link)
            self.queue.put(link[1])
        return (self.queue, self.queue.qsize())

    def make_queue_single_url_subcategory(self):
        urls_link = self.parser_subcategories()
        for link in urls_link:
            cat_link = link[1]
            self.queue.put(link[1])
        return (self.queue, self.queue.qsize())

    def parsing_thread_category(self):
        queue = self.make_queue_single_url_category()[0]
        with ThreadPoolExecutor(max_workers=self.pools) as executor:
            for i in range(self.pools):
                executor.submit(self._parsing_categories, queue)

    def _parsing_categories(self, queue):
        work_list = []
        while queue.qsize() > 0:
            link = queue.get()
            # print(f'WORKING ON {link}. Remain {queue.qsize()} links')
            work_list.append(link)

        for i in work_list:
            url = i
            resp = requests.get(url)
            print(url)
            content = resp.content
            soup = BeautifulSoup(content, 'html.parser')
            quant_page = soup.select('.css-1mi714g')[-1].text
            print('Страниц', quant_page)


    def main(self):
        # self.parser_categories()
        # self.parser_subcategories()
        # self.make_queue_single_url_category()
        self.parsing_thread_category()


cat = ParserOlx('https://www.olx.ua/')
cat.main()


# для телефона
# 'https://www.olx.ua/api/v1/offers/770485169/limited-phones/'
# Autorization -  Bearer Token 84c0b04ccac52283bd66332dfc01fba1b18d2c9c