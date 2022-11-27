#https://www.machineseeker.com/
import time

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from googletrans import Translator
import sqlite3
from sqlite3 import Error


class MachineSeeker:

    datapath = 'Macheneseeker.db'

    def __init__(self, url):
        self.url = url
        self.cat_queue = Queue()


    def pars_categories(self):
        #'https://www.machineseeker.com/#kategorien'
        url = self.url+'#kategorien'
        with requests.Session() as session:
            responce = session.get(url)
        assert responce.status_code == 200, 'BAD RESPONSE'
        print(responce.status_code)

        soup = BeautifulSoup(responce.text, 'html.parser')

        categories = soup.select('.text-dark')
        for cat in range(17, len(categories)):
            self.cat_queue.put('https://www.machineseeker.com'+categories[
                cat].get('href'))
            name = categories[cat].text.strip()
            name_rus = self._translator(categories[cat].text.strip())
            link = 'https://www.machineseeker.com'+categories[cat].get('href')
            print(name_rus+'/' + name)
            print(link)
            self.fill_categories_table(name, name_rus, link)
       # return self.cat_queue

    def querries_url_from_db(self):
        connection = self.create_db()
        cursor = connection.cursor()
        querry_1 = """
            SELECT id, link
            FROM categories
        """
        cursor.execute(querry_1)
        self.info_cat_id_link = cursor.fetchall()
        # для теста нескольких категорий 3-х например
        # self.info_cat_id_link = cursor.fetchmany(3)
        print(self.info_cat_id_link)
        return self.info_cat_id_link

    def pars_single_cat(self):
        count = 0
        self.create_subcategory_table()
        for i in self.info_cat_id_link:
            id = i[0]
            count += 1
            url = i[1]
            print('ID=', id, f'REMAINE: {41-count} page')
            print(f'WORKING WITH: {url}')
            with requests.Session() as session:
                responce = session.get(url)
            assert responce.status_code == 200, 'BAD RESPONSE'
            print(responce.status_code)

            soup = BeautifulSoup(responce.text, 'html.parser')
            try:
                categories = soup.select('.list-group-flush a')
                for cat in range(len(categories)):
                    name = categories[cat].select('.col')[0].text.strip()
                    name_rus = self._translator(name)
                    print(name_rus + ' / ' + name)
                    link = 'https://www.machineseeker.com' + categories[cat].get('href')
                    print(link)
                    self.fill_subcategory_table(name, name_rus, link, id)
            except Exception as error:
                print('НЕТ ПОДКАТЕГОРИЙ', error)

    def parsing_pages_and_links(self, querry_name=None):
        self.link_list = []

        if querry_name:
            self.querry_link_for_product(querry_name)
            list_links = self.info_subcat_id_link
        else:
            self.querries_url_from_db()
            list_links = self.info_cat_id_link

        #self.querries_url_from_db() # запрос из таблицы категорий
        #self.querry_link_for_product('Tractors') #запрос из таблицы
        # подкатегорий

        for i in list_links:
            url = i[1]
            cat_id = i[0]
            # url = 'https://www.machineseeker.com/Agricultural-machinery/ci-4'
            print('UUUUUUURRRRRRLLLLLL', url)
            with requests.Session() as session:
                responce = session.get(url, timeout=10)

            assert responce.status_code == 200, 'Bad response'

            soup = BeautifulSoup(responce.text, 'html.parser')

            try:
                pages = int(soup.select('.page-link')[-2].text.strip())
                print('pages:', pages)
            except Exception as error:
                pages = 1
                print('NOT PAGES', error)

            #pages = 1 # для тестирования одной страницы

            for page in range(1, pages+1):
                url_p = f'{url}?page={page}'
                print(f'WORKING WITH PAGE {page}. TOTAL {pages+1}')
                resp = requests.get(url_p, timeout=10)
                print(resp.status_code, url_p)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.content, 'html.parser')
                links = soup.findAll('a', class_='d-flex')
                for i in range(len(links)):
                    link = 'https://www.machineseeker.com' + str(links[i].get(
                        'href'))
                    # print(link)
                    id = link.split('/')[-1].replace('i-', '')
                    # print(id)
                    self.link_list.append((link, id, cat_id))
            print(self.link_list)
        return self.link_list

    def product(self):
        self.create_product_table()
        time.sleep(2)
        for i in self.link_list:
            url = i[0]
            id = i[1]
            cat_id = i[2]
            print(url)
            with requests.Session() as session:
                resp = session.get(url, timeout=10)
            assert resp.status_code == 200, 'BAD RESPONCE'

            soup = BeautifulSoup(resp.text, 'html.parser')

            cart_product = soup.select('.card-body dl dd')
            type = cart_product[0].text
            manufacturer = cart_product[1].text
            model = cart_product[2].text
            print('MANUFACTURER: ', manufacturer)
            print('MODEL:', model)

            description = soup.select('.card-body div')[3].text.\
                replace('\n', '').strip()

            seller_info_1 = soup.select('.card-body')[4].select('p')[
                1].text.strip()
            seller_info_2 = soup.select('.card-body')[4].select('p')[
                2].text.strip()

            # изменяя индекс меняется табличка
            #name = soup.select('.fs-5')[1].text.strip() - type model product
            try:
                price_n = soup.select('.fs-5')[2].text.strip().replace(',', '')
                if '€' in price_n:
                    price = price_n
                else:
                    price = None
            except Exception as error:
                price = None
                print("Not Price", error)

            print('PRICEEEEEEE', price)

            request_info = requests.get(
            f'https://www.machineseeker.com/inquiry/inquiry/get-ajax-form'
            f'?listing_id={id}&scenario=callback')

            soup = BeautifulSoup(request_info.text, 'html.parser')

            info = soup.findAll('li', class_="pl-1")
            seller = info[1].text.strip()
            phone_numb = info[2].text.strip()
            print('description: ', type, 'DESC: ',description[0:80] + '...-> '
                                            'to link', url)
            print(f'name: {seller}; phone: {phone_numb}; adress: '
                  f'{seller_info_1}, {seller_info_2}')

            name_prod = str(manufacturer) + ' ' + str(model)
            seller_info_t = str(seller_info_1) + ',' + str(seller_info_2)

            self.fill_product_table(name_prod, price, description,
                                    url, seller, phone_numb,
                                    seller_info_t, cat_id)

    def create_subcategory_table(self):
        connection = self.create_db()
        create_subcategories_table = """
            CREATE TABLE IF NOT EXISTS subcategory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                name_rus TEXT,
                link TEXT UNIQUE,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)  
            );
        """
        self.create_queries(connection, create_subcategories_table)
        time.sleep(3)

    def fill_subcategory_table(self, title, title_rus, url, id):
        connect = self.create_db()
        fill_subcategories = f"""
            INSERT INTO 
               subcategory (name, name_rus, link, category_id)
            VALUES 
                ('{title}', '{title_rus}', '{url}', '{id}')
        """
        self.create_queries(connect, fill_subcategories)

    def create_db(self):
        connect = None
        try:
            connect = sqlite3.connect(self.datapath)
        except Error as error:
            print('Wrong connection', error)
        return connect

    def create_queries(self, connection, queries):
        cursor = connection.cursor()
        try:
            cursor.execute(queries)
            connection.commit()
        except Error as error:
            print('Wrong execute', error)

    def fill_categories_table(self, title, title_rus, url):
        connection = self.create_db()
        fill_categories_tabel = f"""
            INSERT INTO 
                categories(name, name_rus, link)
            VALUES 
                ('{title}', '{title_rus}', '{url}');
        """
        self.create_queries(connection, fill_categories_tabel)

    def querry_link_for_product(self, querry_name):
        #querry_name = 'Manipulators'
        connection = self.create_db()
        cursor = connection.cursor()
        get_url = f"""
            SELECT category_id, link
            FROM subcategory
            WHERE name='{querry_name}'
        """
        cursor.execute(get_url)
        self.info_subcat_id_link = cursor.fetchall()
        print(self.info_subcat_id_link)
        return self.info_subcat_id_link

    def create_product_table(self):
        connection = self.create_db()

        create_product = """
        CREATE TABLE IF NOT EXISTS product(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            description TEXT,
            link TEXT UNIQUE,
            nameseller TEXT,
            phoneseller TEXT,
            adressseller TEXT,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id),
        );
        """
        self.create_queries(connection, create_product)

    def fill_product_table(self, prod_name, prod_price, prod_descr, prod_link,
                           sel_name, sel_phone, sel_adr, cat_id):
        conn = self.create_db()
        fill_prod_table = f"""
            INSERT INTO 
                product (name, price, description, link, nameseller, 
                phoneseller, adressseller, category_id)
            VALUES 
                ('{prod_name}', '{prod_price}', '{prod_descr}', '{prod_link}', 
              '{sel_name}', '{sel_phone}', '{sel_adr}', '{cat_id}');
        """
        self.create_queries(conn, fill_prod_table)

    def _translator(self, text):
        translator = Translator()
        trans_text = translator.translate(text, dest='ru', src='auto')
        return trans_text.text


    def main(self):
       # self.pars_categories()
       # connection = self.create_db()
       #
       #  create_categories_table = """
       #  CREATE TABLE IF NOT EXISTS categories (
       #      id INTEGER PRIMARY KEY AUTOINCREMENT,
       #      name TEXT UNIQUE,
       #      name_rus TEXT UNIQUE,
       #      link TEXT UNIQUE
       #      );
       #  """
       #  self.create_queries(connection, create_categories_table)

        # self.querries_url_from_db()
        #
        # self.pars_single_cat()

        # Таблицы созданы, категории и подкатегории собраны
        self.parsing_pages_and_links('Deburring machines')
        self.product()

        # удалить полностью таблицу
        # conn = self.create_db()
        # del_table = """DROP TABLE product"""
        # self.create_queries(conn, del_table)


if __name__ == '__main__':
    cat = MachineSeeker('https://www.machineseeker.com/')
    cat.main()





