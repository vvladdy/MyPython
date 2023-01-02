import csv
import requests
from bs4 import BeautifulSoup
import datetime
import openpyxl
from pprint import pprint
from fake_useragent import UserAgent
from decimal import Decimal
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter

async def collect_data(promo=''):
    url_base = f'https://www.atbmarket.com/promo/{promo}'

    all_products = []
    ua = UserAgent()

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,'
                 'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-agent': ua.random
    }

    response = requests.get(url_base, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        pages = int(soup.select('.product-pagination__link')[-2].text.strip())
    except Exception:
        pages = 1
    finish_date = soup.select('.actions-timer.actionsTimer')[0].get(
        'data-time').replace(',', '')
    print('Total pages:', pages)
    # pages = 2
    for i in range(1, pages+1):
        print(f'WORKING WITH PAGE {i}...')
        url = url_base + f'?page={i}'
        print(f'WORKING WITH PAGE {url}...')
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=headers)
            print(response.status)
            soup = BeautifulSoup(await response.text(), 'html.parser')

            products = soup.select('.catalog-item')
            for prod in range(len(products)):
                title = soup.select('.catalog-item__title')[prod].text.strip()
                link = 'https://www.atbmarket.com' + soup.select(
                    '.catalog-item__title a')[prod].get('href')
                old_price = soup.select('.catalog-item__product-price.product-price.'
                'product-price--weight')[prod].find('data',
                                class_='product-price__top').get('value')
                try:
                    new_price = soup.select(
                        '.catalog-item__product-price.product-price.'
                    'product-price--weight')[prod].find('data',
                                    class_='product-price__bottom').get('value')
                except Exception:
                    new_price = 0

                sale = Decimal(new_price)/Decimal(old_price)*100 - 100
                if sale < 0:
                    sale = 0
                else:
                    sale = round(sale)
                #
                # if new_price == 0:
                #     print('ZERO')
                #     continue
                # else:
                all_products.append([
                    title, old_price, new_price,
                    str(sale) + ' %', finish_date, link])

    cur_time = datetime.datetime.now().strftime("%d-%b-%Y")
    async with aiofiles.open(f'Files/ATB/Sale-{cur_time}{promo}.csv', 'w',
                             newline='',
              encoding='cp1251') as file:
        writer = AsyncWriter(file)
        await writer.writerow(
            ['Продукт', 'Новая цена', 'Старая цена', 'Процент скидки',
             'Окончание акции', 'Cсылка на продукт']
        )
        await writer.writerows(
            all_products
        )
    # return f'Sale-{cur_time}.csv'
    path = f'Files/ATB/Sale-{cur_time}{promo}.csv'
    # file = await csv_to_excel(path)
    return await csv_to_excel(path)

async def csv_to_excel(path):
    promo = path.split('.')[0][-5:0]
    print(promo)
    cur_time = datetime.datetime.now().strftime("%d-%b-%Y")
    with open(path, 'r', newline='', encoding='cp1251') as file:
        content = csv.DictReader(file)

        filecontent = openpyxl.Workbook()
        sheet = filecontent.active

        sheet['A1'] = 'Продукт'.upper()
        sheet['B1'] = 'Новая цена'.upper()
        sheet['C1'] = 'Старая цена'.upper()
        sheet['D1'] = 'Процент скидки'.upper()
        sheet['E1'] = 'Окончание акции'.upper()
        sheet['F1'] = 'Cсылка на продукт'.upper()

        row = 2
        for info in content:
            sheet[row][0].value = info['Продукт']
            sheet[row][1].value = info['Новая цена']
            sheet[row][2].value = info['Старая цена']
            sheet[row][3].value = info['Процент скидки']
            sheet[row][4].value = info['Окончание акции']
            sheet[row][5].value = info['Cсылка на продукт']
            row += 1
        filecontent.save(f'Files/ATB/SaleATB{cur_time}.xlsx')
        filecontent.close()
    print('File SUCCESS create')
    return f'SaleATB{cur_time}.xlsx'

def get_promo():
    promo_name = []
    url = 'https://www.atbmarket.com/promo/all'
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    promo = soup.select('.actions-list__title a')
    for i in range(len(promo)):
        promo_links = promo[i].get('href')
        promo_name.append(promo_links.split('/')[-1])
    return promo_name

async def main():
    start = datetime.datetime.now()
    # url = 'https://www.atbmarket.com/promo/novorichni_zini'
    # url = 'https://www.atbmarket.com/promo/economy'
    print(get_promo())
    await collect_data(promo='economy')
    # end = datetime.datetime.now()
    # during = end - start
    # print('Parsing time', during)
    # cur_time = datetime.datetime.now().strftime("%d-%b-%Y")
    # await csv_to_excel(f'Files/ATB/Sale-{cur_time}.csv')

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
