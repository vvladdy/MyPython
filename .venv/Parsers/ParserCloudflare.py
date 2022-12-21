import json
import re
import undetected_chromedriver
from undetected_chromedriver.options import ChromeOptions
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By


def pars(url):
    options = ChromeOptions()
    options.headless = True
    try:
        driver = undetected_chromedriver.Chrome()
        driver.get(url)
        time.sleep(10)
        # print(driver.page_source)
        with open('tuttimoto.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
    except Exception as err:
        print(err)
    finally:
        driver.close()
        driver.quit()

def get_info(file_path):
    prices, tit_info, info = [], [], []

    with open(file_path, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        titles = soup.select('.css-1buk2iu')
        for i in range(len(titles)):
            title = titles[i].text.strip()
            link = 'https://www.tutti.ch' + titles[i].get('href')
            tit_info.append((title, link))

        price = soup.findAll('span', class_='MuiTypography-root')
        for i in range(32, len(price), 3):
            prices.append(price[i].text.strip('.- ').replace("'",''))
        # print(len(prices))
        # print('Titles', len(tit_info))

        for i in range(len(tit_info)):
            info.append({
                'title': tit_info[i][0],
                'link': tit_info[i][1],
                'price': prices[i]
            })
        # print(info)
        return info

def find_script(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'lxml')

    scripts = soup.findAll('script')
    # for i, g in enumerate(scripts):
    #     print(i, g)
    print(scripts[12])
    token = re.findall(r'(?<="searchToken":)"[A-Z0-9a-z]+"', str(scripts[12]))
    name = re.findall(r'(?<="categoryID":)"[A-Z0-9a-z]+"', str(scripts[12]))
    print(token, name)


def write_json(file_path):
    content = get_info(file_path)

    with open('D:/MyPythonFolder/MyPython/.venv/Parsers/Files/filetuttui.json'
              '', 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


def main():
    file_path = 'tuttimoto.html'
    url = 'https://www.tutti.ch/de/q/motorraeder/Ak8CrbW90b3JjeWNsZXOUwMDAwA?sorting=newest&page=1'
    pars(url)
    get_info(file_path)
    write_json(file_path)
    # find_script(file_path)
if __name__ == '__main__':
    main()
